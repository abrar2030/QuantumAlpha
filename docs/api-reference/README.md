# QuantumAlpha API Reference

This section provides comprehensive documentation for the QuantumAlpha platform APIs. The platform follows a microservices architecture, with each service exposing its own REST API.

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Error Handling](#error-handling)
4. [Rate Limiting](#rate-limiting)
5. [API Services](#api-services)
6. [API Versioning](#api-versioning)
7. [Webhooks](#webhooks)
8. [SDKs and Client Libraries](#sdks-and-client-libraries)

## API Overview

The QuantumAlpha platform exposes a set of RESTful APIs that allow you to interact with the platform programmatically. The APIs are organized by service:

- **[AI Engine API](./ai-engine/)**: Manage machine learning models, predictions, and reinforcement learning environments
- **[Data Service API](./data-service/)**: Access market data, alternative data, and feature engineering
- **[Risk Service API](./risk-service/)**: Manage risk metrics, stress testing, and position sizing
- **[Execution Service API](./execution-service/)**: Manage orders, executions, and broker integrations

All APIs follow REST principles and use JSON for request and response bodies. The base URL for all API endpoints is:

```
https://api.quantumalpha.com/v1
```

For local development, the base URL is:

```
http://localhost:8080/v1
```

## Authentication

All API requests require authentication using JWT (JSON Web Tokens). To authenticate:

1. Obtain an API key and secret from the QuantumAlpha dashboard
2. Generate a JWT token using your API key and secret
3. Include the token in the `Authorization` header of your requests

### Obtaining API Credentials

1. Log in to the QuantumAlpha dashboard
2. Navigate to Settings > API Keys
3. Click "Create New API Key"
4. Save the API key and secret securely

### Generating a JWT Token

```python
import jwt
import time

def generate_token(api_key, api_secret):
    payload = {
        'sub': api_key,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600  # Token expires in 1 hour
    }
    return jwt.encode(payload, api_secret, algorithm='HS256')

token = generate_token('your_api_key', 'your_api_secret')
```

### Using the Token

Include the token in the `Authorization` header of your requests:

```
Authorization: Bearer <token>
```

Example:

```bash
curl -X GET \
  https://api.quantumalpha.com/v1/data/market/prices \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- **2xx**: Success
- **4xx**: Client error (e.g., invalid request, authentication error)
- **5xx**: Server error

All error responses include a JSON body with the following structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `AUTHENTICATION_ERROR` | Invalid or expired authentication token |
| `AUTHORIZATION_ERROR` | Insufficient permissions to perform the requested action |
| `VALIDATION_ERROR` | Invalid request parameters |
| `RESOURCE_NOT_FOUND` | The requested resource does not exist |
| `RATE_LIMIT_EXCEEDED` | Too many requests in a given time period |
| `INTERNAL_ERROR` | An unexpected error occurred on the server |

## Rate Limiting

To ensure fair usage and system stability, the API implements rate limiting. The current limits are:

| API | Rate Limit |
|-----|------------|
| Data Service | 100 requests per minute |
| AI Engine | 50 requests per minute |
| Risk Service | 100 requests per minute |
| Execution Service | 200 requests per minute |

Rate limit information is included in the response headers:

- `X-RateLimit-Limit`: The maximum number of requests allowed per time window
- `X-RateLimit-Remaining`: The number of requests remaining in the current time window
- `X-RateLimit-Reset`: The time at which the current rate limit window resets (Unix timestamp)

If you exceed the rate limit, you will receive a `429 Too Many Requests` response.

## API Services

### AI Engine API

The AI Engine API allows you to manage machine learning models, predictions, and reinforcement learning environments. See the [AI Engine API documentation](./ai-engine/) for details.

Key endpoints:

- `/ai/models`: Manage machine learning models
- `/ai/predictions`: Generate predictions from models
- `/ai/rl-environments`: Manage reinforcement learning environments
- `/ai/experiments`: Track and manage experiments

### Data Service API

The Data Service API provides access to market data, alternative data, and feature engineering. See the [Data Service API documentation](./data-service/) for details.

Key endpoints:

- `/data/market`: Access market data (prices, volumes, etc.)
- `/data/alternative`: Access alternative data (news, sentiment, etc.)
- `/data/features`: Access engineered features
- `/data/sources`: Manage data sources

### Risk Service API

The Risk Service API allows you to manage risk metrics, stress testing, and position sizing. See the [Risk Service API documentation](./risk-service/) for details.

Key endpoints:

- `/risk/metrics`: Calculate risk metrics
- `/risk/stress-tests`: Run stress tests
- `/risk/position-sizing`: Calculate optimal position sizes
- `/risk/limits`: Manage risk limits

### Execution Service API

The Execution Service API allows you to manage orders, executions, and broker integrations. See the [Execution Service API documentation](./execution-service/) for details.

Key endpoints:

- `/execution/orders`: Manage orders
- `/execution/executions`: Track executions
- `/execution/brokers`: Manage broker connections
- `/execution/algorithms`: Configure execution algorithms

## API Versioning

The QuantumAlpha API uses versioning to ensure backward compatibility. The version is included in the URL path:

```
https://api.quantumalpha.com/v1/...
```

When a new version is released, the previous version will continue to be supported for a deprecation period, typically 6 months. Deprecation notices will be provided in advance.

## Webhooks

The QuantumAlpha platform supports webhooks for real-time notifications of events. To set up webhooks:

1. Log in to the QuantumAlpha dashboard
2. Navigate to Settings > Webhooks
3. Click "Create New Webhook"
4. Configure the webhook URL and events

### Webhook Events

| Event | Description |
|-------|-------------|
| `order.created` | An order has been created |
| `order.filled` | An order has been filled |
| `order.canceled` | An order has been canceled |
| `model.trained` | A model has completed training |
| `risk.limit_breached` | A risk limit has been breached |
| `data.new_available` | New data is available |

### Webhook Payload

Webhook payloads are sent as JSON in the request body:

```json
{
  "event": "order.filled",
  "timestamp": "2025-06-06T09:30:00Z",
  "data": {
    "order_id": "ord_123456",
    "symbol": "AAPL",
    "quantity": 100,
    "price": 150.25,
    "side": "buy"
  }
}
```

### Webhook Security

To verify that webhook requests are coming from QuantumAlpha, a signature is included in the `X-QuantumAlpha-Signature` header. The signature is a HMAC-SHA256 hash of the request body, using your webhook secret as the key.

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
```

## SDKs and Client Libraries

The QuantumAlpha platform provides official SDKs for several programming languages:

- [Python SDK](https://github.com/abrar2030/quantumalpha-python)
- [JavaScript SDK](https://github.com/abrar2030/quantumalpha-js)
- [Java SDK](https://github.com/abrar2030/quantumalpha-java)
- [C# SDK](https://github.com/abrar2030/quantumalpha-csharp)

### Python SDK Example

```python
from quantumalpha import Client

# Initialize client
client = Client(api_key='your_api_key', api_secret='your_api_secret')

# Get market data
prices = client.data.market.get_prices(
    symbols=['AAPL', 'MSFT', 'GOOGL'],
    start_date='2025-01-01',
    end_date='2025-06-01',
    interval='1d'
)

# Create a model
model = client.ai.models.create(
    name='my-model',
    type='temporal_fusion_transformer',
    parameters={
        'hidden_size': 128,
        'num_heads': 4,
        'dropout_rate': 0.1
    }
)

# Train the model
training_job = client.ai.models.train(
    model_id=model['id'],
    dataset_id='dataset_123',
    hyperparameters={
        'learning_rate': 0.001,
        'batch_size': 64,
        'epochs': 100
    }
)

# Get predictions
predictions = client.ai.predictions.create(
    model_id=model['id'],
    data={
        'features': [...],
        'timestamps': [...]
    }
)

# Place an order
order = client.execution.orders.create(
    symbol='AAPL',
    quantity=100,
    side='buy',
    type='limit',
    price=150.00,
    time_in_force='day'
)
```

For more information on using the SDKs, refer to the SDK documentation.
