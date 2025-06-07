# Execution Service API Reference

The Execution Service API provides endpoints for order management, trade execution, and post-trade processing. This service handles the entire lifecycle of trades from order creation to settlement.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Orders](#orders)
4. [Executions](#executions)
5. [Allocations](#allocations)
6. [Settlements](#settlements)
7. [Broker Connections](#broker-connections)
8. [Market Data](#market-data)
9. [Algorithms](#algorithms)
10. [Transaction Cost Analysis](#transaction-cost-analysis)
11. [Reports](#reports)

## Overview

The Execution Service provides a comprehensive set of APIs for managing the entire trade lifecycle. Key features include:

- Order management and routing
- Trade execution across multiple venues
- Pre-trade and post-trade analytics
- Algorithmic trading capabilities
- Transaction cost analysis
- Settlement and reconciliation
- Integration with multiple brokers and exchanges

## Authentication

All API requests must include an API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

API keys can be generated and managed through the QuantumAlpha Admin Portal.

## Orders

### List Orders

```
GET /orders
```

Retrieves a list of orders based on specified filters.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | Filter by portfolio ID |
| `status` | string | Filter by order status (e.g., `new`, `open`, `filled`, `canceled`) |
| `symbol` | string | Filter by symbol |
| `side` | string | Filter by side (`buy` or `sell`) |
| `start_date` | string | Filter by start date (ISO 8601 format) |
| `end_date` | string | Filter by end date (ISO 8601 format) |
| `limit` | integer | Maximum number of orders to return (default: 100) |
| `offset` | integer | Number of orders to skip (default: 0) |

#### Response

```json
{
  "orders": [
    {
      "id": "order_123456",
      "client_order_id": "client_order_123456",
      "portfolio_id": "portfolio_123456",
      "symbol": "AAPL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 1000,
      "price": 200.00,
      "time_in_force": "day",
      "status": "open",
      "filled_quantity": 500,
      "average_fill_price": 199.95,
      "created_at": "2025-06-06T09:30:00Z",
      "updated_at": "2025-06-06T10:15:00Z"
    },
    {
      "id": "order_789012",
      "client_order_id": "client_order_789012",
      "portfolio_id": "portfolio_123456",
      "symbol": "MSFT",
      "side": "sell",
      "order_type": "market",
      "quantity": 500,
      "time_in_force": "day",
      "status": "filled",
      "filled_quantity": 500,
      "average_fill_price": 350.25,
      "created_at": "2025-06-06T09:35:00Z",
      "updated_at": "2025-06-06T09:35:05Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Order

```
GET /orders/{order_id}
```

Retrieves a specific order by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `order_id` | string | The ID of the order to retrieve |

#### Response

```json
{
  "id": "order_123456",
  "client_order_id": "client_order_123456",
  "portfolio_id": "portfolio_123456",
  "symbol": "AAPL",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1000,
  "price": 200.00,
  "time_in_force": "day",
  "status": "open",
  "filled_quantity": 500,
  "average_fill_price": 199.95,
  "remaining_quantity": 500,
  "created_at": "2025-06-06T09:30:00Z",
  "updated_at": "2025-06-06T10:15:00Z",
  "executions": [
    {
      "id": "execution_123456",
      "quantity": 300,
      "price": 199.90,
      "timestamp": "2025-06-06T09:45:00Z",
      "venue": "NASDAQ"
    },
    {
      "id": "execution_789012",
      "quantity": 200,
      "price": 200.00,
      "timestamp": "2025-06-06T10:15:00Z",
      "venue": "NYSE"
    }
  ],
  "routing": {
    "destination": "smart",
    "strategy": "vwap",
    "parameters": {
      "start_time": "2025-06-06T09:30:00Z",
      "end_time": "2025-06-06T16:00:00Z",
      "participation_rate": 0.1
    }
  },
  "additional_parameters": {
    "display_quantity": 100,
    "min_quantity": 100,
    "all_or_none": false,
    "stop_price": null
  }
}
```

### Create Order

```
POST /orders
```

Creates a new order.

#### Request Body

```json
{
  "client_order_id": "client_order_345678",
  "portfolio_id": "portfolio_123456",
  "symbol": "GOOGL",
  "side": "buy",
  "order_type": "limit",
  "quantity": 200,
  "price": 150.00,
  "time_in_force": "day",
  "routing": {
    "destination": "smart",
    "strategy": "twap",
    "parameters": {
      "start_time": "2025-06-06T09:30:00Z",
      "end_time": "2025-06-06T16:00:00Z",
      "interval_minutes": 30
    }
  },
  "additional_parameters": {
    "display_quantity": 50,
    "min_quantity": 50,
    "all_or_none": false
  }
}
```

#### Response

```json
{
  "id": "order_345678",
  "client_order_id": "client_order_345678",
  "portfolio_id": "portfolio_123456",
  "symbol": "GOOGL",
  "side": "buy",
  "order_type": "limit",
  "quantity": 200,
  "price": 150.00,
  "time_in_force": "day",
  "status": "new",
  "filled_quantity": 0,
  "average_fill_price": null,
  "remaining_quantity": 200,
  "created_at": "2025-06-06T11:00:00Z",
  "updated_at": "2025-06-06T11:00:00Z",
  "routing": {
    "destination": "smart",
    "strategy": "twap",
    "parameters": {
      "start_time": "2025-06-06T09:30:00Z",
      "end_time": "2025-06-06T16:00:00Z",
      "interval_minutes": 30
    }
  },
  "additional_parameters": {
    "display_quantity": 50,
    "min_quantity": 50,
    "all_or_none": false
  }
}
```

### Update Order

```
PUT /orders/{order_id}
```

Updates an existing order.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `order_id` | string | The ID of the order to update |

#### Request Body

```json
{
  "quantity": 300,
  "price": 155.00,
  "additional_parameters": {
    "display_quantity": 100,
    "min_quantity": 100
  }
}
```

#### Response

```json
{
  "id": "order_345678",
  "client_order_id": "client_order_345678",
  "portfolio_id": "portfolio_123456",
  "symbol": "GOOGL",
  "side": "buy",
  "order_type": "limit",
  "quantity": 300,
  "price": 155.00,
  "time_in_force": "day",
  "status": "open",
  "filled_quantity": 0,
  "average_fill_price": null,
  "remaining_quantity": 300,
  "created_at": "2025-06-06T11:00:00Z",
  "updated_at": "2025-06-06T11:15:00Z",
  "routing": {
    "destination": "smart",
    "strategy": "twap",
    "parameters": {
      "start_time": "2025-06-06T09:30:00Z",
      "end_time": "2025-06-06T16:00:00Z",
      "interval_minutes": 30
    }
  },
  "additional_parameters": {
    "display_quantity": 100,
    "min_quantity": 100,
    "all_or_none": false
  }
}
```

### Cancel Order

```
DELETE /orders/{order_id}
```

Cancels an existing order.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `order_id` | string | The ID of the order to cancel |

#### Response

```json
{
  "id": "order_345678",
  "client_order_id": "client_order_345678",
  "status": "canceled",
  "canceled_at": "2025-06-06T11:30:00Z",
  "filled_quantity": 0,
  "remaining_quantity": 300
}
```

### Create Basket Order

```
POST /orders/basket
```

Creates a basket of orders.

#### Request Body

```json
{
  "portfolio_id": "portfolio_123456",
  "orders": [
    {
      "client_order_id": "client_order_901234",
      "symbol": "AAPL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 1000,
      "price": 200.00,
      "time_in_force": "day"
    },
    {
      "client_order_id": "client_order_901235",
      "symbol": "MSFT",
      "side": "buy",
      "order_type": "limit",
      "quantity": 500,
      "price": 350.00,
      "time_in_force": "day"
    },
    {
      "client_order_id": "client_order_901236",
      "symbol": "GOOGL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 200,
      "price": 150.00,
      "time_in_force": "day"
    }
  ],
  "execution_strategy": "sequential",
  "additional_parameters": {
    "max_notional": 1000000.00,
    "max_percentage": 0.1
  }
}
```

#### Response

```json
{
  "basket_id": "basket_123456",
  "portfolio_id": "portfolio_123456",
  "status": "processing",
  "orders": [
    {
      "id": "order_901234",
      "client_order_id": "client_order_901234",
      "symbol": "AAPL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 1000,
      "price": 200.00,
      "time_in_force": "day",
      "status": "new"
    },
    {
      "id": "order_901235",
      "client_order_id": "client_order_901235",
      "symbol": "MSFT",
      "side": "buy",
      "order_type": "limit",
      "quantity": 500,
      "price": 350.00,
      "time_in_force": "day",
      "status": "new"
    },
    {
      "id": "order_901236",
      "client_order_id": "client_order_901236",
      "symbol": "GOOGL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 200,
      "price": 150.00,
      "time_in_force": "day",
      "status": "new"
    }
  ],
  "execution_strategy": "sequential",
  "additional_parameters": {
    "max_notional": 1000000.00,
    "max_percentage": 0.1
  },
  "created_at": "2025-06-06T12:00:00Z",
  "updated_at": "2025-06-06T12:00:00Z"
}
```

### Get Basket Order

```
GET /orders/basket/{basket_id}
```

Retrieves a specific basket order by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `basket_id` | string | The ID of the basket order to retrieve |

#### Response

```json
{
  "basket_id": "basket_123456",
  "portfolio_id": "portfolio_123456",
  "status": "completed",
  "orders": [
    {
      "id": "order_901234",
      "client_order_id": "client_order_901234",
      "symbol": "AAPL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 1000,
      "price": 200.00,
      "time_in_force": "day",
      "status": "filled",
      "filled_quantity": 1000,
      "average_fill_price": 199.95
    },
    {
      "id": "order_901235",
      "client_order_id": "client_order_901235",
      "symbol": "MSFT",
      "side": "buy",
      "order_type": "limit",
      "quantity": 500,
      "price": 350.00,
      "time_in_force": "day",
      "status": "filled",
      "filled_quantity": 500,
      "average_fill_price": 349.90
    },
    {
      "id": "order_901236",
      "client_order_id": "client_order_901236",
      "symbol": "GOOGL",
      "side": "buy",
      "order_type": "limit",
      "quantity": 200,
      "price": 150.00,
      "time_in_force": "day",
      "status": "filled",
      "filled_quantity": 200,
      "average_fill_price": 149.95
    }
  ],
  "execution_strategy": "sequential",
  "additional_parameters": {
    "max_notional": 1000000.00,
    "max_percentage": 0.1
  },
  "summary": {
    "total_orders": 3,
    "filled_orders": 3,
    "partial_fills": 0,
    "unfilled_orders": 0,
    "total_notional": 399950.00
  },
  "created_at": "2025-06-06T12:00:00Z",
  "updated_at": "2025-06-06T12:15:00Z"
}
```

### Cancel Basket Order

```
DELETE /orders/basket/{basket_id}
```

Cancels a basket order.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `basket_id` | string | The ID of the basket order to cancel |

#### Response

```json
{
  "basket_id": "basket_123456",
  "status": "canceled",
  "canceled_at": "2025-06-06T12:05:00Z",
  "orders": [
    {
      "id": "order_901234",
      "client_order_id": "client_order_901234",
      "status": "canceled",
      "filled_quantity": 500,
      "remaining_quantity": 500
    },
    {
      "id": "order_901235",
      "client_order_id": "client_order_901235",
      "status": "canceled",
      "filled_quantity": 0,
      "remaining_quantity": 500
    },
    {
      "id": "order_901236",
      "client_order_id": "client_order_901236",
      "status": "canceled",
      "filled_quantity": 0,
      "remaining_quantity": 200
    }
  ]
}
```

## Executions

### List Executions

```
GET /executions
```

Retrieves a list of executions based on specified filters.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `order_id` | string | Filter by order ID |
| `portfolio_id` | string | Filter by portfolio ID |
| `symbol` | string | Filter by symbol |
| `side` | string | Filter by side (`buy` or `sell`) |
| `start_date` | string | Filter by start date (ISO 8601 format) |
| `end_date` | string | Filter by end date (ISO 8601 format) |
| `limit` | integer | Maximum number of executions to return (default: 100) |
| `offset` | integer | Number of executions to skip (default: 0) |

#### Response

```json
{
  "executions": [
    {
      "id": "execution_123456",
      "order_id": "order_123456",
      "portfolio_id": "portfolio_123456",
      "symbol": "AAPL",
      "side": "buy",
      "quantity": 300,
      "price": 199.90,
      "venue": "NASDAQ",
      "timestamp": "2025-06-06T09:45:00Z"
    },
    {
      "id": "execution_789012",
      "order_id": "order_123456",
      "portfolio_id": "portfolio_123456",
      "symbol": "AAPL",
      "side": "buy",
      "quantity": 200,
      "price": 200.00,
      "venue": "NYSE",
      "timestamp": "2025-06-06T10:15:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Execution

```
GET /executions/{execution_id}
```

Retrieves a specific execution by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `execution_id` | string | The ID of the execution to retrieve |

#### Response

```json
{
  "id": "execution_123456",
  "order_id": "order_123456",
  "client_order_id": "client_order_123456",
  "portfolio_id": "portfolio_123456",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 300,
  "price": 199.90,
  "venue": "NASDAQ",
  "timestamp": "2025-06-06T09:45:00Z",
  "fees": {
    "commission": 2.99,
    "sec_fee": 0.10,
    "exchange_fee": 0.25,
    "clearing_fee": 0.05,
    "total_fees": 3.39
  },
  "settlement": {
    "settlement_date": "2025-06-08",
    "status": "pending"
  },
  "additional_details": {
    "liquidity_indicator": "added",
    "broker_id": "broker_123456",
    "execution_type": "regular",
    "order_capacity": "agency"
  }
}
```

## Allocations

### List Allocations

```
GET /allocations
```

Retrieves a list of allocations based on specified filters.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `execution_id` | string | Filter by execution ID |
| `portfolio_id` | string | Filter by portfolio ID |
| `account_id` | string | Filter by account ID |
| `symbol` | string | Filter by symbol |
| `start_date` | string | Filter by start date (ISO 8601 format) |
| `end_date` | string | Filter by end date (ISO 8601 format) |
| `limit` | integer | Maximum number of allocations to return (default: 100) |
| `offset` | integer | Number of allocations to skip (default: 0) |

#### Response

```json
{
  "allocations": [
    {
      "id": "allocation_123456",
      "execution_id": "execution_123456",
      "portfolio_id": "portfolio_123456",
      "account_id": "account_123456",
      "symbol": "AAPL",
      "side": "buy",
      "quantity": 150,
      "price": 199.90,
      "timestamp": "2025-06-06T09:50:00Z",
      "status": "confirmed"
    },
    {
      "id": "allocation_789012",
      "execution_id": "execution_123456",
      "portfolio_id": "portfolio_123456",
      "account_id": "account_789012",
      "symbol": "AAPL",
      "side": "buy",
      "quantity": 150,
      "price": 199.90,
      "timestamp": "2025-06-06T09:50:00Z",
      "status": "confirmed"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Allocation

```
GET /allocations/{allocation_id}
```

Retrieves a specific allocation by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `allocation_id` | string | The ID of the allocation to retrieve |

#### Response

```json
{
  "id": "allocation_123456",
  "execution_id": "execution_123456",
  "order_id": "order_123456",
  "portfolio_id": "portfolio_123456",
  "account_id": "account_123456",
  "account_name": "Main Investment Account",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 150,
  "price": 199.90,
  "amount": 29985.00,
  "fees": {
    "commission": 1.50,
    "sec_fee": 0.05,
    "exchange_fee": 0.13,
    "clearing_fee": 0.03,
    "total_fees": 1.71
  },
  "timestamp": "2025-06-06T09:50:00Z",
  "status": "confirmed",
  "settlement": {
    "settlement_date": "2025-06-08",
    "status": "pending"
  },
  "created_at": "2025-06-06T09:50:00Z",
  "updated_at": "2025-06-06T09:55:00Z"
}
```

### Create Allocation

```
POST /allocations
```

Creates a new allocation.

#### Request Body

```json
{
  "execution_id": "execution_789012",
  "allocations": [
    {
      "account_id": "account_123456",
      "quantity": 100,
      "fees": {
        "commission": 1.00,
        "sec_fee": 0.03,
        "exchange_fee": 0.08,
        "clearing_fee": 0.02
      }
    },
    {
      "account_id": "account_789012",
      "quantity": 100,
      "fees": {
        "commission": 1.00,
        "sec_fee": 0.03,
        "exchange_fee": 0.08,
        "clearing_fee": 0.02
      }
    }
  ]
}
```

#### Response

```json
{
  "execution_id": "execution_789012",
  "allocations": [
    {
      "id": "allocation_345678",
      "account_id": "account_123456",
      "quantity": 100,
      "price": 200.00,
      "amount": 20000.00,
      "fees": {
        "commission": 1.00,
        "sec_fee": 0.03,
        "exchange_fee": 0.08,
        "clearing_fee": 0.02,
        "total_fees": 1.13
      },
      "status": "pending"
    },
    {
      "id": "allocation_901234",
      "account_id": "account_789012",
      "quantity": 100,
      "price": 200.00,
      "amount": 20000.00,
      "fees": {
        "commission": 1.00,
        "sec_fee": 0.03,
        "exchange_fee": 0.08,
        "clearing_fee": 0.02,
        "total_fees": 1.13
      },
      "status": "pending"
    }
  ],
  "created_at": "2025-06-06T10:20:00Z"
}
```

### Update Allocation

```
PUT /allocations/{allocation_id}
```

Updates an existing allocation.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `allocation_id` | string | The ID of the allocation to update |

#### Request Body

```json
{
  "quantity": 120,
  "fees": {
    "commission": 1.20,
    "sec_fee": 0.04,
    "exchange_fee": 0.10,
    "clearing_fee": 0.02
  }
}
```

#### Response

```json
{
  "id": "allocation_345678",
  "execution_id": "execution_789012",
  "order_id": "order_123456",
  "portfolio_id": "portfolio_123456",
  "account_id": "account_123456",
  "account_name": "Main Investment Account",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 120,
  "price": 200.00,
  "amount": 24000.00,
  "fees": {
    "commission": 1.20,
    "sec_fee": 0.04,
    "exchange_fee": 0.10,
    "clearing_fee": 0.02,
    "total_fees": 1.36
  },
  "timestamp": "2025-06-06T10:20:00Z",
  "status": "pending",
  "settlement": {
    "settlement_date": "2025-06-08",
    "status": "pending"
  },
  "created_at": "2025-06-06T10:20:00Z",
  "updated_at": "2025-06-06T10:25:00Z"
}
```

### Confirm Allocation

```
POST /allocations/{allocation_id}/confirm
```

Confirms an allocation.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `allocation_id` | string | The ID of the allocation to confirm |

#### Response

```json
{
  "id": "allocation_345678",
  "status": "confirmed",
  "confirmed_at": "2025-06-06T10:30:00Z"
}
```

## Settlements

### List Settlements

```
GET /settlements
```

Retrieves a list of settlements based on specified filters.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `allocation_id` | string | Filter by allocation ID |
| `portfolio_id` | string | Filter by portfolio ID |
| `account_id` | string | Filter by account ID |
| `symbol` | string | Filter by symbol |
| `status` | string | Filter by status (e.g., `pending`, `settled`, `failed`) |
| `settlement_date` | string | Filter by settlement date (ISO 8601 format) |
| `start_date` | string | Filter by start date (ISO 8601 format) |
| `end_date` | string | Filter by end date (ISO 8601 format) |
| `limit` | integer | Maximum number of settlements to return (default: 100) |
| `offset` | integer | Number of settlements to skip (default: 0) |

#### Response

```json
{
  "settlements": [
    {
      "id": "settlement_123456",
      "allocation_id": "allocation_123456",
      "portfolio_id": "portfolio_123456",
      "account_id": "account_123456",
      "symbol": "AAPL",
      "side": "buy",
      "quantity": 150,
      "price": 199.90,
      "amount": 29985.00,
      "settlement_date": "2025-06-08",
      "status": "settled",
      "settled_at": "2025-06-08T16:00:00Z"
    },
    {
      "id": "settlement_789012",
      "allocation_id": "allocation_789012",
      "portfolio_id": "portfolio_123456",
      "account_id": "account_789012",
      "symbol": "AAPL",
      "side": "buy",
      "quantity": 150,
      "price": 199.90,
      "amount": 29985.00,
      "settlement_date": "2025-06-08",
      "status": "pending"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Settlement

```
GET /settlements/{settlement_id}
```

Retrieves a specific settlement by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `settlement_id` | string | The ID of the settlement to retrieve |

#### Response

```json
{
  "id": "settlement_123456",
  "allocation_id": "allocation_123456",
  "execution_id": "execution_123456",
  "order_id": "order_123456",
  "portfolio_id": "portfolio_123456",
  "account_id": "account_123456",
  "account_name": "Main Investment Account",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 150,
  "price": 199.90,
  "amount": 29985.00,
  "fees": {
    "commission": 1.50,
    "sec_fee": 0.05,
    "exchange_fee": 0.13,
    "clearing_fee": 0.03,
    "total_fees": 1.71
  },
  "settlement_date": "2025-06-08",
  "status": "settled",
  "settled_at": "2025-06-08T16:00:00Z",
  "settlement_details": {
    "custodian": "Example Custodian",
    "settlement_account": "ABCD1234",
    "settlement_currency": "USD",
    "settlement_amount": 29986.71,
    "settlement_reference": "REF123456"
  },
  "created_at": "2025-06-06T09:55:00Z",
  "updated_at": "2025-06-08T16:00:00Z"
}
```

### Update Settlement

```
PUT /settlements/{settlement_id}
```

Updates an existing settlement.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `settlement_id` | string | The ID of the settlement to update |

#### Request Body

```json
{
  "status": "settled",
  "settlement_details": {
    "settlement_reference": "REF789012",
    "settlement_notes": "Settled via DTC"
  }
}
```

#### Response

```json
{
  "id": "settlement_789012",
  "allocation_id": "allocation_789012",
  "portfolio_id": "portfolio_123456",
  "account_id": "account_789012",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 150,
  "price": 199.90,
  "amount": 29985.00,
  "settlement_date": "2025-06-08",
  "status": "settled",
  "settled_at": "2025-06-08T16:30:00Z",
  "settlement_details": {
    "custodian": "Example Custodian",
    "settlement_account": "EFGH5678",
    "settlement_currency": "USD",
    "settlement_amount": 29986.71,
    "settlement_reference": "REF789012",
    "settlement_notes": "Settled via DTC"
  },
  "created_at": "2025-06-06T09:55:00Z",
  "updated_at": "2025-06-08T16:30:00Z"
}
```

### Fail Settlement

```
POST /settlements/{settlement_id}/fail
```

Marks a settlement as failed.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `settlement_id` | string | The ID of the settlement to mark as failed |

#### Request Body

```json
{
  "reason": "Insufficient funds in settlement account",
  "notes": "Client notified, will retry settlement on 2025-06-09"
}
```

#### Response

```json
{
  "id": "settlement_789012",
  "status": "failed",
  "failed_at": "2025-06-08T16:45:00Z",
  "failure_reason": "Insufficient funds in settlement account",
  "failure_notes": "Client notified, will retry settlement on 2025-06-09"
}
```

## Broker Connections

### List Broker Connections

```
GET /brokers
```

Retrieves a list of broker connections.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status (e.g., `active`, `inactive`) |
| `limit` | integer | Maximum number of broker connections to return (default: 100) |
| `offset` | integer | Number of broker connections to skip (default: 0) |

#### Response

```json
{
  "brokers": [
    {
      "id": "broker_123456",
      "name": "Example Broker 1",
      "status": "active",
      "connection_type": "fix",
      "markets": ["US", "Europe"],
      "asset_classes": ["equity", "option", "future"],
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    {
      "id": "broker_789012",
      "name": "Example Broker 2",
      "status": "active",
      "connection_type": "api",
      "markets": ["US", "Asia"],
      "asset_classes": ["equity", "fixed_income"],
      "created_at": "2025-01-02T00:00:00Z",
      "updated_at": "2025-01-02T00:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Broker Connection

```
GET /brokers/{broker_id}
```

Retrieves a specific broker connection by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `broker_id` | string | The ID of the broker connection to retrieve |

#### Response

```json
{
  "id": "broker_123456",
  "name": "Example Broker 1",
  "status": "active",
  "connection_type": "fix",
  "connection_details": {
    "fix_version": "4.4",
    "sender_comp_id": "QUANTUMALPHA",
    "target_comp_id": "EXAMPLEBROKER",
    "host": "fix.examplebroker.com",
    "port": 9823
  },
  "markets": ["US", "Europe"],
  "asset_classes": ["equity", "option", "future"],
  "trading_hours": {
    "US": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/New_York"
    },
    "Europe": {
      "open": "08:00:00",
      "close": "16:30:00",
      "timezone": "Europe/London"
    }
  },
  "capabilities": {
    "algorithms": true,
    "dma": true,
    "program_trading": true,
    "care_orders": true
  },
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### Create Broker Connection

```
POST /brokers
```

Creates a new broker connection.

#### Request Body

```json
{
  "name": "Example Broker 3",
  "connection_type": "api",
  "connection_details": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "base_url": "https://api.examplebroker3.com/v1",
    "timeout_seconds": 30
  },
  "markets": ["US", "Canada"],
  "asset_classes": ["equity", "option"],
  "trading_hours": {
    "US": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/New_York"
    },
    "Canada": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/Toronto"
    }
  },
  "capabilities": {
    "algorithms": true,
    "dma": true,
    "program_trading": false,
    "care_orders": false
  }
}
```

#### Response

```json
{
  "id": "broker_345678",
  "name": "Example Broker 3",
  "status": "active",
  "connection_type": "api",
  "connection_details": {
    "api_key": "YOUR_API_KEY",
    "api_secret": "********",
    "base_url": "https://api.examplebroker3.com/v1",
    "timeout_seconds": 30
  },
  "markets": ["US", "Canada"],
  "asset_classes": ["equity", "option"],
  "trading_hours": {
    "US": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/New_York"
    },
    "Canada": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/Toronto"
    }
  },
  "capabilities": {
    "algorithms": true,
    "dma": true,
    "program_trading": false,
    "care_orders": false
  },
  "created_at": "2025-06-06T13:00:00Z",
  "updated_at": "2025-06-06T13:00:00Z"
}
```

### Update Broker Connection

```
PUT /brokers/{broker_id}
```

Updates an existing broker connection.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `broker_id` | string | The ID of the broker connection to update |

#### Request Body

```json
{
  "name": "Example Broker 3 (Updated)",
  "connection_details": {
    "api_key": "YOUR_NEW_API_KEY",
    "api_secret": "YOUR_NEW_API_SECRET",
    "timeout_seconds": 60
  },
  "capabilities": {
    "algorithms": true,
    "dma": true,
    "program_trading": true,
    "care_orders": false
  }
}
```

#### Response

```json
{
  "id": "broker_345678",
  "name": "Example Broker 3 (Updated)",
  "status": "active",
  "connection_type": "api",
  "connection_details": {
    "api_key": "YOUR_NEW_API_KEY",
    "api_secret": "********",
    "base_url": "https://api.examplebroker3.com/v1",
    "timeout_seconds": 60
  },
  "markets": ["US", "Canada"],
  "asset_classes": ["equity", "option"],
  "trading_hours": {
    "US": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/New_York"
    },
    "Canada": {
      "open": "09:30:00",
      "close": "16:00:00",
      "timezone": "America/Toronto"
    }
  },
  "capabilities": {
    "algorithms": true,
    "dma": true,
    "program_trading": true,
    "care_orders": false
  },
  "created_at": "2025-06-06T13:00:00Z",
  "updated_at": "2025-06-06T13:15:00Z"
}
```

### Delete Broker Connection

```
DELETE /brokers/{broker_id}
```

Deletes a broker connection.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `broker_id` | string | The ID of the broker connection to delete |

#### Response

```json
{
  "success": true,
  "message": "Broker connection deleted successfully"
}
```

### Test Broker Connection

```
POST /brokers/{broker_id}/test
```

Tests a broker connection.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `broker_id` | string | The ID of the broker connection to test |

#### Response

```json
{
  "success": true,
  "connection_status": "connected",
  "latency_ms": 45,
  "details": {
    "session_established": true,
    "heartbeat_received": true,
    "market_data_available": true,
    "order_submission_available": true
  },
  "tested_at": "2025-06-06T13:30:00Z"
}
```

## Market Data

### Get Market Data

```
GET /market-data/{symbol}
```

Retrieves market data for a specific symbol.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | The symbol to retrieve market data for |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | string | Market data level (`1`, `2`) (default: `1`) |

#### Response

```json
{
  "symbol": "AAPL",
  "timestamp": "2025-06-06T13:45:00Z",
  "exchange": "NASDAQ",
  "last_price": 200.50,
  "last_size": 100,
  "last_trade_time": "2025-06-06T13:44:55Z",
  "bid": 200.45,
  "bid_size": 500,
  "ask": 200.55,
  "ask_size": 300,
  "volume": 5000000,
  "open": 199.00,
  "high": 201.00,
  "low": 198.50,
  "close": null,
  "change": 1.50,
  "change_percent": 0.75,
  "level2": {
    "bids": [
      {
        "price": 200.45,
        "size": 500,
        "exchange": "NASDAQ"
      },
      {
        "price": 200.40,
        "size": 800,
        "exchange": "NYSE"
      },
      {
        "price": 200.35,
        "size": 1200,
        "exchange": "BATS"
      }
    ],
    "asks": [
      {
        "price": 200.55,
        "size": 300,
        "exchange": "NASDAQ"
      },
      {
        "price": 200.60,
        "size": 600,
        "exchange": "NYSE"
      },
      {
        "price": 200.65,
        "size": 900,
        "exchange": "BATS"
      }
    ]
  }
}
```

### Get Historical Market Data

```
GET /market-data/{symbol}/history
```

Retrieves historical market data for a specific symbol.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | string | The symbol to retrieve historical market data for |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `interval` | string | Data interval (`1m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1w`, `1mo`) |
| `start_date` | string | Start date in ISO 8601 format |
| `end_date` | string | End date in ISO 8601 format |
| `limit` | integer | Maximum number of data points to return (default: 100) |

#### Response

```json
{
  "symbol": "AAPL",
  "interval": "1d",
  "data": [
    {
      "timestamp": "2025-06-06T00:00:00Z",
      "open": 199.00,
      "high": 201.00,
      "low": 198.50,
      "close": 200.50,
      "volume": 5000000
    },
    {
      "timestamp": "2025-06-05T00:00:00Z",
      "open": 198.00,
      "high": 200.00,
      "low": 197.50,
      "close": 199.00,
      "volume": 4800000
    },
    {
      "timestamp": "2025-06-04T00:00:00Z",
      "open": 197.50,
      "high": 199.50,
      "low": 197.00,
      "close": 198.00,
      "volume": 4600000
    }
  ],
  "meta": {
    "symbol": "AAPL",
    "interval": "1d",
    "start_date": "2025-06-04T00:00:00Z",
    "end_date": "2025-06-06T00:00:00Z",
    "count": 3
  }
}
```

## Algorithms

### List Algorithms

```
GET /algorithms
```

Retrieves a list of available trading algorithms.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `broker_id` | string | Filter by broker ID |
| `asset_class` | string | Filter by asset class |
| `limit` | integer | Maximum number of algorithms to return (default: 100) |
| `offset` | integer | Number of algorithms to skip (default: 0) |

#### Response

```json
{
  "algorithms": [
    {
      "id": "algo_123456",
      "name": "VWAP",
      "description": "Volume Weighted Average Price algorithm",
      "broker_id": "broker_123456",
      "broker_name": "Example Broker 1",
      "asset_classes": ["equity", "option"],
      "parameters": [
        {
          "name": "start_time",
          "type": "datetime",
          "required": true,
          "description": "Algorithm start time"
        },
        {
          "name": "end_time",
          "type": "datetime",
          "required": true,
          "description": "Algorithm end time"
        },
        {
          "name": "participation_rate",
          "type": "float",
          "required": false,
          "default": 0.1,
          "min": 0.01,
          "max": 0.5,
          "description": "Target participation rate"
        }
      ]
    },
    {
      "id": "algo_789012",
      "name": "TWAP",
      "description": "Time Weighted Average Price algorithm",
      "broker_id": "broker_123456",
      "broker_name": "Example Broker 1",
      "asset_classes": ["equity", "option"],
      "parameters": [
        {
          "name": "start_time",
          "type": "datetime",
          "required": true,
          "description": "Algorithm start time"
        },
        {
          "name": "end_time",
          "type": "datetime",
          "required": true,
          "description": "Algorithm end time"
        },
        {
          "name": "interval_minutes",
          "type": "integer",
          "required": false,
          "default": 5,
          "min": 1,
          "max": 60,
          "description": "Time interval in minutes"
        }
      ]
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Algorithm

```
GET /algorithms/{algorithm_id}
```

Retrieves a specific algorithm by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `algorithm_id` | string | The ID of the algorithm to retrieve |

#### Response

```json
{
  "id": "algo_123456",
  "name": "VWAP",
  "description": "Volume Weighted Average Price algorithm",
  "broker_id": "broker_123456",
  "broker_name": "Example Broker 1",
  "asset_classes": ["equity", "option"],
  "parameters": [
    {
      "name": "start_time",
      "type": "datetime",
      "required": true,
      "description": "Algorithm start time"
    },
    {
      "name": "end_time",
      "type": "datetime",
      "required": true,
      "description": "Algorithm end time"
    },
    {
      "name": "participation_rate",
      "type": "float",
      "required": false,
      "default": 0.1,
      "min": 0.01,
      "max": 0.5,
      "description": "Target participation rate"
    },
    {
      "name": "min_size",
      "type": "integer",
      "required": false,
      "default": 100,
      "min": 1,
      "description": "Minimum order size"
    },
    {
      "name": "max_size",
      "type": "integer",
      "required": false,
      "default": 10000,
      "min": 100,
      "description": "Maximum order size"
    },
    {
      "name": "price_limit",
      "type": "float",
      "required": false,
      "description": "Price limit"
    },
    {
      "name": "aggressive_completion",
      "type": "boolean",
      "required": false,
      "default": false,
      "description": "Aggressively complete order at end time"
    }
  ],
  "performance_metrics": {
    "average_slippage": 0.02,
    "average_participation_rate": 0.12,
    "average_completion_rate": 0.98
  },
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

## Transaction Cost Analysis

### Get Transaction Cost Analysis

```
GET /tca/{execution_id}
```

Retrieves transaction cost analysis for a specific execution.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `execution_id` | string | The ID of the execution to analyze |

#### Response

```json
{
  "execution_id": "execution_123456",
  "order_id": "order_123456",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 300,
  "price": 199.90,
  "execution_time": "2025-06-06T09:45:00Z",
  "market_conditions": {
    "arrival_price": 199.80,
    "vwap": 199.85,
    "twap": 199.83,
    "open": 199.00,
    "high": 200.00,
    "low": 198.90,
    "close": 200.50,
    "volume": 5000000
  },
  "metrics": {
    "implementation_shortfall": {
      "value": 0.10,
      "percentage": 0.05,
      "amount": 30.00
    },
    "arrival_price_slippage": {
      "value": 0.10,
      "percentage": 0.05,
      "amount": 30.00
    },
    "vwap_slippage": {
      "value": 0.05,
      "percentage": 0.025,
      "amount": 15.00
    },
    "market_impact": {
      "value": 0.08,
      "percentage": 0.04,
      "amount": 24.00
    },
    "timing_cost": {
      "value": 0.02,
      "percentage": 0.01,
      "amount": 6.00
    },
    "opportunity_cost": {
      "value": 0.60,
      "percentage": 0.30,
      "amount": 180.00
    },
    "total_cost": {
      "value": 0.70,
      "percentage": 0.35,
      "amount": 210.00
    }
  },
  "peer_comparison": {
    "percentile": 25,
    "average_cost": 0.90,
    "median_cost": 0.80,
    "min_cost": 0.40,
    "max_cost": 1.50
  },
  "created_at": "2025-06-06T10:00:00Z"
}
```

### Get Aggregate Transaction Cost Analysis

```
POST /tca/aggregate
```

Retrieves aggregate transaction cost analysis for multiple executions.

#### Request Body

```json
{
  "execution_ids": ["execution_123456", "execution_789012"],
  "start_date": "2025-06-01",
  "end_date": "2025-06-06",
  "group_by": ["broker", "algorithm", "symbol"]
}
```

#### Response

```json
{
  "period": {
    "start_date": "2025-06-01",
    "end_date": "2025-06-06"
  },
  "overall_metrics": {
    "total_executions": 2,
    "total_volume": 500,
    "total_notional": 99950.00,
    "average_implementation_shortfall": 0.08,
    "average_arrival_price_slippage": 0.08,
    "average_vwap_slippage": 0.04,
    "average_market_impact": 0.07,
    "average_timing_cost": 0.01,
    "average_opportunity_cost": 0.50,
    "average_total_cost": 0.58
  },
  "breakdowns": {
    "by_broker": [
      {
        "broker": "Example Broker 1",
        "executions": 2,
        "volume": 500,
        "notional": 99950.00,
        "implementation_shortfall": 0.08,
        "arrival_price_slippage": 0.08,
        "vwap_slippage": 0.04,
        "market_impact": 0.07,
        "timing_cost": 0.01,
        "opportunity_cost": 0.50,
        "total_cost": 0.58
      }
    ],
    "by_algorithm": [
      {
        "algorithm": "VWAP",
        "executions": 1,
        "volume": 300,
        "notional": 59970.00,
        "implementation_shortfall": 0.10,
        "arrival_price_slippage": 0.10,
        "vwap_slippage": 0.05,
        "market_impact": 0.08,
        "timing_cost": 0.02,
        "opportunity_cost": 0.60,
        "total_cost": 0.70
      },
      {
        "algorithm": "Market",
        "executions": 1,
        "volume": 200,
        "notional": 39980.00,
        "implementation_shortfall": 0.05,
        "arrival_price_slippage": 0.05,
        "vwap_slippage": 0.02,
        "market_impact": 0.05,
        "timing_cost": 0.00,
        "opportunity_cost": 0.35,
        "total_cost": 0.40
      }
    ],
    "by_symbol": [
      {
        "symbol": "AAPL",
        "executions": 2,
        "volume": 500,
        "notional": 99950.00,
        "implementation_shortfall": 0.08,
        "arrival_price_slippage": 0.08,
        "vwap_slippage": 0.04,
        "market_impact": 0.07,
        "timing_cost": 0.01,
        "opportunity_cost": 0.50,
        "total_cost": 0.58
      }
    ]
  },
  "created_at": "2025-06-06T14:00:00Z"
}
```

## Reports

### Generate Execution Report

```
POST /reports/executions
```

Generates an execution report.

#### Request Body

```json
{
  "portfolio_id": "portfolio_123456",
  "start_date": "2025-06-01",
  "end_date": "2025-06-06",
  "group_by": ["symbol", "side", "broker"],
  "format": "csv"
}
```

#### Response

```json
{
  "report_id": "report_123456",
  "status": "processing",
  "estimated_completion_time": "2025-06-06T14:05:00Z",
  "created_at": "2025-06-06T14:00:00Z"
}
```

### Get Report Status

```
GET /reports/{report_id}
```

Retrieves the status of a report.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string | The ID of the report to retrieve |

#### Response

```json
{
  "report_id": "report_123456",
  "status": "completed",
  "download_url": "https://api.quantumalpha.com/v1/execution/reports/report_123456/download",
  "expiry_time": "2025-06-13T14:05:00Z",
  "created_at": "2025-06-06T14:00:00Z",
  "completed_at": "2025-06-06T14:05:00Z"
}
```

### Download Report

```
GET /reports/{report_id}/download
```

Downloads a completed report.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string | The ID of the report to download |

#### Response

The response will be a file download with the appropriate content type based on the requested format (e.g., `text/csv`, `application/json`, `application/pdf`).

