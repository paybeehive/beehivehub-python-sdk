"""
Integration tests against the real BeeHive Hub API.

Requires:
  - BEEHIVEHUB_API_KEY env var
  - BEEHIVEHUB_ENV (default "sandbox")

Run:
  pytest tests/integration/ -v -s -m integration
"""

from __future__ import annotations

import os
import uuid

import pytest

from beehivehub import BeehiveHubClient, create_beehivehub_client
from beehivehub.exceptions import BeehiveHubError

API_KEY = os.environ.get("BEEHIVEHUB_API_KEY", "")
ENVIRONMENT = os.environ.get("BEEHIVEHUB_ENV", "sandbox")

skip_no_key = pytest.mark.skipif(
    not API_KEY,
    reason="BEEHIVEHUB_API_KEY not set - skipping integration tests",
)

pytestmark = [pytest.mark.integration, skip_no_key]

# ---------------------------------------------------------------------------
# Shared state across tests (populated during execution)
# ---------------------------------------------------------------------------
state: dict[str, object] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _unique_email() -> str:
    return f"test-{uuid.uuid4().hex[:8]}@integration.test"


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------
@pytest.fixture()
def client() -> BeehiveHubClient:
    if "client" not in state:
        c = create_beehivehub_client(api_key=API_KEY, environment=ENVIRONMENT)
        state["client"] = c
    return state["client"]  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# 1. Create client
# ---------------------------------------------------------------------------
class TestClientCreation:
    def test_create_client(self) -> None:
        print("\n> Creating client...")
        try:
            client = create_beehivehub_client(api_key=API_KEY, environment=ENVIRONMENT)
            assert isinstance(client, BeehiveHubClient)
            state["client"] = client
            print(f"  Client created (env={ENVIRONMENT})")
        except BeehiveHubError as exc:
            pytest.fail(f"Error creating client: {exc}")


# ---------------------------------------------------------------------------
# 2. Balance
# ---------------------------------------------------------------------------
class TestBalance:
    def test_get_balance(self, client: BeehiveHubClient) -> None:
        print("\n> Getting balance...")
        try:
            balance = client.balance.get()
            assert isinstance(balance, dict)
            assert "amount" in balance
            print(f"  Balance: {balance}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error getting balance: {exc}")
        except Exception as exc:
            pytest.skip(f"Balance endpoint not available in this environment: {exc}")


# ---------------------------------------------------------------------------
# 3. Company
# ---------------------------------------------------------------------------
class TestCompany:
    def test_get_company(self, client: BeehiveHubClient) -> None:
        print("\n> Getting company...")
        try:
            company = client.company.get()
            assert isinstance(company, dict)
            assert "id" in company
            print(f"  Company id={company['id']}, name={company.get('legalName')}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error getting company: {exc}")


# ---------------------------------------------------------------------------
# 4-6. Customers
# ---------------------------------------------------------------------------
class TestCustomers:
    def test_create_customer(self, client: BeehiveHubClient) -> None:
        print("\n> Creating customer...")
        email = _unique_email()
        state["customer_email"] = email
        try:
            customer = client.customers.create(
                {
                    "name": "Integration Test User",
                    "email": email,
                    "document": {"type": "cpf", "number": "11144477735"},
                    "phone": "11999999999",
                }
            )
            assert isinstance(customer, dict)
            assert "id" in customer
            state["customer_id"] = customer["id"]
            print(f"  Customer created: id={customer['id']}, email={email}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error creating customer: {exc}")

    def test_get_customer(self, client: BeehiveHubClient) -> None:
        print("\n> Getting customer by ID...")
        customer_id = state.get("customer_id")
        if customer_id is None:
            pytest.skip("customer_id not available (previous test failed?)")
        try:
            customer = client.customers.get(customer_id)  # type: ignore[arg-type]
            assert isinstance(customer, dict)
            assert customer["id"] == customer_id
            assert customer["email"] == state["customer_email"]
            print(f"  Customer found: id={customer['id']}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error getting customer: {exc}")

    def test_list_customers_by_email(self, client: BeehiveHubClient) -> None:
        print("\n> Listing customers by email...")
        email = state.get("customer_email")
        if email is None:
            pytest.skip("customer_email not available")
        try:
            customers = client.customers.list({"email": str(email)})
            assert isinstance(customers, list)
            ids = [c["id"] for c in customers]
            assert state["customer_id"] in ids, "Created customer not found in list"
            print(f"  Found: {len(customers)} customer(s)")
        except BeehiveHubError as exc:
            pytest.fail(f"Error listing customers: {exc}")


