"""
Helper functions for QuantumAlpha tests.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd


def load_test_data(filename: str) -> Dict[str, Any]:
    """
    Load test data from a JSON file.

    Args:
        filename: Name of the JSON file in the fixtures directory

    Returns:
        Dictionary containing the test data
    """
    fixtures_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fixtures"
    )
    file_path = os.path.join(fixtures_dir, filename)

    with open(file_path, "r") as f:
        data = json.load(f)

    return data


def generate_market_data(
    symbol: str,
    start_date: str,
    end_date: Optional[str] = None,
    periods: Optional[int] = None,
    start_price: float = 100.0,
    volatility: float = 0.01,
) -> List[Dict[str, Any]]:
    """
    Generate synthetic market data for testing.

    Args:
        symbol: Stock symbol
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (optional)
        periods: Number of periods to generate (optional, used if end_date is not provided)
        start_price: Initial price
        volatility: Price volatility

    Returns:
        List of dictionaries containing market data
    """
    if end_date:
        dates = pd.date_range(start=start_date, end=end_date)
    else:
        dates = pd.date_range(start=start_date, periods=periods or 30)

    data = []
    price = start_price

    for date in dates:
        # Generate random price movement
        price = price * (1 + np.random.normal(0, volatility))

        # Generate random volume
        volume = int(1000000 + np.random.normal(0, 100000))

        # Create data point
        data_point = {
            "timestamp": date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "open": round(price * (1 - 0.005), 2),
            "high": round(price * (1 + 0.01), 2),
            "low": round(price * (1 - 0.01), 2),
            "close": round(price, 2),
            "volume": volume,
            "symbol": symbol,
        }

        data.append(data_point)

    return data


def calculate_returns(prices: np.ndarray) -> np.ndarray:
    """
    Calculate returns from price data.

    Args:
        prices: Array of prices

    Returns:
        Array of returns
    """
    return np.diff(prices) / prices[:-1]


def calculate_metrics(actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
    """
    Calculate performance metrics for predictions.

    Args:
        actual: Array of actual values
        predicted: Array of predicted values

    Returns:
        Dictionary of metrics
    """
    from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                                 r2_score)

    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)

    return {"mse": float(mse), "rmse": float(rmse), "mae": float(mae), "r2": float(r2)}


def create_test_user(
    user_id: Optional[str] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a test user.

    Args:
        user_id: User ID (optional)
        username: Username (optional)
        email: Email (optional)

    Returns:
        Dictionary containing user data
    """
    return {
        "id": user_id or "user_test",
        "username": username or "testuser",
        "email": email or "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "created_at": datetime.utcnow().isoformat(),
        "last_login": datetime.utcnow().isoformat(),
    }


def create_test_portfolio(
    portfolio_id: Optional[str] = None,
    user_id: Optional[str] = None,
    name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a test portfolio.

    Args:
        portfolio_id: Portfolio ID (optional)
        user_id: User ID (optional)
        name: Portfolio name (optional)

    Returns:
        Dictionary containing portfolio data
    """
    return {
        "id": portfolio_id or "portfolio_test",
        "user_id": user_id or "user_test",
        "name": name or "Test Portfolio",
        "description": "Portfolio for testing",
        "initial_balance": 100000.0,
        "current_balance": 105000.0,
        "currency": "USD",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "positions": [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "entry_price": 150.0,
                "current_price": 155.0,
            },
            {
                "symbol": "MSFT",
                "quantity": 50,
                "entry_price": 250.0,
                "current_price": 260.0,
            },
        ],
    }


def create_test_strategy(
    strategy_id: Optional[str] = None,
    user_id: Optional[str] = None,
    name: Optional[str] = None,
    strategy_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a test strategy.

    Args:
        strategy_id: Strategy ID (optional)
        user_id: User ID (optional)
        name: Strategy name (optional)
        strategy_type: Strategy type (optional)

    Returns:
        Dictionary containing strategy data
    """
    return {
        "id": strategy_id or "strategy_test",
        "user_id": user_id or "user_test",
        "name": name or "Test Strategy",
        "description": "Strategy for testing",
        "type": strategy_type or "trend_following",
        "status": "active",
        "config": {
            "timeframe": "1d",
            "symbols": ["AAPL", "MSFT", "GOOGL"],
            "parameters": {
                "sma_fast": 20,
                "sma_slow": 50,
                "rsi_period": 14,
                "rsi_overbought": 70,
                "rsi_oversold": 30,
            },
        },
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }


def create_test_model(
    model_id: Optional[str] = None,
    strategy_id: Optional[str] = None,
    name: Optional[str] = None,
    model_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a test model.

    Args:
        model_id: Model ID (optional)
        strategy_id: Strategy ID (optional)
        name: Model name (optional)
        model_type: Model type (optional)

    Returns:
        Dictionary containing model data
    """
    return {
        "id": model_id or "model_test",
        "strategy_id": strategy_id or "strategy_test",
        "name": name or "Test Model",
        "type": model_type or "lstm",
        "status": "active",
        "config": {
            "layers": [50, 100, 50],
            "dropout": 0.2,
            "activation": "relu",
            "optimizer": "adam",
            "loss": "mse",
            "epochs": 100,
            "batch_size": 32,
        },
        "performance": {"mse": 0.0025, "rmse": 0.05, "mae": 0.04, "r2": 0.85},
        "registry_path": "/models/model_test",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "last_trained": datetime.utcnow().isoformat(),
    }


def create_test_signal(
    signal_id: Optional[str] = None,
    strategy_id: Optional[str] = None,
    model_id: Optional[str] = None,
    symbol: Optional[str] = None,
    direction: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a test signal.

    Args:
        signal_id: Signal ID (optional)
        strategy_id: Strategy ID (optional)
        model_id: Model ID (optional)
        symbol: Symbol (optional)
        direction: Direction (optional)

    Returns:
        Dictionary containing signal data
    """
    return {
        "id": signal_id or "signal_test",
        "strategy_id": strategy_id or "strategy_test",
        "model_id": model_id or "model_test",
        "symbol": symbol or "AAPL",
        "direction": direction or "buy",
        "strength": 0.8,
        "confidence": 0.75,
        "target_price": 160.0,
        "stop_loss": 145.0,
        "timestamp": datetime.utcnow().isoformat(),
        "expiration": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    }


def create_test_order(
    order_id: Optional[str] = None,
    user_id: Optional[str] = None,
    portfolio_id: Optional[str] = None,
    strategy_id: Optional[str] = None,
    signal_id: Optional[str] = None,
    symbol: Optional[str] = None,
    side: Optional[str] = None,
    order_type: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a test order.

    Args:
        order_id: Order ID (optional)
        user_id: User ID (optional)
        portfolio_id: Portfolio ID (optional)
        strategy_id: Strategy ID (optional)
        signal_id: Signal ID (optional)
        symbol: Symbol (optional)
        side: Side (optional)
        order_type: Order type (optional)
        status: Status (optional)

    Returns:
        Dictionary containing order data
    """
    return {
        "id": order_id or "order_test",
        "user_id": user_id or "user_test",
        "portfolio_id": portfolio_id or "portfolio_test",
        "strategy_id": strategy_id or "strategy_test",
        "signal_id": signal_id or "signal_test",
        "symbol": symbol or "AAPL",
        "side": side or "buy",
        "type": order_type or "market",
        "status": status or "filled",
        "quantity": 100,
        "price": 150.0,
        "filled_quantity": 100,
        "average_fill_price": 150.0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "broker_order_id": "broker_test",
    }
