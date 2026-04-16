"""Tests for requests module."""

import httpx
import pytest
import respx

from beehivehub.constants import BASE_URL_PRODUCTION, BASE_URL_SANDBOX
from beehivehub.exceptions import (
    BeehiveHubAPIError,
    BeehiveHubAuthenticationError,
    BeehiveHubNetworkError,
    BeehiveHubNotFoundError,
    BeehiveHubRateLimitError,
    BeehiveHubValidationError,
)
from beehivehub.requests import create_request


class TestCreateRequest:
    def test_returns_callable(self):
        request_fn = create_request("test-api-key")
        assert callable(request_fn)


class TestRequestSuccess:
    @respx.mock
    def test_production_url_by_default(self):
        route = respx.get(f"{BASE_URL_PRODUCTION}/test").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "success"})
        )
        request_fn = create_request("test-api-key")
        result = request_fn("/test", method="GET")

        assert result == {"id": "123", "status": "success"}
        assert route.called

    @respx.mock
    def test_sandbox_url_when_sandbox_environment(self):
        route = respx.get(f"{BASE_URL_SANDBOX}/test").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "success"})
        )
        request_fn = create_request("test-api-key", environment="sandbox")
        result = request_fn("/test", method="GET")

        assert result == {"id": "123", "status": "success"}
        assert route.called

    @respx.mock
    def test_empty_body_returns_none(self):
        respx.delete(f"{BASE_URL_PRODUCTION}/payment-links/123").mock(
            return_value=httpx.Response(200, text="")
        )
        request_fn = create_request("test-api-key")
        result = request_fn("/payment-links/123", method="DELETE")

        assert result is None

    @respx.mock
    def test_custom_headers_are_merged(self):
        route = respx.post(f"{BASE_URL_PRODUCTION}/test").mock(
            return_value=httpx.Response(200, json={})
        )
        request_fn = create_request("test-api-key")
        request_fn(
            "/test",
            method="POST",
            headers_override={"X-Custom-Header": "custom-value"},
        )

        sent_headers = route.calls[0].request.headers
        assert sent_headers["authorization"].startswith("Basic ")
        assert sent_headers["content-type"] == "application/json"
        assert sent_headers["x-custom-header"] == "custom-value"


class TestRequestErrors:
    @respx.mock
    def test_400_raises_validation_error(self):
        respx.post(f"{BASE_URL_PRODUCTION}/transactions").mock(
            return_value=httpx.Response(400, json={"message": "Invalid payload", "field": "amount"})
        )
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubValidationError) as exc_info:
            request_fn("/transactions", method="POST", data={"amount": -1})

        assert exc_info.value.status_code == 400
        assert "Invalid payload" in str(exc_info.value)

    @respx.mock
    def test_401_raises_authentication_error(self):
        respx.get(f"{BASE_URL_PRODUCTION}/test").mock(
            return_value=httpx.Response(401, json={"message": "Invalid API key"})
        )
        request_fn = create_request("bad-key")

        with pytest.raises(BeehiveHubAuthenticationError) as exc_info:
            request_fn("/test", method="GET")

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_404_raises_not_found_error(self):
        respx.get(f"{BASE_URL_PRODUCTION}/transactions/999").mock(
            return_value=httpx.Response(
                404, json={"message": "Not found", "resource": "Transaction"}
            )
        )
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubNotFoundError) as exc_info:
            request_fn("/transactions/999", method="GET")

        assert exc_info.value.status_code == 404
        assert exc_info.value.resource == "Transaction"

    @respx.mock
    def test_429_raises_rate_limit_error(self):
        respx.get(f"{BASE_URL_PRODUCTION}/test").mock(
            return_value=httpx.Response(429, json={"message": "Too many requests"})
        )
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubRateLimitError) as exc_info:
            request_fn("/test", method="GET")

        assert exc_info.value.status_code == 429

    @respx.mock
    def test_500_raises_api_error(self):
        respx.get(f"{BASE_URL_PRODUCTION}/test").mock(
            return_value=httpx.Response(500, json={"message": "Error occurred"})
        )
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubAPIError) as exc_info:
            request_fn("/test", method="GET")

        assert exc_info.value.status_code == 500
        assert "Error occurred" in str(exc_info.value)

    @respx.mock
    def test_network_error(self):
        respx.get(f"{BASE_URL_PRODUCTION}/test").mock(
            side_effect=httpx.ConnectError("Network error")
        )
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubNetworkError) as exc_info:
            request_fn("/test", method="GET")

        assert "Network error" in str(exc_info.value)
        assert exc_info.value.status_code is None

    @respx.mock
    def test_error_message_from_error_field(self):
        respx.get(f"{BASE_URL_PRODUCTION}/test").mock(
            return_value=httpx.Response(500, json={"error": "Something went wrong"})
        )
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubAPIError) as exc_info:
            request_fn("/test", method="GET")

        assert "Something went wrong" in str(exc_info.value)

    @respx.mock
    def test_unknown_error_message_fallback(self):
        respx.get(f"{BASE_URL_PRODUCTION}/test").mock(return_value=httpx.Response(500, json={}))
        request_fn = create_request("test-api-key")

        with pytest.raises(BeehiveHubAPIError) as exc_info:
            request_fn("/test", method="GET")

        assert "Unknown error" in str(exc_info.value)
