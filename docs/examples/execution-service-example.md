# Execution Service Example

## Overview

Examples for order placement, execution strategies, and broker integration.

---

## Example 1: Place a Market Order

### Python Code

```python
import requests
import time

BASE_URL = "http://localhost:8084/api"
TOKEN = "your_access_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Create market order
order_request = {
    "portfolio_id": "portfolio_123",
    "symbol": "AAPL",
    "side": "buy",
    "quantity": 100,
    "order_type": "market",
    "time_in_force": "day"
}

response = requests.post(
    f"{BASE_URL}/orders",
    headers=headers,
    json=order_request
)

order = response.json()
print(f"Order ID: {order['order_id']}")
print(f"Status: {order['status']}")

# Monitor order status
while order['status'] in ['pending', 'partially_filled']:
    time.sleep(2)
    response = requests.get(
        f"{BASE_URL}/orders/{order['order_id']}",
        headers=headers
    )
    order = response.json()
    print(f"Status: {order['status']}, Filled: {order['filled_quantity']}/{order['quantity']}")

print(f"Final Status: {order['status']}")
print(f"Average Fill Price: ${order.get('average_fill_price', 0):.2f}")
```

---

## Example 2: VWAP Execution Strategy

### Python Code

```python
# Place VWAP order
vwap_order = {
    "portfolio_id": "portfolio_123",
    "symbol": "AAPL",
    "side": "buy",
    "quantity": 1000,
    "order_type": "limit",
    "limit_price": 176.00,
    "execution_strategy": "vwap",
    "strategy_params": {
        "time_window": 300,  # 5 minutes
        "participation_rate": 0.10
    },
    "time_in_force": "day"
}

response = requests.post(
    f"{BASE_URL}/orders",
    headers=headers,
    json=vwap_order
)

print(f"VWAP Order Created: {response.json()['order_id']}")
```

---

## Example 3: List and Filter Orders

### Python Code

```python
# Get all pending orders
response = requests.get(
    f"{BASE_URL}/orders",
    headers=headers,
    params={"status": "pending", "portfolio_id": "portfolio_123"}
)

orders = response.json()["orders"]
print(f"Pending Orders: {len(orders)}")

for order in orders:
    print(f"  {order['symbol']}: {order['side']} {order['quantity']} @ {order.get('limit_price', 'Market')}")
```

---

## See Also

- [Risk Management Example](./risk-management-example.md)
- [API Reference](../API.md)
