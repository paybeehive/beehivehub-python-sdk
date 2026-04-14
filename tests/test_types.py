"""Tests for Pydantic model alias generation and serialization."""

from beehivehub.types import (
    Address,
    BankAccount,
    Boleto,
    CreateBankAccountData,
    CreateCustomerData,
    CreatePaymentLinkData,
    CreateTransactionData,
    CreateTransferData,
    Delivery,
    Fee,
    Item,
    ListTransactionsParams,
    Pix,
    Refund,
    Split,
    Transaction,
    Transfer,
    UpdateCompanyData,
    UpdateDeliveryStatusData,
)


class TestAddressAlias:
    def test_street_number_alias(self):
        addr = Address(street_number="123")
        data = addr.model_dump(by_alias=True, exclude_none=True)
        assert "streetNumber" in data

    def test_zip_code_alias(self):
        addr = Address(zip_code="01234567")
        data = addr.model_dump(by_alias=True, exclude_none=True)
        assert "zipCode" in data
        assert "zip_code" not in data

    def test_complement_alias(self):
        addr = Address(complement="Apto 101")
        data = addr.model_dump(by_alias=True, exclude_none=True)
        assert "complement" in data

    def test_populate_by_camel_case(self):
        addr = Address(**{"zipCode": "01234567", "streetNumber": "100"})
        assert addr.zip_code == "01234567"
        assert addr.street_number == "100"


class TestItemAlias:
    def test_external_ref_alias(self):
        item = Item(external_ref="ref-123", title="Test", unit_price=100, quantity=1, tangible=True)
        data = item.model_dump(by_alias=True, exclude_none=True)
        assert "externalRef" in data
        assert "external_ref" not in data

    def test_unit_price_alias(self):
        item = Item(unit_price=500)
        data = item.model_dump(by_alias=True, exclude_none=True)
        assert "unitPrice" in data


class TestSplitAlias:
    def test_recipient_id_alias(self):
        split = Split(recipient_id=916, amount=5000)
        data = split.model_dump(by_alias=True, exclude_none=True)
        assert "recipientId" in data

    def test_net_amount_alias(self):
        split = Split(net_amount=4500)
        data = split.model_dump(by_alias=True, exclude_none=True)
        assert "netAmount" in data

    def test_charge_processing_fee_alias(self):
        split = Split(charge_processing_fee=True)
        data = split.model_dump(by_alias=True, exclude_none=True)
        assert "chargeProcessingFee" in data


class TestFeeAlias:
    def test_fixed_amount_alias(self):
        fee = Fee(fixed_amount=100, spread_percentage=5, estimated_fee=150, net_amount=9850)
        data = fee.model_dump(by_alias=True, exclude_none=True)
        assert "fixedAmount" in data
        assert "spreadPercentage" in data
        assert "estimatedFee" in data
        assert "netAmount" in data


class TestPixAlias:
    def test_qrcode_stays_lowercase(self):
        pix = Pix(qrcode="data:image/png;base64,...")
        data = pix.model_dump(by_alias=True, exclude_none=True)
        assert "qrcode" in data

    def test_expiration_date_alias(self):
        pix = Pix(expiration_date="2026-01-01T00:00:00Z")
        data = pix.model_dump(by_alias=True, exclude_none=True)
        assert "expirationDate" in data

    def test_end2_end_id_alias(self):
        pix = Pix(end2_end_id="E12345")
        data = pix.model_dump(by_alias=True, exclude_none=True)
        assert "end2EndId" in data

    def test_receipt_url_alias(self):
        pix = Pix(receipt_url="https://example.com/receipt")
        data = pix.model_dump(by_alias=True, exclude_none=True)
        assert "receiptUrl" in data


class TestBoletoAlias:
    def test_digitable_line_alias(self):
        boleto = Boleto(digitable_line="12345.67890")
        data = boleto.model_dump(by_alias=True, exclude_none=True)
        assert "digitableLine" in data

    def test_expiration_date_alias(self):
        boleto = Boleto(expiration_date="2026-01-01")
        data = boleto.model_dump(by_alias=True, exclude_none=True)
        assert "expirationDate" in data


