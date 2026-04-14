"""Tests for exceptions module."""

from beehivehub.constants import BEEHIVE_DOCS
from beehivehub.exceptions import (
    BeehiveHubAPIError,
    BeehiveHubAuthenticationError,
    BeehiveHubError,
    BeehiveHubNetworkError,
    BeehiveHubNotFoundError,
    BeehiveHubRateLimitError,
    BeehiveHubValidationError,
)


class TestBeehiveHubError:
    def test_is_instance_of_exception(self):
        error = BeehiveHubError("Test error")
        assert isinstance(error, Exception)

    def test_message_contains_docs_url(self):
        error = BeehiveHubError("Test error")
        assert BEEHIVE_DOCS in str(error)

    def test_message_contains_original_text(self):
        error = BeehiveHubError("Test error message")
        assert "Test error message" in str(error)

    def test_to_dict_contains_name(self):
        error = BeehiveHubError("Test error")
        result = error.to_dict()
        assert result["name"] == "BeehiveHubError"

    def test_to_dict_contains_message(self):
        error = BeehiveHubError("Test error")
        result = error.to_dict()
        assert "Test error" in result["message"]

    def test_default_status_code_is_none(self):
        error = BeehiveHubError("Test error")
        assert error.status_code is None

    def test_default_code_is_none(self):
        error = BeehiveHubError("Test error")
        assert error.code is None


class TestBeehiveHubAPIError:
    def test_status_code(self):
        error = BeehiveHubAPIError("Server error", status_code=500)
        assert error.status_code == 500

    def test_body(self):
        body = {"message": "Error"}
        error = BeehiveHubAPIError("Error", status_code=500, body=body)
        assert error.body == body

    def test_to_dict_includes_body(self):
        body = {"detail": "something"}
        error = BeehiveHubAPIError("Error", status_code=500, body=body)
        result = error.to_dict()
        assert result["body"] == body
        assert result["name"] == "BeehiveHubAPIError"

    def test_message_contains_docs(self):
        error = BeehiveHubAPIError("Error", status_code=500)
        assert BEEHIVE_DOCS in str(error)


class TestBeehiveHubAuthenticationError:
    def test_status_code_is_401(self):
        error = BeehiveHubAuthenticationError("Invalid key")
        assert error.status_code == 401

    def test_code(self):
        error = BeehiveHubAuthenticationError("Invalid key")
        assert error.code == "authentication_error"

    def test_message_contains_docs(self):
        error = BeehiveHubAuthenticationError("Invalid key")
        assert BEEHIVE_DOCS in str(error)


class TestBeehiveHubValidationError:
    def test_status_code_is_400(self):
        error = BeehiveHubValidationError("Bad request")
        assert error.status_code == 400

    def test_code(self):
        error = BeehiveHubValidationError("Bad request")
        assert error.code == "validation_error"

    def test_details(self):
        details = {"field": "amount", "error": "required"}
        error = BeehiveHubValidationError("Bad request", details=details)
        assert error.details == details

    def test_to_dict_includes_details(self):
        details = {"field": "amount"}
        error = BeehiveHubValidationError("Bad request", details=details)
        result = error.to_dict()
        assert result["details"] == details
        assert result["name"] == "BeehiveHubValidationError"


class TestBeehiveHubNotFoundError:
    def test_status_code_is_404(self):
        error = BeehiveHubNotFoundError("Transaction")
        assert error.status_code == 404

    def test_code(self):
        error = BeehiveHubNotFoundError()
        assert error.code == "not_found"

    def test_resource(self):
        error = BeehiveHubNotFoundError("Transaction")
        assert error.resource == "Transaction"

    def test_default_resource(self):
        error = BeehiveHubNotFoundError()
        assert error.resource == "Resource"

    def test_to_dict_includes_resource(self):
        error = BeehiveHubNotFoundError("Customer")
        result = error.to_dict()
        assert result["resource"] == "Customer"
        assert result["name"] == "BeehiveHubNotFoundError"

    def test_message_contains_resource_name(self):
        error = BeehiveHubNotFoundError("Transaction")
        assert "Transaction not found" in str(error)


class TestBeehiveHubRateLimitError:
    def test_status_code_is_429(self):
        error = BeehiveHubRateLimitError("Too many requests")
        assert error.status_code == 429

    def test_code(self):
        error = BeehiveHubRateLimitError("Too many requests")
        assert error.code == "rate_limit_error"

    def test_message_contains_docs(self):
        error = BeehiveHubRateLimitError("Too many requests")
        assert BEEHIVE_DOCS in str(error)


class TestBeehiveHubNetworkError:
    def test_status_code_is_none(self):
        error = BeehiveHubNetworkError("Connection refused")
        assert error.status_code is None

    def test_code(self):
        error = BeehiveHubNetworkError("Connection refused")
        assert error.code == "network_error"

    def test_message_contains_docs(self):
        error = BeehiveHubNetworkError("Connection refused")
        assert BEEHIVE_DOCS in str(error)

    def test_to_dict(self):
        error = BeehiveHubNetworkError("Timeout")
        result = error.to_dict()
        assert result["name"] == "BeehiveHubNetworkError"
        assert result["status_code"] is None
