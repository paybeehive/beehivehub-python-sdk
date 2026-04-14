"""Tests for client module."""

import pytest
import respx

from beehivehub.client import BeehiveHubClient, create_beehivehub_client
from beehivehub.exceptions import BeehiveHubError
from beehivehub.resources.balance import Balance
from beehivehub.resources.bank_accounts import BankAccounts
from beehivehub.resources.company import Company
from beehivehub.resources.customers import Customers
from beehivehub.resources.payment_links import PaymentLinks
from beehivehub.resources.recipients import Recipients
from beehivehub.resources.transactions import Transactions
from beehivehub.resources.transfers import Transfers


class TestCreateClient:
    def test_returns_client_with_all_resources(self):
        client = create_beehivehub_client("test-api-key")
        assert isinstance(client, BeehiveHubClient)
        assert isinstance(client.transactions, Transactions)
        assert isinstance(client.customers, Customers)
        assert isinstance(client.balance, Balance)
        assert isinstance(client.recipients, Recipients)
        assert isinstance(client.bank_accounts, BankAccounts)
        assert isinstance(client.transfers, Transfers)
        assert isinstance(client.company, Company)
        assert isinstance(client.payment_links, PaymentLinks)

    def test_default_environment_is_production(self):
        client = create_beehivehub_client("test-api-key")
        assert isinstance(client, BeehiveHubClient)

    @respx.mock
    def test_sandbox_environment(self):
        client = create_beehivehub_client("test-api-key", environment="sandbox")
        assert isinstance(client, BeehiveHubClient)

    def test_empty_api_key_raises_error(self):
        with pytest.raises(BeehiveHubError) as exc_info:
            create_beehivehub_client("")
        assert "API key is required" in str(exc_info.value)

    def test_whitespace_api_key_raises_error(self):
        with pytest.raises(BeehiveHubError):
            create_beehivehub_client("   ")
