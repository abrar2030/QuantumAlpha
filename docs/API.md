# API Reference

## Overview

QuantumAlpha provides a comprehensive REST API for interacting with all platform services. This document covers all public API endpoints, parameters, and response formats.

---

## Table of Contents

- [Authentication](#authentication)
- [Data Service API](#data-service-api)
- [AI Engine API](#ai-engine-api)
- [Risk Service API](#risk-service-api)
- [Execution Service API](#execution-service-api)
- [Common Responses](#common-responses)
- [Rate Limiting](#rate-limiting)

---

## Authentication

### Overview

All API endpoints (except `/health` and `/auth/*`) require JWT-based authentication.

### Login

```http
POST /api/v1/auth/login
```

| Name     | Type   | Required? | Default | Description        | Example          |
| -------- | ------ | --------- | ------- | ------------------ | ---------------- |
| username | string | Yes       | -       | User email address | user@example.com |
| password | string | Yes       | -       | User password      | mypassword123    |

**Example Request:**

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "mypassword123"
  }'
```

**Example Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### Using Access Token

Include the access token in the `Authorization` header:

```bash
curl -X GET http://localhost:8080/api/v1/models \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Data Service API

**Base URL:** `http://localhost:8081/api` or via API Gateway: `http://localhost:8080/api/v1/data`

### Endpoints

| Method | Path                               | Description                | Query/Body params                    | Auth required | Example request                                                                                                     |
| ------ | ---------------------------------- | -------------------------- | ------------------------------------ | ------------- | ------------------------------------------------------------------------------------------------------------------- |
| GET    | `/health`                          | Health check               | None                                 | No            | `curl http://localhost:8081/health`                                                                                 |
| GET    | `/market-data/{symbol}`            | Get market data for symbol | `period`, `interval`                 | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8081/api/market-data/AAPL?period=1d`                        |
| GET    | `/market-data/{symbol}/historical` | Get historical data        | `start_date`, `end_date`, `interval` | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8081/api/market-data/AAPL/historical?start_date=2023-01-01` |
| GET    | `/alternative-data/{symbol}`       | Get alternative data       | `data_types`                         | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8081/api/alternative-data/AAPL?data_types=sentiment,news`   |
| POST   | `/features/generate`               | Generate features          | Body: `symbol`, `data`, `features`   | Yes           | See example below                                                                                                   |

### Get Market Data

```http
GET /api/market-data/{symbol}
```

**Parameters:**

| Name     | Type   | Required? | Default | Description                         | Example |
| -------- | ------ | --------- | ------- | ----------------------------------- | ------- |
| symbol   | string | Yes       | -       | Stock ticker symbol                 | AAPL    |
| period   | string | No        | 1d      | Time period (1d, 5d, 1mo, 3mo, 1y)  | 1d      |
| interval | string | No        | 1h      | Data interval (1m, 5m, 15m, 1h, 1d) | 1h      |

**Example Request:**

```bash
curl -X GET "http://localhost:8081/api/market-data/AAPL?period=1d&interval=1h" \
  -H "Authorization: Bearer TOKEN"
```

**Example Response:**

```json
{
  "symbol": "AAPL",
  "period": "1d",
  "interval": "1h",
  "data": [
    {
      "timestamp": "2023-12-15T09:00:00Z",
      "open": 175.2,
      "high": 176.5,
      "low": 175.0,
      "close": 176.3,
      "volume": 1250000
    }
  ],
  "current_price": 176.3,
  "change": 2.3,
  "change_percent": 1.32
}
```

### Generate Features

```http
POST /api/features/generate
```

**Request Body:**

| Name     | Type   | Required? | Default | Description           | Example                         |
| -------- | ------ | --------- | ------- | --------------------- | ------------------------------- |
| symbol   | string | Yes       | -       | Stock ticker          | AAPL                            |
| data     | array  | Yes       | -       | Historical price data | See below                       |
| features | array  | Yes       | -       | Features to generate  | ["rsi_14", "macd", "bollinger"] |

**Example Request:**

```bash
curl -X POST http://localhost:8081/api/features/generate \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "data": [
      {"date": "2023-12-01", "close": 175.0, "volume": 1000000},
      {"date": "2023-12-02", "close": 176.0, "volume": 1200000}
    ],
    "features": ["rsi_14", "macd", "bollinger_bands"]
  }'
```

**Example Response:**

```json
{
  "symbol": "AAPL",
  "features": {
    "rsi_14": [45.2, 48.3, 52.1],
    "macd": [0.5, 0.7, 0.9],
    "bollinger_bands": {
      "upper": [180.0, 181.0],
      "middle": [175.0, 176.0],
      "lower": [170.0, 171.0]
    }
  }
}
```

---

## AI Engine API

**Base URL:** `http://localhost:8082/api` or via API Gateway: `http://localhost:8080/api/v1/ai`

### Endpoints

| Method | Path                 | Description              | Query/Body params                  | Auth required | Example request                                                                       |
| ------ | -------------------- | ------------------------ | ---------------------------------- | ------------- | ------------------------------------------------------------------------------------- |
| GET    | `/health`            | Health check             | None                               | No            | `curl http://localhost:8082/health`                                                   |
| GET    | `/models`            | List all models          | None                               | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8082/api/models`              |
| GET    | `/models/{model_id}` | Get model details        | None                               | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8082/api/models/model_abc123` |
| POST   | `/train-model`       | Train new model          | Body: model configuration          | Yes           | See example below                                                                     |
| POST   | `/predict`           | Generate predictions     | Body: `model_id`, `data`           | Yes           | See example below                                                                     |
| POST   | `/generate-signals`  | Generate trading signals | Body: `symbol`, `data`, `model_id` | Yes           | See example below                                                                     |
| POST   | `/rl/train`          | Train RL agent           | Body: agent configuration          | Yes           | See example below                                                                     |
| POST   | `/rl/act`            | Get RL action            | Body: `agent_id`, `state`          | Yes           | See example below                                                                     |

### Train Model

```http
POST /api/train-model
```

**Request Body:**

| Name        | Type   | Required? | Default | Description                      | Example                          |
| ----------- | ------ | --------- | ------- | -------------------------------- | -------------------------------- |
| name        | string | Yes       | -       | Model name                       | lstm_aapl_predictor              |
| type        | string | Yes       | -       | Model type (lstm, xgboost, etc.) | lstm                             |
| description | string | No        | ""      | Model description                | Price prediction for AAPL        |
| parameters  | object | Yes       | -       | Model hyperparameters            | See below                        |
| features    | array  | Yes       | -       | Feature names                    | ["price_close", "volume", "rsi"] |

**Example Request:**

```bash
curl -X POST http://localhost:8082/api/train-model \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "lstm_aapl_predictor",
    "type": "lstm",
    "description": "LSTM model for AAPL price prediction",
    "parameters": {
      "lstm_units": 128,
      "dropout_rate": 0.2,
      "learning_rate": 0.001,
      "batch_size": 64,
      "epochs": 100
    },
    "features": [
      "price_close_normalized",
      "volume_normalized",
      "rsi_14",
      "macd"
    ]
  }'
```

**Example Response:**

```json
{
  "id": "model_abc123",
  "name": "lstm_aapl_predictor",
  "type": "lstm",
  "status": "training",
  "created_at": "2023-12-15T10:00:00Z",
  "estimated_completion": "2023-12-15T10:30:00Z"
}
```

### Generate Predictions

```http
POST /api/predict
```

**Request Body:**

| Name     | Type   | Required? | Default | Description      | Example      |
| -------- | ------ | --------- | ------- | ---------------- | ------------ |
| model_id | string | Yes       | -       | Model identifier | model_abc123 |
| data     | array  | Yes       | -       | Input features   | See below    |

**Example Request:**

```bash
curl -X POST http://localhost:8082/api/predict \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "model_abc123",
    "data": [
      [175.0, 1000000, 45.2, 0.5],
      [176.0, 1200000, 48.3, 0.7]
    ]
  }'
```

**Example Response:**

```json
{
  "model_id": "model_abc123",
  "predictions": [177.5, 178.2],
  "confidence": [0.85, 0.82],
  "timestamp": "2023-12-15T10:30:00Z"
}
```

### Generate Trading Signals

```http
POST /api/generate-signals
```

**Request Body:**

| Name     | Type   | Required? | Default | Description               | Example      |
| -------- | ------ | --------- | ------- | ------------------------- | ------------ |
| symbol   | string | Yes       | -       | Stock ticker              | AAPL         |
| data     | array  | Yes       | -       | Market data with features | See below    |
| model_id | string | No        | default | Model to use              | model_abc123 |

**Example Request:**

```bash
curl -X POST http://localhost:8082/api/generate-signals \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "data": [
      {
        "date": "2023-12-01",
        "close": 175.0,
        "volume": 1000000,
        "rsi": 45.2,
        "macd": 0.5
      }
    ],
    "model_id": "model_abc123"
  }'
```

**Example Response:**

```json
{
  "symbol": "AAPL",
  "signals": {
    "signal": "BUY",
    "confidence": 0.85,
    "predicted_price": 177.5,
    "predicted_return": 0.014,
    "timestamp": "2023-12-15T10:30:00Z"
  }
}
```

### Train Reinforcement Learning Agent

```http
POST /api/rl/train
```

**Request Body:**

| Name        | Type   | Required? | Default | Description                  | Example     |
| ----------- | ------ | --------- | ------- | ---------------------------- | ----------- |
| name        | string | Yes       | -       | Agent name                   | dqn_trader  |
| algorithm   | string | Yes       | -       | RL algorithm (dqn, ppo, a3c) | dqn         |
| environment | string | Yes       | -       | Trading environment          | trading_env |
| parameters  | object | Yes       | -       | Hyperparameters              | See below   |

**Example Request:**

```bash
curl -X POST http://localhost:8082/api/rl/train \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dqn_trader",
    "algorithm": "dqn",
    "environment": "trading_env",
    "parameters": {
      "learning_rate": 0.0001,
      "gamma": 0.99,
      "epsilon_start": 1.0,
      "epsilon_end": 0.01,
      "episodes": 1000
    }
  }'
```

**Example Response:**

```json
{
  "agent_id": "agent_xyz789",
  "name": "dqn_trader",
  "status": "training",
  "episode": 0,
  "total_episodes": 1000,
  "created_at": "2023-12-15T10:00:00Z"
}
```

---

## Risk Service API

**Base URL:** `http://localhost:8083/api` or via API Gateway: `http://localhost:8080/api/v1/risk`

### Endpoints

| Method | Path                  | Description             | Query/Body params               | Auth required | Example request                                                                                     |
| ------ | --------------------- | ----------------------- | ------------------------------- | ------------- | --------------------------------------------------------------------------------------------------- |
| GET    | `/health`             | Health check            | None                            | No            | `curl http://localhost:8083/health`                                                                 |
| POST   | `/risk-metrics`       | Calculate risk metrics  | Body: portfolio, metrics        | Yes           | See example below                                                                                   |
| POST   | `/stress-test`        | Run stress tests        | Body: portfolio, scenarios      | Yes           | See example below                                                                                   |
| POST   | `/calculate-position` | Calculate position size | Body: symbol, signal, portfolio | Yes           | See example below                                                                                   |
| GET    | `/portfolio-risk`     | Get portfolio risk      | Query: `portfolio_id`           | Yes           | `curl -H "Authorization: Bearer TOKEN" "http://localhost:8083/api/portfolio-risk?portfolio_id=123"` |
| GET    | `/risk-alerts`        | Get risk alerts         | Query: `portfolio_id`           | Yes           | `curl -H "Authorization: Bearer TOKEN" "http://localhost:8083/api/risk-alerts?portfolio_id=123"`    |

### Calculate Risk Metrics

```http
POST /api/risk-metrics
```

**Request Body:**

| Name             | Type   | Required? | Default | Description              | Example                   |
| ---------------- | ------ | --------- | ------- | ------------------------ | ------------------------- |
| portfolio        | object | Yes       | -       | Portfolio positions      | See below                 |
| risk_metrics     | array  | Yes       | -       | Metrics to calculate     | ["var", "cvar", "sharpe"] |
| confidence_level | float  | No        | 0.95    | Confidence level for VaR | 0.95                      |
| lookback_period  | int    | No        | 252     | Historical period (days) | 252                       |

**Example Request:**

```bash
curl -X POST http://localhost:8083/api/risk-metrics \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio": {
      "positions": [
        {"symbol": "AAPL", "quantity": 100, "entry_price": 175.0},
        {"symbol": "GOOGL", "quantity": 50, "entry_price": 140.0}
      ]
    },
    "risk_metrics": ["var", "cvar", "sharpe_ratio", "max_drawdown"],
    "confidence_level": 0.95,
    "lookback_period": 252
  }'
```

**Example Response:**

```json
{
  "portfolio_value": 24500.0,
  "risk_metrics": {
    "var": 1250.5,
    "cvar": 1800.3,
    "sharpe_ratio": 1.45,
    "max_drawdown": 0.15,
    "volatility": 0.22,
    "beta": 1.05
  },
  "confidence_level": 0.95,
  "timestamp": "2023-12-15T10:30:00Z"
}
```

### Run Stress Tests

```http
POST /api/stress-test
```

**Request Body:**

| Name      | Type   | Required? | Default | Description           | Example   |
| --------- | ------ | --------- | ------- | --------------------- | --------- |
| portfolio | object | Yes       | -       | Portfolio positions   | See above |
| scenarios | array  | Yes       | -       | Stress test scenarios | See below |

**Example Request:**

```bash
curl -X POST http://localhost:8083/api/stress-test \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio": {
      "positions": [
        {"symbol": "AAPL", "quantity": 100, "entry_price": 175.0}
      ]
    },
    "scenarios": [
      {
        "name": "market_crash",
        "shocks": {"AAPL": -0.20}
      },
      {
        "name": "volatility_spike",
        "volatility_multiplier": 3.0
      }
    ]
  }'
```

**Example Response:**

```json
{
  "portfolio_value": 17500.0,
  "scenarios": [
    {
      "name": "market_crash",
      "loss": 3500.0,
      "loss_pct": 0.2,
      "breach_threshold": true,
      "new_portfolio_value": 14000.0
    },
    {
      "name": "volatility_spike",
      "loss": 2100.0,
      "loss_pct": 0.12,
      "breach_threshold": false,
      "new_portfolio_value": 15400.0
    }
  ],
  "timestamp": "2023-12-15T10:30:00Z"
}
```

### Calculate Position Size

```http
POST /api/calculate-position
```

**Request Body:**

| Name            | Type   | Required? | Default | Description             | Example   |
| --------------- | ------ | --------- | ------- | ----------------------- | --------- |
| symbol          | string | Yes       | -       | Stock ticker            | AAPL      |
| signal_strength | float  | Yes       | -       | Signal confidence (0-1) | 0.75      |
| portfolio_value | float  | Yes       | -       | Total portfolio value   | 100000.00 |
| risk_tolerance  | float  | Yes       | -       | Risk per trade (0-1)    | 0.02      |
| volatility      | float  | No        | auto    | Asset volatility        | 0.25      |

**Example Request:**

```bash
curl -X POST http://localhost:8083/api/calculate-position \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "signal_strength": 0.75,
    "portfolio_value": 100000.00,
    "risk_tolerance": 0.02,
    "volatility": 0.25
  }'
```

**Example Response:**

```json
{
  "symbol": "AAPL",
  "position_size": 1200.0,
  "quantity": 7,
  "risk_amount": 2000.0,
  "risk_percent": 0.02,
  "stop_loss_price": 168.5,
  "take_profit_price": 184.0,
  "method": "kelly_criterion"
}
```

---

## Execution Service API

**Base URL:** `http://localhost:8084/api` or via API Gateway: `http://localhost:8080/api/v1/execution`

### Endpoints

| Method | Path                             | Description          | Query/Body params                         | Auth required | Example request                                                                                   |
| ------ | -------------------------------- | -------------------- | ----------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------- |
| GET    | `/health`                        | Health check         | None                                      | No            | `curl http://localhost:8084/health`                                                               |
| GET    | `/orders`                        | List orders          | Query: `portfolio_id`, `status`, `symbol` | Yes           | `curl -H "Authorization: Bearer TOKEN" "http://localhost:8084/api/orders?status=pending"`         |
| GET    | `/orders/{order_id}`             | Get order details    | None                                      | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8084/api/orders/order_123`                |
| POST   | `/orders`                        | Create new order     | Body: order details                       | Yes           | See example below                                                                                 |
| POST   | `/orders/{order_id}/cancel`      | Cancel order         | None                                      | Yes           | `curl -X POST -H "Authorization: Bearer TOKEN" http://localhost:8084/api/orders/order_123/cancel` |
| GET    | `/execution-strategies`          | List strategies      | None                                      | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8084/api/execution-strategies`            |
| GET    | `/brokers`                       | List brokers         | None                                      | Yes           | `curl -H "Authorization: Bearer TOKEN" http://localhost:8084/api/brokers`                         |
| GET    | `/brokers/{broker_id}/positions` | Get broker positions | Query: `account_id`                       | Yes           | See example below                                                                                 |

### Create Order

```http
POST /api/orders
```

**Request Body:**

| Name               | Type   | Required? | Default | Description                        | Example       |
| ------------------ | ------ | --------- | ------- | ---------------------------------- | ------------- |
| portfolio_id       | string | Yes       | -       | Portfolio identifier               | portfolio_123 |
| symbol             | string | Yes       | -       | Stock ticker                       | AAPL          |
| side               | string | Yes       | -       | Order side (buy, sell)             | buy           |
| quantity           | int    | Yes       | -       | Number of shares                   | 100           |
| order_type         | string | Yes       | -       | Order type (market, limit, stop)   | market        |
| limit_price        | float  | No        | -       | Limit price (for limit orders)     | 175.50        |
| stop_price         | float  | No        | -       | Stop price (for stop orders)       | 170.00        |
| execution_strategy | string | No        | default | Execution algorithm                | vwap          |
| time_in_force      | string | No        | day     | Time in force (day, gtc, ioc, fok) | day           |

**Example Request:**

```bash
curl -X POST http://localhost:8084/api/orders \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": "portfolio_123",
    "symbol": "AAPL",
    "side": "buy",
    "quantity": 100,
    "order_type": "limit",
    "limit_price": 175.50,
    "execution_strategy": "vwap",
    "time_in_force": "day"
  }'
```

**Example Response:**

```json
{
  "order_id": "order_abc123",
  "portfolio_id": "portfolio_123",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 100,
  "filled_quantity": 0,
  "order_type": "limit",
  "limit_price": 175.5,
  "status": "pending",
  "execution_strategy": "vwap",
  "created_at": "2023-12-15T10:00:00Z",
  "updated_at": "2023-12-15T10:00:00Z"
}
```

---

## Common Responses

### Error Response Format

```json
{
  "error": "ValidationError",
  "message": "Symbol is required",
  "status_code": 400,
  "timestamp": "2023-12-15T10:30:00Z"
}
```

### HTTP Status Codes

| Code | Meaning               | Description                       |
| ---- | --------------------- | --------------------------------- |
| 200  | OK                    | Request succeeded                 |
| 201  | Created               | Resource created successfully     |
| 400  | Bad Request           | Invalid input parameters          |
| 401  | Unauthorized          | Missing or invalid authentication |
| 403  | Forbidden             | Insufficient permissions          |
| 404  | Not Found             | Resource not found                |
| 429  | Too Many Requests     | Rate limit exceeded               |
| 500  | Internal Server Error | Server error                      |

---

## Rate Limiting

API endpoints are rate-limited to ensure fair usage:

| Endpoint Type   | Rate Limit   | Window     |
| --------------- | ------------ | ---------- |
| Authentication  | 10 requests  | per minute |
| Data fetching   | 100 requests | per minute |
| Model training  | 5 requests   | per hour   |
| Order placement | 50 requests  | per minute |

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1702641600
```

---

## SDK Libraries

Official SDK libraries are available for:

- **Python**: `pip install quantumalpha-sdk`
- **JavaScript/Node.js**: `npm install quantumalpha-sdk`
- **TypeScript**: Full type definitions included

Example using Python SDK:

```python
from quantumalpha import QuantumAlphaClient

client = QuantumAlphaClient(
    api_key='your_api_key',
    base_url='http://localhost:8080'
)

# Get market data
data = client.data.get_market_data('AAPL', period='1d')

# Create order
order = client.execution.create_order(
    symbol='AAPL',
    side='buy',
    quantity=100,
    order_type='market'
)
```
