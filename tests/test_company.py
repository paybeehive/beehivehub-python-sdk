"""Tests for company resource."""

import httpx
import respx


class TestCompanyGet:
    @respx.mock
    def test_get_company(self, client, prod_url):
        route = respx.get(f"{prod_url}/company").mock(
            return_value=httpx.Response(200, json={"id": "comp-123", "name": "Test Company"})
        )
        result = client.company.get()

        assert result == {"id": "comp-123", "name": "Test Company"}
        assert route.called


class TestCompanyUpdate:
    @respx.mock
    def test_update_company(self, client, prod_url):
        route = respx.put(f"{prod_url}/company").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "comp-123",
                    "name": "Test Company",
                    "invoiceDescriptor": "Beehive Hub",
                },
            )
        )
        result = client.company.update(
            {"invoiceDescriptor": "Beehive Hub", "details": {"averageRevenue": 10000}}
        )

        assert result["invoiceDescriptor"] == "Beehive Hub"
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"invoiceDescriptor" in sent_body
        assert b"details" in sent_body
