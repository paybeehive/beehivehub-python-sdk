"""Tests for transactions resource."""

import httpx
import respx


class TestTransactionsCreate:
    @respx.mock
    def test_create_transaction(self, client, prod_url):
        route = respx.post(f"{prod_url}/transactions").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "paid"})
        )
        data = {"amount": 1000, "paymentMethod": "pix", "customer": {"name": "Test"}}
        result = client.transactions.create(data)

        assert result == {"id": "123", "status": "paid"}
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"amount" in sent_body
        assert b"paymentMethod" in sent_body


class TestTransactionsList:
    @respx.mock
    def test_list_with_filters(self, client, prod_url):
        route = respx.get(f"{prod_url}/transactions").mock(
            return_value=httpx.Response(200, json=[{"id": "123"}, {"id": "456"}])
        )
        result = client.transactions.list({"status": "paid", "paymentMethods": "pix"})

        assert result == [{"id": "123"}, {"id": "456"}]
        assert route.called
        request_url = str(route.calls[0].request.url)
        assert "status=paid" in request_url
        assert "paymentMethods=pix" in request_url

    @respx.mock
    def test_list_with_multiple_filters(self, client, prod_url):
        route = respx.get(f"{prod_url}/transactions").mock(
            return_value=httpx.Response(200, json=[])
        )
        client.transactions.list({
            "status": "paid",
            "deliveryStatus": "delivered",
            "email": "test@test.com",
            "documentNumber": "12345678900",
        })

        request_url = str(route.calls[0].request.url)
        assert "status=paid" in request_url
        assert "deliveryStatus=delivered" in request_url
        assert "email=test%40test.com" in request_url
        assert "documentNumber=12345678900" in request_url

    @respx.mock
    def test_list_filters_none_values(self, client, prod_url):
        route = respx.get(f"{prod_url}/transactions").mock(
            return_value=httpx.Response(200, json=[])
        )
        client.transactions.list({"status": "paid", "email": None})

        request_url = str(route.calls[0].request.url)
        assert "status=paid" in request_url
        assert "email" not in request_url

    @respx.mock
    def test_list_without_params(self, client, prod_url):
        route = respx.get(f"{prod_url}/transactions").mock(
            return_value=httpx.Response(200, json=[{"id": "123"}])
        )
        result = client.transactions.list()

        assert result == [{"id": "123"}]
        assert route.called


class TestTransactionsGet:
    @respx.mock
    def test_get_by_id(self, client, prod_url):
        route = respx.get(f"{prod_url}/transactions/123").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "paid"})
        )
        result = client.transactions.get(123)

        assert result == {"id": "123", "status": "paid"}
        assert route.called


class TestTransactionsRefund:
    @respx.mock
    def test_full_refund(self, client, prod_url):
        route = respx.post(f"{prod_url}/transactions/123/refund").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "refunded"})
        )
        result = client.transactions.refund(123)

        assert result == {"id": "123", "status": "refunded"}
        assert route.called

    @respx.mock
    def test_partial_refund(self, client, prod_url):
        route = respx.post(f"{prod_url}/transactions/123/refund").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "refunded"})
        )
        result = client.transactions.refund(123, amount=500)

        assert result["status"] == "refunded"
        sent_body = route.calls[0].request.content
        assert b"500" in sent_body


class TestTransactionsUpdateDelivery:
    @respx.mock
    def test_update_delivery(self, client, prod_url):
        route = respx.put(f"{prod_url}/transactions/123/delivery").mock(
            return_value=httpx.Response(200, json={"id": "123", "status": "paid"})
        )
        data = {"tracking_code": "BR123", "status": "shipped"}
        result = client.transactions.update_delivery(123, data)

        assert result == {"id": "123", "status": "paid"}
        assert route.called