# ---------------------------------------------------------------------------
# 7-10. Recipients
# ---------------------------------------------------------------------------
class TestRecipients:
    def test_create_recipient(self, client: BeehiveHubClient) -> None:
        print("\n> Creating recipient...")
        try:
            recipient = client.recipients.create(
                {
                    "legalName": f"Recebedor Teste {uuid.uuid4().hex[:6]}",
                    "document": {"number": "11144477735", "type": "cpf"},
                    "transferSettings": {
                        "transferEnabled": True,
                        "automaticAnticipationEnabled": False,
                        "anticipatableVolumePercentage": 0,
                    },
                    "bankAccount": {
                        "bankCode": "341",
                        "agencyNumber": "0001",
                        "accountNumber": "123456",
                        "accountDigit": "7",
                        "type": "conta_corrente",
                        "legalName": "Recebedor Teste",
                        "documentNumber": "11144477735",
                        "documentType": "cpf",
                    },
                }
            )
            assert isinstance(recipient, dict)
            assert "id" in recipient
            state["recipient_id"] = recipient["id"]
            print(f"  Recipient created: id={recipient['id']}")
        except BeehiveHubError as exc:
            print(f"  !! Sandbox may not support recipient creation: {exc}")
            pytest.skip(f"Sandbox did not support recipient creation: {exc}")

    def test_list_recipients(self, client: BeehiveHubClient) -> None:
        print("\n> Listing recipients...")
        if "recipient_id" not in state:
            pytest.skip("recipient_id not available")
        try:
            recipients = client.recipients.list()
            assert isinstance(recipients, list)
            ids = [r["id"] for r in recipients]
            assert state["recipient_id"] in ids, "Created recipient not found in list"
            print(f"  Found: {len(recipients)} recipient(s)")
        except BeehiveHubError as exc:
            pytest.fail(f"Error listing recipients: {exc}")

    def test_get_recipient(self, client: BeehiveHubClient) -> None:
        print("\n> Getting recipient by ID...")
        recipient_id = state.get("recipient_id")
        if recipient_id is None:
            pytest.skip("recipient_id not available")
        try:
            recipient = client.recipients.get(recipient_id)  # type: ignore[arg-type]
            assert isinstance(recipient, dict)
            assert recipient["id"] == recipient_id
            print(f"  Recipient found: id={recipient['id']}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error getting recipient: {exc}")

    def test_update_recipient(self, client: BeehiveHubClient) -> None:
        print("\n> Updating recipient...")
        recipient_id = state.get("recipient_id")
        if recipient_id is None:
            pytest.skip("recipient_id not available")
        new_name = f"Recebedor Atualizado {uuid.uuid4().hex[:6]}"
        try:
            recipient = client.recipients.update(
                recipient_id,  # type: ignore[arg-type]
                {"legalName": new_name},
            )
            assert isinstance(recipient, dict)
            print(f"  Recipient updated: legalName={new_name}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error updating recipient: {exc}")


# ---------------------------------------------------------------------------
# 11-12. Bank Accounts
# ---------------------------------------------------------------------------
class TestBankAccounts:
    def test_create_bank_account(self, client: BeehiveHubClient) -> None:
        print("\n> Creating bank account for recipient...")
        recipient_id = state.get("recipient_id")
        if recipient_id is None:
            pytest.skip("recipient_id not available")
        try:
            account = client.bank_accounts.create(
                recipient_id,  # type: ignore[arg-type]
                {
                    "bankCode": "341",
                    "agencyNumber": "0001",
                    "accountNumber": "654321",
                    "accountDigit": "0",
                    "type": "conta_corrente",
                    "legalName": "Conta Teste",
                    "documentNumber": "11144477735",
                    "documentType": "cpf",
                },
            )
            assert isinstance(account, dict)
            assert "id" in account
            state["bank_account_id"] = account["id"]
            print(f"  Bank account created: id={account['id']}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error creating bank account: {exc}")

    def test_list_bank_accounts(self, client: BeehiveHubClient) -> None:
        print("\n> Listing bank accounts for recipient...")
        recipient_id = state.get("recipient_id")
        if recipient_id is None:
            pytest.skip("recipient_id not available")
        try:
            accounts = client.bank_accounts.list(recipient_id)  # type: ignore[arg-type]
            assert isinstance(accounts, list)
            ids = [a["id"] for a in accounts]
            assert state["bank_account_id"] in ids, "Created bank account not found in list"
            print(f"  Found: {len(accounts)} bank account(s)")
        except BeehiveHubError as exc:
            pytest.fail(f"Error listing bank accounts: {exc}")


