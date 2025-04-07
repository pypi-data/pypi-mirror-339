"""Base API client for interacting with LightWave services."""

from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ApiClient:
    """Base client for making API requests to LightWave services.

    This is a simple example. In a real implementation, you might use
    httpx, requests, or another HTTP library.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: int = 30,
    ):
        """Initialize the API client.

        Args:
            base_url: The base URL for the API
            api_key: Optional API key for authentication
            timeout: Timeout in seconds for requests
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _get_headers(self) -> dict[str, str]:
        """Get the headers for the request."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        model_class: type[T] | None = None,
    ) -> dict[str, Any] | T | None:
        """Make a GET request to the API.

        Args:
            endpoint: The API endpoint (without base URL)
            params: Optional query parameters
            model_class: Optional Pydantic model class to parse the response

        Returns:
            The response data as a dictionary, model instance, or None
        """
        # In a real implementation, you would use requests or httpx here
        # For example:
        # url = f"{self.base_url}/{endpoint.lstrip('/')}"
        # headers = self._get_headers()
        # response = requests.get(
        #     url, headers=headers, params=params, timeout=self.timeout
        # )
        # response.raise_for_status()
        # response_data = response.json()

        # Unused parameters in this implementation, but would be used in real code
        _ = endpoint, params

        # Simulate a response
        response_data = {"status": "success", "data": {}}

        if model_class:
            return model_class.model_validate(response_data["data"])

        return response_data

    def post(
        self,
        endpoint: str,
        data: dict[str, Any] | BaseModel | None = None,
        model_class: type[T] | None = None,
    ) -> dict[str, Any] | T | None:
        """Make a POST request to the API.

        Args:
            endpoint: The API endpoint (without base URL)
            data: The request data (dict or Pydantic model)
            model_class: Optional Pydantic model class to parse the response

        Returns:
            The response data as a dictionary, model instance, or None
        """
        # Unused parameter in this implementation, but would be used in real code
        _ = endpoint

        # Process the data for use in a real implementation
        if data is not None and isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)

        # In a real implementation, you would use requests or httpx here
        # For example:
        # url = f"{self.base_url}/{endpoint.lstrip('/')}"
        # headers = self._get_headers()
        # response = requests.post(
        #     url,
        #     headers=headers,
        #     json=data,
        #     timeout=self.timeout
        # )
        # response.raise_for_status()
        # response_data = response.json()

        # Simulate a response
        response_data = {"status": "success", "data": {}}

        if model_class:
            return model_class.model_validate(response_data["data"])

        return response_data
