"""Shared fixtures for BeeHive Hub SDK tests."""

import pytest
import respx

from beehivehub.client import create_beehivehub_client
from beehivehub.constants import BASE_URL_PRODUCTION, BASE_URL_SANDBOX
from beehivehub.requests import create_request


@pytest.fixture
def mock_api():
    """Provide a respx mock router for HTTP requests."""
    with respx.mock(assert_all_called=False) as router:
        yield router


@pytest.fixture
def request_fn():
    """Create a request function configured for production."""
    return create_request("test-api-key")


@pytest.fixture
def sandbox_request_fn():
    """Create a request function configured for sandbox."""
    return create_request("test-api-key", environment="sandbox")


@pytest.fixture
def client():
    """Create a full SDK client configured for production."""
    return create_beehivehub_client("test-api-key")


@pytest.fixture
def sandbox_client():
    """Create a full SDK client configured for sandbox."""
    return create_beehivehub_client("test-api-key", environment="sandbox")


@pytest.fixture
def prod_url():
    """Return the production base URL."""
    return BASE_URL_PRODUCTION


@pytest.fixture
def sandbox_url():
    """Return the sandbox base URL."""
    return BASE_URL_SANDBOX