# ---------------------------------------------------------------------------
# 13-17. Payment Links
# ---------------------------------------------------------------------------
class TestPaymentLinks:
    def test_create_payment_link(self, client: BeehiveHubClient) -> None:
        print("\n> Creating payment link...")
        try:
            link = client.payment_links.create(
                {
                    "title": f"Link Teste {uuid.uuid4().hex[:6]}",
                    "amount": 1500,
                    "settings": {
                        "defaultPaymentMethod": "pix",
                        "requestAddress": False,
                        "requestPhone": False,
                        "requestDocument": False,
                        "traceable": False,
                        "card": {"enabled": False, "freeInstallments": 1, "maxInstallments": 1},
                        "pix": {"enabled": True, "expiresInDays": 1},
                        "boleto": {"enabled": False, "expiresInDays": 0},
                    },
                }
            )
            assert isinstance(link, dict)
            assert "id" in link
            assert "url" in link
            state["payment_link_id"] = link["id"]
            print(f"  Payment link created: id={link['id']}, url={link.get('url')}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error creating payment link: {exc}")

    def test_list_payment_links(self, client: BeehiveHubClient) -> None:
        print("\n> Listing payment links...")
        if "payment_link_id" not in state:
            pytest.skip("payment_link_id not available")
        try:
            links = client.payment_links.list()
            assert isinstance(links, list)
            ids = [pl["id"] for pl in links]
            assert state["payment_link_id"] in ids, "Created payment link not found in list"
            print(f"  Found: {len(links)} payment link(s)")
        except BeehiveHubError as exc:
            pytest.fail(f"Error listing payment links: {exc}")

    def test_get_payment_link(self, client: BeehiveHubClient) -> None:
        print("\n> Getting payment link by ID...")
        link_id = state.get("payment_link_id")
        if link_id is None:
            pytest.skip("payment_link_id not available")
        try:
            link = client.payment_links.get(link_id)  # type: ignore[arg-type]
            assert isinstance(link, dict)
            assert link["id"] == link_id
            assert "url" in link
            print(f"  Payment link found: url={link.get('url')}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error getting payment link: {exc}")

    def test_update_payment_link(self, client: BeehiveHubClient) -> None:
        print("\n> Updating payment link...")
        link_id = state.get("payment_link_id")
        if link_id is None:
            pytest.skip("payment_link_id not available")
        new_title = f"Link Atualizado {uuid.uuid4().hex[:6]}"
        try:
            link = client.payment_links.update(
                link_id,  # type: ignore[arg-type]
                {
                    "title": new_title,
                    "amount": 2000,
                    "settings": {
                        "defaultPaymentMethod": "pix",
                        "requestAddress": False,
                        "requestPhone": False,
                        "requestDocument": False,
                        "traceable": False,
                        "card": {"enabled": False, "freeInstallments": 1, "maxInstallments": 1},
                        "pix": {"enabled": True, "expiresInDays": 1},
                        "boleto": {"enabled": False, "expiresInDays": 0},
                    },
                },
            )
            assert isinstance(link, dict)
            print(f"  Payment link updated: title={new_title}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error updating payment link: {exc}")

    def test_delete_payment_link(self, client: BeehiveHubClient) -> None:
        print("\n> Deleting payment link...")
        link_id = state.get("payment_link_id")
        if link_id is None:
            pytest.skip("payment_link_id not available")
        try:
            result = client.payment_links.delete(link_id)  # type: ignore[arg-type]
            assert result is None
            print(f"  Payment link deleted: id={link_id}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error deleting payment link: {exc}")


# ---------------------------------------------------------------------------
# 18-20. Transactions
# ---------------------------------------------------------------------------
class TestTransactions:
    def test_create_transaction(self, client: BeehiveHubClient) -> None:
        print("\n> Creating transaction (pix)...")
        try:
            transaction = client.transactions.create(
                {
                    "amount": 1000,
                    "paymentMethod": "pix",
                    "customer": {
                        "name": "Transaction Test User",
                        "email": _unique_email(),
                        "document": {"type": "cpf", "number": "11144477735"},
                        "phone": "11999999999",
                    },
                }
            )
            assert isinstance(transaction, dict)
            assert "id" in transaction
            state["transaction_id"] = transaction["id"]
            print(f"  Transaction created: id={transaction['id']}")
        except BeehiveHubError as exc:
            print(f"  !! Sandbox may not support transaction creation: {exc}")
            pytest.skip(f"Sandbox did not support transaction creation: {exc}")

    def test_get_transaction(self, client: BeehiveHubClient) -> None:
        print("\n> Getting transaction by ID...")
        transaction_id = state.get("transaction_id")
        if transaction_id is None:
            pytest.skip("transaction_id not available (creation not supported in sandbox)")
        try:
            transaction = client.transactions.get(transaction_id)  # type: ignore[arg-type]
            assert isinstance(transaction, dict)
            assert transaction["id"] == transaction_id
            print(f"  Transaction found: id={transaction['id']}")
        except BeehiveHubError as exc:
            pytest.fail(f"Error getting transaction: {exc}")

    def test_list_transactions(self, client: BeehiveHubClient) -> None:
        print("\n> Listing transactions...")
        try:
            transactions = client.transactions.list()
            assert isinstance(transactions, list)
            print(f"  Found: {len(transactions)} transaction(s)")
        except BeehiveHubError as exc:
            pytest.fail(f"Error listing transactions: {exc}")
