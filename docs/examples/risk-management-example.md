# Risk Management Example

## Overview

Examples demonstrating risk calculation, position sizing, and stress testing.

---

## Example 1: Calculate Risk Metrics

### Python Code

```python
import requests

BASE_URL = "http://localhost:8083/api"
TOKEN = "your_access_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Define portfolio
portfolio = {
    "positions": [
        {"symbol": "AAPL", "quantity": 100, "entry_price": 175.0},
        {"symbol": "GOOGL", "quantity": 50, "entry_price": 140.0},
        {"symbol": "MSFT", "quantity": 75, "entry_price": 380.0}
    ]
}

# Calculate risk metrics
risk_request = {
    "portfolio": portfolio,
    "risk_metrics": ["var", "cvar", "sharpe_ratio", "max_drawdown", "beta"],
    "confidence_level": 0.95,
    "lookback_period": 252
}

response = requests.post(
    f"{BASE_URL}/risk-metrics",
    headers=headers,
    json=risk_request
)

metrics = response.json()
print(f"Portfolio Value: ${metrics['portfolio_value']:,.2f}")
print(f"Value at Risk (95%): ${metrics['risk_metrics']['var']:,.2f}")
print(f"Conditional VaR: ${metrics['risk_metrics']['cvar']:,.2f}")
print(f"Sharpe Ratio: {metrics['risk_metrics']['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {metrics['risk_metrics']['max_drawdown']:.2%}")
```

---

## Example 2: Position Sizing with Kelly Criterion

### Python Code

```python
# Calculate optimal position size
position_request = {
    "symbol": "AAPL",
    "signal_strength": 0.75,  # High confidence signal
    "portfolio_value": 100000.00,
    "risk_tolerance": 0.02,  # 2% risk per trade
    "volatility": 0.25
}

response = requests.post(
    f"{BASE_URL}/calculate-position",
    headers=headers,
    json=position_request
)

position = response.json()
print(f"Recommended Position Size: ${position['position_size']:,.2f}")
print(f"Quantity: {position['quantity']} shares")
print(f"Risk Amount: ${position['risk_amount']:,.2f}")
print(f"Stop Loss Price: ${position['stop_loss_price']:.2f}")
print(f"Take Profit Price: ${position['take_profit_price']:.2f}")
```

---

## Example 3: Stress Testing

### Python Code

```python
# Define stress test scenarios
scenarios = [
    {
        "name": "market_crash",
        "description": "20% market drop",
        "shocks": {
            "AAPL": -0.20,
            "GOOGL": -0.22,
            "MSFT": -0.18
        }
    },
    {
        "name": "volatility_spike",
        "description": "3x volatility increase",
        "volatility_multiplier": 3.0
    },
    {
        "name": "interest_rate_hike",
        "description": "2% rate increase",
        "rate_change": 0.02
    }
]

stress_request = {
    "portfolio": portfolio,
    "scenarios": scenarios
}

response = requests.post(
    f"{BASE_URL}/stress-test",
    headers=headers,
    json=stress_request
)

results = response.json()
print(f"Current Portfolio Value: ${results['portfolio_value']:,.2f}\\n")

for scenario in results["scenarios"]:
    print(f"Scenario: {scenario['name']}")
    print(f"  Portfolio Loss: ${scenario['loss']:,.2f}")
    print(f"  Loss Percentage: {scenario['loss_pct']:.2%}")
    print(f"  Breach Threshold: {scenario['breach_threshold']}")
    print(f"  New Value: ${scenario['new_portfolio_value']:,.2f}\\n")
```

---

## See Also

- [Execution Service Example](./execution-service-example.md)
- [API Reference](../API.md)
