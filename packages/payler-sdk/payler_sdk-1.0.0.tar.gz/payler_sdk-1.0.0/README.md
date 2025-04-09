# Payler SDK

Python SDK for integration with the Payler payment system.

## Installation

```bash
pip install payler-sdk
```

## Features

- Card saving and management
- Customer registration
- Processing payments with saved cards
- Transaction status handling
- Get payment status

## Quick Start

```python
from payler_sdk import PaylerClient

# Initialize the client
client = PaylerClient(
    base_url="sandbox.payler.com",
    auth_key="your_auth_key",
)

# Save card and process payment
response = client.initialize_save_card_session(
    customer_id="customer123",
    currency="RUB",
    return_url_success="https://your-website.com/payment/sync-cards"
)

# Get the redirect URL for card saving
redirect_url = response.save_card_url

# After card saving, process payment with saved card
payment = client.charge_saved_card(
    amount=100.50,
    order_id="order_12345",
    currency="RUB",
    recurrent_template_id="template_id_from_saved_card"
)

# Get payment status
status = client.get_payment_status(order_id="order_12345")
```

## Usage Examples

### Register a New Customer

```python
from payler_sdk.models import PaylerCustomerUpdateOrCreateRequest

customer = PaylerCustomerUpdateOrCreateRequest(
    name="Erlich Bachman",
    email="erlich.bachman@gmail.com",
    phone="+79001234567"
)
response = client.register_new_customer(customer)
customer_id = response.customer_id
```

### Error Handling

```python
from payler_sdk.exceptions import PaylerApiError, PaylerSessionError

try:
    payment = client.charge_saved_card(...)
except PaylerApiError as e:
    print(f"API error: {e}, status code: {e.status_code}")
except PaylerSessionError as e:
    print(f"Session error: {e}")
```

## Requirements

- Python 3.8+
- requests library

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
