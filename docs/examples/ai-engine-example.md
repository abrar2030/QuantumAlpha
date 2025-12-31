# AI Engine Usage Example

## Overview

This example demonstrates how to train models, generate predictions, and use the AI Engine service.

---

## Prerequisites

- QuantumAlpha services running
- Authentication token
- Historical market data

---

## Example 1: Train an LSTM Model

### Python Code

```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8082/api"
TOKEN = "your_access_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Model configuration
model_config = {
    "name": "lstm_aapl_daily",
    "type": "lstm",
    "description": "LSTM model for AAPL daily price prediction",
    "parameters": {
        "lstm_units": 128,
        "dropout_rate": 0.2,
        "learning_rate": 0.001,
        "batch_size": 64,
        "epochs": 100,
        "early_stopping_patience": 10
    },
    "features": [
        "price_close_normalized",
        "volume_normalized",
        "rsi_14",
        "macd",
        "bollinger_percent_b",
        "moving_avg_5_normalized",
        "moving_avg_20_normalized"
    ]
}

# Train model
response = requests.post(
    f"{BASE_URL}/train-model",
    headers=headers,
    json=model_config
)

if response.status_code == 200:
    model = response.json()
    print(f"Model ID: {model['id']}")
    print(f"Status: {model['status']}")
    print(f"Created: {model['created_at']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Expected Output

```json
{
  "id": "model_abc123def456",
  "name": "lstm_aapl_daily",
  "type": "lstm",
  "status": "training",
  "created_at": "2023-12-15T10:00:00Z",
  "estimated_completion": "2023-12-15T10:45:00Z"
}
```

---

## Example 2: Generate Trading Signals

### Python Code

```python
# Fetch market data first
data_response = requests.get(
    "http://localhost:8081/api/market-data/AAPL",
    headers=headers,
    params={"period": "30d", "interval": "1d"}
)

market_data = data_response.json()

# Generate signals
signal_request = {
    "symbol": "AAPL",
    "data": market_data["data"],
    "model_id": "model_abc123def456"
}

response = requests.post(
    f"{BASE_URL}/generate-signals",
    headers=headers,
    json=signal_request
)

signals = response.json()
print(f"Signal: {signals['signals']['signal']}")
print(f"Confidence: {signals['signals']['confidence']:.2%}")
print(f"Predicted Price: ${signals['signals']['predicted_price']:.2f}")
```

### Expected Output

```json
{
  "symbol": "AAPL",
  "signals": {
    "signal": "BUY",
    "confidence": 0.85,
    "predicted_price": 178.5,
    "predicted_return": 0.014,
    "timestamp": "2023-12-15T14:30:00Z"
  }
}
```

---

## Example 3: List and Retrieve Models

### Python Code

```python
# List all models
response = requests.get(
    f"{BASE_URL}/models",
    headers=headers
)

models = response.json()
for model in models["models"]:
    print(f"{model['name']} ({model['type']}) - Status: {model['status']}")
    print(f"  Metrics: {model.get('metrics', {})}")

# Get specific model details
model_id = "model_abc123def456"
response = requests.get(
    f"{BASE_URL}/models/{model_id}",
    headers=headers
)

model_details = response.json()
print(json.dumps(model_details, indent=2))
```

---

## Example 4: Batch Predictions

### Python Code

```python
# Prepare batch data
batch_data = []
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]

for symbol in symbols:
    data_response = requests.get(
        f"http://localhost:8081/api/market-data/{symbol}",
        headers=headers,
        params={"period": "1d"}
    )
    batch_data.append({
        "symbol": symbol,
        "data": data_response.json()["data"]
    })

# Generate predictions for all symbols
predictions = {}
for item in batch_data:
    response = requests.post(
        f"{BASE_URL}/generate-signals",
        headers=headers,
        json={
            "symbol": item["symbol"],
            "data": item["data"],
            "model_id": "model_abc123def456"
        }
    )
    predictions[item["symbol"]] = response.json()["signals"]

# Display results
for symbol, signal in predictions.items():
    print(f"{symbol}: {signal['signal']} (Confidence: {signal['confidence']:.2%})")
```

---

## See Also

- [Risk Management Example](./risk-management-example.md)
- [Execution Service Example](./execution-service-example.md)
- [API Reference](../API.md)
