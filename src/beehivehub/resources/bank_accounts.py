"""Bank accounts resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class BankAccounts:
    """Operations on bank accounts of a recipient.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def create(self, recipient_id: int, data: dict[str, Any]) -> Any:
        """Add a bank account to a recipient.

        Args:
            recipient_id: Recipient ID.
            data: Bank account payload (use CreateBankAccountData.model_dump(exclude_none=True)).

        Returns:
            The created bank account object.
        """
        return self._request(f"/recipients/{recipient_id}/bank-accounts", method="POST", data=data)

    def list(self, recipient_id: int) -> Any:
        """List bank accounts of a recipient.

        Args:
            recipient_id: Recipient ID.

        Returns:
            A list of bank account objects.
        """
        return self._request(f"/recipients/{recipient_id}/bank-accounts", method="GET")
