"""Tests for customers resource."""

import httpx
import respx


class TestCustomersCreate:
    @respx.mock
    def test_create_customer(self, client, prod_url):
        route = respx.post(f"{prod_url}/customers").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 123,
                    "name": "Test Customer",
                    "email": "test@example.com",
                },
            )
        )
        data = {
            "name": "Test Customer",
            "email": "test@example.com",
            "document": {"type": "cpf", "number": "12345678900"},
            "phone": "11999999999",
        }
        result = client.customers.create(data)

        assert result["id"] == 123
        assert result["name"] == "Test Customer"
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"name" in sent_body
        assert b"email" in sent_body


class TestCustomersList:
    @respx.mock
    def test_list_by_email(self, client, prod_url):
        route = respx.get(f"{prod_url}/customers").mock(
            return_value=httpx.Response(200, json=[{"id": 123}, {"id": 456}])
        )
        result = client.customers.list({"email": "cliente@example.com"})

        assert result == [{"id": 123}, {"id": 456}]
        assert route.called
        request_url = str(route.calls[0].request.url)
        assert "email=cliente%40example.com" in request_url


class TestCustomersGet:
    @respx.mock
    def test_get_by_id(self, client, prod_url):
        respx.get(f"{prod_url}/customers/123").mock(
            return_value=httpx.Response(200, json={"id": 123, "name": "Test Customer"})
        )
        result = client.customers.get(123)

        assert result == {"id": 123, "name": "Test Customer"}
