"""Tests for bank accounts resource."""

import httpx
import respx


class TestBankAccountsCreate:
    @respx.mock
    def test_create_bank_account(self, client, prod_url):
        route = respx.post(f"{prod_url}/recipients/916/bank-accounts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 1048,
                    "bankCode": "001",
                    "agencyNumber": "1234",
                    "accountNumber": "12345",
                    "accountDigit": "6",
                    "type": "conta_corrente",
                    "legalName": "Teste",
                    "documentNumber": "12345678900",
                    "documentType": "cpf",
                    "isActive": True,
                    "isVisible": True,
                },
            )
        )
        data = {
            "bankCode": "001",
            "agencyNumber": "1234",
            "accountNumber": "12345",
            "accountDigit": "6",
            "type": "conta_corrente",
            "legalName": "Teste",
            "documentNumber": "12345678900",
            "documentType": "cpf",
        }
        result = client.bank_accounts.create(916, data)

        assert result["id"] == 1048
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"bankCode" in sent_body


class TestBankAccountsList:
    @respx.mock
    def test_list_bank_accounts(self, client, prod_url):
        route = respx.get(f"{prod_url}/recipients/916/bank-accounts").mock(
            return_value=httpx.Response(200, json=[{"id": 1048}, {"id": 1049}])
        )
        result = client.bank_accounts.list(916)

        assert result == [{"id": 1048}, {"id": 1049}]
        assert route.called
