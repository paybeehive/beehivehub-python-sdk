"""Data models for the BeeHive Hub SDK."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


def _to_camel(string: str) -> str:
    """Convert snake_case to camelCase."""
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


Environment = Literal["production", "sandbox"]

TransactionStatus = Literal[
    "processing",
    "authorized",
    "paid",
    "refunded",
    "waiting_payment",
    "pending_refund",
    "refused",
    "chargedback",
    "analyzing",
    "pending_review",
    "unknown",
]

TransactionPaymentMethod = Literal["credit_card", "debit_card", "boleto", "pix"]

TransferStatus = Literal["pending", "bank_processing", "success", "failed"]


# ---------------------------------------------------------------------------
# Base model with camelCase alias support
# ---------------------------------------------------------------------------


class ApiModel(BaseModel):
    """Base model with camelCase alias generation for API compatibility."""

    model_config = ConfigDict(
        alias_generator=_to_camel,
        populate_by_name=True,
    )


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------


class Document(ApiModel):
    """CPF or CNPJ document."""

    type: str
    number: str


class Address(ApiModel):
    """Complete address."""

    street: str | None = None
    street_number: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    country: str | None = None


class Item(ApiModel):
    """Line item in a transaction."""

    external_ref: str | None = None
    title: str | None = None
    unit_price: int | None = None
    quantity: int | None = None
    tangible: bool | None = None


class Split(ApiModel):
    """Split of payment between recipients."""

    recipient_id: int | None = None
    amount: int | None = None
    net_amount: int | None = None
    charge_processing_fee: bool | None = None


class Fee(ApiModel):
    """Fee breakdown of a transaction."""

    fixed_amount: int | None = None
    spread_percentage: int | None = None
    estimated_fee: int | None = None
    net_amount: int | None = None


class Pix(ApiModel):
    """PIX payment data."""

    qrcode: str | None = None
    expiration_date: str | None = None
    end2_end_id: str | None = None
    receipt_url: str | None = None


class Boleto(ApiModel):
    """Boleto payment data."""

    url: str | None = None
    barcode: str | None = None
    digitable_line: str | None = None
    expiration_date: str | None = None
    instructions: str | None = None


class Delivery(ApiModel):
    """Delivery tracking data."""

    status: str | None = None
    tracking_code: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class Refund(ApiModel):
    """Refund of a transaction."""

    amount: int | None = None
    trigger: str | None = None
    pre_chargeback: bool | None = None
    pre_chargeback_cents: int | None = None
    created_at: str | None = None


# ---------------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------------


class CreateTransactionData(ApiModel):
    """Payload for creating a transaction."""

    amount: int
    payment_method: TransactionPaymentMethod
    customer: CreateCustomerData | dict[str, Any] | None = None
    installments: int | None = None
    items: list[Item] | None = None
    splits: list[Split] | None = None
    shipping: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    postback_url: str | None = None


class ListTransactionsParams(ApiModel):
    """Filters for listing transactions."""

    id: int | None = None
    payment_methods: str | None = None
    status: str | None = None
    delivery_status: str | None = None
    installments: str | None = None
    name: str | None = None
    email: str | None = None
    document_number: str | None = None
    phone: str | None = None
    traceable: bool | None = None


class UpdateDeliveryStatusData(ApiModel):
    """Payload for updating delivery status."""

    status: str | None = None
    tracking_code: str | None = None


class Transaction(ApiModel):
    """Complete transaction object."""

    id: int | None = None
    status: TransactionStatus | str | None = None
    amount: int | None = None
    paid_amount: int | None = None
    refunded_amount: int | None = None
    company_id: int | None = None
    payment_method: TransactionPaymentMethod | str | None = None
    installments: int | None = None
    postback_url: str | None = None
    traceable: bool | None = None
    ip: str | None = None
    authorization_code: str | None = None
    base_price: int | None = None
    interest_rate: float | None = None
    origin: str | None = None
    subaccount_id: int | None = None
    balance_managed_by: Any | None = None
    external_ref: str | None = None
    secure_id: str | None = None
    secure_url: str | None = None
    customer: Customer | None = None
    fee: Fee | None = None
    card: dict[str, Any] | None = None
    shipping: dict[str, Any] | None = None
    items: list[Item] | None = None
    splits: list[Split] | None = None
    pix: Pix | None = None
    boleto: Boleto | None = None
    refused_reason: Any | None = None
    delivery: Delivery | None = None
    payer: Any | None = None
    refunds: list[Refund] | None = None
    metadata: dict[str, Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    paid_at: str | None = None


# ---------------------------------------------------------------------------
# Customers
# ---------------------------------------------------------------------------


class CreateCustomerData(ApiModel):
    """Payload for creating a customer."""

    name: str
    email: str
    document: Document | dict[str, Any]
    phone: str
    birthdate: str | None = None
    address: Address | None = None


class Customer(ApiModel):
    """Complete customer object."""

    id: int | None = None
    name: str | None = None
    email: str | None = None
    document: Document | dict[str, Any] | None = None
    phone: str | None = None
    birthdate: str | None = None
    external_ref: str | None = None
    revenue: int | None = None
    address: Address | None = None
    created_at: str | None = None


# ---------------------------------------------------------------------------
# Balance
# ---------------------------------------------------------------------------


class Balance(ApiModel):
    """Available balance."""

    amount: int | None = None
    recipient_id: int | None = None


# ---------------------------------------------------------------------------
# Recipients
# ---------------------------------------------------------------------------


class CreateRecipientData(ApiModel):
    """Payload for creating a recipient."""

    legal_name: str
    document: Document | dict[str, Any]
    transfer_settings: dict[str, Any]
    bank_account: CreateBankAccountData | dict[str, Any]


class UpdateRecipientData(ApiModel):
    """Payload for updating a recipient."""

    legal_name: str | None = None


class Recipient(ApiModel):
    """Complete recipient object."""

    id: int | None = None
    company_id: int | None = None
    tenant_id: int | None = None
    legal_name: str | None = None
    document: Document | dict[str, Any] | None = None
    transfer_settings: dict[str, Any] | None = None
    balance: dict[str, Any] | None = None
    created_at: str | None = None


# ---------------------------------------------------------------------------
# Bank Accounts
# ---------------------------------------------------------------------------


class CreateBankAccountData(ApiModel):
    """Payload for creating a bank account."""

    bank_code: str
    agency_number: str
    account_number: str
    account_digit: str
    type: str
    legal_name: str
    document_number: str
    document_type: str


class BankAccount(ApiModel):
    """Complete bank account object."""

    id: int | None = None
    bank_code: str | None = None
    agency_number: str | None = None
    account_number: str | None = None
    account_digit: str | None = None
    agency_digit: str | None = None
    type: str | None = None
    legal_name: str | None = None
    document_number: str | None = None
    document_type: str | None = None
    is_active: bool | None = None
    is_visible: bool | None = None
    created_at: str | None = None


# ---------------------------------------------------------------------------
# Transfers
# ---------------------------------------------------------------------------


class CreateTransferData(ApiModel):
    """Payload for creating a transfer."""

    amount: int
    recipient_id: int
    bank_account: CreateBankAccountData | dict[str, Any] | None = None


class Transfer(ApiModel):
    """Complete transfer object."""

    id: int | None = None
    amount: int | None = None
    fee: int | None = None
    recipient_id: int | None = None
    company_id: int | None = None
    bank_account: BankAccount | dict[str, Any] | None = None
    status: TransferStatus | str | None = None
    type: str | None = None
    fail_reason: str | None = None
    metadata: dict[str, Any] | None = None
    external_ref: str | None = None
    postback_url: str | None = None
    description: str | None = None
    pix_key: str | None = None
    check_payer: Any | None = None
    pix_end2_end_id: str | None = None
    receipt_url: str | None = None
    secure_id: str | None = None
    crypto: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    transferred_at: str | None = None
    processed_at: str | None = None
    attempts: int | None = None
    next_attempt_at: str | None = None


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------


class UpdateCompanyData(ApiModel):
    """Payload for updating company data."""

    invoice_descriptor: str | None = None
    details: dict[str, Any] | None = None


class Company(ApiModel):
    """Company object — free-form structure with known base fields."""

    model_config = ConfigDict(
        alias_generator=_to_camel,
        populate_by_name=True,
        extra="allow",
    )

    id: int | str | None = None
    name: str | None = None


# ---------------------------------------------------------------------------
# Payment Links
# ---------------------------------------------------------------------------


class CreatePaymentLinkData(ApiModel):
    """Payload for creating a payment link."""

    title: str | None = None
    amount: int
    alias: str | None = None
    settings: dict[str, Any] | None = None


class UpdatePaymentLinkData(ApiModel):
    """Payload for updating a payment link — all fields optional."""

    title: str | None = None
    amount: int | None = None
    alias: str | None = None
    settings: dict[str, Any] | None = None


class PaymentLink(ApiModel):
    """Complete payment link object."""

    id: int | None = None
    company_id: int | None = None
    title: str | None = None
    amount: int | None = None
    alias: str | None = None
    url: str | None = None
    status: str | None = None
    settings: dict[str, Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None
