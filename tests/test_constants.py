"""Tests for constants module."""

import base64

from beehivehub.constants import (
    BASE_URL_PRODUCTION,
    BASE_URL_SANDBOX,
    BEEHIVE_DOCS,
    PAYMENT_LINK_URL_PRODUCTION,
    PAYMENT_LINK_URL_SANDBOX,
    SDK_VERSION,
    default_headers,
)


class TestURLConstants:
    def test_base_url_production(self):
        assert BASE_URL_PRODUCTION == "https://api.conta.paybeehive.com.br/v1"

    def test_base_url_sandbox(self):
        assert BASE_URL_SANDBOX == "https://api.sandbox.hopysplit.com.br/v1"

    def test_payment_link_url_production(self):
        assert PAYMENT_LINK_URL_PRODUCTION == "https://link.conta.paybeehive.com.br"

    def test_payment_link_url_sandbox(self):
        assert PAYMENT_LINK_URL_SANDBOX == "https://link.sandbox.hopysplit.com.br"

    def test_beehive_docs(self):
        assert BEEHIVE_DOCS == "https://docs.beehivehub.io/"

    def test_sdk_version(self):
        assert SDK_VERSION == "1.0.0"


class TestDefaultHeaders:
    def test_returns_authorization_header(self):
        headers = default_headers("test-api-key")
        assert headers["Authorization"].startswith("Basic ")

    def test_returns_content_type(self):
        headers = default_headers("test-api-key")
        assert headers["Content-Type"] == "application/json"

    def test_returns_user_agent(self):
        headers = default_headers("test-api-key")
        assert headers["User-Agent"] == "Beehive Hub Python SDK (1.0.0)"

    def test_base64_encoding(self):
        headers = default_headers("my-secret-key")
        expected = base64.b64encode(b"my-secret-key:x").decode()
        assert headers["Authorization"] == f"Basic {expected}"

    def test_base64_encoding_different_key(self):
        headers = default_headers("another-key-123")
        expected = base64.b64encode(b"another-key-123:x").decode()
        assert headers["Authorization"] == f"Basic {expected}"
