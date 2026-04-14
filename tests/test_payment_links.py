"""Tests for payment links resource."""

import json
import re

import httpx
import respx

from beehivehub.constants import PAYMENT_LINK_URL_PRODUCTION


class TestPaymentLinksCreate:
    @respx.mock
    def test_create_with_explicit_alias(self, client, prod_url):
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 123,
                    "alias": "7oVnM7sUTE",
                    "title": "novo link",
                    "amount": 15000,
                },
            )
        )
        data = {
            "title": "novo link",
            "amount": 15000,
            "alias": "7oVnM7sUTE",
            "settings": {},
        }
        result = client.payment_links.create(data)

        assert result["id"] == 123
        assert result["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/7oVnM7sUTE"
        assert route.called
        sent = json.loads(route.calls[0].request.content)
        assert sent["alias"] == "7oVnM7sUTE"

    @respx.mock
    def test_create_without_alias_generates_automatically(self, client, prod_url):
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(
                200,
                json={"id": 123, "alias": "Ab1Cd2Ef3G"},
            )
        )
        data = {"title": "link", "amount": 1000}
        client.payment_links.create(data)

        sent = json.loads(route.calls[0].request.content)
        assert re.match(r"^[a-zA-Z0-9]{10}$", sent["alias"])

    @respx.mock
    def test_create_with_empty_alias_generates_automatically(self, client, prod_url):
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(
                200,
                json={"id": 123, "alias": "Xy9Zw8Ab1C"},
            )
        )
        data = {"title": "link", "amount": 1000, "alias": ""}
        client.payment_links.create(data)

        sent = json.loads(route.calls[0].request.content)
        assert re.match(r"^[a-zA-Z0-9]{10}$", sent["alias"])


class TestPaymentLinksList:
    @respx.mock
    def test_list_without_alias_no_url(self, client, prod_url):
        respx.get(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(200, json=[{"id": 123}, {"id": 456}])
        )
        result = client.payment_links.list()

        assert result == [{"id": 123}, {"id": 456}]
        assert "url" not in result[0]
        assert "url" not in result[1]

    @respx.mock
    def test_list_with_alias_adds_url(self, client, prod_url):
        respx.get(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"id": 123, "alias": "abc1234567"},
                    {"id": 456},
                ],
            )
        )
        result = client.payment_links.list()

        assert result[0]["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/abc1234567"
        assert "url" not in result[1]


class TestPaymentLinksGet:
    @respx.mock
    def test_get_adds_url(self, client, prod_url):
        respx.get(f"{prod_url}/payment-links/247").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 123,
                    "alias": "7oVnM7sUTE",
                    "title": "link atualizado",
                    "amount": 20000,
                },
            )
        )
        result = client.payment_links.get(247)

        assert result["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/7oVnM7sUTE"
        assert result["id"] == 123


class TestPaymentLinksUpdate:
    @respx.mock
    def test_update_with_explicit_alias(self, client, prod_url):
        route = respx.put(f"{prod_url}/payment-links/247").mock(
            return_value=httpx.Response(
                200,
                json={"id": 247, "amount": 20000, "alias": "meu-alias-custom"},
            )
        )
        data = {"amount": 20000, "alias": "meu-alias-custom"}
        result = client.payment_links.update(247, data)

        sent = json.loads(route.calls[0].request.content)
        assert sent == {"amount": 20000, "alias": "meu-alias-custom"}
        assert result["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/meu-alias-custom"

    @respx.mock
    def test_update_without_alias_generates_automatically(self, client, prod_url):
        route = respx.put(f"{prod_url}/payment-links/247").mock(
            return_value=httpx.Response(
                200,
                json={"id": 247, "amount": 20000},
            )
        )
        data = {"amount": 20000}
        client.payment_links.update(247, data)

        sent = json.loads(route.calls[0].request.content)
        assert sent["amount"] == 20000
        assert re.match(r"^[a-zA-Z0-9]{10}$", sent["alias"])


class TestPaymentLinksDelete:
    @respx.mock
    def test_delete(self, client, prod_url):
        route = respx.delete(f"{prod_url}/payment-links/247").mock(
            return_value=httpx.Response(200, text="")
        )
        result = client.payment_links.delete(247)

        assert result is None
        assert route.called


class TestPaymentLinksSandbox:
    @respx.mock
    def test_sandbox_url(self, sandbox_client, sandbox_url):
        respx.get(f"{sandbox_url}/payment-links/1").mock(
            return_value=httpx.Response(
                200,
                json={"id": 1, "alias": "testAlias01"},
            )
        )
        result = sandbox_client.payment_links.get(1)

        assert result["url"] == "https://link.sandbox.hopysplit.com.br/testAlias01"
