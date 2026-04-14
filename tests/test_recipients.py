"""Tests for recipients resource."""

import httpx
import respx


class TestRecipientsCreate:
    @respx.mock
    def test_create_recipient(self, client, prod_url):
        route = respx.post(f"{prod_url}/recipients").mock(
            return_value=httpx.Response(
                200,
                json={"id": 916, "legalName": "Recebedor Teste"},
            )
        )
        data = {
            "legalName": "Recebedor Teste",
            "document": {"type": "cpf", "number": "12345678900"},
            "transferSettings": {
                "transferEnabled": True,
                "automaticAnticipationEnabled": False,
                "anticipatableVolumePercentage": 0,
            },
            "bankAccount": {
                "bankCode": "001",
                "agencyNumber": "1234",
                "accountNumber": "12345",
                "accountDigit": "6",
                "type": "conta_corrente",
                "legalName": "Recebedor Teste",
                "documentNumber": "12345678900",
                "documentType": "cpf",
            },
        }
        result = client.recipients.create(data)

        assert result["id"] == 916
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"legalName" in sent_body


class TestRecipientsList:
    @respx.mock
    def test_list_recipients(self, client, prod_url):
        route = respx.get(f"{prod_url}/recipients").mock(
            return_value=httpx.Response(200, json=[{"id": 916}, {"id": 917}])
        )
        result = client.recipients.list()

        assert result == [{"id": 916}, {"id": 917}]
        assert route.called


class TestRecipientsGet:
    @respx.mock
    def test_get_by_id(self, client, prod_url):
        respx.get(f"{prod_url}/recipients/916").mock(
            return_value=httpx.Response(200, json={"id": 916, "legalName": "Recebedor Teste"})
        )
        result = client.recipients.get(916)

        assert result == {"id": 916, "legalName": "Recebedor Teste"}


class TestRecipientsUpdate:
    @respx.mock
    def test_update_recipient(self, client, prod_url):
        route = respx.put(f"{prod_url}/recipients/916").mock(
            return_value=httpx.Response(200, json={"id": 916, "legalName": "Nome Atualizado"})
        )
        result = client.recipients.update(916, {"legalName": "Nome Atualizado"})

        assert result == {"id": 916, "legalName": "Nome Atualizado"}
        assert route.called
        sent_body = route.calls[0].request.content
        assert b"Nome Atualizado" in sent_body
