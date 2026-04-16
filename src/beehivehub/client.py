"""Client factory for the BeeHive Hub SDK."""

from __future__ import annotations

from dataclasses import dataclass

from beehivehub.exceptions import BeehiveHubError
from beehivehub.requests import create_request
from beehivehub.resources.balance import Balance
from beehivehub.resources.bank_accounts import BankAccounts
from beehivehub.resources.company import Company
from beehivehub.resources.customers import Customers
from beehivehub.resources.payment_links import PaymentLinks
from beehivehub.resources.recipients import Recipients
from beehivehub.resources.transactions import Transactions
from beehivehub.resources.transfers import Transfers


@dataclass(frozen=True)
class BeehiveHubClient:
    """SDK client with all API resources.

    Attributes:
        transactions: Operations on transactions.
        customers: Operations on customers.
        balance: Operations on account balance.
        recipients: Operations on recipients.
        bank_accounts: Operations on bank accounts.
        transfers: Operations on transfers.
        company: Operations on company data.
        payment_links: Operations on payment links.
    """

    transactions: Transactions
    customers: Customers
    balance: Balance
    recipients: Recipients
    bank_accounts: BankAccounts
    transfers: Transfers
    company: Company
    payment_links: PaymentLinks


def create_beehivehub_client(
    api_key: str,
    environment: str = "production",
) -> BeehiveHubClient:
    """Create a BeeHive Hub SDK client.

    Args:
        api_key: API key for authentication. Must not be empty.
        environment: API environment — "production" or "sandbox".

    Returns:
        A configured client with all API resources.

    Raises:
        BeehiveHubError: If api_key is empty.
    """
    if not api_key or not api_key.strip():
        raise BeehiveHubError("API key is required")

    request = create_request(api_key, environment)

    return BeehiveHubClient(
        transactions=Transactions(request),
        customers=Customers(request),
        balance=Balance(request),
        recipients=Recipients(request),
        bank_accounts=BankAccounts(request),
        transfers=Transfers(request),
        company=Company(request),
        payment_links=PaymentLinks(request, environment),
    )
