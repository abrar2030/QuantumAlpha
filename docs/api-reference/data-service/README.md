# Data Service API Reference

The Data Service API provides access to market data, alternative data, and feature engineering capabilities within the QuantumAlpha platform.

## Table of Contents

1. [Overview](#overview)
2. [Market Data](#market-data)
3. [Alternative Data](#alternative-data)
4. [Feature Engineering](#feature-engineering)
5. [Data Sources](#data-sources)
6. [Data Storage](#data-storage)
7. [Data Streaming](#data-streaming)
8. [Data Quality](#data-quality)

## Overview

The Data Service API provides endpoints for:

- Retrieving market data (prices, volumes, etc.)
- Accessing alternative data (news, sentiment, etc.)
- Managing data sources
- Creating and retrieving engineered features
- Streaming real-time data
- Monitoring data quality

Base URL: `https://api.quantumalpha.com/v1/data`

## Market Data

### Get Market Prices

```
GET /market/prices
```

Retrieves historical price data for specified symbols.

#### Query Parameters

| Parameter    | Type    | Description                                                                    |
| ------------ | ------- | ------------------------------------------------------------------------------ |
| `symbols`    | string  | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)                      |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                             |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                               |
| `interval`   | string  | Data interval (`1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `1w`, `1mo`)        |
| `fields`     | string  | Comma-separated list of fields to include (e.g., `open,high,low,close,volume`) |
| `timezone`   | string  | Timezone for timestamps (default: `UTC`)                                       |
| `adjust`     | boolean | Whether to adjust for splits and dividends (default: `true`)                   |
| `limit`      | integer | Maximum number of data points to return per symbol (default: 1000)             |

#### Response

```json
{
  "data": {
    "AAPL": [
      {
        "timestamp": "2025-06-01T16:00:00Z",
        "open": 150.25,
        "high": 152.3,
        "low": 149.8,
        "close": 151.75,
        "volume": 1250000,
        "adjusted_close": 151.75
      },
      {
        "timestamp": "2025-05-31T16:00:00Z",
        "open": 151.75,
        "high": 153.5,
        "low": 151.0,
        "close": 153.25,
        "volume": 1350000,
        "adjusted_close": 153.25
      }
    ],
    "MSFT": [
      {
        "timestamp": "2025-06-01T16:00:00Z",
        "open": 320.5,
        "high": 325.75,
        "low": 319.25,
        "close": 324.5,
        "volume": 980000,
        "adjusted_close": 324.5
      },
      {
        "timestamp": "2025-05-31T16:00:00Z",
        "open": 318.25,
        "high": 321.0,
        "low": 317.5,
        "close": 320.5,
        "volume": 1050000,
        "adjusted_close": 320.5
      }
    ]
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "start_date": "2025-05-31T16:00:00Z",
    "end_date": "2025-06-01T16:00:00Z",
    "interval": "1d",
    "timezone": "UTC",
    "adjusted": true
  }
}
```

### Get Market Quotes

```
GET /market/quotes
```

Retrieves the latest quotes for specified symbols.

#### Query Parameters

| Parameter | Type   | Description                                                     |
| --------- | ------ | --------------------------------------------------------------- |
| `symbols` | string | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)       |
| `fields`  | string | Comma-separated list of fields to include (default: all fields) |

#### Response

```json
{
  "data": {
    "AAPL": {
      "timestamp": "2025-06-06T15:30:00Z",
      "bid": 151.5,
      "ask": 151.55,
      "last": 151.52,
      "volume": 1250000,
      "bid_size": 500,
      "ask_size": 700
    },
    "MSFT": {
      "timestamp": "2025-06-06T15:30:00Z",
      "bid": 324.25,
      "ask": 324.3,
      "last": 324.28,
      "volume": 980000,
      "bid_size": 300,
      "ask_size": 400
    }
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "timestamp": "2025-06-06T15:30:00Z"
  }
}
```

### Get Market Bars

```
GET /market/bars
```

Retrieves OHLCV (Open, High, Low, Close, Volume) bars for specified symbols.

#### Query Parameters

| Parameter    | Type    | Description                                                            |
| ------------ | ------- | ---------------------------------------------------------------------- |
| `symbols`    | string  | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)              |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                     |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                       |
| `interval`   | string  | Bar interval (`1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `1w`, `1mo`) |
| `timezone`   | string  | Timezone for timestamps (default: `UTC`)                               |
| `adjust`     | boolean | Whether to adjust for splits and dividends (default: `true`)           |
| `limit`      | integer | Maximum number of bars to return per symbol (default: 1000)            |

#### Response

```json
{
  "data": {
    "AAPL": [
      {
        "timestamp": "2025-06-01T16:00:00Z",
        "open": 150.25,
        "high": 152.3,
        "low": 149.8,
        "close": 151.75,
        "volume": 1250000
      },
      {
        "timestamp": "2025-05-31T16:00:00Z",
        "open": 151.75,
        "high": 153.5,
        "low": 151.0,
        "close": 153.25,
        "volume": 1350000
      }
    ],
    "MSFT": [
      {
        "timestamp": "2025-06-01T16:00:00Z",
        "open": 320.5,
        "high": 325.75,
        "low": 319.25,
        "close": 324.5,
        "volume": 980000
      },
      {
        "timestamp": "2025-05-31T16:00:00Z",
        "open": 318.25,
        "high": 321.0,
        "low": 317.5,
        "close": 320.5,
        "volume": 1050000
      }
    ]
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "start_date": "2025-05-31T16:00:00Z",
    "end_date": "2025-06-01T16:00:00Z",
    "interval": "1d",
    "timezone": "UTC",
    "adjusted": true
  }
}
```

### Get Market Depth

```
GET /market/depth
```

Retrieves order book data for specified symbols.

#### Query Parameters

| Parameter | Type    | Description                                      |
| --------- | ------- | ------------------------------------------------ |
| `symbol`  | string  | Symbol to retrieve order book data for           |
| `limit`   | integer | Maximum number of levels to return (default: 10) |

#### Response

```json
{
  "data": {
    "symbol": "AAPL",
    "timestamp": "2025-06-06T15:30:00Z",
    "bids": [
      {
        "price": 151.5,
        "size": 500
      },
      {
        "price": 151.45,
        "size": 700
      },
      {
        "price": 151.4,
        "size": 1000
      }
    ],
    "asks": [
      {
        "price": 151.55,
        "size": 600
      },
      {
        "price": 151.6,
        "size": 800
      },
      {
        "price": 151.65,
        "size": 1200
      }
    ]
  },
  "meta": {
    "symbol": "AAPL",
    "timestamp": "2025-06-06T15:30:00Z",
    "levels": 3
  }
}
```

### Get Market Trades

```
GET /market/trades
```

Retrieves recent trades for specified symbols.

#### Query Parameters

| Parameter    | Type    | Description                                       |
| ------------ | ------- | ------------------------------------------------- |
| `symbol`     | string  | Symbol to retrieve trades for                     |
| `start_time` | string  | Start time in ISO 8601 format                     |
| `end_time`   | string  | End time in ISO 8601 format                       |
| `limit`      | integer | Maximum number of trades to return (default: 100) |

#### Response

```json
{
  "data": {
    "symbol": "AAPL",
    "trades": [
      {
        "id": "trade_123456",
        "timestamp": "2025-06-06T15:30:00.123Z",
        "price": 151.52,
        "size": 100,
        "conditions": ["@", "T"],
        "exchange": "NASDAQ"
      },
      {
        "id": "trade_123457",
        "timestamp": "2025-06-06T15:30:00.456Z",
        "price": 151.53,
        "size": 50,
        "conditions": ["@"],
        "exchange": "NYSE"
      },
      {
        "id": "trade_123458",
        "timestamp": "2025-06-06T15:30:01.789Z",
        "price": 151.51,
        "size": 200,
        "conditions": ["@", "T"],
        "exchange": "NASDAQ"
      }
    ]
  },
  "meta": {
    "symbol": "AAPL",
    "count": 3,
    "start_time": "2025-06-06T15:30:00.000Z",
    "end_time": "2025-06-06T15:30:02.000Z"
  }
}
```

### Get Market Calendar

```
GET /market/calendar
```

Retrieves market calendar information.

#### Query Parameters

| Parameter    | Type   | Description                                        |
| ------------ | ------ | -------------------------------------------------- |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2025-01-01`) |
| `end_date`   | string | End date in ISO 8601 format (e.g., `2025-12-31`)   |
| `exchange`   | string | Exchange code (e.g., `NYSE`, `NASDAQ`)             |

#### Response

```json
{
  "data": [
    {
      "date": "2025-06-06",
      "open": "09:30",
      "close": "16:00",
      "status": "open",
      "exchange": "NYSE"
    },
    {
      "date": "2025-06-07",
      "open": null,
      "close": null,
      "status": "closed",
      "exchange": "NYSE"
    },
    {
      "date": "2025-06-08",
      "open": null,
      "close": null,
      "status": "closed",
      "exchange": "NYSE"
    },
    {
      "date": "2025-06-09",
      "open": "09:30",
      "close": "16:00",
      "status": "open",
      "exchange": "NYSE"
    }
  ],
  "meta": {
    "count": 4,
    "start_date": "2025-06-06",
    "end_date": "2025-06-09",
    "exchange": "NYSE"
  }
}
```

### Get Market Symbols

```
GET /market/symbols
```

Retrieves information about available symbols.

#### Query Parameters

| Parameter  | Type    | Description                                                            |
| ---------- | ------- | ---------------------------------------------------------------------- |
| `status`   | string  | Filter by status (`active`, `inactive`, `all`)                         |
| `type`     | string  | Filter by type (`stock`, `etf`, `forex`, `crypto`, `future`, `option`) |
| `exchange` | string  | Filter by exchange (e.g., `NYSE`, `NASDAQ`)                            |
| `search`   | string  | Search term to filter symbols by name or description                   |
| `limit`    | integer | Maximum number of symbols to return (default: 100)                     |
| `offset`   | integer | Number of symbols to skip (default: 0)                                 |

#### Response

```json
{
  "data": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "type": "stock",
      "exchange": "NASDAQ",
      "status": "active",
      "tradable": true,
      "marginable": true,
      "shortable": true,
      "easy_to_borrow": true
    },
    {
      "symbol": "MSFT",
      "name": "Microsoft Corporation",
      "type": "stock",
      "exchange": "NASDAQ",
      "status": "active",
      "tradable": true,
      "marginable": true,
      "shortable": true,
      "easy_to_borrow": true
    }
  ],
  "meta": {
    "count": 2,
    "total": 10000,
    "limit": 100,
    "offset": 0
  }
}
```

## Alternative Data

### Get News

```
GET /alternative/news
```

Retrieves news articles for specified symbols or topics.

#### Query Parameters

| Parameter    | Type    | Description                                                          |
| ------------ | ------- | -------------------------------------------------------------------- |
| `symbols`    | string  | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)            |
| `topics`     | string  | Comma-separated list of topics (e.g., `earnings,mergers,technology`) |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                   |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                     |
| `limit`      | integer | Maximum number of articles to return (default: 50)                   |
| `offset`     | integer | Number of articles to skip (default: 0)                              |
| `sort_by`    | string  | Sort field (`relevance`, `date`)                                     |
| `sort_order` | string  | Sort order (`asc`, `desc`)                                           |

#### Response

```json
{
  "data": [
    {
      "id": "news_123456",
      "title": "Apple Announces New iPhone 15 Pro with Revolutionary AI Features",
      "summary": "Apple Inc. unveiled its latest iPhone model with groundbreaking AI capabilities that could reshape the smartphone industry.",
      "content": "Apple Inc. (NASDAQ: AAPL) today announced the iPhone 15 Pro, featuring...",
      "author": "John Smith",
      "source": "Tech News Daily",
      "url": "https://technewsdaily.com/apple-iphone-15-pro",
      "published_at": "2025-06-05T10:30:00Z",
      "symbols": ["AAPL"],
      "topics": ["technology", "product_launch"],
      "sentiment": {
        "score": 0.75,
        "label": "positive"
      },
      "entities": [
        {
          "name": "Apple Inc.",
          "type": "organization",
          "sentiment": 0.8
        },
        {
          "name": "iPhone 15 Pro",
          "type": "product",
          "sentiment": 0.9
        }
      ]
    },
    {
      "id": "news_123457",
      "title": "Microsoft Cloud Revenue Surges 35% in Q2",
      "summary": "Microsoft reported strong quarterly results driven by cloud services growth.",
      "content": "Microsoft Corporation (NASDAQ: MSFT) reported financial results for...",
      "author": "Jane Doe",
      "source": "Financial Times",
      "url": "https://ft.com/microsoft-q2-results",
      "published_at": "2025-06-04T14:15:00Z",
      "symbols": ["MSFT"],
      "topics": ["earnings", "cloud_computing"],
      "sentiment": {
        "score": 0.85,
        "label": "positive"
      },
      "entities": [
        {
          "name": "Microsoft Corporation",
          "type": "organization",
          "sentiment": 0.85
        },
        {
          "name": "Azure",
          "type": "product",
          "sentiment": 0.9
        }
      ]
    }
  ],
  "meta": {
    "count": 2,
    "total": 156,
    "limit": 50,
    "offset": 0
  }
}
```

### Get Sentiment

```
GET /alternative/sentiment
```

Retrieves sentiment data for specified symbols.

#### Query Parameters

| Parameter    | Type    | Description                                                          |
| ------------ | ------- | -------------------------------------------------------------------- |
| `symbols`    | string  | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)            |
| `sources`    | string  | Comma-separated list of sources (e.g., `news,social,earnings_calls`) |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                   |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                     |
| `interval`   | string  | Data interval (`1h`, `4h`, `1d`, `1w`)                               |
| `limit`      | integer | Maximum number of data points to return per symbol (default: 100)    |

#### Response

```json
{
  "data": {
    "AAPL": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "sentiment_score": 0.75,
        "sentiment_label": "positive",
        "volume": 1250,
        "sources": {
          "news": 0.78,
          "social": 0.72,
          "earnings_calls": null
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "sentiment_score": 0.65,
        "sentiment_label": "positive",
        "volume": 980,
        "sources": {
          "news": 0.68,
          "social": 0.62,
          "earnings_calls": null
        }
      }
    ],
    "MSFT": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "sentiment_score": 0.85,
        "sentiment_label": "very_positive",
        "volume": 1500,
        "sources": {
          "news": 0.88,
          "social": 0.82,
          "earnings_calls": null
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "sentiment_score": 0.8,
        "sentiment_label": "positive",
        "volume": 1200,
        "sources": {
          "news": 0.82,
          "social": 0.78,
          "earnings_calls": null
        }
      }
    ]
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "start_date": "2025-06-04T00:00:00Z",
    "end_date": "2025-06-05T00:00:00Z",
    "interval": "1d",
    "sources": ["news", "social"]
  }
}
```

### Get Social Media Data

```
GET /alternative/social
```

Retrieves social media data for specified symbols.

#### Query Parameters

| Parameter    | Type    | Description                                                           |
| ------------ | ------- | --------------------------------------------------------------------- |
| `symbols`    | string  | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)             |
| `platforms`  | string  | Comma-separated list of platforms (e.g., `twitter,reddit,stocktwits`) |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                    |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                      |
| `interval`   | string  | Data interval (`1h`, `4h`, `1d`, `1w`)                                |
| `metrics`    | string  | Comma-separated list of metrics (e.g., `volume,sentiment,engagement`) |
| `limit`      | integer | Maximum number of data points to return per symbol (default: 100)     |

#### Response

```json
{
  "data": {
    "AAPL": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "volume": {
          "total": 12500,
          "twitter": 8500,
          "reddit": 3000,
          "stocktwits": 1000
        },
        "sentiment": {
          "score": 0.72,
          "label": "positive",
          "twitter": 0.75,
          "reddit": 0.68,
          "stocktwits": 0.7
        },
        "engagement": {
          "total": 85000,
          "twitter": 60000,
          "reddit": 20000,
          "stocktwits": 5000
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "volume": {
          "total": 10800,
          "twitter": 7500,
          "reddit": 2500,
          "stocktwits": 800
        },
        "sentiment": {
          "score": 0.62,
          "label": "positive",
          "twitter": 0.65,
          "reddit": 0.58,
          "stocktwits": 0.6
        },
        "engagement": {
          "total": 75000,
          "twitter": 52000,
          "reddit": 18000,
          "stocktwits": 5000
        }
      }
    ],
    "MSFT": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "volume": {
          "total": 9500,
          "twitter": 6500,
          "reddit": 2000,
          "stocktwits": 1000
        },
        "sentiment": {
          "score": 0.82,
          "label": "positive",
          "twitter": 0.85,
          "reddit": 0.78,
          "stocktwits": 0.8
        },
        "engagement": {
          "total": 65000,
          "twitter": 45000,
          "reddit": 15000,
          "stocktwits": 5000
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "volume": {
          "total": 8200,
          "twitter": 5500,
          "reddit": 1800,
          "stocktwits": 900
        },
        "sentiment": {
          "score": 0.78,
          "label": "positive",
          "twitter": 0.8,
          "reddit": 0.75,
          "stocktwits": 0.76
        },
        "engagement": {
          "total": 58000,
          "twitter": 40000,
          "reddit": 13000,
          "stocktwits": 5000
        }
      }
    ]
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "start_date": "2025-06-04T00:00:00Z",
    "end_date": "2025-06-05T00:00:00Z",
    "interval": "1d",
    "platforms": ["twitter", "reddit", "stocktwits"],
    "metrics": ["volume", "sentiment", "engagement"]
  }
}
```

### Get Satellite Imagery

```
GET /alternative/satellite
```

Retrieves satellite imagery data for specified locations.

#### Query Parameters

| Parameter    | Type    | Description                                                                    |
| ------------ | ------- | ------------------------------------------------------------------------------ |
| `locations`  | string  | Comma-separated list of location IDs                                           |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                             |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                               |
| `metrics`    | string  | Comma-separated list of metrics (e.g., `car_count,building_count,crop_health`) |
| `limit`      | integer | Maximum number of data points to return per location (default: 10)             |

#### Response

```json
{
  "data": {
    "loc_123456": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "image_url": "https://api.quantumalpha.com/v1/data/alternative/satellite/images/img_123456",
        "metrics": {
          "car_count": 1250,
          "building_count": 45,
          "crop_health": 0.85
        },
        "coordinates": {
          "latitude": 37.7749,
          "longitude": -122.4194
        },
        "resolution": "high",
        "cloud_cover": 0.05
      },
      {
        "timestamp": "2025-05-05T00:00:00Z",
        "image_url": "https://api.quantumalpha.com/v1/data/alternative/satellite/images/img_123457",
        "metrics": {
          "car_count": 1180,
          "building_count": 45,
          "crop_health": 0.82
        },
        "coordinates": {
          "latitude": 37.7749,
          "longitude": -122.4194
        },
        "resolution": "high",
        "cloud_cover": 0.1
      }
    ],
    "loc_789012": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "image_url": "https://api.quantumalpha.com/v1/data/alternative/satellite/images/img_789012",
        "metrics": {
          "car_count": 850,
          "building_count": 30,
          "crop_health": 0.9
        },
        "coordinates": {
          "latitude": 40.7128,
          "longitude": -74.006
        },
        "resolution": "high",
        "cloud_cover": 0.15
      },
      {
        "timestamp": "2025-05-05T00:00:00Z",
        "image_url": "https://api.quantumalpha.com/v1/data/alternative/satellite/images/img_789013",
        "metrics": {
          "car_count": 820,
          "building_count": 30,
          "crop_health": 0.88
        },
        "coordinates": {
          "latitude": 40.7128,
          "longitude": -74.006
        },
        "resolution": "high",
        "cloud_cover": 0.2
      }
    ]
  },
  "meta": {
    "count": 2,
    "locations": ["loc_123456", "loc_789012"],
    "start_date": "2025-05-05T00:00:00Z",
    "end_date": "2025-06-05T00:00:00Z",
    "metrics": ["car_count", "building_count", "crop_health"]
  }
}
```

### Get Web Scraped Data

```
GET /alternative/web-scraped
```

Retrieves web scraped data for specified sources.

#### Query Parameters

| Parameter    | Type    | Description                                                       |
| ------------ | ------- | ----------------------------------------------------------------- |
| `sources`    | string  | Comma-separated list of source IDs                                |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                  |
| `metrics`    | string  | Comma-separated list of metrics                                   |
| `limit`      | integer | Maximum number of data points to return per source (default: 100) |

#### Response

```json
{
  "data": {
    "src_123456": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "url": "https://example.com/products/iphone",
        "metrics": {
          "price": 999.99,
          "inventory": 500,
          "rating": 4.8,
          "review_count": 1250
        },
        "metadata": {
          "source_name": "Example Electronics",
          "product_id": "iphone-15-pro",
          "category": "smartphones"
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "url": "https://example.com/products/iphone",
        "metrics": {
          "price": 999.99,
          "inventory": 450,
          "rating": 4.8,
          "review_count": 1240
        },
        "metadata": {
          "source_name": "Example Electronics",
          "product_id": "iphone-15-pro",
          "category": "smartphones"
        }
      }
    ],
    "src_789012": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "url": "https://example.com/products/surface",
        "metrics": {
          "price": 1299.99,
          "inventory": 350,
          "rating": 4.7,
          "review_count": 980
        },
        "metadata": {
          "source_name": "Example Electronics",
          "product_id": "surface-pro-10",
          "category": "laptops"
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "url": "https://example.com/products/surface",
        "metrics": {
          "price": 1299.99,
          "inventory": 320,
          "rating": 4.7,
          "review_count": 975
        },
        "metadata": {
          "source_name": "Example Electronics",
          "product_id": "surface-pro-10",
          "category": "laptops"
        }
      }
    ]
  },
  "meta": {
    "count": 2,
    "sources": ["src_123456", "src_789012"],
    "start_date": "2025-06-04T00:00:00Z",
    "end_date": "2025-06-05T00:00:00Z",
    "metrics": ["price", "inventory", "rating", "review_count"]
  }
}
```

## Feature Engineering

### List Features

```
GET /features
```

Retrieves a list of available engineered features.

#### Query Parameters

| Parameter     | Type    | Description                                                                |
| ------------- | ------- | -------------------------------------------------------------------------- |
| `category`    | string  | Filter by feature category (e.g., `technical`, `fundamental`, `sentiment`) |
| `asset_class` | string  | Filter by asset class (e.g., `equity`, `forex`, `crypto`)                  |
| `limit`       | integer | Maximum number of features to return (default: 100)                        |
| `offset`      | integer | Number of features to skip (default: 0)                                    |

#### Response

```json
{
  "data": [
    {
      "id": "feature_123456",
      "name": "RSI_14",
      "description": "Relative Strength Index with 14-day lookback period",
      "category": "technical",
      "asset_classes": ["equity", "forex", "crypto"],
      "parameters": {
        "lookback_period": 14
      },
      "created_at": "2025-01-01T00:00:00Z"
    },
    {
      "id": "feature_789012",
      "name": "SMA_50",
      "description": "Simple Moving Average with 50-day lookback period",
      "category": "technical",
      "asset_classes": ["equity", "forex", "crypto"],
      "parameters": {
        "lookback_period": 50
      },
      "created_at": "2025-01-01T00:00:00Z"
    },
    {
      "id": "feature_345678",
      "name": "SENTIMENT_SCORE_NEWS",
      "description": "Sentiment score derived from news articles",
      "category": "sentiment",
      "asset_classes": ["equity"],
      "parameters": {
        "lookback_period": 7,
        "source": "news"
      },
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "count": 3,
    "total": 150,
    "limit": 100,
    "offset": 0
  }
}
```

### Get Feature Values

```
GET /features/values
```

Retrieves values for specified features.

#### Query Parameters

| Parameter    | Type    | Description                                                       |
| ------------ | ------- | ----------------------------------------------------------------- |
| `symbols`    | string  | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`)         |
| `features`   | string  | Comma-separated list of feature IDs                               |
| `start_date` | string  | Start date in ISO 8601 format (e.g., `2025-01-01`)                |
| `end_date`   | string  | End date in ISO 8601 format (e.g., `2025-06-01`)                  |
| `interval`   | string  | Data interval (`1d`, `1w`, `1mo`)                                 |
| `limit`      | integer | Maximum number of data points to return per symbol (default: 100) |

