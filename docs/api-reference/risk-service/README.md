# Risk Service API Reference

The Risk Service API provides tools for risk modeling, analysis, and management within the QuantumAlpha platform.

## Table of Contents

1. [Overview](#overview)
2. [Risk Models](#risk-models)
3. [Portfolio Risk](#portfolio-risk)
4. [Scenario Analysis](#scenario-analysis)
5. [Stress Testing](#stress-testing)
6. [Risk Attribution](#risk-attribution)
7. [Limits Management](#limits-management)
8. [Compliance](#compliance)

## Overview

The Risk Service API allows you to:

- Manage and configure risk models
- Calculate portfolio risk metrics (VaR, CVaR, etc.)
- Perform scenario analysis and stress testing
- Analyze risk attribution
- Define and monitor risk limits
- Ensure compliance with regulatory requirements

Base URL: `https://api.quantumalpha.com/v1/risk`

## Risk Models

### List Risk Models

```
GET /models
```

Retrieves a list of all configured risk models.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by model type (e.g., `var`, `cvar`, `factor_model`) |
| `asset_class` | string | Filter by asset class (e.g., `equity`, `fixed_income`, `multi_asset`) |
| `status` | string | Filter by model status (e.g., `active`, `inactive`, `calibrating`) |
| `limit` | integer | Maximum number of models to return (default: 100) |
| `offset` | integer | Number of models to skip (default: 0) |

#### Response

```json
{
  "models": [
    {
      "id": "model_123456",
      "name": "Equity VaR - Historical Simulation",
      "type": "var",
      "asset_class": "equity",
      "description": "Value at Risk model using historical simulation for equity portfolios.",
      "status": "active",
      "parameters": {
        "confidence_level": 0.99,
        "holding_period": 1,
        "lookback_window": 252
      },
      "created_at": "2025-04-01T10:00:00Z",
      "updated_at": "2025-04-15T14:30:00Z"
    },
    {
      "id": "model_789012",
      "name": "Fixed Income CVaR - Monte Carlo",
      "type": "cvar",
      "asset_class": "fixed_income",
      "description": "Conditional Value at Risk model using Monte Carlo simulation for fixed income portfolios.",
      "status": "active",
      "parameters": {
        "confidence_level": 0.975,
        "holding_period": 5,
        "simulations": 10000,
        "interest_rate_model": "vasicek"
      },
      "created_at": "2025-03-10T09:00:00Z",
      "updated_at": "2025-03-20T11:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Risk Model

```
GET /models/{model_id}
```

Retrieves a specific risk model by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model to retrieve |

#### Response

```json
{
  "id": "model_123456",
  "name": "Equity VaR - Historical Simulation",
  "type": "var",
  "asset_class": "equity",
  "description": "Value at Risk model using historical simulation for equity portfolios.",
  "status": "active",
  "parameters": {
    "confidence_level": 0.99,
    "holding_period": 1,
    "lookback_window": 252,
    "weighting_scheme": "equal"
  },
  "calibration_details": {
    "last_calibrated_at": "2025-06-01T08:00:00Z",
    "calibration_status": "completed",
    "calibration_frequency": "daily",
    "next_calibration_at": "2025-06-07T08:00:00Z"
  },
  "validation_details": {
    "last_validated_at": "2025-05-15T10:00:00Z",
    "validation_status": "passed",
    "validation_metrics": {
      "backtesting_exceptions": 2,
      "kupiec_pof_test_p_value": 0.15
    }
  },
  "created_at": "2025-04-01T10:00:00Z",
  "updated_at": "2025-04-15T14:30:00Z"
}
```

### Create Risk Model

```
POST /models
```

Creates a new risk model.

#### Request Body

```json
{
  "name": "Multi-Asset Factor Model",
  "type": "factor_model",
  "asset_class": "multi_asset",
  "description": "Factor model for multi-asset portfolios incorporating macroeconomic and style factors.",
  "parameters": {
    "factors": ["market", "size", "value", "momentum", "interest_rate", "inflation"],
    "covariance_matrix_estimation": "ewma",
    "ewma_lambda": 0.94
  },
  "calibration_frequency": "weekly"
}
```

#### Response

```json
{
  "id": "model_345678",
  "name": "Multi-Asset Factor Model",
  "type": "factor_model",
  "asset_class": "multi_asset",
  "description": "Factor model for multi-asset portfolios incorporating macroeconomic and style factors.",
  "status": "calibrating",
  "parameters": {
    "factors": ["market", "size", "value", "momentum", "interest_rate", "inflation"],
    "covariance_matrix_estimation": "ewma",
    "ewma_lambda": 0.94
  },
  "created_at": "2025-06-06T14:00:00Z",
  "updated_at": "2025-06-06T14:00:00Z"
}
```

### Update Risk Model

```
PUT /models/{model_id}
```

Updates an existing risk model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model to update |

#### Request Body

```json
{
  "description": "Updated Factor model for multi-asset portfolios with revised factor set.",
  "parameters": {
    "factors": ["market", "size", "value", "momentum", "interest_rate", "inflation", "credit_spread"],
    "covariance_matrix_estimation": "ewma",
    "ewma_lambda": 0.97
  },
  "calibration_frequency": "daily"
}
```

#### Response

```json
{
  "id": "model_345678",
  "name": "Multi-Asset Factor Model",
  "type": "factor_model",
  "asset_class": "multi_asset",
  "description": "Updated Factor model for multi-asset portfolios with revised factor set.",
  "status": "calibrating",
  "parameters": {
    "factors": ["market", "size", "value", "momentum", "interest_rate", "inflation", "credit_spread"],
    "covariance_matrix_estimation": "ewma",
    "ewma_lambda": 0.97
  },
  "created_at": "2025-06-06T14:00:00Z",
  "updated_at": "2025-06-06T14:05:00Z"
}
```

### Delete Risk Model

```
DELETE /models/{model_id}
```

Deletes a risk model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model to delete |

#### Response

```json
{
  "success": true,
  "message": "Risk model deleted successfully"
}
```

### Calibrate Risk Model

```
POST /models/{model_id}/calibrate
```

Triggers a manual calibration for a risk model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model to calibrate |

#### Request Body

```json
{
  "calibration_date": "2025-06-06",
  "data_sources": ["source_market_data_1", "source_macro_data_1"]
}
```

#### Response

```json
{
  "job_id": "calib_job_123456",
  "model_id": "model_345678",
  "status": "queued",
  "created_at": "2025-06-06T14:10:00Z"
}
```

### Get Model Calibration Status

```
GET /models/{model_id}/calibrate/{job_id}
```

Retrieves the status of a risk model calibration job.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model |
| `job_id` | string | The ID of the calibration job |

#### Response

```json
{
  "job_id": "calib_job_123456",
  "model_id": "model_345678",
  "status": "running",
  "created_at": "2025-06-06T14:10:00Z",
  "started_at": "2025-06-06T14:11:00Z",
  "progress": {
    "current_step": "Estimating factor covariances",
    "percentage": 60.0
  }
}
```

### Validate Risk Model

```
POST /models/{model_id}/validate
```

Triggers a validation process for a risk model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model to validate |

#### Request Body

```json
{
  "validation_period_start": "2024-01-01",
  "validation_period_end": "2024-12-31",
  "validation_tests": ["backtesting_var", "stress_tests_historical"]
}
```

#### Response

```json
{
  "job_id": "valid_job_123456",
  "model_id": "model_123456",
  "status": "queued",
  "created_at": "2025-06-06T14:15:00Z"
}
```

### Get Model Validation Results

```
GET /models/{model_id}/validate/{job_id}
```

Retrieves the results of a risk model validation job.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the risk model |
| `job_id` | string | The ID of the validation job |

#### Response

```json
{
  "job_id": "valid_job_123456",
  "model_id": "model_123456",
  "status": "completed",
  "created_at": "2025-06-06T14:15:00Z",
  "completed_at": "2025-06-06T14:45:00Z",
  "validation_summary": {
    "overall_status": "passed",
    "tests_performed": 2,
    "tests_passed": 2,
    "tests_failed": 0
  },
  "validation_details": [
    {
      "test_name": "backtesting_var",
      "status": "passed",
      "metrics": {
        "confidence_level": 0.99,
        "exceptions": 2,
        "expected_exceptions": 2.52,
        "kupiec_pof_p_value": 0.18,
        "christoffersen_test_p_value": 0.25
      }
    },
    {
      "test_name": "stress_tests_historical",
      "status": "passed",
      "metrics": {
        "scenario_count": 5,
        "max_drawdown_observed": -0.15,
        "max_drawdown_predicted": -0.18
      }
    }
  ]
}
```


## Portfolio Risk

### Calculate Portfolio Risk

```
POST /portfolio/risk
```

Calculates risk metrics for a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "risk_models": [
    {
      "model_id": "model_123456",
      "parameters": {
        "confidence_level": 0.99,
        "holding_period": 1
      }
    },
    {
      "model_id": "model_789012",
      "parameters": {
        "confidence_level": 0.975,
        "holding_period": 5
      }
    }
  ],
  "calculation_date": "2025-06-06",
  "include_position_level_metrics": true
}
```

#### Response

```json
{
  "calculation_id": "calc_123456",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "portfolio_risk_metrics": {
    "model_123456": {
      "var": {
        "value": 37500.00,
        "percentage": 0.03,
        "confidence_level": 0.99,
        "holding_period": 1
      },
      "cvar": {
        "value": 45000.00,
        "percentage": 0.036,
        "confidence_level": 0.99,
        "holding_period": 1
      },
      "volatility": {
        "value": 0.18,
        "annualized": true
      },
      "beta": 1.05,
      "sharpe_ratio": 1.2,
      "sortino_ratio": 1.5,
      "max_drawdown": {
        "value": 0.25,
        "start_date": "2025-03-15",
        "end_date": "2025-03-25"
      }
    },
    "model_789012": {
      "var": {
        "value": 87500.00,
        "percentage": 0.07,
        "confidence_level": 0.975,
        "holding_period": 5
      },
      "cvar": {
        "value": 100000.00,
        "percentage": 0.08,
        "confidence_level": 0.975,
        "holding_period": 5
      }
    }
  },
  "position_risk_metrics": {
    "AAPL": {
      "model_123456": {
        "var_contribution": {
          "value": 15000.00,
          "percentage": 0.04,
          "contribution_percentage": 0.4
        },
        "volatility": 0.22,
        "beta": 1.1
      }
    },
    "MSFT": {
      "model_123456": {
        "var_contribution": {
          "value": 12000.00,
          "percentage": 0.03,
          "contribution_percentage": 0.32
        },
        "volatility": 0.20,
        "beta": 1.05
      }
    },
    "GOOGL": {
      "model_123456": {
        "var_contribution": {
          "value": 7500.00,
          "percentage": 0.025,
          "contribution_percentage": 0.2
        },
        "volatility": 0.25,
        "beta": 1.15
      }
    },
    "TLT": {
      "model_123456": {
        "var_contribution": {
          "value": 3000.00,
          "percentage": 0.015,
          "contribution_percentage": 0.08
        },
        "volatility": 0.10,
        "beta": -0.2
      }
    }
  }
}
```

### Get Historical Portfolio Risk

```
GET /portfolio/risk/history
```

Retrieves historical risk metrics for a portfolio.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | The ID of the portfolio |
| `model_id` | string | The ID of the risk model |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2025-01-01`) |
| `end_date` | string | End date in ISO 8601 format (e.g., `2025-06-01`) |
| `metrics` | string | Comma-separated list of metrics (e.g., `var,cvar,volatility`) |
| `interval` | string | Data interval (`1d`, `1w`, `1mo`) |

#### Response

```json
{
  "portfolio_id": "portfolio_123456",
  "model_id": "model_123456",
  "data": [
    {
      "date": "2025-06-01",
      "portfolio_value": 1250000.00,
      "metrics": {
        "var": {
          "value": 37500.00,
          "percentage": 0.03
        },
        "cvar": {
          "value": 45000.00,
          "percentage": 0.036
        },
        "volatility": 0.18
      }
    },
    {
      "date": "2025-05-01",
      "portfolio_value": 1200000.00,
      "metrics": {
        "var": {
          "value": 36000.00,
          "percentage": 0.03
        },
        "cvar": {
          "value": 43200.00,
          "percentage": 0.036
        },
        "volatility": 0.17
      }
    },
    {
      "date": "2025-04-01",
      "portfolio_value": 1180000.00,
      "metrics": {
        "var": {
          "value": 35400.00,
          "percentage": 0.03
        },
        "cvar": {
          "value": 42480.00,
          "percentage": 0.036
        },
        "volatility": 0.16
      }
    }
  ],
  "meta": {
    "start_date": "2025-04-01",
    "end_date": "2025-06-01",
    "interval": "1mo",
    "metrics": ["var", "cvar", "volatility"]
  }
}
```

### Calculate Risk Decomposition

```
POST /portfolio/risk/decomposition
```

Calculates risk decomposition for a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "model_id": "model_345678",
  "decomposition_type": "factor",
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "calculation_id": "calc_789012",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "model_id": "model_345678",
  "decomposition_type": "factor",
  "total_risk": {
    "volatility": 0.18,
    "var": {
      "value": 37500.00,
      "percentage": 0.03
    }
  },
  "factor_contributions": [
    {
      "factor": "market",
      "volatility_contribution": 0.12,
      "volatility_contribution_percentage": 0.667,
      "var_contribution": {
        "value": 25000.00,
        "percentage": 0.02,
        "contribution_percentage": 0.667
      }
    },
    {
      "factor": "size",
      "volatility_contribution": 0.02,
      "volatility_contribution_percentage": 0.111,
      "var_contribution": {
        "value": 4166.67,
        "percentage": 0.0033,
        "contribution_percentage": 0.111
      }
    },
    {
      "factor": "value",
      "volatility_contribution": 0.01,
      "volatility_contribution_percentage": 0.056,
      "var_contribution": {
        "value": 2083.33,
        "percentage": 0.0017,
        "contribution_percentage": 0.056
      }
    },
    {
      "factor": "momentum",
      "volatility_contribution": 0.015,
      "volatility_contribution_percentage": 0.083,
      "var_contribution": {
        "value": 3125.00,
        "percentage": 0.0025,
        "contribution_percentage": 0.083
      }
    },
    {
      "factor": "interest_rate",
      "volatility_contribution": 0.01,
      "volatility_contribution_percentage": 0.056,
      "var_contribution": {
        "value": 2083.33,
        "percentage": 0.0017,
        "contribution_percentage": 0.056
      }
    },
    {
      "factor": "inflation",
      "volatility_contribution": 0.005,
      "volatility_contribution_percentage": 0.028,
      "var_contribution": {
        "value": 1041.67,
        "percentage": 0.0008,
        "contribution_percentage": 0.028
      }
    }
  ],
  "position_contributions": {
    "AAPL": {
      "volatility_contribution": 0.072,
      "volatility_contribution_percentage": 0.4,
      "var_contribution": {
        "value": 15000.00,
        "percentage": 0.012,
        "contribution_percentage": 0.4
      },
      "factor_exposures": {
        "market": 1.1,
        "size": -0.2,
        "value": 0.3,
        "momentum": 0.5,
        "interest_rate": 0.1,
        "inflation": 0.2
      }
    },
    "MSFT": {
      "volatility_contribution": 0.054,
      "volatility_contribution_percentage": 0.3,
      "var_contribution": {
        "value": 11250.00,
        "percentage": 0.009,
        "contribution_percentage": 0.3
      },
      "factor_exposures": {
        "market": 1.05,
        "size": -0.3,
        "value": 0.1,
        "momentum": 0.6,
        "interest_rate": 0.15,
        "inflation": 0.1
      }
    },
    "GOOGL": {
      "volatility_contribution": 0.036,
      "volatility_contribution_percentage": 0.2,
      "var_contribution": {
        "value": 7500.00,
        "percentage": 0.006,
        "contribution_percentage": 0.2
      },
      "factor_exposures": {
        "market": 1.15,
        "size": -0.1,
        "value": 0.2,
        "momentum": 0.4,
        "interest_rate": 0.05,
        "inflation": 0.15
      }
    },
    "TLT": {
      "volatility_contribution": 0.018,
      "volatility_contribution_percentage": 0.1,
      "var_contribution": {
        "value": 3750.00,
        "percentage": 0.003,
        "contribution_percentage": 0.1
      },
      "factor_exposures": {
        "market": -0.2,
        "size": 0.0,
        "value": 0.0,
        "momentum": 0.1,
        "interest_rate": 0.9,
        "inflation": 0.5
      }
    }
  }
}
```

### Calculate Portfolio Correlation

```
POST /portfolio/correlation
```

Calculates correlation between portfolios or assets.

#### Request Body

```json
{
  "portfolios": [
    {
      "id": "portfolio_123456",
      "name": "Portfolio A"
    },
    {
      "id": "portfolio_789012",
      "name": "Portfolio B"
    }
  ],
  "assets": [
    "SPY",
    "AGG",
    "GLD"
  ],
  "start_date": "2025-01-01",
  "end_date": "2025-06-01",
  "frequency": "daily",
  "method": "pearson"
}
```

#### Response

```json
{
  "calculation_id": "calc_345678",
  "correlation_matrix": {
    "portfolio_123456": {
      "portfolio_123456": 1.0,
      "portfolio_789012": 0.75,
      "SPY": 0.85,
      "AGG": 0.25,
      "GLD": 0.15
    },
    "portfolio_789012": {
      "portfolio_123456": 0.75,
      "portfolio_789012": 1.0,
      "SPY": 0.65,
      "AGG": 0.45,
      "GLD": 0.20
    },
    "SPY": {
      "portfolio_123456": 0.85,
      "portfolio_789012": 0.65,
      "SPY": 1.0,
      "AGG": 0.10,
      "GLD": 0.05
    },
    "AGG": {
      "portfolio_123456": 0.25,
      "portfolio_789012": 0.45,
      "SPY": 0.10,
      "AGG": 1.0,
      "GLD": 0.30
    },
    "GLD": {
      "portfolio_123456": 0.15,
      "portfolio_789012": 0.20,
      "SPY": 0.05,
      "AGG": 0.30,
      "GLD": 1.0
    }
  },
  "meta": {
    "start_date": "2025-01-01",
    "end_date": "2025-06-01",
    "frequency": "daily",
    "method": "pearson",
    "items_count": 5
  }
}
```

### Calculate Portfolio Sensitivity

```
POST /portfolio/sensitivity
```

Calculates portfolio sensitivity to various risk factors.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "risk_factors": [
    {
      "name": "equity_market",
      "shocks": [-0.1, -0.05, 0.05, 0.1]
    },
    {
      "name": "interest_rate",
      "shocks": [-0.01, -0.005, 0.005, 0.01]
    },
    {
      "name": "credit_spread",
      "shocks": [-0.005, -0.0025, 0.0025, 0.005]
    },
    {
      "name": "usd_exchange_rate",
      "shocks": [-0.05, -0.025, 0.025, 0.05]
    }
  ],
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "calculation_id": "calc_456789",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "sensitivities": {
    "equity_market": {
      "shocks": [-0.1, -0.05, 0.05, 0.1],
      "pnl": [-125000.00, -62500.00, 62500.00, 125000.00],
      "pnl_percentage": [-0.1, -0.05, 0.05, 0.1],
      "beta": 1.0
    },
    "interest_rate": {
      "shocks": [-0.01, -0.005, 0.005, 0.01],
      "pnl": [12500.00, 6250.00, -6250.00, -12500.00],
      "pnl_percentage": [0.01, 0.005, -0.005, -0.01],
      "duration": -1.0
    },
    "credit_spread": {
      "shocks": [-0.005, -0.0025, 0.0025, 0.005],
      "pnl": [6250.00, 3125.00, -3125.00, -6250.00],
      "pnl_percentage": [0.005, 0.0025, -0.0025, -0.005],
      "spread_duration": -1.0
    },
    "usd_exchange_rate": {
      "shocks": [-0.05, -0.025, 0.025, 0.05],
      "pnl": [-12500.00, -6250.00, 6250.00, 12500.00],
      "pnl_percentage": [-0.01, -0.005, 0.005, 0.01],
      "fx_exposure": 0.2
    }
  },
  "position_sensitivities": {
    "AAPL": {
      "equity_market": {
        "beta": 1.1,
        "pnl_percentage": [-0.11, -0.055, 0.055, 0.11]
      },
      "interest_rate": {
        "duration": -0.5,
        "pnl_percentage": [0.005, 0.0025, -0.0025, -0.005]
      },
      "credit_spread": {
        "spread_duration": -0.2,
        "pnl_percentage": [0.001, 0.0005, -0.0005, -0.001]
      },
      "usd_exchange_rate": {
        "fx_exposure": 0.15,
        "pnl_percentage": [-0.0075, -0.00375, 0.00375, 0.0075]
      }
    },
    "MSFT": {
      "equity_market": {
        "beta": 1.05,
        "pnl_percentage": [-0.105, -0.0525, 0.0525, 0.105]
      },
      "interest_rate": {
        "duration": -0.4,
        "pnl_percentage": [0.004, 0.002, -0.002, -0.004]
      },
      "credit_spread": {
        "spread_duration": -0.15,
        "pnl_percentage": [0.00075, 0.000375, -0.000375, -0.00075]
      },
      "usd_exchange_rate": {
        "fx_exposure": 0.25,
        "pnl_percentage": [-0.0125, -0.00625, 0.00625, 0.0125]
      }
    },
    "GOOGL": {
      "equity_market": {
        "beta": 1.15,
        "pnl_percentage": [-0.115, -0.0575, 0.0575, 0.115]
      },
      "interest_rate": {
        "duration": -0.3,
        "pnl_percentage": [0.003, 0.0015, -0.0015, -0.003]
      },
      "credit_spread": {
        "spread_duration": -0.1,
        "pnl_percentage": [0.0005, 0.00025, -0.00025, -0.0005]
      },
      "usd_exchange_rate": {
        "fx_exposure": 0.2,
        "pnl_percentage": [-0.01, -0.005, 0.005, 0.01]
      }
    },
    "TLT": {
      "equity_market": {
        "beta": -0.2,
        "pnl_percentage": [0.02, 0.01, -0.01, -0.02]
      },
      "interest_rate": {
        "duration": -7.5,
        "pnl_percentage": [0.075, 0.0375, -0.0375, -0.075]
      },
      "credit_spread": {
        "spread_duration": -7.0,
        "pnl_percentage": [0.035, 0.0175, -0.0175, -0.035]
      },
      "usd_exchange_rate": {
        "fx_exposure": 0.05,
        "pnl_percentage": [-0.0025, -0.00125, 0.00125, 0.0025]
      }
    }
  }
}
```

### Calculate Portfolio Liquidity Risk

```
POST /portfolio/liquidity-risk
```

Calculates liquidity risk metrics for a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "ILLIQUID_CORP_BOND",
        "quantity": 500000,
        "asset_class": "fixed_income"
      }
    ]
  },
  "liquidation_scenarios": [
    {
      "name": "normal",
      "market_impact_factor": 1.0,
      "daily_volume_percentage": 0.1
    },
    {
      "name": "stressed",
      "market_impact_factor": 2.0,
      "daily_volume_percentage": 0.05
    },
    {
      "name": "crisis",
      "market_impact_factor": 5.0,
      "daily_volume_percentage": 0.02
    }
  ],
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "calculation_id": "calc_567890",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "portfolio_liquidity_metrics": {
    "normal": {
      "time_to_liquidate": {
        "days_50_percent": 1,
        "days_90_percent": 2,
        "days_100_percent": 10
      },
      "liquidation_cost": {
        "value": 6250.00,
        "percentage": 0.005
      },
      "liquidity_score": 0.9
    },
    "stressed": {
      "time_to_liquidate": {
        "days_50_percent": 2,
        "days_90_percent": 5,
        "days_100_percent": 20
      },
      "liquidation_cost": {
        "value": 18750.00,
        "percentage": 0.015
      },
      "liquidity_score": 0.75
    },
    "crisis": {
      "time_to_liquidate": {
        "days_50_percent": 5,
        "days_90_percent": 15,
        "days_100_percent": 50
      },
      "liquidation_cost": {
        "value": 62500.00,
        "percentage": 0.05
      },
      "liquidity_score": 0.5
    }
  },
  "position_liquidity_metrics": {
    "AAPL": {
      "normal": {
        "time_to_liquidate_days": 1,
        "liquidation_cost_percentage": 0.002,
        "average_daily_volume": 80000000,
        "position_to_adv_ratio": 0.0000125
      },
      "stressed": {
        "time_to_liquidate_days": 2,
        "liquidation_cost_percentage": 0.005,
        "average_daily_volume": 40000000,
        "position_to_adv_ratio": 0.000025
      },
      "crisis": {
        "time_to_liquidate_days": 5,
        "liquidation_cost_percentage": 0.015,
        "average_daily_volume": 16000000,
        "position_to_adv_ratio": 0.0000625
      }
    },
    "MSFT": {
      "normal": {
        "time_to_liquidate_days": 1,
        "liquidation_cost_percentage": 0.002,
        "average_daily_volume": 60000000,
        "position_to_adv_ratio": 0.0000133
      },
      "stressed": {
        "time_to_liquidate_days": 2,
        "liquidation_cost_percentage": 0.005,
        "average_daily_volume": 30000000,
        "position_to_adv_ratio": 0.0000267
      },
      "crisis": {
        "time_to_liquidate_days": 5,
        "liquidation_cost_percentage": 0.015,
        "average_daily_volume": 12000000,
        "position_to_adv_ratio": 0.0000667
      }
    },
    "GOOGL": {
      "normal": {
        "time_to_liquidate_days": 1,
        "liquidation_cost_percentage": 0.003,
        "average_daily_volume": 20000000,
        "position_to_adv_ratio": 0.00001
      },
      "stressed": {
        "time_to_liquidate_days": 2,
        "liquidation_cost_percentage": 0.007,
        "average_daily_volume": 10000000,
        "position_to_adv_ratio": 0.00002
      },
      "crisis": {
        "time_to_liquidate_days": 5,
        "liquidation_cost_percentage": 0.02,
        "average_daily_volume": 4000000,
        "position_to_adv_ratio": 0.00005
      }
    },
    "ILLIQUID_CORP_BOND": {
      "normal": {
        "time_to_liquidate_days": 10,
        "liquidation_cost_percentage": 0.02,
        "average_daily_volume": 5000000,
        "position_to_adv_ratio": 0.1
      },
      "stressed": {
        "time_to_liquidate_days": 20,
        "liquidation_cost_percentage": 0.05,
        "average_daily_volume": 2500000,
        "position_to_adv_ratio": 0.2
      },
      "crisis": {
        "time_to_liquidate_days": 50,
        "liquidation_cost_percentage": 0.15,
        "average_daily_volume": 1000000,
        "position_to_adv_ratio": 0.5
      }
    }
  }
}
```


## Scenario Analysis

### List Scenarios

```
GET /scenarios
```

Retrieves a list of all available scenarios.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by scenario type (e.g., `historical`, `hypothetical`, `monte_carlo`) |
| `category` | string | Filter by scenario category (e.g., `market_crash`, `interest_rate_shock`, `geopolitical`) |
| `limit` | integer | Maximum number of scenarios to return (default: 100) |
| `offset` | integer | Number of scenarios to skip (default: 0) |

#### Response

```json
{
  "scenarios": [
    {
      "id": "scenario_123456",
      "name": "2008 Financial Crisis",
      "type": "historical",
      "category": "market_crash",
      "description": "Scenario based on market movements during the 2008 financial crisis.",
      "time_period": {
        "start_date": "2008-09-01",
        "end_date": "2009-03-31"
      },
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    },
    {
      "id": "scenario_789012",
      "name": "Fed Rate Hike 100bps",
      "type": "hypothetical",
      "category": "interest_rate_shock",
      "description": "Hypothetical scenario with a sudden 100 basis point increase in Federal Reserve interest rates.",
      "created_at": "2025-02-10T14:30:00Z",
      "updated_at": "2025-02-10T14:30:00Z"
    },
    {
      "id": "scenario_345678",
      "name": "Market Volatility Spike",
      "type": "monte_carlo",
      "category": "volatility_shock",
      "description": "Monte Carlo simulation of a sudden spike in market volatility.",
      "created_at": "2025-03-05T09:15:00Z",
      "updated_at": "2025-03-05T09:15:00Z"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0
}
```

### Get Scenario

```
GET /scenarios/{scenario_id}
```

Retrieves a specific scenario by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `scenario_id` | string | The ID of the scenario to retrieve |

#### Response

```json
{
  "id": "scenario_123456",
  "name": "2008 Financial Crisis",
  "type": "historical",
  "category": "market_crash",
  "description": "Scenario based on market movements during the 2008 financial crisis.",
  "time_period": {
    "start_date": "2008-09-01",
    "end_date": "2009-03-31"
  },
  "market_shocks": [
    {
      "factor": "equity_market",
      "value": -0.55
    },
    {
      "factor": "credit_spread_investment_grade",
      "value": 0.02
    },
    {
      "factor": "credit_spread_high_yield",
      "value": 0.08
    },
    {
      "factor": "interest_rate_10y",
      "value": -0.015
    },
    {
      "factor": "vix",
      "value": 0.8
    }
  ],
  "asset_class_impacts": {
    "equity": {
      "us_large_cap": -0.55,
      "us_small_cap": -0.60,
      "europe": -0.50,
      "japan": -0.45,
      "emerging_markets": -0.65
    },
    "fixed_income": {
      "us_treasury": 0.05,
      "us_corporate_investment_grade": -0.10,
      "us_corporate_high_yield": -0.35,
      "emerging_market_debt": -0.30
    },
    "alternatives": {
      "real_estate": -0.40,
      "commodities": -0.50,
      "hedge_funds": -0.20
    }
  },
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

### Create Scenario

```
POST /scenarios
```

Creates a new scenario.

#### Request Body

```json
{
  "name": "Global Trade War Escalation",
  "type": "hypothetical",
  "category": "geopolitical",
  "description": "Hypothetical scenario modeling the impact of a severe escalation in global trade tensions.",
  "market_shocks": [
    {
      "factor": "equity_market",
      "value": -0.25
    },
    {
      "factor": "credit_spread_investment_grade",
      "value": 0.01
    },
    {
      "factor": "credit_spread_high_yield",
      "value": 0.03
    },
    {
      "factor": "interest_rate_10y",
      "value": -0.005
    },
    {
      "factor": "vix",
      "value": 0.5
    }
  ],
  "asset_class_impacts": {
    "equity": {
      "us_large_cap": -0.25,
      "us_small_cap": -0.30,
      "europe": -0.28,
      "japan": -0.26,
      "emerging_markets": -0.35
    },
    "fixed_income": {
      "us_treasury": 0.02,
      "us_corporate_investment_grade": -0.05,
      "us_corporate_high_yield": -0.15,
      "emerging_market_debt": -0.20
    },
    "alternatives": {
      "real_estate": -0.10,
      "commodities": -0.20,
      "hedge_funds": -0.08
    }
  }
}
```

#### Response

```json
{
  "id": "scenario_901234",
  "name": "Global Trade War Escalation",
  "type": "hypothetical",
  "category": "geopolitical",
  "description": "Hypothetical scenario modeling the impact of a severe escalation in global trade tensions.",
  "market_shocks": [
    {
      "factor": "equity_market",
      "value": -0.25
    },
    {
      "factor": "credit_spread_investment_grade",
      "value": 0.01
    },
    {
      "factor": "credit_spread_high_yield",
      "value": 0.03
    },
    {
      "factor": "interest_rate_10y",
      "value": -0.005
    },
    {
      "factor": "vix",
      "value": 0.5
    }
  ],
  "asset_class_impacts": {
    "equity": {
      "us_large_cap": -0.25,
      "us_small_cap": -0.30,
      "europe": -0.28,
      "japan": -0.26,
      "emerging_markets": -0.35
    },
    "fixed_income": {
      "us_treasury": 0.02,
      "us_corporate_investment_grade": -0.05,
      "us_corporate_high_yield": -0.15,
      "emerging_market_debt": -0.20
    },
    "alternatives": {
      "real_estate": -0.10,
      "commodities": -0.20,
      "hedge_funds": -0.08
    }
  },
  "created_at": "2025-06-06T15:00:00Z",
  "updated_at": "2025-06-06T15:00:00Z"
}
```

### Update Scenario

```
PUT /scenarios/{scenario_id}
```

Updates an existing scenario.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `scenario_id` | string | The ID of the scenario to update |

#### Request Body

```json
{
  "name": "Global Trade War Escalation (Updated)",
  "description": "Updated hypothetical scenario modeling the impact of a severe escalation in global trade tensions.",
  "market_shocks": [
    {
      "factor": "equity_market",
      "value": -0.30
    },
    {
      "factor": "credit_spread_investment_grade",
      "value": 0.015
    },
    {
      "factor": "credit_spread_high_yield",
      "value": 0.04
    },
    {
      "factor": "interest_rate_10y",
      "value": -0.008
    },
    {
      "factor": "vix",
      "value": 0.6
    }
  ],
  "asset_class_impacts": {
    "equity": {
      "us_large_cap": -0.30,
      "us_small_cap": -0.35,
      "europe": -0.32,
      "japan": -0.28,
      "emerging_markets": -0.40
    },
    "fixed_income": {
      "us_treasury": 0.03,
      "us_corporate_investment_grade": -0.08,
      "us_corporate_high_yield": -0.20,
      "emerging_market_debt": -0.25
    },
    "alternatives": {
      "real_estate": -0.15,
      "commodities": -0.25,
      "hedge_funds": -0.10
    }
  }
}
```

#### Response

```json
{
  "id": "scenario_901234",
  "name": "Global Trade War Escalation (Updated)",
  "type": "hypothetical",
  "category": "geopolitical",
  "description": "Updated hypothetical scenario modeling the impact of a severe escalation in global trade tensions.",
  "market_shocks": [
    {
      "factor": "equity_market",
      "value": -0.30
    },
    {
      "factor": "credit_spread_investment_grade",
      "value": 0.015
    },
    {
      "factor": "credit_spread_high_yield",
      "value": 0.04
    },
    {
      "factor": "interest_rate_10y",
      "value": -0.008
    },
    {
      "factor": "vix",
      "value": 0.6
    }
  ],
  "asset_class_impacts": {
    "equity": {
      "us_large_cap": -0.30,
      "us_small_cap": -0.35,
      "europe": -0.32,
      "japan": -0.28,
      "emerging_markets": -0.40
    },
    "fixed_income": {
      "us_treasury": 0.03,
      "us_corporate_investment_grade": -0.08,
      "us_corporate_high_yield": -0.20,
      "emerging_market_debt": -0.25
    },
    "alternatives": {
      "real_estate": -0.15,
      "commodities": -0.25,
      "hedge_funds": -0.10
    }
  },
  "created_at": "2025-06-06T15:00:00Z",
  "updated_at": "2025-06-06T15:10:00Z"
}
```

### Delete Scenario

```
DELETE /scenarios/{scenario_id}
```

Deletes a scenario.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `scenario_id` | string | The ID of the scenario to delete |

#### Response

```json
{
  "success": true,
  "message": "Scenario deleted successfully"
}
```

### Run Scenario Analysis

```
POST /scenarios/analysis
```

Runs a scenario analysis on a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "scenarios": [
    "scenario_123456",
    "scenario_789012",
    "scenario_901234"
  ],
  "calculation_date": "2025-06-06",
  "include_position_level_impacts": true
}
```

#### Response

```json
{
  "analysis_id": "analysis_123456",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "scenario_results": [
    {
      "scenario_id": "scenario_123456",
      "scenario_name": "2008 Financial Crisis",
      "portfolio_impact": {
        "value": -687500.00,
        "percentage": -0.55
      },
      "position_impacts": {
        "AAPL": {
          "value": -275000.00,
          "percentage": -0.55
        },
        "MSFT": {
          "value": -220000.00,
          "percentage": -0.55
        },
        "GOOGL": {
          "value": -55000.00,
          "percentage": -0.55
        },
        "TLT": {
          "value": 12500.00,
          "percentage": 0.05
        }
      },
      "risk_metrics": {
        "var": {
          "value": 687500.00,
          "percentage": 0.55
        },
        "expected_shortfall": {
          "value": 750000.00,
          "percentage": 0.60
        },
        "max_drawdown": {
          "value": 687500.00,
          "percentage": 0.55
        }
      }
    },
    {
      "scenario_id": "scenario_789012",
      "scenario_name": "Fed Rate Hike 100bps",
      "portfolio_impact": {
        "value": -125000.00,
        "percentage": -0.10
      },
      "position_impacts": {
        "AAPL": {
          "value": -25000.00,
          "percentage": -0.05
        },
        "MSFT": {
          "value": -20000.00,
          "percentage": -0.05
        },
        "GOOGL": {
          "value": -5000.00,
          "percentage": -0.05
        },
        "TLT": {
          "value": -75000.00,
          "percentage": -0.30
        }
      },
      "risk_metrics": {
        "var": {
          "value": 125000.00,
          "percentage": 0.10
        },
        "expected_shortfall": {
          "value": 150000.00,
          "percentage": 0.12
        },
        "max_drawdown": {
          "value": 125000.00,
          "percentage": 0.10
        }
      }
    },
    {
      "scenario_id": "scenario_901234",
      "scenario_name": "Global Trade War Escalation (Updated)",
      "portfolio_impact": {
        "value": -375000.00,
        "percentage": -0.30
      },
      "position_impacts": {
        "AAPL": {
          "value": -150000.00,
          "percentage": -0.30
        },
        "MSFT": {
          "value": -120000.00,
          "percentage": -0.30
        },
        "GOOGL": {
          "value": -30000.00,
          "percentage": -0.30
        },
        "TLT": {
          "value": 7500.00,
          "percentage": 0.03
        }
      },
      "risk_metrics": {
        "var": {
          "value": 375000.00,
          "percentage": 0.30
        },
        "expected_shortfall": {
          "value": 400000.00,
          "percentage": 0.32
        },
        "max_drawdown": {
          "value": 375000.00,
          "percentage": 0.30
        }
      }
    }
  ],
  "created_at": "2025-06-06T15:30:00Z"
}
```

### Create Monte Carlo Scenario

```
POST /scenarios/monte-carlo
```

Creates a Monte Carlo scenario.

#### Request Body

```json
{
  "name": "Equity Market Crash Monte Carlo",
  "description": "Monte Carlo simulation of an equity market crash with varying severity.",
  "category": "market_crash",
  "simulation_parameters": {
    "number_of_simulations": 1000,
    "time_horizon_days": 30,
    "confidence_level": 0.99,
    "distribution": "student_t",
    "degrees_of_freedom": 5
  },
  "risk_factors": [
    {
      "name": "equity_market",
      "mean": -0.30,
      "volatility": 0.10,
      "min": -0.60,
      "max": -0.10
    },
    {
      "name": "interest_rate_10y",
      "mean": -0.005,
      "volatility": 0.002,
      "min": -0.01,
      "max": 0.0
    },
    {
      "name": "credit_spread_investment_grade",
      "mean": 0.01,
      "volatility": 0.003,
      "min": 0.005,
      "max": 0.02
    },
    {
      "name": "credit_spread_high_yield",
      "mean": 0.04,
      "volatility": 0.01,
      "min": 0.02,
      "max": 0.08
    },
    {
      "name": "vix",
      "mean": 0.5,
      "volatility": 0.15,
      "min": 0.3,
      "max": 1.0
    }
  ],
  "correlations": [
    {
      "factor1": "equity_market",
      "factor2": "interest_rate_10y",
      "value": 0.3
    },
    {
      "factor1": "equity_market",
      "factor2": "credit_spread_investment_grade",
      "value": -0.7
    },
    {
      "factor1": "equity_market",
      "factor2": "credit_spread_high_yield",
      "value": -0.8
    },
    {
      "factor1": "equity_market",
      "factor2": "vix",
      "value": -0.9
    },
    {
      "factor1": "interest_rate_10y",
      "factor2": "credit_spread_investment_grade",
      "value": -0.4
    },
    {
      "factor1": "interest_rate_10y",
      "factor2": "credit_spread_high_yield",
      "value": -0.3
    },
    {
      "factor1": "interest_rate_10y",
      "factor2": "vix",
      "value": -0.2
    },
    {
      "factor1": "credit_spread_investment_grade",
      "factor2": "credit_spread_high_yield",
      "value": 0.9
    },
    {
      "factor1": "credit_spread_investment_grade",
      "factor2": "vix",
      "value": 0.7
    },
    {
      "factor1": "credit_spread_high_yield",
      "factor2": "vix",
      "value": 0.8
    }
  ]
}
```

#### Response

```json
{
  "id": "scenario_567890",
  "name": "Equity Market Crash Monte Carlo",
  "type": "monte_carlo",
  "category": "market_crash",
  "description": "Monte Carlo simulation of an equity market crash with varying severity.",
  "simulation_parameters": {
    "number_of_simulations": 1000,
    "time_horizon_days": 30,
    "confidence_level": 0.99,
    "distribution": "student_t",
    "degrees_of_freedom": 5
  },
  "risk_factors": [
    {
      "name": "equity_market",
      "mean": -0.30,
      "volatility": 0.10,
      "min": -0.60,
      "max": -0.10
    },
    {
      "name": "interest_rate_10y",
      "mean": -0.005,
      "volatility": 0.002,
      "min": -0.01,
      "max": 0.0
    },
    {
      "name": "credit_spread_investment_grade",
      "mean": 0.01,
      "volatility": 0.003,
      "min": 0.005,
      "max": 0.02
    },
    {
      "name": "credit_spread_high_yield",
      "mean": 0.04,
      "volatility": 0.01,
      "min": 0.02,
      "max": 0.08
    },
    {
      "name": "vix",
      "mean": 0.5,
      "volatility": 0.15,
      "min": 0.3,
      "max": 1.0
    }
  ],
  "correlations": [
    {
      "factor1": "equity_market",
      "factor2": "interest_rate_10y",
      "value": 0.3
    },
    {
      "factor1": "equity_market",
      "factor2": "credit_spread_investment_grade",
      "value": -0.7
    },
    {
      "factor1": "equity_market",
      "factor2": "credit_spread_high_yield",
      "value": -0.8
    },
    {
      "factor1": "equity_market",
      "factor2": "vix",
      "value": -0.9
    },
    {
      "factor1": "interest_rate_10y",
      "factor2": "credit_spread_investment_grade",
      "value": -0.4
    },
    {
      "factor1": "interest_rate_10y",
      "factor2": "credit_spread_high_yield",
      "value": -0.3
    },
    {
      "factor1": "interest_rate_10y",
      "factor2": "vix",
      "value": -0.2
    },
    {
      "factor1": "credit_spread_investment_grade",
      "factor2": "credit_spread_high_yield",
      "value": 0.9
    },
    {
      "factor1": "credit_spread_investment_grade",
      "factor2": "vix",
      "value": 0.7
    },
    {
      "factor1": "credit_spread_high_yield",
      "factor2": "vix",
      "value": 0.8
    }
  ],
  "created_at": "2025-06-06T16:00:00Z",
  "updated_at": "2025-06-06T16:00:00Z"
}
```

### Run Monte Carlo Analysis

```
POST /scenarios/monte-carlo/analysis
```

Runs a Monte Carlo scenario analysis on a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "scenario_id": "scenario_567890",
  "calculation_date": "2025-06-06",
  "include_position_level_impacts": true
}
```

#### Response

```json
{
  "analysis_id": "analysis_789012",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "scenario_id": "scenario_567890",
  "scenario_name": "Equity Market Crash Monte Carlo",
  "simulation_summary": {
    "number_of_simulations": 1000,
    "time_horizon_days": 30,
    "confidence_level": 0.99
  },
  "portfolio_impact": {
    "mean": {
      "value": -375000.00,
      "percentage": -0.30
    },
    "median": {
      "value": -362500.00,
      "percentage": -0.29
    },
    "min": {
      "value": -750000.00,
      "percentage": -0.60
    },
    "max": {
      "value": -125000.00,
      "percentage": -0.10
    },
    "std_dev": {
      "value": 125000.00,
      "percentage": 0.10
    },
    "var_99": {
      "value": -687500.00,
      "percentage": -0.55
    },
    "expected_shortfall_99": {
      "value": -725000.00,
      "percentage": -0.58
    }
  },
  "position_impacts": {
    "AAPL": {
      "mean": {
        "value": -150000.00,
        "percentage": -0.30
      },
      "median": {
        "value": -145000.00,
        "percentage": -0.29
      },
      "min": {
        "value": -300000.00,
        "percentage": -0.60
      },
      "max": {
        "value": -50000.00,
        "percentage": -0.10
      },
      "std_dev": {
        "value": 50000.00,
        "percentage": 0.10
      },
      "var_99": {
        "value": -275000.00,
        "percentage": -0.55
      },
      "expected_shortfall_99": {
        "value": -290000.00,
        "percentage": -0.58
      }
    },
    "MSFT": {
      "mean": {
        "value": -120000.00,
        "percentage": -0.30
      },
      "median": {
        "value": -116000.00,
        "percentage": -0.29
      },
      "min": {
        "value": -240000.00,
        "percentage": -0.60
      },
      "max": {
        "value": -40000.00,
        "percentage": -0.10
      },
      "std_dev": {
        "value": 40000.00,
        "percentage": 0.10
      },
      "var_99": {
        "value": -220000.00,
        "percentage": -0.55
      },
      "expected_shortfall_99": {
        "value": -232000.00,
        "percentage": -0.58
      }
    },
    "GOOGL": {
      "mean": {
        "value": -30000.00,
        "percentage": -0.30
      },
      "median": {
        "value": -29000.00,
        "percentage": -0.29
      },
      "min": {
        "value": -60000.00,
        "percentage": -0.60
      },
      "max": {
        "value": -10000.00,
        "percentage": -0.10
      },
      "std_dev": {
        "value": 10000.00,
        "percentage": 0.10
      },
      "var_99": {
        "value": -55000.00,
        "percentage": -0.55
      },
      "expected_shortfall_99": {
        "value": -58000.00,
        "percentage": -0.58
      }
    },
    "TLT": {
      "mean": {
        "value": -75000.00,
        "percentage": -0.30
      },
      "median": {
        "value": -72500.00,
        "percentage": -0.29
      },
      "min": {
        "value": -150000.00,
        "percentage": -0.60
      },
      "max": {
        "value": -25000.00,
        "percentage": -0.10
      },
      "std_dev": {
        "value": 25000.00,
        "percentage": 0.10
      },
      "var_99": {
        "value": -137500.00,
        "percentage": -0.55
      },
      "expected_shortfall_99": {
        "value": -145000.00,
        "percentage": -0.58
      }
    }
  },
  "risk_factor_realizations": {
    "equity_market": {
      "mean": -0.30,
      "median": -0.29,
      "min": -0.59,
      "max": -0.11,
      "std_dev": 0.10,
      "percentile_1": -0.55,
      "percentile_5": -0.48,
      "percentile_95": -0.14,
      "percentile_99": -0.12
    },
    "interest_rate_10y": {
      "mean": -0.005,
      "median": -0.005,
      "min": -0.01,
      "max": -0.001,
      "std_dev": 0.002,
      "percentile_1": -0.009,
      "percentile_5": -0.008,
      "percentile_95": -0.002,
      "percentile_99": -0.001
    },
    "credit_spread_investment_grade": {
      "mean": 0.01,
      "median": 0.01,
      "min": 0.005,
      "max": 0.019,
      "std_dev": 0.003,
      "percentile_1": 0.005,
      "percentile_5": 0.006,
      "percentile_95": 0.016,
      "percentile_99": 0.018
    },
    "credit_spread_high_yield": {
      "mean": 0.04,
      "median": 0.04,
      "min": 0.02,
      "max": 0.079,
      "std_dev": 0.01,
      "percentile_1": 0.021,
      "percentile_5": 0.024,
      "percentile_95": 0.058,
      "percentile_99": 0.072
    },
    "vix": {
      "mean": 0.5,
      "median": 0.48,
      "min": 0.31,
      "max": 0.98,
      "std_dev": 0.15,
      "percentile_1": 0.32,
      "percentile_5": 0.34,
      "percentile_95": 0.78,
      "percentile_99": 0.92
    }
  },
  "created_at": "2025-06-06T16:30:00Z"
}
```


## Stress Testing

### List Stress Tests

```
GET /stress-tests
```

Retrieves a list of all available stress tests.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by stress test type (e.g., `historical`, `hypothetical`, `regulatory`) |
| `category` | string | Filter by stress test category (e.g., `market_crash`, `interest_rate_shock`, `liquidity_crisis`) |
| `limit` | integer | Maximum number of stress tests to return (default: 100) |
| `offset` | integer | Number of stress tests to skip (default: 0) |

#### Response

```json
{
  "stress_tests": [
    {
      "id": "stress_test_123456",
      "name": "CCAR 2025 Severely Adverse Scenario",
      "type": "regulatory",
      "category": "comprehensive",
      "description": "Federal Reserve's Comprehensive Capital Analysis and Review (CCAR) 2025 severely adverse scenario.",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    },
    {
      "id": "stress_test_789012",
      "name": "Liquidity Crisis Stress Test",
      "type": "hypothetical",
      "category": "liquidity_crisis",
      "description": "Hypothetical stress test simulating a severe market-wide liquidity crisis.",
      "created_at": "2025-02-10T14:30:00Z",
      "updated_at": "2025-02-10T14:30:00Z"
    },
    {
      "id": "stress_test_345678",
      "name": "1987 Black Monday",
      "type": "historical",
      "category": "market_crash",
      "description": "Stress test based on the 1987 Black Monday market crash.",
      "created_at": "2025-03-05T09:15:00Z",
      "updated_at": "2025-03-05T09:15:00Z"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0
}
```

### Get Stress Test

```
GET /stress-tests/{stress_test_id}
```

Retrieves a specific stress test by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `stress_test_id` | string | The ID of the stress test to retrieve |

#### Response

```json
{
  "id": "stress_test_123456",
  "name": "CCAR 2025 Severely Adverse Scenario",
  "type": "regulatory",
  "category": "comprehensive",
  "description": "Federal Reserve's Comprehensive Capital Analysis and Review (CCAR) 2025 severely adverse scenario.",
  "scenario_details": {
    "time_horizon": {
      "start_date": "2025-01-01",
      "end_date": "2026-12-31",
      "quarters": 8
    },
    "macroeconomic_variables": [
      {
        "name": "real_gdp_growth",
        "values": [-6.0, -3.5, -2.0, -0.5, 1.0, 2.0, 2.5, 3.0],
        "unit": "percent_annualized"
      },
      {
        "name": "unemployment_rate",
        "values": [5.5, 7.0, 8.5, 9.5, 10.0, 9.8, 9.5, 9.0],
        "unit": "percent"
      },
      {
        "name": "cpi_inflation",
        "values": [1.0, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, 1.0],
        "unit": "percent_annualized"
      },
      {
        "name": "treasury_10y_yield",
        "values": [1.5, 1.2, 1.0, 0.8, 0.8, 0.9, 1.0, 1.2],
        "unit": "percent"
      },
      {
        "name": "bbb_corporate_spread",
        "values": [3.5, 4.0, 4.5, 5.0, 5.0, 4.8, 4.5, 4.0],
        "unit": "percent"
      },
      {
        "name": "equity_market_index",
        "values": [-30.0, -15.0, -10.0, -5.0, 0.0, 5.0, 7.5, 10.0],
        "unit": "percent_change_from_baseline"
      },
      {
        "name": "house_price_index",
        "values": [-10.0, -12.5, -15.0, -17.5, -20.0, -17.5, -15.0, -12.5],
        "unit": "percent_change_from_baseline"
      },
      {
        "name": "commercial_real_estate_price_index",
        "values": [-15.0, -20.0, -25.0, -30.0, -35.0, -30.0, -25.0, -20.0],
        "unit": "percent_change_from_baseline"
      },
      {
        "name": "vix_index",
        "values": [45.0, 40.0, 35.0, 30.0, 28.0, 26.0, 24.0, 22.0],
        "unit": "index_level"
      }
    ],
    "asset_class_impacts": {
      "equity": {
        "us_large_cap": [-30.0, -15.0, -10.0, -5.0, 0.0, 5.0, 7.5, 10.0],
        "us_small_cap": [-40.0, -20.0, -15.0, -7.5, 0.0, 7.5, 10.0, 12.5],
        "europe": [-35.0, -17.5, -12.5, -6.0, 0.0, 6.0, 9.0, 11.0],
        "japan": [-25.0, -12.5, -8.0, -4.0, 0.0, 4.0, 6.0, 8.0],
        "emerging_markets": [-45.0, -22.5, -15.0, -7.5, 0.0, 7.5, 11.0, 15.0]
      },
      "fixed_income": {
        "us_treasury": [3.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.5],
        "us_corporate_investment_grade": [-5.0, -2.5, -1.5, -0.5, 0.0, 0.5, 1.0, 1.5],
        "us_corporate_high_yield": [-20.0, -10.0, -7.5, -3.5, 0.0, 3.5, 5.0, 7.5],
        "emerging_market_debt": [-15.0, -7.5, -5.0, -2.5, 0.0, 2.5, 3.5, 5.0]
      },
      "alternatives": {
        "real_estate": [-20.0, -17.5, -15.0, -10.0, -5.0, 0.0, 2.5, 5.0],
        "commodities": [-30.0, -15.0, -10.0, -5.0, 0.0, 5.0, 7.5, 10.0],
        "hedge_funds": [-15.0, -7.5, -5.0, -2.5, 0.0, 2.5, 3.5, 5.0]
      }
    }
  },
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

### Create Stress Test

```
POST /stress-tests
```

Creates a new stress test.

#### Request Body

```json
{
  "name": "Stagflation Scenario",
  "type": "hypothetical",
  "category": "macroeconomic",
  "description": "Hypothetical stress test simulating a severe stagflation scenario with high inflation and negative growth.",
  "scenario_details": {
    "time_horizon": {
      "start_date": "2025-07-01",
      "end_date": "2026-06-30",
      "quarters": 4
    },
    "macroeconomic_variables": [
      {
        "name": "real_gdp_growth",
        "values": [-2.0, -1.5, -1.0, -0.5],
        "unit": "percent_annualized"
      },
      {
        "name": "unemployment_rate",
        "values": [5.0, 6.0, 7.0, 7.5],
        "unit": "percent"
      },
      {
        "name": "cpi_inflation",
        "values": [8.0, 9.0, 10.0, 9.5],
        "unit": "percent_annualized"
      },
      {
        "name": "treasury_10y_yield",
        "values": [5.0, 5.5, 6.0, 6.5],
        "unit": "percent"
      },
      {
        "name": "bbb_corporate_spread",
        "values": [3.0, 3.5, 4.0, 4.5],
        "unit": "percent"
      },
      {
        "name": "equity_market_index",
        "values": [-15.0, -10.0, -5.0, -2.5],
        "unit": "percent_change_from_baseline"
      }
    ],
    "asset_class_impacts": {
      "equity": {
        "us_large_cap": [-15.0, -10.0, -5.0, -2.5],
        "us_small_cap": [-20.0, -15.0, -7.5, -5.0],
        "europe": [-17.5, -12.5, -6.0, -3.0],
        "japan": [-12.5, -8.0, -4.0, -2.0],
        "emerging_markets": [-22.5, -15.0, -7.5, -3.5]
      },
      "fixed_income": {
        "us_treasury": [-10.0, -7.5, -5.0, -2.5],
        "us_corporate_investment_grade": [-12.5, -10.0, -7.5, -5.0],
        "us_corporate_high_yield": [-15.0, -12.5, -10.0, -7.5],
        "emerging_market_debt": [-17.5, -15.0, -12.5, -10.0]
      },
      "alternatives": {
        "real_estate": [-10.0, -7.5, -5.0, -2.5],
        "commodities": [15.0, 10.0, 7.5, 5.0],
        "hedge_funds": [-5.0, -2.5, 0.0, 2.5]
      }
    }
  }
}
```

#### Response

```json
{
  "id": "stress_test_901234",
  "name": "Stagflation Scenario",
  "type": "hypothetical",
  "category": "macroeconomic",
  "description": "Hypothetical stress test simulating a severe stagflation scenario with high inflation and negative growth.",
  "scenario_details": {
    "time_horizon": {
      "start_date": "2025-07-01",
      "end_date": "2026-06-30",
      "quarters": 4
    },
    "macroeconomic_variables": [
      {
        "name": "real_gdp_growth",
        "values": [-2.0, -1.5, -1.0, -0.5],
        "unit": "percent_annualized"
      },
      {
        "name": "unemployment_rate",
        "values": [5.0, 6.0, 7.0, 7.5],
        "unit": "percent"
      },
      {
        "name": "cpi_inflation",
        "values": [8.0, 9.0, 10.0, 9.5],
        "unit": "percent_annualized"
      },
      {
        "name": "treasury_10y_yield",
        "values": [5.0, 5.5, 6.0, 6.5],
        "unit": "percent"
      },
      {
        "name": "bbb_corporate_spread",
        "values": [3.0, 3.5, 4.0, 4.5],
        "unit": "percent"
      },
      {
        "name": "equity_market_index",
        "values": [-15.0, -10.0, -5.0, -2.5],
        "unit": "percent_change_from_baseline"
      }
    ],
    "asset_class_impacts": {
      "equity": {
        "us_large_cap": [-15.0, -10.0, -5.0, -2.5],
        "us_small_cap": [-20.0, -15.0, -7.5, -5.0],
        "europe": [-17.5, -12.5, -6.0, -3.0],
        "japan": [-12.5, -8.0, -4.0, -2.0],
        "emerging_markets": [-22.5, -15.0, -7.5, -3.5]
      },
      "fixed_income": {
        "us_treasury": [-10.0, -7.5, -5.0, -2.5],
        "us_corporate_investment_grade": [-12.5, -10.0, -7.5, -5.0],
        "us_corporate_high_yield": [-15.0, -12.5, -10.0, -7.5],
        "emerging_market_debt": [-17.5, -15.0, -12.5, -10.0]
      },
      "alternatives": {
        "real_estate": [-10.0, -7.5, -5.0, -2.5],
        "commodities": [15.0, 10.0, 7.5, 5.0],
        "hedge_funds": [-5.0, -2.5, 0.0, 2.5]
      }
    }
  },
  "created_at": "2025-06-06T17:00:00Z",
  "updated_at": "2025-06-06T17:00:00Z"
}
```

### Update Stress Test

```
PUT /stress-tests/{stress_test_id}
```

Updates an existing stress test.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `stress_test_id` | string | The ID of the stress test to update |

#### Request Body

```json
{
  "name": "Stagflation Scenario (Updated)",
  "description": "Updated hypothetical stress test simulating a severe stagflation scenario with high inflation and negative growth.",
  "scenario_details": {
    "macroeconomic_variables": [
      {
        "name": "real_gdp_growth",
        "values": [-3.0, -2.0, -1.5, -1.0],
        "unit": "percent_annualized"
      },
      {
        "name": "unemployment_rate",
        "values": [5.5, 6.5, 7.5, 8.0],
        "unit": "percent"
      },
      {
        "name": "cpi_inflation",
        "values": [9.0, 10.0, 11.0, 10.5],
        "unit": "percent_annualized"
      },
      {
        "name": "treasury_10y_yield",
        "values": [5.5, 6.0, 6.5, 7.0],
        "unit": "percent"
      },
      {
        "name": "bbb_corporate_spread",
        "values": [3.5, 4.0, 4.5, 5.0],
        "unit": "percent"
      },
      {
        "name": "equity_market_index",
        "values": [-20.0, -15.0, -10.0, -5.0],
        "unit": "percent_change_from_baseline"
      }
    ],
    "asset_class_impacts": {
      "equity": {
        "us_large_cap": [-20.0, -15.0, -10.0, -5.0],
        "us_small_cap": [-25.0, -20.0, -12.5, -7.5],
        "europe": [-22.5, -17.5, -11.0, -5.5],
        "japan": [-17.5, -12.5, -7.5, -3.5],
        "emerging_markets": [-27.5, -20.0, -12.5, -6.0]
      },
      "fixed_income": {
        "us_treasury": [-12.5, -10.0, -7.5, -5.0],
        "us_corporate_investment_grade": [-15.0, -12.5, -10.0, -7.5],
        "us_corporate_high_yield": [-17.5, -15.0, -12.5, -10.0],
        "emerging_market_debt": [-20.0, -17.5, -15.0, -12.5]
      },
      "alternatives": {
        "real_estate": [-12.5, -10.0, -7.5, -5.0],
        "commodities": [20.0, 15.0, 10.0, 7.5],
        "hedge_funds": [-7.5, -5.0, -2.5, 0.0]
      }
    }
  }
}
```

#### Response

```json
{
  "id": "stress_test_901234",
  "name": "Stagflation Scenario (Updated)",
  "type": "hypothetical",
  "category": "macroeconomic",
  "description": "Updated hypothetical stress test simulating a severe stagflation scenario with high inflation and negative growth.",
  "scenario_details": {
    "time_horizon": {
      "start_date": "2025-07-01",
      "end_date": "2026-06-30",
      "quarters": 4
    },
    "macroeconomic_variables": [
      {
        "name": "real_gdp_growth",
        "values": [-3.0, -2.0, -1.5, -1.0],
        "unit": "percent_annualized"
      },
      {
        "name": "unemployment_rate",
        "values": [5.5, 6.5, 7.5, 8.0],
        "unit": "percent"
      },
      {
        "name": "cpi_inflation",
        "values": [9.0, 10.0, 11.0, 10.5],
        "unit": "percent_annualized"
      },
      {
        "name": "treasury_10y_yield",
        "values": [5.5, 6.0, 6.5, 7.0],
        "unit": "percent"
      },
      {
        "name": "bbb_corporate_spread",
        "values": [3.5, 4.0, 4.5, 5.0],
        "unit": "percent"
      },
      {
        "name": "equity_market_index",
        "values": [-20.0, -15.0, -10.0, -5.0],
        "unit": "percent_change_from_baseline"
      }
    ],
    "asset_class_impacts": {
      "equity": {
        "us_large_cap": [-20.0, -15.0, -10.0, -5.0],
        "us_small_cap": [-25.0, -20.0, -12.5, -7.5],
        "europe": [-22.5, -17.5, -11.0, -5.5],
        "japan": [-17.5, -12.5, -7.5, -3.5],
        "emerging_markets": [-27.5, -20.0, -12.5, -6.0]
      },
      "fixed_income": {
        "us_treasury": [-12.5, -10.0, -7.5, -5.0],
        "us_corporate_investment_grade": [-15.0, -12.5, -10.0, -7.5],
        "us_corporate_high_yield": [-17.5, -15.0, -12.5, -10.0],
        "emerging_market_debt": [-20.0, -17.5, -15.0, -12.5]
      },
      "alternatives": {
        "real_estate": [-12.5, -10.0, -7.5, -5.0],
        "commodities": [20.0, 15.0, 10.0, 7.5],
        "hedge_funds": [-7.5, -5.0, -2.5, 0.0]
      }
    }
  },
  "created_at": "2025-06-06T17:00:00Z",
  "updated_at": "2025-06-06T17:10:00Z"
}
```

### Delete Stress Test

```
DELETE /stress-tests/{stress_test_id}
```

Deletes a stress test.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `stress_test_id` | string | The ID of the stress test to delete |

#### Response

```json
{
  "success": true,
  "message": "Stress test deleted successfully"
}
```

### Run Stress Test

```
POST /stress-tests/run
```

Runs a stress test on a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "stress_test_id": "stress_test_901234",
  "calculation_date": "2025-06-06",
  "include_position_level_impacts": true,
  "include_time_series": true
}
```

#### Response

```json
{
  "run_id": "stress_run_123456",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "stress_test_id": "stress_test_901234",
  "stress_test_name": "Stagflation Scenario (Updated)",
  "overall_impact": {
    "value": -250000.00,
    "percentage": -0.20
  },
  "time_series_impacts": [
    {
      "date": "2025-09-30",
      "portfolio_value": 1000000.00,
      "change": {
        "value": -250000.00,
        "percentage": -0.20
      }
    },
    {
      "date": "2025-12-31",
      "portfolio_value": 1062500.00,
      "change": {
        "value": -187500.00,
        "percentage": -0.15
      }
    },
    {
      "date": "2026-03-31",
      "portfolio_value": 1125000.00,
      "change": {
        "value": -125000.00,
        "percentage": -0.10
      }
    },
    {
      "date": "2026-06-30",
      "portfolio_value": 1187500.00,
      "change": {
        "value": -62500.00,
        "percentage": -0.05
      }
    }
  ],
  "position_impacts": {
    "AAPL": {
      "initial_value": 500000.00,
      "time_series": [
        {
          "date": "2025-09-30",
          "value": 400000.00,
          "change": {
            "value": -100000.00,
            "percentage": -0.20
          }
        },
        {
          "date": "2025-12-31",
          "value": 425000.00,
          "change": {
            "value": -75000.00,
            "percentage": -0.15
          }
        },
        {
          "date": "2026-03-31",
          "value": 450000.00,
          "change": {
            "value": -50000.00,
            "percentage": -0.10
          }
        },
        {
          "date": "2026-06-30",
          "value": 475000.00,
          "change": {
            "value": -25000.00,
            "percentage": -0.05
          }
        }
      ]
    },
    "MSFT": {
      "initial_value": 400000.00,
      "time_series": [
        {
          "date": "2025-09-30",
          "value": 320000.00,
          "change": {
            "value": -80000.00,
            "percentage": -0.20
          }
        },
        {
          "date": "2025-12-31",
          "value": 340000.00,
          "change": {
            "value": -60000.00,
            "percentage": -0.15
          }
        },
        {
          "date": "2026-03-31",
          "value": 360000.00,
          "change": {
            "value": -40000.00,
            "percentage": -0.10
          }
        },
        {
          "date": "2026-06-30",
          "value": 380000.00,
          "change": {
            "value": -20000.00,
            "percentage": -0.05
          }
        }
      ]
    },
    "GOOGL": {
      "initial_value": 100000.00,
      "time_series": [
        {
          "date": "2025-09-30",
          "value": 80000.00,
          "change": {
            "value": -20000.00,
            "percentage": -0.20
          }
        },
        {
          "date": "2025-12-31",
          "value": 85000.00,
          "change": {
            "value": -15000.00,
            "percentage": -0.15
          }
        },
        {
          "date": "2026-03-31",
          "value": 90000.00,
          "change": {
            "value": -10000.00,
            "percentage": -0.10
          }
        },
        {
          "date": "2026-06-30",
          "value": 95000.00,
          "change": {
            "value": -5000.00,
            "percentage": -0.05
          }
        }
      ]
    },
    "TLT": {
      "initial_value": 250000.00,
      "time_series": [
        {
          "date": "2025-09-30",
          "value": 200000.00,
          "change": {
            "value": -50000.00,
            "percentage": -0.20
          }
        },
        {
          "date": "2025-12-31",
          "value": 212500.00,
          "change": {
            "value": -37500.00,
            "percentage": -0.15
          }
        },
        {
          "date": "2026-03-31",
          "value": 225000.00,
          "change": {
            "value": -25000.00,
            "percentage": -0.10
          }
        },
        {
          "date": "2026-06-30",
          "value": 237500.00,
          "change": {
            "value": -12500.00,
            "percentage": -0.05
          }
        }
      ]
    }
  },
  "risk_metrics": {
    "var": {
      "value": 250000.00,
      "percentage": 0.20
    },
    "expected_shortfall": {
      "value": 275000.00,
      "percentage": 0.22
    },
    "max_drawdown": {
      "value": 250000.00,
      "percentage": 0.20,
      "date": "2025-09-30"
    }
  },
  "created_at": "2025-06-06T17:30:00Z"
}
```

### Compare Stress Tests

```
POST /stress-tests/compare
```

Compares multiple stress tests on a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "stress_test_ids": [
    "stress_test_123456",
    "stress_test_789012",
    "stress_test_901234"
  ],
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "comparison_id": "comparison_123456",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "stress_test_results": [
    {
      "stress_test_id": "stress_test_123456",
      "stress_test_name": "CCAR 2025 Severely Adverse Scenario",
      "overall_impact": {
        "value": -687500.00,
        "percentage": -0.55
      },
      "risk_metrics": {
        "var": {
          "value": 687500.00,
          "percentage": 0.55
        },
        "expected_shortfall": {
          "value": 750000.00,
          "percentage": 0.60
        },
        "max_drawdown": {
          "value": 687500.00,
          "percentage": 0.55
        }
      }
    },
    {
      "stress_test_id": "stress_test_789012",
      "stress_test_name": "Liquidity Crisis Stress Test",
      "overall_impact": {
        "value": -375000.00,
        "percentage": -0.30
      },
      "risk_metrics": {
        "var": {
          "value": 375000.00,
          "percentage": 0.30
        },
        "expected_shortfall": {
          "value": 400000.00,
          "percentage": 0.32
        },
        "max_drawdown": {
          "value": 375000.00,
          "percentage": 0.30
        }
      }
    },
    {
      "stress_test_id": "stress_test_901234",
      "stress_test_name": "Stagflation Scenario (Updated)",
      "overall_impact": {
        "value": -250000.00,
        "percentage": -0.20
      },
      "risk_metrics": {
        "var": {
          "value": 250000.00,
          "percentage": 0.20
        },
        "expected_shortfall": {
          "value": 275000.00,
          "percentage": 0.22
        },
        "max_drawdown": {
          "value": 250000.00,
          "percentage": 0.20
        }
      }
    }
  ],
  "asset_class_impacts": {
    "equity": {
      "stress_test_123456": -0.55,
      "stress_test_789012": -0.35,
      "stress_test_901234": -0.20
    },
    "fixed_income": {
      "stress_test_123456": 0.05,
      "stress_test_789012": -0.15,
      "stress_test_901234": -0.20
    }
  },
  "created_at": "2025-06-06T18:00:00Z"
}
```


## Risk Attribution

### Calculate Risk Attribution

```
POST /attribution
```

Calculates risk attribution for a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "benchmark_portfolio": {
    "positions": [
      {
        "symbol": "SPY",
        "quantity": 2000,
        "asset_class": "equity"
      },
      {
        "symbol": "AGG",
        "quantity": 1000,
        "asset_class": "fixed_income"
      }
    ]
  },
  "model_id": "model_345678",
  "attribution_type": "brinson",
  "start_date": "2025-01-01",
  "end_date": "2025-06-01",
  "frequency": "monthly"
}
```

#### Response

```json
{
  "attribution_id": "attr_123456",
  "start_date": "2025-01-01",
  "end_date": "2025-06-01",
  "frequency": "monthly",
  "portfolio_return": 0.085,
  "benchmark_return": 0.072,
  "active_return": 0.013,
  "attribution_summary": {
    "allocation_effect": 0.005,
    "selection_effect": 0.007,
    "interaction_effect": 0.001,
    "total_active_return": 0.013
  },
  "attribution_by_asset_class": {
    "equity": {
      "portfolio_weight": 0.8,
      "benchmark_weight": 0.7,
      "portfolio_return": 0.10,
      "benchmark_return": 0.09,
      "allocation_effect": 0.002,
      "selection_effect": 0.005,
      "interaction_effect": 0.0005,
      "total_active_return": 0.0075
    },
    "fixed_income": {
      "portfolio_weight": 0.2,
      "benchmark_weight": 0.3,
      "portfolio_return": 0.03,
      "benchmark_return": 0.02,
      "allocation_effect": 0.003,
      "selection_effect": 0.002,
      "interaction_effect": 0.0005,
      "total_active_return": 0.0055
    }
  },
  "attribution_by_sector": {
    "technology": {
      "portfolio_weight": 0.6,
      "benchmark_weight": 0.5,
      "portfolio_return": 0.12,
      "benchmark_return": 0.11,
      "allocation_effect": 0.003,
      "selection_effect": 0.004,
      "interaction_effect": 0.0003,
      "total_active_return": 0.0073
    },
    "financials": {
      "portfolio_weight": 0.1,
      "benchmark_weight": 0.15,
      "portfolio_return": 0.05,
      "benchmark_return": 0.04,
      "allocation_effect": 0.001,
      "selection_effect": 0.001,
      "interaction_effect": 0.0001,
      "total_active_return": 0.0021
    },
    "healthcare": {
      "portfolio_weight": 0.1,
      "benchmark_weight": 0.05,
      "portfolio_return": 0.08,
      "benchmark_return": 0.07,
      "allocation_effect": 0.001,
      "selection_effect": 0.002,
      "interaction_effect": 0.0001,
      "total_active_return": 0.0031
    }
  },
  "attribution_by_position": {
    "AAPL": {
      "portfolio_weight": 0.4,
      "benchmark_weight": 0.0,
      "portfolio_return": 0.15,
      "benchmark_return": 0.09,
      "allocation_effect": 0.024,
      "selection_effect": 0.024,
      "interaction_effect": 0.000,
      "total_active_return": 0.048
    },
    "MSFT": {
      "portfolio_weight": 0.32,
      "benchmark_weight": 0.0,
      "portfolio_return": 0.10,
      "benchmark_return": 0.09,
      "allocation_effect": 0.0032,
      "selection_effect": 0.0032,
      "interaction_effect": 0.000,
      "total_active_return": 0.0064
    },
    "GOOGL": {
      "portfolio_weight": 0.08,
      "benchmark_weight": 0.0,
      "portfolio_return": 0.08,
      "benchmark_return": 0.09,
      "allocation_effect": -0.0008,
      "selection_effect": -0.0008,
      "interaction_effect": 0.000,
      "total_active_return": -0.0016
    },
    "TLT": {
      "portfolio_weight": 0.2,
      "benchmark_weight": 0.0,
      "portfolio_return": 0.03,
      "benchmark_return": 0.02,
      "allocation_effect": 0.002,
      "selection_effect": 0.002,
      "interaction_effect": 0.000,
      "total_active_return": 0.004
    },
    "SPY": {
      "portfolio_weight": 0.0,
      "benchmark_weight": 0.7,
      "portfolio_return": 0.0,
      "benchmark_return": 0.09,
      "allocation_effect": -0.063,
      "selection_effect": 0.0,
      "interaction_effect": 0.0,
      "total_active_return": -0.063
    },
    "AGG": {
      "portfolio_weight": 0.0,
      "benchmark_weight": 0.3,
      "portfolio_return": 0.0,
      "benchmark_return": 0.02,
      "allocation_effect": -0.006,
      "selection_effect": 0.0,
      "interaction_effect": 0.0,
      "total_active_return": -0.006
    }
  },
  "created_at": "2025-06-06T18:30:00Z"
}
```

### Get Historical Risk Attribution

```
GET /attribution/history
```

Retrieves historical risk attribution for a portfolio.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | The ID of the portfolio |
| `benchmark_id` | string | The ID of the benchmark portfolio |
| `model_id` | string | The ID of the risk model |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2024-01-01`) |
| `end_date` | string | End date in ISO 8601 format (e.g., `2025-06-01`) |
| `frequency` | string | Data interval (`monthly`, `quarterly`, `annual`) |

#### Response

```json
{
  "portfolio_id": "portfolio_123456",
  "benchmark_id": "benchmark_789012",
  "model_id": "model_345678",
  "data": [
    {
      "date": "2025-06-01",
      "portfolio_return": 0.015,
      "benchmark_return": 0.012,
      "active_return": 0.003,
      "attribution_summary": {
        "allocation_effect": 0.001,
        "selection_effect": 0.0015,
        "interaction_effect": 0.0005,
        "total_active_return": 0.003
      }
    },
    {
      "date": "2025-05-01",
      "portfolio_return": 0.020,
      "benchmark_return": 0.018,
      "active_return": 0.002,
      "attribution_summary": {
        "allocation_effect": 0.0008,
        "selection_effect": 0.001,
        "interaction_effect": 0.0002,
        "total_active_return": 0.002
      }
    },
    {
      "date": "2025-04-01",
      "portfolio_return": -0.005,
      "benchmark_return": -0.008,
      "active_return": 0.003,
      "attribution_summary": {
        "allocation_effect": 0.0015,
        "selection_effect": 0.0012,
        "interaction_effect": 0.0003,
        "total_active_return": 0.003
      }
    }
  ],
  "meta": {
    "start_date": "2025-04-01",
    "end_date": "2025-06-01",
    "frequency": "monthly"
  }
}
```

### Calculate Factor Risk Attribution

```
POST /attribution/factor
```

Calculates factor risk attribution for a portfolio.

#### Request Body

```json
{
  "portfolio": {
    "positions": [
      {
        "symbol": "AAPL",
        "quantity": 1000,
        "asset_class": "equity"
      },
      {
        "symbol": "MSFT",
        "quantity": 800,
        "asset_class": "equity"
      },
      {
        "symbol": "GOOGL",
        "quantity": 200,
        "asset_class": "equity"
      },
      {
        "symbol": "TLT",
        "quantity": 500,
        "asset_class": "fixed_income"
      }
    ]
  },
  "model_id": "model_345678",
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "attribution_id": "attr_factor_123456",
  "calculation_date": "2025-06-06",
  "portfolio_value": 1250000.00,
  "model_id": "model_345678",
  "total_risk": {
    "volatility": 0.18,
    "var": {
      "value": 37500.00,
      "percentage": 0.03
    }
  },
  "factor_attribution": [
    {
      "factor": "market",
      "exposure": 1.05,
      "risk_contribution": {
        "volatility": 0.12,
        "volatility_percentage": 0.667,
        "var": {
          "value": 25000.00,
          "percentage": 0.02,
          "contribution_percentage": 0.667
        }
      }
    },
    {
      "factor": "size",
      "exposure": -0.25,
      "risk_contribution": {
        "volatility": 0.02,
        "volatility_percentage": 0.111,
        "var": {
          "value": 4166.67,
          "percentage": 0.0033,
          "contribution_percentage": 0.111
        }
      }
    },
    {
      "factor": "value",
      "exposure": 0.15,
      "risk_contribution": {
        "volatility": 0.01,
        "volatility_percentage": 0.056,
        "var": {
          "value": 2083.33,
          "percentage": 0.0017,
          "contribution_percentage": 0.056
        }
      }
    },
    {
      "factor": "momentum",
      "exposure": 0.45,
      "risk_contribution": {
        "volatility": 0.015,
        "volatility_percentage": 0.083,
        "var": {
          "value": 3125.00,
          "percentage": 0.0025,
          "contribution_percentage": 0.083
        }
      }
    },
    {
      "factor": "interest_rate",
      "exposure": 0.35,
      "risk_contribution": {
        "volatility": 0.01,
        "volatility_percentage": 0.056,
        "var": {
          "value": 2083.33,
          "percentage": 0.0017,
          "contribution_percentage": 0.056
        }
      }
    },
    {
      "factor": "inflation",
      "exposure": 0.25,
      "risk_contribution": {
        "volatility": 0.005,
        "volatility_percentage": 0.028,
        "var": {
          "value": 1041.67,
          "percentage": 0.0008,
          "contribution_percentage": 0.028
        }
      }
    }
  ],
  "specific_risk": {
    "volatility": 0.03,
    "volatility_percentage": 0.167,
    "var": {
      "value": 6250.00,
      "percentage": 0.005,
      "contribution_percentage": 0.167
    }
  },
  "created_at": "2025-06-06T19:00:00Z"
}
```


## Limits Management

### List Risk Limits

```
GET /limits
```

Retrieves a list of all configured risk limits.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | Filter by portfolio ID |
| `type` | string | Filter by limit type (e.g., `exposure`, `var`, `concentration`) |
| `status` | string | Filter by limit status (e.g., `active`, `breached`, `warning`) |
| `limit` | integer | Maximum number of risk limits to return (default: 100) |
| `offset` | integer | Number of risk limits to skip (default: 0) |

#### Response

```json
{
  "limits": [
    {
      "id": "limit_123456",
      "name": "Portfolio VaR Limit",
      "portfolio_id": "portfolio_123456",
      "type": "var",
      "description": "Value at Risk limit for the overall portfolio.",
      "parameters": {
        "model_id": "model_123456",
        "confidence_level": 0.99,
        "holding_period": 1
      },
      "threshold": {
        "warning": 0.025,
        "breach": 0.03
      },
      "status": "active",
      "current_value": 0.02,
      "last_checked_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    },
    {
      "id": "limit_789012",
      "name": "Sector Concentration Limit - Technology",
      "portfolio_id": "portfolio_123456",
      "type": "concentration",
      "description": "Concentration limit for technology sector exposure.",
      "parameters": {
        "sector": "technology",
        "include_derivatives": true
      },
      "threshold": {
        "warning": 0.35,
        "breach": 0.40
      },
      "status": "warning",
      "current_value": 0.38,
      "last_checked_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-02-10T14:30:00Z",
      "updated_at": "2025-02-10T14:30:00Z"
    },
    {
      "id": "limit_345678",
      "name": "Single Issuer Exposure Limit - AAPL",
      "portfolio_id": "portfolio_123456",
      "type": "exposure",
      "description": "Exposure limit for a single issuer (Apple Inc.).",
      "parameters": {
        "symbol": "AAPL",
        "include_derivatives": true
      },
      "threshold": {
        "warning": 0.075,
        "breach": 0.10
      },
      "status": "breached",
      "current_value": 0.12,
      "last_checked_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-03-05T09:15:00Z",
      "updated_at": "2025-03-05T09:15:00Z"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0
}
```

### Get Risk Limit

```
GET /limits/{limit_id}
```

Retrieves a specific risk limit by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit_id` | string | The ID of the risk limit to retrieve |

#### Response

```json
{
  "id": "limit_123456",
  "name": "Portfolio VaR Limit",
  "portfolio_id": "portfolio_123456",
  "type": "var",
  "description": "Value at Risk limit for the overall portfolio.",
  "parameters": {
    "model_id": "model_123456",
    "confidence_level": 0.99,
    "holding_period": 1
  },
  "threshold": {
    "warning": 0.025,
    "breach": 0.03
  },
  "status": "active",
  "current_value": 0.02,
  "history": [
    {
      "date": "2025-06-06",
      "value": 0.02,
      "status": "active"
    },
    {
      "date": "2025-06-05",
      "value": 0.022,
      "status": "active"
    },
    {
      "date": "2025-06-04",
      "value": 0.026,
      "status": "warning"
    },
    {
      "date": "2025-06-03",
      "value": 0.028,
      "status": "warning"
    },
    {
      "date": "2025-06-02",
      "value": 0.024,
      "status": "active"
    }
  ],
  "notifications": {
    "email": ["risk_manager@example.com", "portfolio_manager@example.com"],
    "webhook": ["https://api.example.com/risk-alerts"],
    "frequency": "immediate"
  },
  "last_checked_at": "2025-06-06T10:00:00Z",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

### Create Risk Limit

```
POST /limits
```

Creates a new risk limit.

#### Request Body

```json
{
  "name": "Interest Rate Sensitivity Limit",
  "portfolio_id": "portfolio_123456",
  "type": "sensitivity",
  "description": "Limit on portfolio sensitivity to interest rate changes.",
  "parameters": {
    "risk_factor": "interest_rate_10y",
    "shock": 0.01
  },
  "threshold": {
    "warning": 0.05,
    "breach": 0.075
  },
  "notifications": {
    "email": ["risk_manager@example.com", "portfolio_manager@example.com"],
    "webhook": ["https://api.example.com/risk-alerts"],
    "frequency": "immediate"
  }
}
```

#### Response

```json
{
  "id": "limit_901234",
  "name": "Interest Rate Sensitivity Limit",
  "portfolio_id": "portfolio_123456",
  "type": "sensitivity",
  "description": "Limit on portfolio sensitivity to interest rate changes.",
  "parameters": {
    "risk_factor": "interest_rate_10y",
    "shock": 0.01
  },
  "threshold": {
    "warning": 0.05,
    "breach": 0.075
  },
  "status": "pending",
  "current_value": null,
  "notifications": {
    "email": ["risk_manager@example.com", "portfolio_manager@example.com"],
    "webhook": ["https://api.example.com/risk-alerts"],
    "frequency": "immediate"
  },
  "last_checked_at": null,
  "created_at": "2025-06-06T19:30:00Z",
  "updated_at": "2025-06-06T19:30:00Z"
}
```

### Update Risk Limit

```
PUT /limits/{limit_id}
```

Updates an existing risk limit.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit_id` | string | The ID of the risk limit to update |

#### Request Body

```json
{
  "name": "Interest Rate Sensitivity Limit (Updated)",
  "description": "Updated limit on portfolio sensitivity to interest rate changes.",
  "parameters": {
    "risk_factor": "interest_rate_10y",
    "shock": 0.01
  },
  "threshold": {
    "warning": 0.06,
    "breach": 0.08
  },
  "notifications": {
    "email": ["risk_manager@example.com", "portfolio_manager@example.com", "cro@example.com"],
    "webhook": ["https://api.example.com/risk-alerts"],
    "frequency": "immediate"
  }
}
```

#### Response

```json
{
  "id": "limit_901234",
  "name": "Interest Rate Sensitivity Limit (Updated)",
  "portfolio_id": "portfolio_123456",
  "type": "sensitivity",
  "description": "Updated limit on portfolio sensitivity to interest rate changes.",
  "parameters": {
    "risk_factor": "interest_rate_10y",
    "shock": 0.01
  },
  "threshold": {
    "warning": 0.06,
    "breach": 0.08
  },
  "status": "pending",
  "current_value": null,
  "notifications": {
    "email": ["risk_manager@example.com", "portfolio_manager@example.com", "cro@example.com"],
    "webhook": ["https://api.example.com/risk-alerts"],
    "frequency": "immediate"
  },
  "last_checked_at": null,
  "created_at": "2025-06-06T19:30:00Z",
  "updated_at": "2025-06-06T19:40:00Z"
}
```

### Delete Risk Limit

```
DELETE /limits/{limit_id}
```

Deletes a risk limit.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit_id` | string | The ID of the risk limit to delete |

#### Response

```json
{
  "success": true,
  "message": "Risk limit deleted successfully"
}
```

### Check Risk Limits

```
POST /limits/check
```

Checks all risk limits for a portfolio.

#### Request Body

```json
{
  "portfolio_id": "portfolio_123456",
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "check_id": "check_123456",
  "portfolio_id": "portfolio_123456",
  "calculation_date": "2025-06-06",
  "limits_checked": 3,
  "limits_breached": 1,
  "limits_warning": 1,
  "limits_active": 1,
  "results": [
    {
      "limit_id": "limit_123456",
      "name": "Portfolio VaR Limit",
      "type": "var",
      "threshold": {
        "warning": 0.025,
        "breach": 0.03
      },
      "previous_value": 0.022,
      "current_value": 0.02,
      "previous_status": "active",
      "current_status": "active"
    },
    {
      "limit_id": "limit_789012",
      "name": "Sector Concentration Limit - Technology",
      "type": "concentration",
      "threshold": {
        "warning": 0.35,
        "breach": 0.40
      },
      "previous_value": 0.36,
      "current_value": 0.38,
      "previous_status": "warning",
      "current_status": "warning"
    },
    {
      "limit_id": "limit_345678",
      "name": "Single Issuer Exposure Limit - AAPL",
      "type": "exposure",
      "threshold": {
        "warning": 0.075,
        "breach": 0.10
      },
      "previous_value": 0.11,
      "current_value": 0.12,
      "previous_status": "breached",
      "current_status": "breached"
    }
  ],
  "created_at": "2025-06-06T20:00:00Z"
}
```

### Get Limit Breach History

```
GET /limits/breaches
```

Retrieves the history of risk limit breaches.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | Filter by portfolio ID |
| `limit_id` | string | Filter by limit ID |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2025-01-01`) |
| `end_date` | string | End date in ISO 8601 format (e.g., `2025-06-01`) |
| `status` | string | Filter by breach status (e.g., `active`, `resolved`) |
| `limit` | integer | Maximum number of breaches to return (default: 100) |
| `offset` | integer | Number of breaches to skip (default: 0) |

#### Response

```json
{
  "breaches": [
    {
      "id": "breach_123456",
      "limit_id": "limit_345678",
      "limit_name": "Single Issuer Exposure Limit - AAPL",
      "portfolio_id": "portfolio_123456",
      "start_date": "2025-06-01",
      "end_date": null,
      "status": "active",
      "threshold": 0.10,
      "max_value": 0.12,
      "current_value": 0.12,
      "resolution_plan": {
        "id": "plan_123456",
        "description": "Reduce AAPL position by selling 300 shares",
        "status": "in_progress",
        "due_date": "2025-06-10",
        "assigned_to": "portfolio_manager@example.com"
      }
    },
    {
      "id": "breach_789012",
      "limit_id": "limit_123456",
      "limit_name": "Portfolio VaR Limit",
      "portfolio_id": "portfolio_123456",
      "start_date": "2025-05-15",
      "end_date": "2025-05-20",
      "status": "resolved",
      "threshold": 0.03,
      "max_value": 0.032,
      "current_value": 0.02,
      "resolution_plan": {
        "id": "plan_789012",
        "description": "Reduce equity exposure and increase fixed income allocation",
        "status": "completed",
        "due_date": "2025-05-20",
        "assigned_to": "portfolio_manager@example.com",
        "completed_at": "2025-05-18T14:30:00Z"
      }
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Create Resolution Plan

```
POST /limits/breaches/{breach_id}/resolution
```

Creates a resolution plan for a risk limit breach.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `breach_id` | string | The ID of the breach to create a resolution plan for |

#### Request Body

```json
{
  "description": "Reduce AAPL position by selling 300 shares to bring exposure below 10% threshold",
  "due_date": "2025-06-10",
  "assigned_to": "portfolio_manager@example.com",
  "steps": [
    {
      "description": "Analyze market conditions for optimal execution",
      "due_date": "2025-06-07",
      "status": "pending"
    },
    {
      "description": "Execute sell order for 300 shares of AAPL",
      "due_date": "2025-06-08",
      "status": "pending"
    },
    {
      "description": "Verify position size and recalculate exposure",
      "due_date": "2025-06-09",
      "status": "pending"
    }
  ]
}
```

#### Response

```json
{
  "id": "plan_123456",
  "breach_id": "breach_123456",
  "description": "Reduce AAPL position by selling 300 shares to bring exposure below 10% threshold",
  "status": "in_progress",
  "due_date": "2025-06-10",
  "assigned_to": "portfolio_manager@example.com",
  "steps": [
    {
      "id": "step_123456",
      "description": "Analyze market conditions for optimal execution",
      "due_date": "2025-06-07",
      "status": "pending"
    },
    {
      "id": "step_789012",
      "description": "Execute sell order for 300 shares of AAPL",
      "due_date": "2025-06-08",
      "status": "pending"
    },
    {
      "id": "step_345678",
      "description": "Verify position size and recalculate exposure",
      "due_date": "2025-06-09",
      "status": "pending"
    }
  ],
  "created_at": "2025-06-06T20:30:00Z",
  "updated_at": "2025-06-06T20:30:00Z"
}
```

### Update Resolution Plan

```
PUT /limits/breaches/{breach_id}/resolution/{plan_id}
```

Updates a resolution plan for a risk limit breach.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `breach_id` | string | The ID of the breach |
| `plan_id` | string | The ID of the resolution plan to update |

#### Request Body

```json
{
  "status": "in_progress",
  "steps": [
    {
      "id": "step_123456",
      "status": "completed",
      "completed_at": "2025-06-06T21:00:00Z",
      "notes": "Market analysis completed, optimal execution time identified for tomorrow morning"
    },
    {
      "id": "step_789012",
      "status": "pending"
    },
    {
      "id": "step_345678",
      "status": "pending"
    }
  ]
}
```

#### Response

```json
{
  "id": "plan_123456",
  "breach_id": "breach_123456",
  "description": "Reduce AAPL position by selling 300 shares to bring exposure below 10% threshold",
  "status": "in_progress",
  "due_date": "2025-06-10",
  "assigned_to": "portfolio_manager@example.com",
  "steps": [
    {
      "id": "step_123456",
      "description": "Analyze market conditions for optimal execution",
      "due_date": "2025-06-07",
      "status": "completed",
      "completed_at": "2025-06-06T21:00:00Z",
      "notes": "Market analysis completed, optimal execution time identified for tomorrow morning"
    },
    {
      "id": "step_789012",
      "description": "Execute sell order for 300 shares of AAPL",
      "due_date": "2025-06-08",
      "status": "pending"
    },
    {
      "id": "step_345678",
      "description": "Verify position size and recalculate exposure",
      "due_date": "2025-06-09",
      "status": "pending"
    }
  ],
  "created_at": "2025-06-06T20:30:00Z",
  "updated_at": "2025-06-06T21:00:00Z"
}
```


## Compliance

### List Compliance Rules

```
GET /compliance/rules
```

Retrieves a list of all configured compliance rules.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | Filter by portfolio ID |
| `type` | string | Filter by rule type (e.g., `regulatory`, `internal`, `client`) |
| `status` | string | Filter by rule status (e.g., `active`, `violated`, `warning`) |
| `limit` | integer | Maximum number of compliance rules to return (default: 100) |
| `offset` | integer | Number of compliance rules to skip (default: 0) |

#### Response

```json
{
  "rules": [
    {
      "id": "rule_123456",
      "name": "SEC Rule 15c3-1 Net Capital Requirement",
      "portfolio_id": "portfolio_123456",
      "type": "regulatory",
      "category": "capital_adequacy",
      "description": "Broker-dealer must maintain minimum net capital as required by SEC Rule 15c3-1.",
      "parameters": {
        "min_net_capital": 250000,
        "currency": "USD"
      },
      "status": "active",
      "current_value": 500000,
      "last_checked_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:00:00Z"
    },
    {
      "id": "rule_789012",
      "name": "Restricted Securities Trading",
      "portfolio_id": "portfolio_123456",
      "type": "internal",
      "category": "trading_restrictions",
      "description": "Prohibition on trading securities on the firm's restricted list.",
      "parameters": {
        "restricted_list_id": "list_123456"
      },
      "status": "violated",
      "violations": [
        {
          "symbol": "XYZ",
          "position": 1000,
          "detected_at": "2025-06-06T09:30:00Z"
        }
      ],
      "last_checked_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-02-10T14:30:00Z",
      "updated_at": "2025-02-10T14:30:00Z"
    },
    {
      "id": "rule_345678",
      "name": "Client Investment Policy - No Tobacco Stocks",
      "portfolio_id": "portfolio_123456",
      "type": "client",
      "category": "esg_restrictions",
      "description": "Client investment policy prohibits investments in tobacco companies.",
      "parameters": {
        "excluded_sectors": ["tobacco"],
        "excluded_activities": ["tobacco_production", "tobacco_distribution"]
      },
      "status": "active",
      "last_checked_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-03-05T09:15:00Z",
      "updated_at": "2025-03-05T09:15:00Z"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0
}
```

### Get Compliance Rule

```
GET /compliance/rules/{rule_id}
```

Retrieves a specific compliance rule by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `rule_id` | string | The ID of the compliance rule to retrieve |

#### Response

```json
{
  "id": "rule_123456",
  "name": "SEC Rule 15c3-1 Net Capital Requirement",
  "portfolio_id": "portfolio_123456",
  "type": "regulatory",
  "category": "capital_adequacy",
  "description": "Broker-dealer must maintain minimum net capital as required by SEC Rule 15c3-1.",
  "parameters": {
    "min_net_capital": 250000,
    "currency": "USD"
  },
  "status": "active",
  "current_value": 500000,
  "history": [
    {
      "date": "2025-06-06",
      "value": 500000,
      "status": "active"
    },
    {
      "date": "2025-06-05",
      "value": 480000,
      "status": "active"
    },
    {
      "date": "2025-06-04",
      "value": 460000,
      "status": "active"
    },
    {
      "date": "2025-06-03",
      "value": 440000,
      "status": "active"
    },
    {
      "date": "2025-06-02",
      "value": 420000,
      "status": "active"
    }
  ],
  "notifications": {
    "email": ["compliance_officer@example.com", "cfo@example.com"],
    "webhook": ["https://api.example.com/compliance-alerts"],
    "frequency": "immediate"
  },
  "documentation": {
    "regulatory_reference": "17 CFR 240.15c3-1",
    "internal_policy_reference": "CAP-001",
    "url": "https://www.sec.gov/rules/final/34-31511.pdf"
  },
  "last_checked_at": "2025-06-06T10:00:00Z",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

### Create Compliance Rule

```
POST /compliance/rules
```

Creates a new compliance rule.

#### Request Body

```json
{
  "name": "UCITS Diversification Requirement",
  "portfolio_id": "portfolio_123456",
  "type": "regulatory",
  "category": "diversification",
  "description": "UCITS funds must limit exposure to a single issuer to 5/10/40% of NAV.",
  "parameters": {
    "max_single_issuer_percentage": 5.0,
    "max_sum_large_exposures_percentage": 40.0,
    "large_exposure_threshold_percentage": 5.0
  },
  "notifications": {
    "email": ["compliance_officer@example.com", "portfolio_manager@example.com"],
    "webhook": ["https://api.example.com/compliance-alerts"],
    "frequency": "immediate"
  },
  "documentation": {
    "regulatory_reference": "UCITS Directive 2009/65/EC",
    "internal_policy_reference": "DIV-002",
    "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0065"
  }
}
```

#### Response

```json
{
  "id": "rule_901234",
  "name": "UCITS Diversification Requirement",
  "portfolio_id": "portfolio_123456",
  "type": "regulatory",
  "category": "diversification",
  "description": "UCITS funds must limit exposure to a single issuer to 5/10/40% of NAV.",
  "parameters": {
    "max_single_issuer_percentage": 5.0,
    "max_sum_large_exposures_percentage": 40.0,
    "large_exposure_threshold_percentage": 5.0
  },
  "status": "pending",
  "current_value": null,
  "notifications": {
    "email": ["compliance_officer@example.com", "portfolio_manager@example.com"],
    "webhook": ["https://api.example.com/compliance-alerts"],
    "frequency": "immediate"
  },
  "documentation": {
    "regulatory_reference": "UCITS Directive 2009/65/EC",
    "internal_policy_reference": "DIV-002",
    "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0065"
  },
  "last_checked_at": null,
  "created_at": "2025-06-06T21:30:00Z",
  "updated_at": "2025-06-06T21:30:00Z"
}
```

### Update Compliance Rule

```
PUT /compliance/rules/{rule_id}
```

Updates an existing compliance rule.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `rule_id` | string | The ID of the compliance rule to update |

#### Request Body

```json
{
  "name": "UCITS Diversification Requirement (Updated)",
  "description": "Updated UCITS funds diversification requirements limiting exposure to a single issuer.",
  "parameters": {
    "max_single_issuer_percentage": 5.0,
    "max_sum_large_exposures_percentage": 40.0,
    "large_exposure_threshold_percentage": 5.0,
    "exclude_government_securities": true
  },
  "notifications": {
    "email": ["compliance_officer@example.com", "portfolio_manager@example.com", "cco@example.com"],
    "webhook": ["https://api.example.com/compliance-alerts"],
    "frequency": "immediate"
  }
}
```

#### Response

```json
{
  "id": "rule_901234",
  "name": "UCITS Diversification Requirement (Updated)",
  "portfolio_id": "portfolio_123456",
  "type": "regulatory",
  "category": "diversification",
  "description": "Updated UCITS funds diversification requirements limiting exposure to a single issuer.",
  "parameters": {
    "max_single_issuer_percentage": 5.0,
    "max_sum_large_exposures_percentage": 40.0,
    "large_exposure_threshold_percentage": 5.0,
    "exclude_government_securities": true
  },
  "status": "pending",
  "current_value": null,
  "notifications": {
    "email": ["compliance_officer@example.com", "portfolio_manager@example.com", "cco@example.com"],
    "webhook": ["https://api.example.com/compliance-alerts"],
    "frequency": "immediate"
  },
  "documentation": {
    "regulatory_reference": "UCITS Directive 2009/65/EC",
    "internal_policy_reference": "DIV-002",
    "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0065"
  },
  "last_checked_at": null,
  "created_at": "2025-06-06T21:30:00Z",
  "updated_at": "2025-06-06T21:40:00Z"
}
```

### Delete Compliance Rule

```
DELETE /compliance/rules/{rule_id}
```

Deletes a compliance rule.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `rule_id` | string | The ID of the compliance rule to delete |

#### Response

```json
{
  "success": true,
  "message": "Compliance rule deleted successfully"
}
```

### Check Compliance Rules

```
POST /compliance/check
```

Checks all compliance rules for a portfolio.

#### Request Body

```json
{
  "portfolio_id": "portfolio_123456",
  "calculation_date": "2025-06-06"
}
```

#### Response

```json
{
  "check_id": "compliance_check_123456",
  "portfolio_id": "portfolio_123456",
  "calculation_date": "2025-06-06",
  "rules_checked": 3,
  "rules_violated": 1,
  "rules_warning": 0,
  "rules_active": 2,
  "results": [
    {
      "rule_id": "rule_123456",
      "name": "SEC Rule 15c3-1 Net Capital Requirement",
      "type": "regulatory",
      "category": "capital_adequacy",
      "previous_value": 480000,
      "current_value": 500000,
      "threshold": 250000,
      "previous_status": "active",
      "current_status": "active"
    },
    {
      "rule_id": "rule_789012",
      "name": "Restricted Securities Trading",
      "type": "internal",
      "category": "trading_restrictions",
      "previous_status": "active",
      "current_status": "violated",
      "violations": [
        {
          "symbol": "XYZ",
          "position": 1000,
          "detected_at": "2025-06-06T09:30:00Z"
        }
      ]
    },
    {
      "rule_id": "rule_345678",
      "name": "Client Investment Policy - No Tobacco Stocks",
      "type": "client",
      "category": "esg_restrictions",
      "previous_status": "active",
      "current_status": "active"
    }
  ],
  "created_at": "2025-06-06T22:00:00Z"
}
```

### Get Compliance Violation History

```
GET /compliance/violations
```

Retrieves the history of compliance rule violations.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `portfolio_id` | string | Filter by portfolio ID |
| `rule_id` | string | Filter by rule ID |
| `start_date` | string | Start date in ISO 8601 format (e.g., `2025-01-01`) |
| `end_date` | string | End date in ISO 8601 format (e.g., `2025-06-01`) |
| `status` | string | Filter by violation status (e.g., `active`, `resolved`) |
| `limit` | integer | Maximum number of violations to return (default: 100) |
| `offset` | integer | Number of violations to skip (default: 0) |

#### Response

```json
{
  "violations": [
    {
      "id": "violation_123456",
      "rule_id": "rule_789012",
      "rule_name": "Restricted Securities Trading",
      "portfolio_id": "portfolio_123456",
      "start_date": "2025-06-06T09:30:00Z",
      "end_date": null,
      "status": "active",
      "details": {
        "symbol": "XYZ",
        "position": 1000,
        "restricted_since": "2025-06-01T00:00:00Z",
        "restriction_reason": "Pending merger announcement"
      },
      "resolution_plan": {
        "id": "plan_456789",
        "description": "Liquidate XYZ position immediately",
        "status": "in_progress",
        "due_date": "2025-06-07",
        "assigned_to": "trader@example.com"
      }
    },
    {
      "id": "violation_789012",
      "rule_id": "rule_345678",
      "rule_name": "Client Investment Policy - No Tobacco Stocks",
      "portfolio_id": "portfolio_123456",
      "start_date": "2025-05-15T10:30:00Z",
      "end_date": "2025-05-16T14:00:00Z",
      "status": "resolved",
      "details": {
        "symbol": "BTI",
        "position": 500,
        "detected_at": "2025-05-15T10:30:00Z"
      },
      "resolution_plan": {
        "id": "plan_123789",
        "description": "Liquidate BTI position immediately",
        "status": "completed",
        "due_date": "2025-05-16",
        "assigned_to": "trader@example.com",
        "completed_at": "2025-05-16T14:00:00Z",
        "resolution_notes": "Position liquidated at market price"
      }
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Create Compliance Resolution Plan

```
POST /compliance/violations/{violation_id}/resolution
```

Creates a resolution plan for a compliance rule violation.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `violation_id` | string | The ID of the violation to create a resolution plan for |

#### Request Body

```json
{
  "description": "Liquidate XYZ position immediately due to restricted securities violation",
  "due_date": "2025-06-07",
  "assigned_to": "trader@example.com",
  "steps": [
    {
      "description": "Notify portfolio manager of the violation",
      "due_date": "2025-06-06T23:00:00Z",
      "status": "pending"
    },
    {
      "description": "Prepare liquidation order for XYZ position",
      "due_date": "2025-06-07T09:00:00Z",
      "status": "pending"
    },
    {
      "description": "Execute liquidation order",
      "due_date": "2025-06-07T10:00:00Z",
      "status": "pending"
    },
    {
      "description": "Verify position is closed and update compliance system",
      "due_date": "2025-06-07T11:00:00Z",
      "status": "pending"
    }
  ]
}
```

#### Response

```json
{
  "id": "plan_456789",
  "violation_id": "violation_123456",
  "description": "Liquidate XYZ position immediately due to restricted securities violation",
  "status": "in_progress",
  "due_date": "2025-06-07",
  "assigned_to": "trader@example.com",
  "steps": [
    {
      "id": "step_456789",
      "description": "Notify portfolio manager of the violation",
      "due_date": "2025-06-06T23:00:00Z",
      "status": "pending"
    },
    {
      "id": "step_567890",
      "description": "Prepare liquidation order for XYZ position",
      "due_date": "2025-06-07T09:00:00Z",
      "status": "pending"
    },
    {
      "id": "step_678901",
      "description": "Execute liquidation order",
      "due_date": "2025-06-07T10:00:00Z",
      "status": "pending"
    },
    {
      "id": "step_789012",
      "description": "Verify position is closed and update compliance system",
      "due_date": "2025-06-07T11:00:00Z",
      "status": "pending"
    }
  ],
  "created_at": "2025-06-06T22:30:00Z",
  "updated_at": "2025-06-06T22:30:00Z"
}
```

### Update Compliance Resolution Plan

```
PUT /compliance/violations/{violation_id}/resolution/{plan_id}
```

Updates a resolution plan for a compliance rule violation.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `violation_id` | string | The ID of the violation |
| `plan_id` | string | The ID of the resolution plan to update |

#### Request Body

```json
{
  "status": "in_progress",
  "steps": [
    {
      "id": "step_456789",
      "status": "completed",
      "completed_at": "2025-06-06T22:45:00Z",
      "notes": "Portfolio manager notified via email and phone"
    },
    {
      "id": "step_567890",
      "status": "in_progress",
      "notes": "Liquidation order being prepared for market open"
    },
    {
      "id": "step_678901",
      "status": "pending"
    },
    {
      "id": "step_789012",
      "status": "pending"
    }
  ]
}
```

#### Response

```json
{
  "id": "plan_456789",
  "violation_id": "violation_123456",
  "description": "Liquidate XYZ position immediately due to restricted securities violation",
  "status": "in_progress",
  "due_date": "2025-06-07",
  "assigned_to": "trader@example.com",
  "steps": [
    {
      "id": "step_456789",
      "description": "Notify portfolio manager of the violation",
      "due_date": "2025-06-06T23:00:00Z",
      "status": "completed",
      "completed_at": "2025-06-06T22:45:00Z",
      "notes": "Portfolio manager notified via email and phone"
    },
    {
      "id": "step_567890",
      "description": "Prepare liquidation order for XYZ position",
      "due_date": "2025-06-07T09:00:00Z",
      "status": "in_progress",
      "notes": "Liquidation order being prepared for market open"
    },
    {
      "id": "step_678901",
      "description": "Execute liquidation order",
      "due_date": "2025-06-07T10:00:00Z",
      "status": "pending"
    },
    {
      "id": "step_789012",
      "description": "Verify position is closed and update compliance system",
      "due_date": "2025-06-07T11:00:00Z",
      "status": "pending"
    }
  ],
  "created_at": "2025-06-06T22:30:00Z",
  "updated_at": "2025-06-06T22:45:00Z"
}
```

### Get Restricted Lists

```
GET /compliance/restricted-lists
```

Retrieves a list of all restricted securities lists.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by list type (e.g., `trading`, `research`, `confidential`) |
| `limit` | integer | Maximum number of lists to return (default: 100) |
| `offset` | integer | Number of lists to skip (default: 0) |

#### Response

```json
{
  "restricted_lists": [
    {
      "id": "list_123456",
      "name": "Firm-wide Trading Restricted List",
      "type": "trading",
      "description": "Securities restricted from trading due to material non-public information or conflicts of interest.",
      "securities_count": 25,
      "last_updated_at": "2025-06-05T16:30:00Z",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-06-05T16:30:00Z"
    },
    {
      "id": "list_789012",
      "name": "Research Restricted List",
      "type": "research",
      "description": "Securities restricted from research coverage due to conflicts of interest.",
      "securities_count": 15,
      "last_updated_at": "2025-06-04T14:15:00Z",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-06-04T14:15:00Z"
    },
    {
      "id": "list_345678",
      "name": "Confidential Information List",
      "type": "confidential",
      "description": "Securities for which the firm possesses material non-public information.",
      "securities_count": 10,
      "last_updated_at": "2025-06-06T10:00:00Z",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-06-06T10:00:00Z"
    }
  ],
  "total": 3,
  "limit": 100,
  "offset": 0
}
```

### Get Restricted List

```
GET /compliance/restricted-lists/{list_id}
```

Retrieves a specific restricted securities list by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `list_id` | string | The ID of the restricted list to retrieve |

#### Response

```json
{
  "id": "list_123456",
  "name": "Firm-wide Trading Restricted List",
  "type": "trading",
  "description": "Securities restricted from trading due to material non-public information or conflicts of interest.",
  "securities": [
    {
      "symbol": "XYZ",
      "name": "XYZ Corporation",
      "reason": "Pending merger announcement",
      "restriction_type": "no_trading",
      "added_at": "2025-06-01T00:00:00Z",
      "expiry_at": "2025-07-01T00:00:00Z",
      "added_by": "compliance_officer@example.com"
    },
    {
      "symbol": "ABC",
      "name": "ABC Inc.",
      "reason": "Pending earnings announcement",
      "restriction_type": "no_trading",
      "added_at": "2025-06-03T00:00:00Z",
      "expiry_at": "2025-06-15T00:00:00Z",
      "added_by": "compliance_officer@example.com"
    },
    {
      "symbol": "DEF",
      "name": "DEF Corp.",
      "reason": "Conflict of interest - investment banking relationship",
      "restriction_type": "no_trading",
      "added_at": "2025-05-15T00:00:00Z",
      "expiry_at": null,
      "added_by": "compliance_officer@example.com"
    }
  ],
  "history": [
    {
      "action": "add_security",
      "symbol": "XYZ",
      "timestamp": "2025-06-01T00:00:00Z",
      "user": "compliance_officer@example.com"
    },
    {
      "action": "add_security",
      "symbol": "ABC",
      "timestamp": "2025-06-03T00:00:00Z",
      "user": "compliance_officer@example.com"
    },
    {
      "action": "remove_security",
      "symbol": "GHI",
      "timestamp": "2025-06-05T16:30:00Z",
      "user": "compliance_officer@example.com"
    }
  ],
  "last_updated_at": "2025-06-05T16:30:00Z",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-06-05T16:30:00Z"
}
```

### Add Security to Restricted List

```
POST /compliance/restricted-lists/{list_id}/securities
```

Adds a security to a restricted list.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `list_id` | string | The ID of the restricted list to add the security to |

#### Request Body

```json
{
  "symbol": "JKL",
  "name": "JKL Industries",
  "reason": "Pending acquisition announcement",
  "restriction_type": "no_trading",
  "expiry_at": "2025-07-15T00:00:00Z"
}
```

#### Response

```json
{
  "list_id": "list_123456",
  "symbol": "JKL",
  "name": "JKL Industries",
  "reason": "Pending acquisition announcement",
  "restriction_type": "no_trading",
  "added_at": "2025-06-06T23:00:00Z",
  "expiry_at": "2025-07-15T00:00:00Z",
  "added_by": "compliance_officer@example.com"
}
```

### Remove Security from Restricted List

```
DELETE /compliance/restricted-lists/{list_id}/securities/{symbol}
```

Removes a security from a restricted list.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `list_id` | string | The ID of the restricted list |
| `symbol` | string | The symbol of the security to remove |

#### Response

```json
{
  "success": true,
  "message": "Security JKL removed from restricted list",
  "list_id": "list_123456",
  "symbol": "JKL",
  "removed_at": "2025-06-06T23:15:00Z",
  "removed_by": "compliance_officer@example.com"
}
```

### Generate Compliance Report

```
POST /compliance/reports
```

Generates a compliance report.

#### Request Body

```json
{
  "portfolio_id": "portfolio_123456",
  "report_type": "regulatory",
  "report_name": "SEC Form 13F",
  "as_of_date": "2025-06-30",
  "parameters": {
    "include_positions": true,
    "include_transactions": false,
    "min_position_value": 100000,
    "format": "json"
  }
}
```

#### Response

```json
{
  "report_id": "report_123456",
  "portfolio_id": "portfolio_123456",
  "report_type": "regulatory",
  "report_name": "SEC Form 13F",
  "as_of_date": "2025-06-30",
  "status": "processing",
  "parameters": {
    "include_positions": true,
    "include_transactions": false,
    "min_position_value": 100000,
    "format": "json"
  },
  "created_at": "2025-06-06T23:30:00Z",
  "estimated_completion_time": "2025-06-06T23:35:00Z"
}
```

### Get Compliance Report Status

```
GET /compliance/reports/{report_id}
```

Retrieves the status of a compliance report.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string | The ID of the compliance report |

#### Response

```json
{
  "report_id": "report_123456",
  "portfolio_id": "portfolio_123456",
  "report_type": "regulatory",
  "report_name": "SEC Form 13F",
  "as_of_date": "2025-06-30",
  "status": "completed",
  "parameters": {
    "include_positions": true,
    "include_transactions": false,
    "min_position_value": 100000,
    "format": "json"
  },
  "result": {
    "download_url": "https://api.quantumalpha.com/v1/risk/compliance/reports/report_123456/download",
    "expiry_time": "2025-06-13T23:35:00Z"
  },
  "created_at": "2025-06-06T23:30:00Z",
  "completed_at": "2025-06-06T23:35:00Z"
}
```

### Download Compliance Report

```
GET /compliance/reports/{report_id}/download
```

Downloads a completed compliance report.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | string | The ID of the compliance report to download |

#### Response

The response will be a file download with the appropriate content type based on the requested format (e.g., `application/json`, `application/pdf`, `text/csv`).

For JSON format, the content might look like:

```json
{
  "report_id": "report_123456",
  "portfolio_id": "portfolio_123456",
  "report_type": "regulatory",
  "report_name": "SEC Form 13F",
  "as_of_date": "2025-06-30",
  "generated_at": "2025-06-06T23:35:00Z",
  "reporting_entity": {
    "name": "Example Asset Management",
    "crd_number": "123456",
    "sec_file_number": "028-12345"
  },
  "positions": [
    {
      "name_of_issuer": "Apple Inc.",
      "title_of_class": "Common Stock",
      "cusip": "037833100",
      "value": 5000000,
      "shares": 25000,
      "investment_discretion": "sole",
      "voting_authority": {
        "sole": 25000,
        "shared": 0,
        "none": 0
      }
    },
    {
      "name_of_issuer": "Microsoft Corporation",
      "title_of_class": "Common Stock",
      "cusip": "594918104",
      "value": 4000000,
      "shares": 10000,
      "investment_discretion": "sole",
      "voting_authority": {
        "sole": 10000,
        "shared": 0,
        "none": 0
      }
    },
    {
      "name_of_issuer": "Alphabet Inc.",
      "title_of_class": "Class A Common Stock",
      "cusip": "02079K305",
      "value": 3000000,
      "shares": 2000,
      "investment_discretion": "sole",
      "voting_authority": {
        "sole": 2000,
        "shared": 0,
        "none": 0
      }
    }
  ],
  "summary": {
    "total_positions": 3,
    "total_value": 12000000,
    "total_shares": 37000
  }
}
```
