"""Tests for balance resource."""

import httpx
import respx


class TestBalanceGet:
    @respx.mock
    def test_get_available_balance(self, client, prod_url):
        route = respx.get(f"{prod_url}/balance/available").mock(
            return_value=httpx.Response(200, json={"amount": 3705, "recipientId": 916})
        )
        result = client.balance.get()

        assert result == {"amount": 3705, "recipientId": 916}
        assert route.called
