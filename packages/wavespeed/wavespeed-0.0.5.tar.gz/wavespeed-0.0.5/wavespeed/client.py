import os
import time
import httpx
from typing import Dict, Any
from urllib.parse import urljoin
import asyncio
import random
from datetime import datetime
from typing import Iterable, Optional, Mapping, Union
import logging

from wavespeed.schemas.prediction import Prediction

class RetryTransport(httpx.AsyncBaseTransport, httpx.BaseTransport):
    """A custom HTTP transport that automatically retries requests using an exponential backoff strategy
    for specific HTTP status codes and request methods.
    """

    RETRYABLE_METHODS = frozenset(["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"])
    RETRYABLE_STATUS_CODES = frozenset(
        [
            429,  # Too Many Requests
            502,  # Bad Gateway
            503,  # Service Unavailable
            504,  # Gateway Timeout
        ]
    )
    MAX_BACKOFF_WAIT = 60


    def __init__(  # pylint: disable=too-many-arguments
        self,
        wrapped_transport: Union[httpx.BaseTransport, httpx.AsyncBaseTransport],
        *,
        max_attempts: int = 10,
        max_backoff_wait: float = MAX_BACKOFF_WAIT,
        backoff_factor: float = 0.1,
        jitter_ratio: float = 0.1,
        retryable_methods: Optional[Iterable[str]] = None,
        retry_status_codes: Optional[Iterable[int]] = None,
    ) -> None:
        self._wrapped_transport = wrapped_transport

        if jitter_ratio < 0 or jitter_ratio > 0.5:
            raise ValueError(
                f"jitter ratio should be between 0 and 0.5, actual {jitter_ratio}"
            )

        self.max_attempts = max_attempts
        self.backoff_factor = backoff_factor
        self.retryable_methods = (
            frozenset(retryable_methods)
            if retryable_methods
            else self.RETRYABLE_METHODS
        )
        self.retry_status_codes = (
            frozenset(retry_status_codes)
            if retry_status_codes
            else self.RETRYABLE_STATUS_CODES
        )
        self.jitter_ratio = jitter_ratio
        self.max_backoff_wait = max_backoff_wait

    def _calculate_sleep(
        self, attempts_made: int, headers: Union[httpx.Headers, Mapping[str, str]]
    ) -> float:
        retry_after_header = (headers.get("Retry-After") or "").strip()
        if retry_after_header:
            if retry_after_header.isdigit():
                return float(retry_after_header)

            try:
                parsed_date = datetime.fromisoformat(retry_after_header).astimezone()
                diff = (parsed_date - datetime.now().astimezone()).total_seconds()
                if diff > 0:
                    return min(diff, self.max_backoff_wait)
            except ValueError:
                pass

        backoff = self.backoff_factor * (2 ** (attempts_made - 1))
        jitter = (backoff * self.jitter_ratio) * random.choice([1, -1])  # noqa: S311
        total_backoff = backoff + jitter
        return min(total_backoff, self.max_backoff_wait)

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        response = self._wrapped_transport.handle_request(request)  # type: ignore

        if request.method not in self.retryable_methods:
            return response

        remaining_attempts = self.max_attempts - 1
        attempts_made = 1

        while True:
            if (
                remaining_attempts < 1
                or response.status_code not in self.retry_status_codes
            ):
                return response

            response.close()

            sleep_for = self._calculate_sleep(attempts_made, response.headers)
            logging.info("Got %s, Retrying request after %s seconds", response.status_code, sleep_for)
            time.sleep(sleep_for)

            response = self._wrapped_transport.handle_request(request)  # type: ignore

            attempts_made += 1
            remaining_attempts -= 1

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        response = await self._wrapped_transport.handle_async_request(request)  # type: ignore

        if request.method not in self.retryable_methods:
            return response

        remaining_attempts = self.max_attempts - 1
        attempts_made = 1

        while True:
            if (
                remaining_attempts < 1
                or response.status_code not in self.retry_status_codes
            ):
                return response

            await response.aclose()

            sleep_for = self._calculate_sleep(attempts_made, response.headers)
            logging.info("Got %s, Retrying request after %s seconds", response.status_code, sleep_for)
            await asyncio.sleep(sleep_for)

            response = await self._wrapped_transport.handle_async_request(request)  # type: ignore

            attempts_made += 1
            remaining_attempts -= 1

    async def aclose(self) -> None:
        await self._wrapped_transport.aclose()  # type: ignore

    def close(self) -> None:
        self._wrapped_transport.close()  # type: ignore