#### Response

```json
{
  "data": {
    "AAPL": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "features": {
          "feature_123456": 65.8,
          "feature_789012": 155.25,
          "feature_345678": 0.75
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "features": {
          "feature_123456": 63.2,
          "feature_789012": 154.8,
          "feature_345678": 0.65
        }
      }
    ],
    "MSFT": [
      {
        "timestamp": "2025-06-05T00:00:00Z",
        "features": {
          "feature_123456": 70.5,
          "feature_789012": 325.5,
          "feature_345678": 0.85
        }
      },
      {
        "timestamp": "2025-06-04T00:00:00Z",
        "features": {
          "feature_123456": 68.7,
          "feature_789012": 324.2,
          "feature_345678": 0.8
        }
      }
    ]
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "features": ["feature_123456", "feature_789012", "feature_345678"],
    "start_date": "2025-06-04T00:00:00Z",
    "end_date": "2025-06-05T00:00:00Z",
    "interval": "1d"
  }
}
```

### Create Custom Feature

```
POST /features/custom
```

Creates a custom feature.

#### Request Body

```json
{
  "name": "CUSTOM_RSI_SENTIMENT",
  "description": "Custom feature combining RSI and sentiment score",
  "formula": "(0.7 * RSI_14 + 0.3 * SENTIMENT_SCORE_NEWS)",
  "dependencies": ["feature_123456", "feature_345678"],
  "parameters": {
    "rsi_weight": 0.7,
    "sentiment_weight": 0.3
  }
}
```

