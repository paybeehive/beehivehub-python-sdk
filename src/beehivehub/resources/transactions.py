"""Transactions resource."""

from __future__ import annotations

from typing import Any

from beehivehub.requests import RequestFunction


class Transactions:
    """Operations on transactions.

    Args:
        request: Configured HTTP request function.
    """

    def __init__(self, request: RequestFunction) -> None:
        self._request = request

    def create(self, data: dict[str, Any]) -> Any:
        """Create a new payment transaction.

        Args:
            data: Transaction payload (use CreateTransactionData.model_dump(exclude_none=True)).

        Returns:
            The created transaction object.
        """
        return self._request("/transactions", method="POST", data=data)

    def list(self, params: dict[str, Any] | None = None) -> Any:
        """List transactions with optional filters.

        Args:
            params: Query parameters (status, paymentMethods, etc.). None values are filtered out.

        Returns:
            A list of transaction objects.
        """
        filtered = {k: v for k, v in params.items() if v is not None} if params else None
        return self._request("/transactions", method="GET", params=filtered or None)

    def get(self, id: int) -> Any:
        """Get a transaction by ID.

        Args:
            id: Transaction ID.

        Returns:
            The transaction object.
        """
        return self._request(f"/transactions/{id}", method="GET")

    def refund(self, id: int, amount: int | None = None) -> Any:
        """Refund a transaction totally or partially.

        Args:
            id: Transaction ID.
            amount: Partial refund amount in cents. If None, refunds the full amount.

        Returns:
            The updated transaction object.
        """
        data = {"amount": amount} if amount is not None else None
        return self._request(f"/transactions/{id}/refund", method="POST", data=data)

    def update_delivery(self, id: int, data: dict[str, Any]) -> Any:
        """Update the delivery status of a transaction.

        Args:
            id: Transaction ID.
            data: Delivery status payload
                (use UpdateDeliveryStatusData.model_dump(exclude_none=True)).

        Returns:
            The updated transaction object.
        """
        return self._request(f"/transactions/{id}/delivery", method="PUT", data=data)