class WaveSpeed:
    """
    A client for interacting with the Wavespeed AI API.
    """
    _async_client: Optional[httpx.AsyncClient] = None
    _client: Optional[httpx.Client] = None
    
    def __init__(self, api_key: str="", base_url: str = "https://api.wavespeed.ai/api/v2/", timeout: int | None = 120, **kwargs):
        """
        Initialize the WaveSpeed client.
        
        Args:
            api_key: Your WaveSpeed API key
            base_url: Base URL for the API
            timeout: Timeout in seconds for http client send request
        """
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.environ.get("WAVESPEED_API_KEY", '')
        if not self.api_key:
            raise ValueError("API key is required.")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.base_url = base_url
        self.timeout = timeout
        self.poll_interval = float(os.environ.get("WAVESPEED_POLL_INTERVAL", 0.5))
        self._client_kwargs = kwargs

    @property
    def async_client(self) -> httpx.AsyncClient:
        if self._async_client:
            return self._async_client
        transport = self._client_kwargs.get("async_transport", None) or httpx.AsyncHTTPTransport()
        self._async_client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout, transport=RetryTransport(transport))
        return self._async_client
    
    @property
    def client(self) -> httpx.Client:
        if self._client:
            return self._client
        transport = self._client_kwargs.get("transport", None) or httpx.HTTPTransport()
        self._client = httpx.Client(headers=self.headers, timeout=self.timeout, transport=RetryTransport(transport))
        return self._client

    async def async_run(
        self,
        modelId: str,
        input: Dict[str, Any],
        **kwargs
    ) -> Prediction:
        """
        Generate an image using the Wavespeed AI API.
        
        Args:
            modelId: The ID of the model to use
            input: Input parameters for the model
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The API response as a dictionary
        """
        url = urljoin(self.base_url, modelId)
        
        payload = input
        
        response = await self.async_client.post(
            url,
            headers=self.headers,
            json=payload,
        )
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 200:
            raise ValueError(f"Unexpected code: {data.get('code')}, data: {data}")
        prediction = Prediction(**data['data'])
        prediction._client = self
        return await prediction.async_wait()
    
    def run(
        self,
        modelId: str,
        input: Dict[str, Any],
        **kwargs
    ) -> Prediction:
        """
        Generate an image using the Wavespeed AI API.
        
        Args:
            modelId: The ID of the model to use
            input: Input parameters for the model
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The API response as a dictionary
        """
        url = urljoin(self.base_url, modelId)
        
        payload = input
        
        response = self.client.post(
            url,
            headers=self.headers,
            json=payload,
        )

        # Raise an exception for HTTP errors
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 200:
            raise ValueError(f"Unexpected code: {data.get('code')}, data: {data}")
        prediction = Prediction(**data['data'])
        prediction._client = self
        return prediction.wait()
    
    async def async_create(self, modelId: str, input: Dict[str, Any], **kwargs) -> Prediction:
        url = urljoin(self.base_url, modelId)
        payload = input
        response = await self.async_client.post(
            url,
            headers=self.headers,
            json=payload,
        )
        # Raise an exception for HTTP errors
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 200:
            raise ValueError(f"Unexpected code: {data.get('code')}, data: {data}")
        prediction = Prediction(**data['data'])
        prediction._client = self
        return prediction
    
    def create(self, modelId: str, input: Dict[str, Any], **kwargs) -> Prediction:
        url = urljoin(self.base_url, modelId)
        payload = input
        response = self.client.post(
            url,
            headers=self.headers,
            json=payload,
        )
        # Raise an exception for HTTP errors
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 200:
            raise ValueError(f"Unexpected code: {data.get('code')}, data: {data}")
        prediction = Prediction(**data['data'])
        prediction._client = self
        return prediction
    
    def get_prediction(self, predictionId: str) -> Prediction:
        url = urljoin(self.base_url, f"predictions/{predictionId}/result")
        response = self.client.get(
            url,
            headers=self.headers,
        )
        # Raise an exception for HTTP errors
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 200:
            raise ValueError(f"Unexpected code: {data.get('code')}, data: {data}")
        prediction = Prediction(**data['data'])
        prediction._client = self
        return prediction
    
    async def async_get_prediction(self, predictionId: str) -> Prediction:
        url = urljoin(self.base_url, f"predictions/{predictionId}/result")
        response = await self.async_client.get(
            url,
            headers=self.headers,
        )
        # Raise an exception for HTTP errors
        response.raise_for_status()
        data = response.json()
        if data.get('code') != 200:
            raise ValueError(f"Unexpected code: {data.get('code')}, data: {data}")
        prediction = Prediction(**data['data'])
        prediction._client = self
        return prediction
        
    async def close(self):
        """Close the httpx client session."""
        self.client.close()
        await self.async_client.aclose()
        
    def __str__(self) -> str:
        """String representation of the client."""
        return f"WaveSpeed()"