#### Response

```json
{
  "id": "feature_custom_123456",
  "name": "CUSTOM_RSI_SENTIMENT",
  "description": "Custom feature combining RSI and sentiment score",
  "category": "custom",
  "asset_classes": ["equity"],
  "formula": "(0.7 * RSI_14 + 0.3 * SENTIMENT_SCORE_NEWS)",
  "dependencies": ["feature_123456", "feature_345678"],
  "parameters": {
    "rsi_weight": 0.7,
    "sentiment_weight": 0.3
  },
  "created_at": "2025-06-06T11:30:00Z"
}
```

### Get Feature Correlation

```
GET /features/correlation
```

Retrieves correlation between features.

#### Query Parameters

| Parameter    | Type   | Description                                               |
| ------------ | ------ | --------------------------------------------------------- |
| `symbols`    | string | Comma-separated list of symbols (e.g., `AAPL,MSFT,GOOGL`) |
| `features`   | string | Comma-separated list of feature IDs                       |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2025-01-01`)        |
| `end_date`   | string | End date in ISO 8601 format (e.g., `2025-06-01`)          |
| `method`     | string | Correlation method (`pearson`, `spearman`, `kendall`)     |

#### Response

```json
{
  "data": {
    "AAPL": {
      "feature_123456": {
        "feature_123456": 1.0,
        "feature_789012": 0.75,
        "feature_345678": 0.45
      },
      "feature_789012": {
        "feature_123456": 0.75,
        "feature_789012": 1.0,
        "feature_345678": 0.3
      },
      "feature_345678": {
        "feature_123456": 0.45,
        "feature_789012": 0.3,
        "feature_345678": 1.0
      }
    },
    "MSFT": {
      "feature_123456": {
        "feature_123456": 1.0,
        "feature_789012": 0.8,
        "feature_345678": 0.5
      },
      "feature_789012": {
        "feature_123456": 0.8,
        "feature_789012": 1.0,
        "feature_345678": 0.35
      },
      "feature_345678": {
        "feature_123456": 0.5,
        "feature_789012": 0.35,
        "feature_345678": 1.0
      }
    }
  },
  "meta": {
    "count": 2,
    "symbols": ["AAPL", "MSFT"],
    "features": ["feature_123456", "feature_789012", "feature_345678"],
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-06-01T00:00:00Z",
    "method": "pearson"
  }
}
```

## Data Sources

### List Data Sources

```
GET /sources
```

Retrieves a list of available data sources.

#### Query Parameters

| Parameter | Type    | Description                                                          |
| --------- | ------- | -------------------------------------------------------------------- |
| `type`    | string  | Filter by source type (e.g., `market`, `alternative`, `fundamental`) |
| `status`  | string  | Filter by status (`active`, `inactive`, `all`)                       |
| `limit`   | integer | Maximum number of sources to return (default: 100)                   |
| `offset`  | integer | Number of sources to skip (default: 0)                               |

#### Response

```json
{
  "data": [
    {
      "id": "src_123456",
      "name": "Alpha Vantage",
      "type": "market",
      "description": "Real-time and historical market data",
      "status": "active",
      "coverage": {
        "asset_classes": ["equity", "forex", "crypto"],
        "markets": ["US", "Europe", "Asia"],
        "symbols_count": 100000
      },
      "latency": "low",
      "update_frequency": "real-time"
    },
    {
      "id": "src_789012",
      "name": "News API",
      "type": "alternative",
      "description": "Financial news and sentiment data",
      "status": "active",
      "coverage": {
        "asset_classes": ["equity"],
        "markets": ["US", "Europe", "Asia"],
        "symbols_count": 10000
      },
      "latency": "medium",
      "update_frequency": "hourly"
    },
    {
      "id": "src_345678",
      "name": "Satellite Imagery Provider",
      "type": "alternative",
      "description": "Satellite imagery and derived metrics",
      "status": "active",
      "coverage": {
        "asset_classes": ["equity", "commodities"],
        "markets": ["Global"],
        "locations_count": 5000
      },
      "latency": "high",
      "update_frequency": "daily"
    }
  ],
  "meta": {
    "count": 3,
    "total": 25,
    "limit": 100,
    "offset": 0
  }
}
```

### Get Data Source

```
GET /sources/{source_id}
```

Retrieves details for a specific data source.

#### Path Parameters

| Parameter   | Type   | Description               |
| ----------- | ------ | ------------------------- |
| `source_id` | string | The ID of the data source |

#### Response

```json
{
  "id": "src_123456",
  "name": "Alpha Vantage",
  "type": "market",
  "description": "Real-time and historical market data",
  "status": "active",
  "coverage": {
    "asset_classes": ["equity", "forex", "crypto"],
    "markets": ["US", "Europe", "Asia"],
    "symbols_count": 100000
  },
  "data_types": [
    {
      "name": "OHLCV",
      "description": "Open, High, Low, Close, Volume data",
      "intervals": ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1mo"]
    },
    {
      "name": "Quotes",
      "description": "Real-time quotes with bid/ask",
      "intervals": ["real-time"]
    },
    {
      "name": "Trades",
      "description": "Individual trade data",
      "intervals": ["real-time"]
    }
  ],
  "latency": "low",
  "update_frequency": "real-time",
  "historical_data": {
    "available": true,
    "start_date": "1980-01-01"
  },
  "api_documentation": "https://www.alphavantage.co/documentation/",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### Get Source Coverage

```
GET /sources/{source_id}/coverage
```

Retrieves coverage information for a specific data source.

#### Path Parameters

| Parameter   | Type   | Description               |
| ----------- | ------ | ------------------------- |
| `source_id` | string | The ID of the data source |

#### Query Parameters

| Parameter     | Type    | Description                                               |
| ------------- | ------- | --------------------------------------------------------- |
| `asset_class` | string  | Filter by asset class (e.g., `equity`, `forex`, `crypto`) |
| `market`      | string  | Filter by market (e.g., `US`, `Europe`, `Asia`)           |
| `limit`       | integer | Maximum number of symbols to return (default: 100)        |
| `offset`      | integer | Number of symbols to skip (default: 0)                    |

#### Response

```json
{
  "data": {
    "source_id": "src_123456",
    "source_name": "Alpha Vantage",
    "coverage_summary": {
      "asset_classes": ["equity", "forex", "crypto"],
      "markets": ["US", "Europe", "Asia"],
      "symbols_count": 100000
    },
    "symbols": [
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "asset_class": "equity",
        "market": "US",
        "exchange": "NASDAQ",
        "data_types": ["OHLCV", "Quotes", "Trades"],
        "start_date": "1980-12-12"
      },
      {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "asset_class": "equity",
        "market": "US",
        "exchange": "NASDAQ",
        "data_types": ["OHLCV", "Quotes", "Trades"],
        "start_date": "1986-03-13"
      }
    ]
  },
  "meta": {
    "count": 2,
    "total": 100000,
    "limit": 100,
    "offset": 0,
    "filters": {
      "asset_class": null,
      "market": "US"
    }
  }
}
```

## Data Storage

### Get Storage Usage

```
GET /storage/usage
```

Retrieves storage usage information.

#### Response

```json
{
  "data": {
    "total_storage": {
      "allocated": 10000,
      "used": 5000,
      "available": 5000,
      "unit": "GB"
    },
    "by_data_type": {
      "market_data": {
        "used": 3000,
        "percentage": 60
      },
      "alternative_data": {
        "used": 1500,
        "percentage": 30
      },
      "features": {
        "used": 500,
        "percentage": 10
      }
    },
    "by_asset_class": {
      "equity": {
        "used": 3500,
        "percentage": 70
      },
      "forex": {
        "used": 1000,
        "percentage": 20
      },
      "crypto": {
        "used": 500,
        "percentage": 10
      }
    }
  },
  "meta": {
    "timestamp": "2025-06-06T12:00:00Z"
  }
}
```

### Get Data Retention Policy

```
GET /storage/retention-policy
```

Retrieves data retention policy information.

#### Response

```json
{
  "data": {
    "policies": [
      {
        "data_type": "market_data",
        "asset_class": "equity",
        "interval": "1m",
        "retention_period": 30,
        "unit": "days"
      },
      {
        "data_type": "market_data",
        "asset_class": "equity",
        "interval": "1h",
        "retention_period": 365,
        "unit": "days"
      },
      {
        "data_type": "market_data",
        "asset_class": "equity",
        "interval": "1d",
        "retention_period": "unlimited",
        "unit": null
      },
      {
        "data_type": "alternative_data",
        "asset_class": "equity",
        "interval": "1d",
        "retention_period": 730,
        "unit": "days"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-06-06T12:00:00Z"
  }
}
```

## Data Streaming

### Get Streaming Status

```
GET /streaming/status
```

Retrieves the status of data streaming services.

#### Response

```json
{
  "data": {
    "status": "active",
    "connections": 5,
    "max_connections": 10,
    "active_streams": [
      {
        "id": "stream_123456",
        "type": "market_data",
        "symbols": ["AAPL", "MSFT", "GOOGL"],
        "created_at": "2025-06-06T10:00:00Z"
      },
      {
        "id": "stream_789012",
        "type": "alternative_data",
        "sources": ["news", "social"],
        "symbols": ["AAPL", "MSFT"],
        "created_at": "2025-06-06T11:00:00Z"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-06-06T12:00:00Z"
  }
}
```

### Create Streaming Connection

```
POST /streaming/connections
```

Creates a new streaming connection.

#### Request Body

```json
{
  "type": "market_data",
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "data_types": ["quotes", "trades"],
  "callback_url": "https://your-server.com/webhook/market-data"
}
```

#### Response

```json
{
  "connection_id": "stream_123456",
  "type": "market_data",
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "data_types": ["quotes", "trades"],
  "status": "active",
  "created_at": "2025-06-06T12:30:00Z",
  "connection_details": {
    "websocket_url": "wss://api.quantumalpha.com/v1/data/streaming/ws/stream_123456",
    "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "callback_url": "https://your-server.com/webhook/market-data"
  }
}
```

### Delete Streaming Connection

```
DELETE /streaming/connections/{connection_id}
```

Deletes a streaming connection.

#### Path Parameters

| Parameter       | Type   | Description                        |
| --------------- | ------ | ---------------------------------- |
| `connection_id` | string | The ID of the streaming connection |

#### Response

```json
{
  "success": true,
  "message": "Streaming connection deleted successfully",
  "connection_id": "stream_123456"
}
```

## Data Quality

### Get Data Quality Metrics

```
GET /quality/metrics
```

Retrieves data quality metrics.

#### Query Parameters

| Parameter    | Type   | Description                                                   |
| ------------ | ------ | ------------------------------------------------------------- |
| `source_id`  | string | Filter by source ID                                           |
| `data_type`  | string | Filter by data type (e.g., `market_data`, `alternative_data`) |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2025-01-01`)            |
| `end_date`   | string | End date in ISO 8601 format (e.g., `2025-06-01`)              |

#### Response

```json
{
  "data": {
    "overall_quality": 0.98,
    "by_source": [
      {
        "source_id": "src_123456",
        "source_name": "Alpha Vantage",
        "quality_score": 0.99,
        "metrics": {
          "completeness": 0.995,
          "timeliness": 0.99,
          "accuracy": 0.98,
          "consistency": 0.99
        }
      },
      {
        "source_id": "src_789012",
        "source_name": "News API",
        "quality_score": 0.97,
        "metrics": {
          "completeness": 0.96,
          "timeliness": 0.98,
          "accuracy": 0.97,
          "consistency": 0.97
        }
      }
    ],
    "by_data_type": {
      "market_data": {
        "quality_score": 0.99,
        "metrics": {
          "completeness": 0.995,
          "timeliness": 0.99,
          "accuracy": 0.98,
          "consistency": 0.99
        }
      },
      "alternative_data": {
        "quality_score": 0.97,
        "metrics": {
          "completeness": 0.96,
          "timeliness": 0.98,
          "accuracy": 0.97,
          "consistency": 0.97
        }
      }
    },
    "issues": [
      {
        "id": "issue_123456",
        "source_id": "src_789012",
        "source_name": "News API",
        "data_type": "alternative_data",
        "issue_type": "missing_data",
        "description": "Missing news data for AAPL on 2025-06-03",
        "severity": "medium",
        "status": "resolved",
        "created_at": "2025-06-03T10:00:00Z",
        "resolved_at": "2025-06-03T14:00:00Z"
      },
      {
        "id": "issue_789012",
        "source_id": "src_123456",
        "source_name": "Alpha Vantage",
        "data_type": "market_data",
        "issue_type": "delayed_data",
        "description": "Delayed market data for MSFT on 2025-06-04",
        "severity": "low",
        "status": "resolved",
        "created_at": "2025-06-04T10:00:00Z",
        "resolved_at": "2025-06-04T10:30:00Z"
      }
    ]
  },
  "meta": {
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-06-01T00:00:00Z",
    "timestamp": "2025-06-06T12:00:00Z"
  }
}
```

### Report Data Issue

```
POST /quality/issues
```

Reports a data quality issue.

#### Request Body

```json
{
  "source_id": "src_123456",
  "data_type": "market_data",
  "issue_type": "missing_data",
  "description": "Missing market data for AAPL on 2025-06-06",
  "symbols": ["AAPL"],
  "date": "2025-06-06",
  "severity": "high"
}
```

#### Response

```json
{
  "issue_id": "issue_123456",
  "source_id": "src_123456",
  "source_name": "Alpha Vantage",
  "data_type": "market_data",
  "issue_type": "missing_data",
  "description": "Missing market data for AAPL on 2025-06-06",
  "symbols": ["AAPL"],
  "date": "2025-06-06",
  "severity": "high",
  "status": "open",
  "created_at": "2025-06-06T12:30:00Z",
  "estimated_resolution_time": "2025-06-06T14:30:00Z"
}
```

### Get Data Issue Status

```
GET /quality/issues/{issue_id}
```

Retrieves the status of a data quality issue.

#### Path Parameters

| Parameter  | Type   | Description                      |
| ---------- | ------ | -------------------------------- |
| `issue_id` | string | The ID of the data quality issue |

#### Response

```json
{
  "issue_id": "issue_123456",
  "source_id": "src_123456",
  "source_name": "Alpha Vantage",
  "data_type": "market_data",
  "issue_type": "missing_data",
  "description": "Missing market data for AAPL on 2025-06-06",
  "symbols": ["AAPL"],
  "date": "2025-06-06",
  "severity": "high",
  "status": "in_progress",
  "created_at": "2025-06-06T12:30:00Z",
  "updated_at": "2025-06-06T13:00:00Z",
  "estimated_resolution_time": "2025-06-06T14:30:00Z",
  "resolution_steps": [
    {
      "timestamp": "2025-06-06T13:00:00Z",
      "description": "Issue identified and assigned to data engineering team"
    }
  ]
}
```
