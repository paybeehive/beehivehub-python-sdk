"""Tests for transfers resource."""

import httpx
import respx


class TestTransfersCreate:
    @respx.mock
    def test_create_simple_transfer(self, client, prod_url):
        route = respx.post(f"{prod_url}/transfers").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 1838,
                    "amount": 50000,
                    "recipientId": 916,
                    "status": "pending",
                },
            )
        )
        data = {"amount": 50000, "recipientId": 916}
        result = client.transfers.create(data)

        assert result["id"] == 1838
        assert result["status"] == "pending"
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"50000" in sent_body
        assert b"recipientId" in sent_body

    @respx.mock
    def test_create_transfer_with_bank_account(self, client, prod_url):
        route = respx.post(f"{prod_url}/transfers").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 1839,
                    "amount": 50000,
                    "recipientId": 916,
                    "status": "pending",
                },
            )
        )
        data = {
            "amount": 50000,
            "recipientId": 916,
            "bankAccount": {
                "bankCode": "001",
                "agencyNumber": "1234",
                "accountNumber": "12345",
                "accountDigit": "6",
                "type": "conta_corrente",
                "legalName": "Teste",
                "documentNumber": "12345678900",
                "documentType": "cpf",
            },
        }
        result = client.transfers.create(data)

        assert result["id"] == 1839
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"bankAccount" in sent_body


class TestTransfersGet:
    @respx.mock
    def test_get_by_id(self, client, prod_url):
        respx.get(f"{prod_url}/transfers/1838").mock(
            return_value=httpx.Response(
                200,
                json={"id": 1838, "amount": 50000, "status": "pending"},
            )
        )
        result = client.transfers.get(1838)

        assert result == {"id": 1838, "amount": 50000, "status": "pending"}
