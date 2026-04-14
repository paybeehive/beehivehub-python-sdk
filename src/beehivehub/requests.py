"""HTTP request layer for the BeeHive Hub SDK."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx

from beehivehub.constants import BASE_URL_PRODUCTION, BASE_URL_SANDBOX, default_headers
from beehivehub.exceptions import (
    BeehiveHubAPIError,
    BeehiveHubAuthenticationError,
    BeehiveHubError,
    BeehiveHubNetworkError,
    BeehiveHubNotFoundError,
    BeehiveHubRateLimitError,
    BeehiveHubValidationError,
)

RequestFunction = Callable[..., Any]

TIMEOUT = 30.0


def create_request(
    api_key: str,
    environment: str = "production",
) -> RequestFunction:
    """Create a configured HTTP request function.

    Args:
        api_key: The API key for authentication.
        environment: API environment — "production" or "sandbox".

    Returns:
        A request function bound to the configured base URL and headers.
    """
    base_url = BASE_URL_SANDBOX if environment == "sandbox" else BASE_URL_PRODUCTION
    headers = default_headers(api_key)

    def request(
        path: str,
        method: str = "GET",
        data: Any = None,
        headers_override: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute an HTTP request against the BeeHive Hub API.

        Args:
            path: API path (e.g. "/transactions").
            method: HTTP method.
            data: Request body (will be sent as JSON).
            headers_override: Extra headers to merge with defaults.
            params: Query parameters.

        Returns:
            Parsed JSON response, or None if the response body is empty.

        Raises:
            BeehiveHubValidationError: On 400 responses.
            BeehiveHubAuthenticationError: On 401 responses.
            BeehiveHubNotFoundError: On 404 responses.
            BeehiveHubRateLimitError: On 429 responses.
            BeehiveHubAPIError: On other 4xx/5xx responses.
            BeehiveHubNetworkError: On network/timeout errors.
        """
        merged_headers = {**headers, **(headers_override or {})}
        url = f"{base_url}{path}"

        try:
            with httpx.Client(timeout=TIMEOUT) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=merged_headers,
                    json=data,
                    params=params,
                )

            text = response.text
            if not response.is_success:
                body: dict[str, Any] = {}
                if text:
                    body = response.json()
                message = body.get("message") or body.get("error") or "Unknown error"

                status = response.status_code
                if status == 400:
                    raise BeehiveHubValidationError(message, details=body)
                if status == 401:
                    raise BeehiveHubAuthenticationError(message)
                if status == 404:
                    resource = body.get("resource", "Resource")
                    raise BeehiveHubNotFoundError(resource)
                if status == 429:
                    raise BeehiveHubRateLimitError(message)
                raise BeehiveHubAPIError(
                    message,
                    status_code=status,
                    code=body.get("code"),
                    body=body,
                )

            if not text:
                return None
            return response.json()

        except BeehiveHubError:
            raise
        except httpx.RequestError as exc:
            raise BeehiveHubNetworkError(str(exc)) from None

    return request
