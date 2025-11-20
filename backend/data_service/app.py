"""
Data Service for QuantumAlpha
This service is responsible for:
1. Market data collection from various sources
2. Alternative data processing
3. Feature engineering
4. Data storage and retrieval
"""

import logging
import os
import sys
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import (
    ServiceError,
    get_config_manager,
    get_db_manager,
    setup_logger,
    validate_schema,
)
from common.validation import MarketDataRequest
from data_service.alternative_data import AlternativeDataService
from data_service.feature_engineering import FeatureEngineeringService

# Import service modules
from data_service.market_data import MarketDataService

# Configure logging
logger = setup_logger("data_service", logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config_manager = get_config_manager(
    env_file=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", ".env"
    )
)

# Initialize database manager
db_manager = get_db_manager(config_manager.get_all())

# Initialize services
market_data_service = MarketDataService(config_manager, db_manager)
alternative_data_service = AlternativeDataService(config_manager, db_manager)
feature_engineering_service = FeatureEngineeringService(config_manager, db_manager)


# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    """Handle errors"""
    if isinstance(error, ServiceError):
        return jsonify(error.to_dict()), error.status_code

    logger.error(f"Unhandled error: {error}")
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
    return jsonify({"status": "ok", "service": "data_service"})


# Market data endpoints
@app.route("/api/market-data/<symbol>", methods=["GET"])
def get_market_data(symbol):
    """Get market data for a symbol"""
    try:
        # Validate request parameters
        params = {
            "symbol": symbol,
            "timeframe": request.args.get("timeframe", "1d"),
            "period": request.args.get("period"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
        }

        validated_params = validate_schema(params, MarketDataRequest)

        # Get market data
        data = market_data_service.get_market_data(
            symbol=validated_params["symbol"],
            timeframe=validated_params["timeframe"],
            period=validated_params["period"],
            start_date=validated_params["start_date"],
            end_date=validated_params["end_date"],
        )

        return jsonify(data)

    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))


@app.route("/api/alternative-data/<source>", methods=["GET"])
def get_alternative_data(source):
    """Get alternative data from a source"""
    try:
        # Get request parameters
        symbol = request.args.get("symbol")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        # Get alternative data
        data = alternative_data_service.get_alternative_data(
            source=source, symbol=symbol, start_date=start_date, end_date=end_date
        )

        return jsonify(data)

    except Exception as e:
        logger.error(f"Error getting alternative data: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))


@app.route("/api/features/<symbol>", methods=["GET"])
def get_features(symbol):
    """Get engineered features for a symbol"""
    try:
        # Get request parameters
        timeframe = request.args.get("timeframe", "1d")
        features = (
            request.args.get("features", "").split(",")
            if request.args.get("features")
            else None
        )

        # Get features
        data = feature_engineering_service.get_features(
            symbol=symbol, timeframe=timeframe, features=features
        )

        return jsonify(data)

    except Exception as e:
        logger.error(f"Error getting features: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))


# Data source management endpoints
@app.route("/api/data-sources", methods=["GET"])
def get_data_sources():
    """Get all data sources"""
    try:
        # Get data sources
        data_sources = market_data_service.get_data_sources()

        return jsonify({"data_sources": data_sources})

    except Exception as e:
        logger.error(f"Error getting data sources: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))


@app.route("/api/data-sources", methods=["POST"])
def create_data_source():
    """Create a new data source"""
    try:
        # Get request data
        data = request.json

        # Create data source
        data_source = market_data_service.create_data_source(data)

        return jsonify(data_source)

    except Exception as e:
        logger.error(f"Error creating data source: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
