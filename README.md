# OxaPay API Library

## Description
This is an unofficial Python library for interacting with the OxaPay API. It provides both synchronous and asynchronous clients for managing payments, invoices, and other features offered by OxaPay.

## Installation
Install the library using pip:
```
pip install oxapay_api
```

## Usage

### Synchronous Client
```python
from oxapay_api.SyncOxaPay import SyncOxaPay

sync_client = SyncOxaPay(merchant_api_key="your_api_key_here")
try:
    api_status = sync_client.get_api_status()
    print(api_status)
except Exception as e:
    print(f"Error: {e}")
```

### Asynchronous Client
```python
import asyncio
from oxapay_api.AsyncOxaPay import AsyncOxaPay

async def main():
    async_client = AsyncOxaPay(merchant_api_key="your_api_key_here")
    try:
        api_status = await async_client.get_api_status()
        print(api_status)
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
```

### Creating an Invoice

#### Synchronously
```python
try:
    invoice = sync_client.create_invoice(amount=10.0, currency="USD")
    print(invoice)
except Exception as e:
    print(f"Error creating invoice: {e}")
```

#### Asynchronously
```python
async def create_invoice_example():
    try:
        invoice = await async_client.create_invoice(amount=10.0, currency="USD")
        print(invoice)
    except Exception as e:
        print(f"Error creating invoice: {e}")

asyncio.run(create_invoice_example())
```

**Note**: Many methods, such as `create_invoice` and `get_payment_information`, can return either the raw API response (if `raw_response=True`) or model objects like `OrderStatus` or `PaymentStatus` (default). For the structure of these models, refer to the `response_models.py` file in the library.

## Available Methods
- `get_api_status`: Gets the current status of the OxaPay API.
- `create_invoice`: Creates a new payment invoice.
- `get_supported_currencies`: Returns a list of supported currencies and their network details.
- `get_supported_networks`: Returns a list of supported blockchain networks.
- `get_supported_fiat_currencies`: Returns a list of supported fiat currencies.
- `get_payment_information`: Gets information about a specific payment by track_id.
- `create_white_label_payment`: Creates a white label payment.
- `create_static_address`: Creates a static address for receiving payments.
- `revoke_static_wallet`: Revokes a static wallet by address.
- `get_static_address_list`: Returns a list of static addresses.
- `get_payment_history`: Gets payment history with various filters.
- `get_accepted_currencies`: Returns a list of accepted currencies.
- `get_prices`: Gets current cryptocurrency prices.

For detailed information about parameters and return types, refer to the documentation strings in the code or the official OxaPay API documentation.

## Requirements
- Python 3.6 or higher
- aiohttp
- requests
- urllib3

## License
This project is distributed under the MIT license.

## Contribution
Any contributions are welcome! Please submit pull requests or open issues in the GitHub repository.

## Links
- GitHub Repository: https://github.com/Rushifakami/oxapay_api

## Disclaimer
This library is unofficial and not affiliated with OxaPay. Use at your own risk.
