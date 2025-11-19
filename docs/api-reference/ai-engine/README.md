# AI Engine API Reference

The AI Engine API allows you to manage machine learning models, predictions, and reinforcement learning environments within the QuantumAlpha platform.

## Table of Contents

1. [Overview](#overview)
2. [Models](#models)
3. [Predictions](#predictions)
4. [Reinforcement Learning](#reinforcement-learning)
5. [Experiments](#experiments)
6. [Model Registry](#model-registry)
7. [Feature Importance](#feature-importance)
8. [Hyperparameter Tuning](#hyperparameter-tuning)

## Overview

The AI Engine API provides endpoints for:

- Creating, training, and managing machine learning models
- Generating predictions from trained models
- Setting up and running reinforcement learning environments
- Tracking experiments and model performance
- Managing the model registry
- Analyzing feature importance
- Performing hyperparameter tuning

Base URL: `https://api.quantumalpha.com/v1/ai`

## Models

### List Models

```
GET /models
```

Retrieves a list of all models.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by model type (e.g., `temporal_fusion_transformer`, `lstm`, `reinforcement_learning`) |
| `status` | string | Filter by model status (e.g., `training`, `ready`, `failed`) |
| `limit` | integer | Maximum number of models to return (default: 100) |
| `offset` | integer | Number of models to skip (default: 0) |

#### Response

```json
{
  "models": [
    {
      "id": "model_123456",
      "name": "TFT-AAPL-Predictor",
      "type": "temporal_fusion_transformer",
      "status": "ready",
      "created_at": "2025-05-01T12:00:00Z",
      "updated_at": "2025-05-02T15:30:00Z",
      "metrics": {
        "accuracy": 0.85,
        "mse": 0.023,
        "mae": 0.15
      }
    },
    {
      "id": "model_789012",
      "name": "LSTM-MSFT-Predictor",
      "type": "lstm",
      "status": "training",
      "created_at": "2025-05-03T09:00:00Z",
      "updated_at": "2025-05-03T09:00:00Z",
      "metrics": null
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Get Model

```
GET /models/{model_id}
```

Retrieves a specific model by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model to retrieve |

#### Response

```json
{
  "id": "model_123456",
  "name": "TFT-AAPL-Predictor",
  "type": "temporal_fusion_transformer",
  "status": "ready",
  "created_at": "2025-05-01T12:00:00Z",
  "updated_at": "2025-05-02T15:30:00Z",
  "parameters": {
    "hidden_size": 128,
    "num_heads": 4,
    "dropout_rate": 0.1
  },
  "metrics": {
    "accuracy": 0.85,
    "mse": 0.023,
    "mae": 0.15
  },
  "features": [
    "price_open",
    "price_high",
    "price_low",
    "price_close",
    "volume",
    "sentiment_score"
  ],
  "target": "price_close_next_day"
}
```

### Create Model

```
POST /models
```

Creates a new model.

#### Request Body

```json
{
  "name": "TFT-AAPL-Predictor",
  "type": "temporal_fusion_transformer",
  "parameters": {
    "hidden_size": 128,
    "num_heads": 4,
    "dropout_rate": 0.1
  },
  "features": [
    "price_open",
    "price_high",
    "price_low",
    "price_close",
    "volume",
    "sentiment_score"
  ],
  "target": "price_close_next_day"
}
```

#### Response

```json
{
  "id": "model_123456",
  "name": "TFT-AAPL-Predictor",
  "type": "temporal_fusion_transformer",
  "status": "created",
  "created_at": "2025-06-06T10:00:00Z",
  "updated_at": "2025-06-06T10:00:00Z",
  "parameters": {
    "hidden_size": 128,
    "num_heads": 4,
    "dropout_rate": 0.1
  },
  "features": [
    "price_open",
    "price_high",
    "price_low",
    "price_close",
    "volume",
    "sentiment_score"
  ],
  "target": "price_close_next_day"
}
```

### Train Model

```
POST /models/{model_id}/train
```

Trains a model with the specified dataset and hyperparameters.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model to train |

#### Request Body

```json
{
  "dataset_id": "dataset_123456",
  "hyperparameters": {
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 100
  },
  "validation_split": 0.2,
  "callbacks": [
    {
      "type": "early_stopping",
      "parameters": {
        "patience": 10,
        "monitor": "val_loss"
      }
    }
  ]
}
```

#### Response

```json
{
  "job_id": "job_123456",
  "model_id": "model_123456",
  "status": "queued",
  "created_at": "2025-06-06T10:05:00Z"
}
```

### Get Training Job

```
GET /models/{model_id}/train/{job_id}
```

Retrieves the status of a training job.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model |
| `job_id` | string | The ID of the training job |

#### Response

```json
{
  "job_id": "job_123456",
  "model_id": "model_123456",
  "status": "running",
  "created_at": "2025-06-06T10:05:00Z",
  "started_at": "2025-06-06T10:06:00Z",
  "progress": {
    "current_epoch": 45,
    "total_epochs": 100,
    "metrics": {
      "loss": 0.05,
      "val_loss": 0.07
    }
  }
}
```

### Delete Model

```
DELETE /models/{model_id}
```

Deletes a model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model to delete |

#### Response

```json
{
  "success": true,
  "message": "Model deleted successfully"
}
```

## Predictions

### Create Prediction

```
POST /predictions
```

Generates predictions using a trained model.

#### Request Body

```json
{
  "model_id": "model_123456",
  "data": {
    "features": [
      {
        "price_open": 150.25,
        "price_high": 152.30,
        "price_low": 149.80,
        "price_close": 151.75,
        "volume": 1250000,
        "sentiment_score": 0.65
      },
      {
        "price_open": 151.75,
        "price_high": 153.50,
        "price_low": 151.00,
        "price_close": 153.25,
        "volume": 1350000,
        "sentiment_score": 0.70
      }
    ],
    "timestamps": [
      "2025-06-05T16:00:00Z",
      "2025-06-06T16:00:00Z"
    ]
  }
}
```

#### Response

```json
{
  "prediction_id": "pred_123456",
  "model_id": "model_123456",
  "created_at": "2025-06-06T10:10:00Z",
  "predictions": [
    {
      "timestamp": "2025-06-07T16:00:00Z",
      "value": 154.75,
      "confidence_interval": {
        "lower": 153.50,
        "upper": 156.00
      }
    }
  ]
}
```

### Get Prediction

```
GET /predictions/{prediction_id}
```

Retrieves a specific prediction by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prediction_id` | string | The ID of the prediction to retrieve |

#### Response

```json
{
  "prediction_id": "pred_123456",
  "model_id": "model_123456",
  "created_at": "2025-06-06T10:10:00Z",
  "predictions": [
    {
      "timestamp": "2025-06-07T16:00:00Z",
      "value": 154.75,
      "confidence_interval": {
        "lower": 153.50,
        "upper": 156.00
      }
    }
  ]
}
```

### List Predictions

```
GET /predictions
```

Retrieves a list of predictions.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | Filter by model ID |
| `start_date` | string | Filter by creation date (ISO 8601 format) |
| `end_date` | string | Filter by creation date (ISO 8601 format) |
| `limit` | integer | Maximum number of predictions to return (default: 100) |
| `offset` | integer | Number of predictions to skip (default: 0) |

#### Response

```json
{
  "predictions": [
    {
      "prediction_id": "pred_123456",
      "model_id": "model_123456",
      "created_at": "2025-06-06T10:10:00Z"
    },
    {
      "prediction_id": "pred_789012",
      "model_id": "model_123456",
      "created_at": "2025-06-05T14:30:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

## Reinforcement Learning

### List RL Environments

```
GET /rl-environments
```

Retrieves a list of reinforcement learning environments.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by environment status (e.g., `active`, `inactive`) |
| `limit` | integer | Maximum number of environments to return (default: 100) |
| `offset` | integer | Number of environments to skip (default: 0) |

#### Response

```json
{
  "environments": [
    {
      "id": "env_123456",
      "name": "StockTradingEnv-AAPL",
      "status": "active",
      "created_at": "2025-05-01T12:00:00Z",
      "updated_at": "2025-05-02T15:30:00Z"
    },
    {
      "id": "env_789012",
      "name": "PortfolioOptimizationEnv",
      "status": "inactive",
      "created_at": "2025-05-03T09:00:00Z",
      "updated_at": "2025-05-03T09:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Create RL Environment

```
POST /rl-environments
```

Creates a new reinforcement learning environment.

#### Request Body

```json
{
  "name": "StockTradingEnv-AAPL",
  "type": "stock_trading",
  "parameters": {
    "symbols": ["AAPL"],
    "initial_balance": 100000,
    "commission": 0.001,
    "reward_function": "sharpe_ratio",
    "state_space": [
      "price_history",
      "volume_history",
      "position",
      "balance"
    ],
    "action_space": "discrete"
  },
  "data_source": {
    "type": "historical",
    "dataset_id": "dataset_123456",
    "start_date": "2024-01-01",
    "end_date": "2025-01-01"
  }
}
```

#### Response

```json
{
  "id": "env_123456",
  "name": "StockTradingEnv-AAPL",
  "type": "stock_trading",
  "status": "created",
  "created_at": "2025-06-06T10:15:00Z",
  "updated_at": "2025-06-06T10:15:00Z",
  "parameters": {
    "symbols": ["AAPL"],
    "initial_balance": 100000,
    "commission": 0.001,
    "reward_function": "sharpe_ratio",
    "state_space": [
      "price_history",
      "volume_history",
      "position",
      "balance"
    ],
    "action_space": "discrete"
  },
  "data_source": {
    "type": "historical",
    "dataset_id": "dataset_123456",
    "start_date": "2024-01-01",
    "end_date": "2025-01-01"
  }
}
```

### Train RL Agent

```
POST /rl-environments/{environment_id}/train
```

Trains a reinforcement learning agent in the specified environment.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `environment_id` | string | The ID of the environment |

#### Request Body

```json
{
  "agent_type": "ppo",
  "hyperparameters": {
    "learning_rate": 0.0003,
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "clip_range_vf": null,
    "ent_coef": 0.0,
    "vf_coef": 0.5,
    "max_grad_norm": 0.5
  },
  "network_architecture": {
    "policy_network": [64, 64],
    "value_network": [64, 64]
  },
  "total_timesteps": 1000000,
  "eval_freq": 10000
}
```

#### Response

```json
{
  "job_id": "job_123456",
  "environment_id": "env_123456",
  "agent_id": "agent_123456",
  "status": "queued",
  "created_at": "2025-06-06T10:20:00Z"
}
```

### Get RL Training Job

```
GET /rl-environments/{environment_id}/train/{job_id}
```

Retrieves the status of a reinforcement learning training job.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `environment_id` | string | The ID of the environment |
| `job_id` | string | The ID of the training job |

#### Response

```json
{
  "job_id": "job_123456",
  "environment_id": "env_123456",
  "agent_id": "agent_123456",
  "status": "running",
  "created_at": "2025-06-06T10:20:00Z",
  "started_at": "2025-06-06T10:21:00Z",
  "progress": {
    "timesteps": 250000,
    "total_timesteps": 1000000,
    "metrics": {
      "mean_reward": 125.5,
      "std_reward": 45.2,
      "max_reward": 350.0,
      "min_reward": -50.0
    }
  }
}
```

### Run RL Agent

```
POST /rl-environments/{environment_id}/agents/{agent_id}/run
```

Runs a trained reinforcement learning agent in the specified environment.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `environment_id` | string | The ID of the environment |
| `agent_id` | string | The ID of the agent |

#### Request Body

```json
{
  "episodes": 10,
  "render": false,
  "data_source": {
    "type": "historical",
    "dataset_id": "dataset_789012",
    "start_date": "2025-01-01",
    "end_date": "2025-06-01"
  }
}
```

#### Response

```json
{
  "run_id": "run_123456",
  "environment_id": "env_123456",
  "agent_id": "agent_123456",
  "status": "queued",
  "created_at": "2025-06-06T10:25:00Z"
}
```

### Get RL Run Results

```
GET /rl-environments/{environment_id}/agents/{agent_id}/runs/{run_id}
```

Retrieves the results of a reinforcement learning agent run.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `environment_id` | string | The ID of the environment |
| `agent_id` | string | The ID of the agent |
| `run_id` | string | The ID of the run |

#### Response

```json
{
  "run_id": "run_123456",
  "environment_id": "env_123456",
  "agent_id": "agent_123456",
  "status": "completed",
  "created_at": "2025-06-06T10:25:00Z",
  "completed_at": "2025-06-06T10:26:00Z",
  "results": {
    "episodes": 10,
    "mean_reward": 1250.75,
    "std_reward": 350.25,
    "max_reward": 2500.0,
    "min_reward": 500.0,
    "total_timesteps": 2500,
    "metrics": {
      "sharpe_ratio": 1.85,
      "max_drawdown": 0.15,
      "win_rate": 0.65
    },
    "episode_rewards": [
      1200.0,
      1500.0,
      900.0,
      1100.0,
      1300.0,
      1400.0,
      2500.0,
      500.0,
      1200.0,
      1600.0
    ]
  }
}
```

## Experiments

### List Experiments

```
GET /experiments
```

Retrieves a list of experiments.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by experiment status (e.g., `running`, `completed`, `failed`) |
| `limit` | integer | Maximum number of experiments to return (default: 100) |
| `offset` | integer | Number of experiments to skip (default: 0) |

#### Response

```json
{
  "experiments": [
    {
      "id": "exp_123456",
      "name": "TFT-Hyperparameter-Tuning",
      "status": "completed",
      "created_at": "2025-05-01T12:00:00Z",
      "updated_at": "2025-05-02T15:30:00Z"
    },
    {
      "id": "exp_789012",
      "name": "LSTM-Feature-Selection",
      "status": "running",
      "created_at": "2025-06-05T09:00:00Z",
      "updated_at": "2025-06-05T09:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

### Create Experiment

```
POST /experiments
```

Creates a new experiment.

#### Request Body

```json
{
  "name": "TFT-Hyperparameter-Tuning",
  "description": "Hyperparameter tuning for Temporal Fusion Transformer",
  "model_type": "temporal_fusion_transformer",
  "dataset_id": "dataset_123456",
  "features": [
    "price_open",
    "price_high",
    "price_low",
    "price_close",
    "volume",
    "sentiment_score"
  ],
  "target": "price_close_next_day",
  "hyperparameter_space": {
    "hidden_size": {
      "type": "int",
      "min": 32,
      "max": 256,
      "step": 32
    },
    "num_heads": {
      "type": "int",
      "min": 1,
      "max": 8,
      "step": 1
    },
    "dropout_rate": {
      "type": "float",
      "min": 0.0,
      "max": 0.5,
      "step": 0.1
    },
    "learning_rate": {
      "type": "float",
      "min": 0.0001,
      "max": 0.01,
      "log": true
    }
  },
  "optimization_metric": "val_loss",
  "optimization_direction": "minimize",
  "max_trials": 20,
  "parallel_trials": 4
}
```

#### Response

```json
{
  "id": "exp_123456",
  "name": "TFT-Hyperparameter-Tuning",
  "description": "Hyperparameter tuning for Temporal Fusion Transformer",
  "status": "created",
  "created_at": "2025-06-06T10:30:00Z",
  "updated_at": "2025-06-06T10:30:00Z",
  "model_type": "temporal_fusion_transformer",
  "dataset_id": "dataset_123456",
  "features": [
    "price_open",
    "price_high",
    "price_low",
    "price_close",
    "volume",
    "sentiment_score"
  ],
  "target": "price_close_next_day",
  "hyperparameter_space": {
    "hidden_size": {
      "type": "int",
      "min": 32,
      "max": 256,
      "step": 32
    },
    "num_heads": {
      "type": "int",
      "min": 1,
      "max": 8,
      "step": 1
    },
    "dropout_rate": {
      "type": "float",
      "min": 0.0,
      "max": 0.5,
      "step": 0.1
    },
    "learning_rate": {
      "type": "float",
      "min": 0.0001,
      "max": 0.01,
      "log": true
    }
  },
  "optimization_metric": "val_loss",
  "optimization_direction": "minimize",
  "max_trials": 20,
  "parallel_trials": 4
}
```

### Start Experiment

```
POST /experiments/{experiment_id}/start
```

Starts an experiment.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `experiment_id` | string | The ID of the experiment to start |

#### Response

```json
{
  "id": "exp_123456",
  "status": "running",
  "started_at": "2025-06-06T10:35:00Z",
  "updated_at": "2025-06-06T10:35:00Z"
}
```

### Get Experiment

```
GET /experiments/{experiment_id}
```

Retrieves a specific experiment by ID.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `experiment_id` | string | The ID of the experiment to retrieve |

#### Response

```json
{
  "id": "exp_123456",
  "name": "TFT-Hyperparameter-Tuning",
  "description": "Hyperparameter tuning for Temporal Fusion Transformer",
  "status": "running",
  "created_at": "2025-06-06T10:30:00Z",
  "started_at": "2025-06-06T10:35:00Z",
  "updated_at": "2025-06-06T10:40:00Z",
  "model_type": "temporal_fusion_transformer",
  "dataset_id": "dataset_123456",
  "features": [
    "price_open",
    "price_high",
    "price_low",
    "price_close",
    "volume",
    "sentiment_score"
  ],
  "target": "price_close_next_day",
  "hyperparameter_space": {
    "hidden_size": {
      "type": "int",
      "min": 32,
      "max": 256,
      "step": 32
    },
    "num_heads": {
      "type": "int",
      "min": 1,
      "max": 8,
      "step": 1
    },
    "dropout_rate": {
      "type": "float",
      "min": 0.0,
      "max": 0.5,
      "step": 0.1
    },
    "learning_rate": {
      "type": "float",
      "min": 0.0001,
      "max": 0.01,
      "log": true
    }
  },
  "optimization_metric": "val_loss",
  "optimization_direction": "minimize",
  "max_trials": 20,
  "parallel_trials": 4,
  "progress": {
    "completed_trials": 5,
    "total_trials": 20,
    "best_trial": {
      "trial_id": "trial_123456",
      "hyperparameters": {
        "hidden_size": 128,
        "num_heads": 4,
        "dropout_rate": 0.2,
        "learning_rate": 0.001
      },
      "metrics": {
        "val_loss": 0.05,
        "val_accuracy": 0.92
      }
    }
  }
}
```

### Get Experiment Trials

```
GET /experiments/{experiment_id}/trials
```

Retrieves the trials for a specific experiment.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `experiment_id` | string | The ID of the experiment |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by trial status (e.g., `running`, `completed`, `failed`) |
| `sort_by` | string | Sort by field (e.g., `created_at`, `val_loss`) |
| `sort_order` | string | Sort order (`asc` or `desc`) |
| `limit` | integer | Maximum number of trials to return (default: 100) |
| `offset` | integer | Number of trials to skip (default: 0) |

#### Response

```json
{
  "trials": [
    {
      "trial_id": "trial_123456",
      "experiment_id": "exp_123456",
      "status": "completed",
      "created_at": "2025-06-06T10:35:00Z",
      "completed_at": "2025-06-06T10:38:00Z",
      "hyperparameters": {
        "hidden_size": 128,
        "num_heads": 4,
        "dropout_rate": 0.2,
        "learning_rate": 0.001
      },
      "metrics": {
        "val_loss": 0.05,
        "val_accuracy": 0.92
      }
    },
    {
      "trial_id": "trial_789012",
      "experiment_id": "exp_123456",
      "status": "completed",
      "created_at": "2025-06-06T10:35:00Z",
      "completed_at": "2025-06-06T10:39:00Z",
      "hyperparameters": {
        "hidden_size": 64,
        "num_heads": 2,
        "dropout_rate": 0.1,
        "learning_rate": 0.0005
      },
      "metrics": {
        "val_loss": 0.07,
        "val_accuracy": 0.90
      }
    }
  ],
  "total": 5,
  "limit": 100,
  "offset": 0
}
```

### Stop Experiment

```
POST /experiments/{experiment_id}/stop
```

Stops a running experiment.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `experiment_id` | string | The ID of the experiment to stop |

#### Response

```json
{
  "id": "exp_123456",
  "status": "stopping",
  "updated_at": "2025-06-06T10:45:00Z"
}
```

## Model Registry

### List Model Versions

```
GET /registry/{model_name}/versions
```

Retrieves all versions of a model in the registry.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | string | The name of the model |

#### Response

```json
{
  "model_name": "TFT-AAPL-Predictor",
  "versions": [
    {
      "version": 3,
      "model_id": "model_123456",
      "status": "production",
      "created_at": "2025-06-01T12:00:00Z",
      "metrics": {
        "accuracy": 0.85,
        "mse": 0.023,
        "mae": 0.15
      }
    },
    {
      "version": 2,
      "model_id": "model_789012",
      "status": "archived",
      "created_at": "2025-05-15T10:00:00Z",
      "metrics": {
        "accuracy": 0.82,
        "mse": 0.028,
        "mae": 0.17
      }
    },
    {
      "version": 1,
      "model_id": "model_345678",
      "status": "archived",
      "created_at": "2025-05-01T09:00:00Z",
      "metrics": {
        "accuracy": 0.80,
        "mse": 0.030,
        "mae": 0.18
      }
    }
  ]
}
```

### Register Model Version

```
POST /registry/{model_name}/versions
```

Registers a new version of a model in the registry.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | string | The name of the model |

#### Request Body

```json
{
  "model_id": "model_123456",
  "description": "Improved TFT model with additional features",
  "metrics": {
    "accuracy": 0.85,
    "mse": 0.023,
    "mae": 0.15
  },
  "tags": ["production-ready", "high-accuracy"]
}
```

#### Response

```json
{
  "model_name": "TFT-AAPL-Predictor",
  "version": 3,
  "model_id": "model_123456",
  "status": "registered",
  "created_at": "2025-06-06T11:00:00Z",
  "description": "Improved TFT model with additional features",
  "metrics": {
    "accuracy": 0.85,
    "mse": 0.023,
    "mae": 0.15
  },
  "tags": ["production-ready", "high-accuracy"]
}
```

### Update Model Version Status

```
PATCH /registry/{model_name}/versions/{version}
```

Updates the status of a model version in the registry.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | string | The name of the model |
| `version` | integer | The version of the model |

#### Request Body

```json
{
  "status": "production"
}
```

#### Response

```json
{
  "model_name": "TFT-AAPL-Predictor",
  "version": 3,
  "model_id": "model_123456",
  "status": "production",
  "updated_at": "2025-06-06T11:05:00Z"
}
```

## Feature Importance

### Get Feature Importance

```
GET /models/{model_id}/feature-importance
```

Retrieves feature importance for a specific model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model |

#### Response

```json
{
  "model_id": "model_123456",
  "feature_importance": [
    {
      "feature": "price_close",
      "importance": 0.35,
      "rank": 1
    },
    {
      "feature": "volume",
      "importance": 0.25,
      "rank": 2
    },
    {
      "feature": "sentiment_score",
      "importance": 0.20,
      "rank": 3
    },
    {
      "feature": "price_high",
      "importance": 0.10,
      "rank": 4
    },
    {
      "feature": "price_low",
      "importance": 0.07,
      "rank": 5
    },
    {
      "feature": "price_open",
      "importance": 0.03,
      "rank": 6
    }
  ],
  "method": "shap",
  "created_at": "2025-06-06T11:10:00Z"
}
```

### Calculate Feature Importance

```
POST /models/{model_id}/feature-importance
```

Calculates feature importance for a specific model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model |

#### Request Body

```json
{
  "method": "shap",
  "dataset_id": "dataset_123456",
  "num_samples": 1000
}
```

#### Response

```json
{
  "job_id": "job_123456",
  "model_id": "model_123456",
  "status": "queued",
  "created_at": "2025-06-06T11:15:00Z"
}
```

## Hyperparameter Tuning

### Create Hyperparameter Tuning Job

```
POST /models/{model_id}/hyperparameter-tuning
```

Creates a hyperparameter tuning job for a specific model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model |

#### Request Body

```json
{
  "dataset_id": "dataset_123456",
  "hyperparameter_space": {
    "learning_rate": {
      "type": "float",
      "min": 0.0001,
      "max": 0.01,
      "log": true
    },
    "batch_size": {
      "type": "int",
      "values": [32, 64, 128, 256]
    },
    "dropout_rate": {
      "type": "float",
      "min": 0.0,
      "max": 0.5,
      "step": 0.1
    }
  },
  "optimization_metric": "val_loss",
  "optimization_direction": "minimize",
  "max_trials": 20,
  "parallel_trials": 4,
  "early_stopping": {
    "patience": 5,
    "min_delta": 0.001
  }
}
```

#### Response

```json
{
  "job_id": "job_123456",
  "model_id": "model_123456",
  "status": "queued",
  "created_at": "2025-06-06T11:20:00Z"
}
```

### Get Hyperparameter Tuning Job

```
GET /models/{model_id}/hyperparameter-tuning/{job_id}
```

Retrieves the status of a hyperparameter tuning job.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model |
| `job_id` | string | The ID of the hyperparameter tuning job |

#### Response

```json
{
  "job_id": "job_123456",
  "model_id": "model_123456",
  "status": "running",
  "created_at": "2025-06-06T11:20:00Z",
  "started_at": "2025-06-06T11:21:00Z",
  "progress": {
    "completed_trials": 8,
    "total_trials": 20,
    "best_trial": {
      "trial_id": "trial_123456",
      "hyperparameters": {
        "learning_rate": 0.001,
        "batch_size": 64,
        "dropout_rate": 0.2
      },
      "metrics": {
        "val_loss": 0.05,
        "val_accuracy": 0.92
      }
    }
  }
}
```

### Get Hyperparameter Tuning Results

```
GET /models/{model_id}/hyperparameter-tuning/{job_id}/results
```

Retrieves the results of a completed hyperparameter tuning job.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | The ID of the model |
| `job_id` | string | The ID of the hyperparameter tuning job |

#### Response

```json
{
  "job_id": "job_123456",
  "model_id": "model_123456",
  "status": "completed",
  "created_at": "2025-06-06T11:20:00Z",
  "started_at": "2025-06-06T11:21:00Z",
  "completed_at": "2025-06-06T12:30:00Z",
  "results": {
    "best_trial": {
      "trial_id": "trial_123456",
      "hyperparameters": {
        "learning_rate": 0.001,
        "batch_size": 64,
        "dropout_rate": 0.2
      },
      "metrics": {
        "val_loss": 0.05,
        "val_accuracy": 0.92
      }
    },
    "all_trials": [
      {
        "trial_id": "trial_123456",
        "hyperparameters": {
          "learning_rate": 0.001,
          "batch_size": 64,
          "dropout_rate": 0.2
        },
        "metrics": {
          "val_loss": 0.05,
          "val_accuracy": 0.92
        }
      },
      {
        "trial_id": "trial_789012",
        "hyperparameters": {
          "learning_rate": 0.0005,
          "batch_size": 128,
          "dropout_rate": 0.1
        },
        "metrics": {
          "val_loss": 0.06,
          "val_accuracy": 0.91
        }
      }
    ],
    "parameter_importance": {
      "learning_rate": 0.6,
      "batch_size": 0.3,
      "dropout_rate": 0.1
    }
  }
}
```
