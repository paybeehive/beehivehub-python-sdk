"""Tests focused on paymentLinks alias generation and url field behavior."""

import json
import re

import httpx
import respx

from beehivehub.constants import PAYMENT_LINK_URL_PRODUCTION, PAYMENT_LINK_URL_SANDBOX
from beehivehub.utils import generate_alias

ALIAS_PATTERN = re.compile(r"^[a-zA-Z0-9]{10}$")


# ---------------------------------------------------------------------------
# Alias generation on create
# ---------------------------------------------------------------------------


class TestCreateAliasGeneration:
    @respx.mock
    def test_create_without_alias_generates_10_char_alphanumeric(self, client, prod_url):
        """1. create SEM alias -> body must contain a 10-char [a-zA-Z0-9] alias."""
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "placeholder"})
        )
        client.payment_links.create({"title": "link", "amount": 1000})

        sent = json.loads(route.calls[0].request.content)
        assert "alias" in sent
        assert ALIAS_PATTERN.match(sent["alias"])

    @respx.mock
    def test_create_with_explicit_alias_keeps_original(self, client, prod_url):
        """2. create COM alias explicito -> body must keep the original alias."""
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "myCustom99"})
        )
        client.payment_links.create({"title": "link", "amount": 1000, "alias": "myCustom99"})

        sent = json.loads(route.calls[0].request.content)
        assert sent["alias"] == "myCustom99"

    @respx.mock
    def test_create_with_empty_string_alias_generates_auto(self, client, prod_url):
        """3. create COM alias string vazia -> must auto-generate alias."""
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "placeholder"})
        )
        client.payment_links.create({"title": "link", "amount": 1000, "alias": ""})

        sent = json.loads(route.calls[0].request.content)
        assert sent["alias"] != ""
        assert ALIAS_PATTERN.match(sent["alias"])

    @respx.mock
    def test_create_with_none_alias_generates_auto(self, client, prod_url):
        """4. create COM alias None -> must auto-generate alias."""
        route = respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "placeholder"})
        )
        client.payment_links.create({"title": "link", "amount": 1000, "alias": None})

        sent = json.loads(route.calls[0].request.content)
        assert ALIAS_PATTERN.match(sent["alias"])


# ---------------------------------------------------------------------------
# Alias generation on update
# ---------------------------------------------------------------------------


class TestUpdateAliasGeneration:
    @respx.mock
    def test_update_without_alias_generates_auto(self, client, prod_url):
        """5. update SEM alias -> body must contain auto-generated alias."""
        route = respx.put(f"{prod_url}/payment-links/10").mock(
            return_value=httpx.Response(200, json={"id": 10, "amount": 5000})
        )
        client.payment_links.update(10, {"amount": 5000})

        sent = json.loads(route.calls[0].request.content)
        assert "alias" in sent
        assert ALIAS_PATTERN.match(sent["alias"])

    @respx.mock
    def test_update_with_explicit_alias_keeps_original(self, client, prod_url):
        """6. update COM alias explicito -> body must keep the original alias."""
        route = respx.put(f"{prod_url}/payment-links/10").mock(
            return_value=httpx.Response(200, json={"id": 10, "alias": "KeepMe1234"})
        )
        client.payment_links.update(10, {"amount": 5000, "alias": "KeepMe1234"})

        sent = json.loads(route.calls[0].request.content)
        assert sent["alias"] == "KeepMe1234"

    @respx.mock
    def test_update_with_empty_string_alias_generates_auto(self, client, prod_url):
        """7. update COM alias string vazia -> must auto-generate alias."""
        route = respx.put(f"{prod_url}/payment-links/10").mock(
            return_value=httpx.Response(200, json={"id": 10, "amount": 5000})
        )
        client.payment_links.update(10, {"amount": 5000, "alias": ""})

        sent = json.loads(route.calls[0].request.content)
        assert sent["alias"] != ""
        assert ALIAS_PATTERN.match(sent["alias"])


# ---------------------------------------------------------------------------
# URL field in responses
# ---------------------------------------------------------------------------


class TestResponseUrlField:
    @respx.mock
    def test_create_returns_url_from_alias(self, client, prod_url):
        """8. create returns object with url = PRODUCTION/alias."""
        respx.post(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "Abc1234567"})
        )
        result = client.payment_links.create({"title": "link", "amount": 1000})

        assert result["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/Abc1234567"

    @respx.mock
    def test_get_returns_url_from_alias(self, client, prod_url):
        """9. get returns object with url = PRODUCTION/alias."""
        respx.get(f"{prod_url}/payment-links/5").mock(
            return_value=httpx.Response(200, json={"id": 5, "alias": "Get1234567"})
        )
        result = client.payment_links.get(5)

        assert result["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/Get1234567"

    @respx.mock
    def test_list_adds_url_when_alias_present(self, client, prod_url):
        """10. list returns objects WITH url when alias is present."""
        respx.get(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"id": 1, "alias": "ListAlias1"},
                    {"id": 2, "alias": "ListAlias2"},
                ],
            )
        )
        result = client.payment_links.list()

        assert result[0]["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/ListAlias1"
        assert result[1]["url"] == f"{PAYMENT_LINK_URL_PRODUCTION}/ListAlias2"

    @respx.mock
    def test_list_no_url_when_alias_absent_or_empty(self, client, prod_url):
        """11. list returns objects WITHOUT url when alias is absent/empty."""
        respx.get(f"{prod_url}/payment-links").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"id": 1},
                    {"id": 2, "alias": ""},
                    {"id": 3, "alias": None},
                ],
            )
        )
        result = client.payment_links.list()

        for item in result:
            assert "url" not in item


# ---------------------------------------------------------------------------
# Sandbox URL
# ---------------------------------------------------------------------------


class TestSandboxUrl:
    @respx.mock
    def test_create_sandbox_uses_sandbox_url(self, sandbox_client, sandbox_url):
        """12. create em sandbox -> url uses PAYMENT_LINK_URL_SANDBOX/alias."""
        respx.post(f"{sandbox_url}/payment-links").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "SandBox001"})
        )
        result = sandbox_client.payment_links.create({"title": "link", "amount": 1000})

        assert result["url"] == f"{PAYMENT_LINK_URL_SANDBOX}/SandBox001"

    @respx.mock
    def test_get_sandbox_uses_sandbox_url(self, sandbox_client, sandbox_url):
        """13. get em sandbox -> url uses PAYMENT_LINK_URL_SANDBOX/alias."""
        respx.get(f"{sandbox_url}/payment-links/1").mock(
            return_value=httpx.Response(200, json={"id": 1, "alias": "SandGet001"})
        )
        result = sandbox_client.payment_links.get(1)

        assert result["url"] == f"{PAYMENT_LINK_URL_SANDBOX}/SandGet001"


# ---------------------------------------------------------------------------
# Alias quality validation
# ---------------------------------------------------------------------------


class TestAliasQuality:
    def test_generated_alias_always_matches_pattern(self):
        """14. Generate alias 100 times and confirm all match r'^[a-zA-Z0-9]{10}$'."""
        for _ in range(100):
            alias = generate_alias()
            assert ALIAS_PATTERN.match(alias), f"Invalid alias: {alias}"

    def test_generated_aliases_are_not_fixed(self):
        """15. Generate alias 2 times and confirm they differ (not constant)."""
        a = generate_alias()
        b = generate_alias()
        assert a != b, "Two generated aliases should not be identical"