class TestDeliveryAlias:
    def test_tracking_code_alias(self):
        delivery = Delivery(status="in_transit", tracking_code="BR123")
        data = delivery.model_dump(by_alias=True, exclude_none=True)
        assert "trackingCode" in data

    def test_created_at_alias(self):
        delivery = Delivery(created_at="2026-01-01T00:00:00Z", updated_at="2026-01-01T00:00:00Z")
        data = delivery.model_dump(by_alias=True, exclude_none=True)
        assert "createdAt" in data
        assert "updatedAt" in data


class TestRefundAlias:
    def test_pre_chargeback_alias(self):
        refund = Refund(amount=1000, pre_chargeback=True, pre_chargeback_cents=500)
        data = refund.model_dump(by_alias=True, exclude_none=True)
        assert "preChargeback" in data
        assert "preChargebackCents" in data

    def test_created_at_alias(self):
        refund = Refund(created_at="2026-01-01T00:00:00Z")
        data = refund.model_dump(by_alias=True, exclude_none=True)
        assert "createdAt" in data


class TestCreateTransactionDataAlias:
    def test_payment_method_alias(self):
        tx = CreateTransactionData(amount=1000, payment_method="pix")
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "paymentMethod" in data

    def test_postback_url_alias(self):
        tx = CreateTransactionData(
            amount=1000, payment_method="pix", postback_url="https://example.com"
        )
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "postbackUrl" in data

    def test_splits_alias(self):
        tx = CreateTransactionData(
            amount=1000,
            payment_method="pix",
            splits=[{"recipientId": 1, "amount": 500}],
        )
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "splits" in data


class TestListTransactionsParamsAlias:
    def test_payment_methods_alias(self):
        params = ListTransactionsParams(payment_methods="pix,credit_card")
        data = params.model_dump(by_alias=True, exclude_none=True)
        assert "paymentMethods" in data

    def test_delivery_status_alias(self):
        params = ListTransactionsParams(delivery_status="in_transit")
        data = params.model_dump(by_alias=True, exclude_none=True)
        assert "deliveryStatus" in data

    def test_document_number_alias(self):
        params = ListTransactionsParams(document_number="12345678900")
        data = params.model_dump(by_alias=True, exclude_none=True)
        assert "documentNumber" in data

    def test_all_filters(self):
        params = ListTransactionsParams(
            id=1,
            payment_methods="pix",
            status="paid",
            delivery_status="delivered",
            installments="1",
            name="Test",
            email="test@test.com",
            document_number="123",
            phone="11999999999",
            traceable=True,
        )
        data = params.model_dump(by_alias=True, exclude_none=True)
        assert len(data) == 10


class TestUpdateDeliveryStatusDataAlias:
    def test_tracking_code_alias(self):
        delivery = UpdateDeliveryStatusData(status="delivered", tracking_code="BR123")
        data = delivery.model_dump(by_alias=True, exclude_none=True)
        assert "trackingCode" in data


class TestTransactionAlias:
    def test_paid_amount_alias(self):
        tx = Transaction(paid_amount=1000, refunded_amount=0, company_id=1)
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "paidAmount" in data
        assert "refundedAmount" in data
        assert "companyId" in data

    def test_secure_fields_alias(self):
        tx = Transaction(secure_id="sec-123", secure_url="https://example.com")
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "secureId" in data
        assert "secureUrl" in data

    def test_external_ref_alias(self):
        tx = Transaction(external_ref="ext-123")
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "externalRef" in data

    def test_paid_at_alias(self):
        tx = Transaction(paid_at="2026-01-01T00:00:00Z")
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "paidAt" in data

    def test_authorization_code_alias(self):
        tx = Transaction(authorization_code="AUTH123", base_price=900, interest_rate=1.5)
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "authorizationCode" in data
        assert "basePrice" in data
        assert "interestRate" in data

    def test_subaccount_id_alias(self):
        tx = Transaction(subaccount_id=42)
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "subaccountId" in data

    def test_postback_url_alias(self):
        tx = Transaction(postback_url="https://example.com")
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "postbackUrl" in data

    def test_refused_reason_alias(self):
        tx = Transaction(refused_reason="insufficient_funds")
        data = tx.model_dump(by_alias=True, exclude_none=True)
        assert "refusedReason" in data


