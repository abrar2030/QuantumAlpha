"""
Simplified Data Service for QuantumAlpha - Deployment Version
This is a minimal version focusing on essential functionality without numpy/pandas
"""

import logging
import os
import random
import traceback
from datetime import datetime, timedelta

from common.logging_config import setup_logging
from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config

# Configure logging
setup_logging(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=app.config["CORS_ORIGINS"])  # Allow all origins for development

# Mock data for demonstration
MOCK_MARKET_DATA = {
    "AAPL": {
        "symbol": "AAPL",
        "price": 175.50,
        "change": 2.30,
        "change_percent": 1.33,
        "volume": 45000000,
        "market_cap": 2800000000000,
    },
    "GOOGL": {
        "symbol": "GOOGL",
        "price": 142.80,
        "change": -1.20,
        "change_percent": -0.83,
        "volume": 28000000,
        "market_cap": 1800000000000,
    },
    "MSFT": {
        "symbol": "MSFT",
        "price": 420.15,
        "change": 5.75,
        "change_percent": 1.39,
        "volume": 32000000,
        "market_cap": 3100000000000,
    },
}


def generate_historical_data(symbol, days=30):
    """Generate mock historical data"""
    base_price = MOCK_MARKET_DATA.get(symbol, {}).get("price", 100)
    data = []

    for i in range(days):
        date = datetime.now() - timedelta(days=days - i)
        price = base_price + (random.random() - 0.5) * 20  # Simple random walk
        data.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "open": price + (random.random() - 0.5) * 4,
                "high": price + random.random() * 10,
                "low": price - random.random() * 10,
                "close": price,
                "volume": int(random.random() * 40000000) + 10000000,
            }
        )

    return data


# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    """Handle errors"""
    logger.error("Unhandled error: %s", error)
    logger.error(traceback.format_exc())

    return (
        jsonify(
            {
                "error": "Internal server error",
                "status_code": 500,
                "details": str(error),
            }
        ),
        500,
    )


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "ok",
            "service": "data_service",
            "timestamp": datetime.now().isoformat(),
        }
    )


# Market data endpoints
@app.route("/api/market-data/<symbol>", methods=["GET"])
def get_market_data(symbol):
    """Get market data for a symbol"""
    try:
        symbol = symbol.upper()

        # Get query parameters
        timeframe = request.args.get("timeframe", "1d")
        period = request.args.get("period", "30d")

        if symbol in MOCK_MARKET_DATA:
            data = MOCK_MARKET_DATA[symbol].copy()

            # Add historical data if requested
            if timeframe == "1d" and period:
                days = int(period.replace("d", "")) if "d" in period else 30
                data["historical"] = generate_historical_data(symbol, days)

            return jsonify(
                {"success": True, "data": data, "timestamp": datetime.now().isoformat()}
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Symbol {symbol} not found",
                        "available_symbols": list(MOCK_MARKET_DATA.keys()),
                    }
                ),
                404,
            )

    except Exception as e:
        logger.error("Error getting market data: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/portfolio", methods=["GET"])
def get_portfolio():
    """Get portfolio data"""
    try:
        portfolio = {
            "total_value": 1250000.00,
            "daily_change": 15750.00,
            "daily_change_percent": 1.28,
            "positions": [
                {
                    "symbol": "AAPL",
                    "shares": 1000,
                    "avg_cost": 165.00,
                    "current_price": 175.50,
                    "market_value": 175500.00,
                    "unrealized_pnl": 10500.00,
                    "weight": 14.04,
                },
                {
                    "symbol": "GOOGL",
                    "shares": 500,
                    "avg_cost": 145.00,
                    "current_price": 142.80,
                    "market_value": 71400.00,
                    "unrealized_pnl": -1100.00,
                    "weight": 5.71,
                },
                {
                    "symbol": "MSFT",
                    "shares": 800,
                    "avg_cost": 410.00,
                    "current_price": 420.15,
                    "market_value": 336120.00,
                    "unrealized_pnl": 8120.00,
                    "weight": 26.89,
                },
            ],
        }

        return jsonify(
            {
                "success": True,
                "data": portfolio,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error("Error getting portfolio: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/strategies", methods=["GET"])
def get_strategies():
    """Get trading strategies"""
    try:
        strategies = [
            {
                "id": 1,
                "name": "Momentum Strategy",
                "description": "Trend-following strategy based on price momentum",
                "status": "active",
                "return_ytd": 12.5,
                "sharpe_ratio": 1.8,
                "max_drawdown": -5.2,
                "positions": 15,
            },
            {
                "id": 2,
                "name": "Mean Reversion",
                "description": "Contrarian strategy exploiting price reversals",
                "status": "active",
                "return_ytd": 8.3,
                "sharpe_ratio": 1.4,
                "max_drawdown": -3.8,
                "positions": 8,
            },
            {
                "id": 3,
                "name": "Pairs Trading",
                "description": "Market-neutral strategy trading correlated pairs",
                "status": "paused",
                "return_ytd": 6.7,
                "sharpe_ratio": 2.1,
                "max_drawdown": -2.1,
                "positions": 12,
            },
        ]

        return jsonify(
            {
                "success": True,
                "data": strategies,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error("Error getting strategies: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/auth/login", methods=["POST"])
def login():
    """Mock login endpoint"""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Mock authentication - accept any email/password for demo
        if email and password:
            return jsonify(
                {
                    "success": True,
                    "data": {
                        "token": "mock_jwt_token_12345",
                        "user": {
                            "id": 1,
                            "email": email,
                            "name": "Demo User",
                            "role": "trader",
                        },
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            )
        else:
            return (
                jsonify({"success": False, "error": "Email and password required"}),
                400,
            )

    except Exception as e:
        logger.error("Error during login: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/auth/user", methods=["GET"])
def get_user():
    """Get current user info"""
    try:
        return jsonify(
            {
                "success": True,
                "data": {
                    "id": 1,
                    "email": "demo@quantumalpha.com",
                    "name": "Demo User",
                    "role": "trader",
                },
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error("Error getting user: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    app.run(host="0.0.0.0", port=port, debug=False)
