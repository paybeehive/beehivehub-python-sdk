# Beehive Hub Python SDK

Official SDK for integrating with the Beehive Hub API. Accept payments simply and quickly.

[![PyPI version](https://img.shields.io/pypi/v/beehivehub-python-sdk)](https://pypi.org/project/beehivehub-python-sdk/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Resources](#resources)
  - [Transactions](#transactions)
  - [Customers](#customers)
  - [Transfers](#transfers)
  - [Balance](#balance)
  - [Recipients](#recipients)
  - [Bank Accounts](#bank-accounts)
  - [Company](#company)
  - [Payment Links](#payment-links)
- [Error Handling](#error-handling)
- [Values in Cents](#values-in-cents)
- [Security Best Practices](#security-best-practices)
- [Type Safety](#type-safety)
- [Development](#development)
- [Support](#support)
- [License](#license)

## Requirements

- Python >= 3.10

## Installation

```bash
pip install beehivehub-python-sdk
```

**Dependencies** (installed automatically):

- [httpx](https://www.python-httpx.org/) - HTTP client
- [pydantic](https://docs.pydantic.dev/) - Data validation and models

## Quick Start

```python
from beehivehub import create_beehivehub_client

beehive = create_beehivehub_client("your_secret_key")

transaction = beehive.transactions.create({
    "amount": 10000,  # BRL 100.00 in cents
    "paymentMethod": "pix",
    "customer": {
        "name": "João Silva",
        "email": "joao@example.com",
        "document": {"type": "cpf", "number": "00000000191"},
        "phone": "11999999999",
    },
    "items": [
        {"title": "Produto Teste", "unitPrice": 10000, "quantity": 1, "tangible": True}
    ],
    "postbackUrl": "https://example.com/webhook",
})

print("Transaction created:", transaction)
```

## Authentication

The SDK uses **Basic Authentication**. Provide your **SECRET_KEY** when initializing.

### Getting your credentials

1. Access the [Beehive Hub dashboard](https://app.conta.paybeehive.com.br)
2. Navigate to **Settings > API Credentials**
3. Copy your **SECRET_KEY**

```python
beehive = create_beehivehub_client("your_secret_key_here")
```

### Sandbox environment

```python
beehive = create_beehivehub_client("your_secret_key", environment="sandbox")
```

**Important:** Never expose your secret key in client-side code or public repositories. Use environment variables:

```python
import os

beehive = create_beehivehub_client(os.environ["BEEHIVE_SECRET_KEY"])
```

## Resources

### Transactions

#### Create a transaction

```python
transaction = beehive.transactions.create({
    "amount": 10000,
    "paymentMethod": "pix",
    "customer": {
        "name": "João Silva",
        "email": "joao@example.com",
        "document": {"type": "cpf", "number": "00000000191"},
        "phone": "11999999999",
    },
    "items": [
        {"title": "Produto Teste", "unitPrice": 10000, "quantity": 1, "tangible": True}
    ],
    "postbackUrl": "https://example.com/webhook",
    "metadata": {"orderId": "1234567890"},
})
```

#### List transactions

```python
transactions = beehive.transactions.list({
    "status": "paid",
    "paymentMethods": "pix",
})
```

#### Get a transaction

```python
transaction = beehive.transactions.get(123456)
```

#### Refund a transaction

```python
# Full refund
refund = beehive.transactions.refund(123456)

# Partial refund
partial_refund = beehive.transactions.refund(123456, 5000)
```

#### Update delivery status

```python
updated = beehive.transactions.update_delivery(123456, {
    "status": "in_transit",
    "trackingCode": "BR123456789",
})
```

### Customers

#### Create a customer

```python
customer = beehive.customers.create({
    "name": "Maria Santos",
    "email": "maria@example.com",
    "document": {"type": "cpf", "number": "98765432100"},
    "phone": "11988888888",
    "address": {
        "street": "Rua Teste",
        "streetNumber": "456",
        "complement": "Apto 101",
        "neighborhood": "Jardins",
        "zipCode": "01234567",
        "city": "São Paulo",
        "state": "SP",
        "country": "br",
    },
})
```

#### List customers

O parâmetro `email` é obrigatório. A API não aceita parâmetros de paginação convencionais.

```python
customers = beehive.customers.list({
    "email": "cliente@example.com",
})
```

#### Get a customer

```python
customer = beehive.customers.get(123456)
```

### Transfers

#### Create a transfer

```python
transfer = beehive.transfers.create({
    "amount": 50000,
    "recipientId": 916,
})

# With optional bank account
transfer_with_account = beehive.transfers.create({
    "amount": 50000,
    "recipientId": 916,
    "bankAccount": {
        "bankCode": "001",
        "agencyNumber": "1234",
        "accountNumber": "12345",
        "accountDigit": "6",
        "type": "conta_corrente",
        "legalName": "Destinatário Teste",
        "documentNumber": "12345678900",
        "documentType": "cpf",
    },
})
```

#### Get a transfer

```python
transfer = beehive.transfers.get(123456)
```

### Balance

```python
balance = beehive.balance.get()
print(f"Available: BRL {balance['amount'] / 100}")
print(f"Recipient ID: {balance['recipientId']}")
```

### Recipients

#### Create a recipient

```python
recipient = beehive.recipients.create({
    "legalName": "Recebedor Teste Ltda",
    "document": {"type": "cnpj", "number": "58593776000142"},
    "transferSettings": {
        "transferEnabled": True,
        "automaticAnticipationEnabled": False,
        "anticipatableVolumePercentage": 100,
    },
    "bankAccount": {
        "bankCode": "001",
        "agencyNumber": "1234",
        "accountNumber": "12345",
        "accountDigit": "6",
        "type": "conta_corrente",
        "legalName": "Recebedor Teste Ltda",
        "documentNumber": "58593776000142",
        "documentType": "cnpj",
    },
})
```

#### List recipients

```python
recipients = beehive.recipients.list()
```

#### Get a recipient

```python
recipient = beehive.recipients.get(916)
```

#### Update a recipient

```python
updated = beehive.recipients.update(916, {
    "legalName": "Beehive Sandbox",
})
```

### Bank Accounts

#### Add a bank account

```python
bank_account = beehive.bank_accounts.create(916, {
    "bankCode": "341",
    "agencyNumber": "9876",
    "accountNumber": "54321",
    "accountDigit": "0",
    "type": "conta_poupanca",
    "legalName": "Empresa Teste Ltda",
    "documentNumber": "60572883000136",
    "documentType": "cnpj",
})
```

#### List bank accounts

```python
accounts = beehive.bank_accounts.list(916)
```

### Company

#### Get company data

```python
company = beehive.company.get()
```

#### Update company data

```python
updated = beehive.company.update({
    "invoiceDescriptor": "Beehive Hub",
    "details": {
        "averageRevenue": 10000,
        "averageTicket": 100.50,
        "physicalProducts": True,
        "productsDescription": "Produtos físicos",
        "siteUrl": "https://www.meusite.com.br",
        "phone": "11999999999",
        "email": "contato@meusite.com.br",
    },
})
```

### Payment Links

O SDK adiciona `url` às respostas (create, get, list, update) quando há `alias`:
- **Produção:** `https://link.conta.paybeehive.com.br/{alias}`
- **Sandbox:** `https://link.sandbox.hopysplit.com.br/{alias}`

#### Create a payment link

Create e update aceitam payloads parciais. Se `alias` não for informado, o SDK gera automaticamente um código alfanumérico de 10 caracteres. Em `pix` e `boleto`, `expiresInDays` é opcional (a API usa 0 quando omitido); recomenda-se informá-lo explicitamente.

```python
payment_link = beehive.payment_links.create({
    "title": "novo link alterado",
    "alias": "alias_alterado",
    "amount": 1000,
    "settings": {
        "defaultPaymentMethod": "credit_card",
        "requestAddress": True,
        "requestPhone": True,
        "traceable": True,
        "boleto": {"enabled": True, "expiresInDays": 0},
        "pix": {"enabled": False, "expiresInDays": 0},
        "card": {"enabled": False, "freeInstallments": 1, "maxInstallments": 12},
    },
})
# payment_link["url"] já vem montada (ex: https://link.conta.paybeehive.com.br/alias_alterado)
```

#### List payment links

A API não aceita filtros por query parameters; retorna todos os links da empresa.

```python
payment_links = beehive.payment_links.list()
```

#### Get a payment link

```python
payment_link = beehive.payment_links.get(247)
```

#### Update a payment link

Aceita atualizações parciais (apenas os campos que deseja alterar).

```python
updated = beehive.payment_links.update(247, {
    "title": "novo link alterado",
    "alias": "alias_alterado",
    "amount": 1000,
    "settings": {
        "defaultPaymentMethod": "credit_card",
        "requestAddress": True,
        "requestPhone": True,
        "traceable": True,
        "boleto": {"enabled": True, "expiresInDays": 0},
        "pix": {"enabled": False, "expiresInDays": 0},
        "card": {"enabled": False, "freeInstallments": 1, "maxInstallments": 12},
    },
})
```

#### Delete a payment link

```python
beehive.payment_links.delete(247)
```

## Error Handling

The SDK raises specific exception classes for different scenarios:

- `BeehiveHubAPIError` - General API errors (4xx, 5xx)
- `BeehiveHubAuthenticationError` - Authentication failures (401)
- `BeehiveHubValidationError` - Request validation errors (400)
- `BeehiveHubNotFoundError` - Resource not found (404)
- `BeehiveHubRateLimitError` - Rate limit exceeded (429)
- `BeehiveHubNetworkError` - Network/connection errors

```python
import os
from beehivehub import (
    create_beehivehub_client,
    BeehiveHubAPIError,
    BeehiveHubAuthenticationError,
    BeehiveHubValidationError,
)

beehive = create_beehivehub_client(os.environ["BEEHIVE_SECRET_KEY"])

try:
    transaction = beehive.transactions.create({
        "amount": 10000,
        "paymentMethod": "pix",
        "customer": {
            "name": "João Silva",
            "email": "joao@example.com",
            "document": {"type": "cpf", "number": "12345678900"},
            "phone": "11999999999",
        },
    })
    print("Transaction created:", transaction)
except BeehiveHubAuthenticationError as e:
    print(f"Invalid API key: {e}")
except BeehiveHubValidationError as e:
    print(f"Validation error: {e}")
except BeehiveHubAPIError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Values in Cents

All monetary values in the API are expressed in **cents**.

```python
# BRL 100.00 = 10000 cents
amount = 10000

# BRL 1.50 = 150 cents
amount = 150

# Convert reais to cents
reais = 100.0
cents = round(reais * 100)  # 10000
```

## Security Best Practices

1. **Never expose your SECRET_KEY** - Use environment variables
2. **Don't generate card_hash on backend** - Use Beehive Hub's JavaScript library on frontend
3. **Validate user data** - Always validate and sanitize before sending to API
4. **Use HTTPS** - Always use secure connections
5. **Implement webhooks** - Receive status change notifications

```python
# .env
BEEHIVE_SECRET_KEY=your_secret_key_here

# app.py
import os
from dotenv import load_dotenv
from beehivehub import create_beehivehub_client

load_dotenv()

beehive = create_beehivehub_client(os.environ["BEEHIVE_SECRET_KEY"])
```

## Type Safety

The SDK exports 40+ Pydantic models and ships with a `py.typed` marker, providing full support for type checkers like **mypy** and **pyright**.

```python
from beehivehub import CreateTransactionData, Document, Item

data: CreateTransactionData = {
    "amount": 10000,
    "paymentMethod": "pix",
    "customer": {
        "name": "João Silva",
        "email": "joao@example.com",
        "document": {"type": "cpf", "number": "00000000191"},
        "phone": "11999999999",
    },
    "items": [
        {"title": "Produto Teste", "unitPrice": 10000, "quantity": 1, "tangible": True}
    ],
}
```

## Development

### Setup

```bash
git clone https://github.com/paybeehive/beehivehub-python-sdk.git
cd beehivehub-python-sdk
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Available commands

The project uses [taskipy](https://github.com/taskipy/taskipy) as task runner:

```bash
task test              # Run unit tests
task test-integration  # Run integration tests (requires .env with API key)
task lint              # Run linter (ruff)
task format            # Format code (ruff)
task typecheck         # Run type checker (mypy)
task coverage-html     # Generate HTML coverage report
```

### Versioning

```bash
task bump-patch        # 1.0.0 → 1.0.1
task bump-minor        # 1.0.0 → 1.1.0
task bump-major        # 1.0.0 → 2.0.0
```

## Support

For suggestions, bug reports, or questions:

- **Email:** contato@paybeehive.com.br
- **Documentation:** https://docs.beehivehub.io

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