class TestCreateCustomerDataAlias:
    def test_required_fields(self):
        customer = CreateCustomerData(
            name="Test",
            email="test@test.com",
            document={"type": "cpf", "number": "123"},
            phone="11999999999",
        )
        data = customer.model_dump(by_alias=True, exclude_none=True)
        assert "name" in data
        assert "email" in data
        assert "document" in data
        assert "phone" in data

    def test_birthdate_alias(self):
        customer = CreateCustomerData(
            name="Test",
            email="test@test.com",
            document={"type": "cpf", "number": "123"},
            phone="11999999999",
            birthdate="1990-01-01",
        )
        data = customer.model_dump(by_alias=True, exclude_none=True)
        assert "birthdate" in data


class TestCreateBankAccountDataAlias:
    def test_all_required_fields(self):
        ba = CreateBankAccountData(
            bank_code="001",
            agency_number="1234",
            account_number="12345",
            account_digit="6",
            type="conta_corrente",
            legal_name="Test",
            document_number="12345678900",
            document_type="cpf",
        )
        data = ba.model_dump(by_alias=True)
        assert "bankCode" in data
        assert "agencyNumber" in data
        assert "accountNumber" in data
        assert "accountDigit" in data
        assert "type" in data
        assert "legalName" in data
        assert "documentNumber" in data
        assert "documentType" in data


class TestBankAccountAlias:
    def test_agency_digit_alias(self):
        ba = BankAccount(agency_digit="1")
        data = ba.model_dump(by_alias=True, exclude_none=True)
        assert "agencyDigit" in data

    def test_is_active_alias(self):
        ba = BankAccount(is_active=True, is_visible=True)
        data = ba.model_dump(by_alias=True, exclude_none=True)
        assert "isActive" in data
        assert "isVisible" in data

    def test_document_number_alias(self):
        ba = BankAccount(document_number="123", document_type="cpf")
        data = ba.model_dump(by_alias=True, exclude_none=True)
        assert "documentNumber" in data
        assert "documentType" in data


class TestTransferAlias:
    def test_fail_reason_alias(self):
        t = Transfer(fail_reason="insufficient_funds")
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "failReason" in data

    def test_pix_fields_alias(self):
        t = Transfer(pix_key="chave@pix", pix_end2_end_id="E12345")
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "pixKey" in data
        assert "pixEnd2EndId" in data

    def test_receipt_url_alias(self):
        t = Transfer(receipt_url="https://example.com")
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "receiptUrl" in data

    def test_secure_id_alias(self):
        t = Transfer(secure_id="sec-123")
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "secureId" in data

    def test_date_fields_alias(self):
        t = Transfer(
            transferred_at="2026-01-01",
            processed_at="2026-01-01",
            next_attempt_at="2026-01-02",
        )
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "transferredAt" in data
        assert "processedAt" in data
        assert "nextAttemptAt" in data

    def test_postback_url_alias(self):
        t = Transfer(postback_url="https://example.com")
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "postbackUrl" in data

    def test_company_id_alias(self):
        t = Transfer(company_id=1, recipient_id=916)
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "companyId" in data
        assert "recipientId" in data


class TestUpdateCompanyDataAlias:
    def test_invoice_descriptor_alias(self):
        company = UpdateCompanyData(invoice_descriptor="Beehive Hub")
        data = company.model_dump(by_alias=True, exclude_none=True)
        assert "invoiceDescriptor" in data

    def test_details_alias(self):
        company = UpdateCompanyData(details={"averageRevenue": 10000})
        data = company.model_dump(by_alias=True, exclude_none=True)
        assert "details" in data


class TestCreatePaymentLinkDataAlias:
    def test_title_is_optional(self):
        link = CreatePaymentLinkData(amount=1000)
        data = link.model_dump(by_alias=True, exclude_none=True)
        assert "title" not in data
        assert "amount" in data

    def test_alias_field(self):
        link = CreatePaymentLinkData(amount=1000, alias="my-alias")
        data = link.model_dump(by_alias=True, exclude_none=True)
        assert "alias" in data


class TestCreateTransferDataAlias:
    def test_recipient_id_alias(self):
        t = CreateTransferData(amount=5000, recipient_id=916)
        data = t.model_dump(by_alias=True, exclude_none=True)
        assert "recipientId" in data
