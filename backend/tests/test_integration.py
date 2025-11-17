"""
Integration tests for QuantumAlpha backend services.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import ServiceError, ValidationError, NotFoundError
from common.config import ConfigManager
from common.database import DatabaseManager


class TestServiceIntegration(unittest.TestCase):
    """Integration tests for service communication"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Initialize config manager
        cls.config_manager = ConfigManager()

        # Initialize database manager
        cls.db_manager = DatabaseManager(cls.config_manager)

        # Service URLs
        cls.data_service_url = f"http://{cls.config_manager.get('services.data_service.host')}:{cls.config_manager.get('services.data_service.port')}"
        cls.ai_engine_url = f"http://{cls.config_manager.get('services.ai_engine.host')}:{cls.config_manager.get('services.ai_engine.port')}"
        cls.risk_service_url = f"http://{cls.config_manager.get('services.risk_service.host')}:{cls.config_manager.get('services.risk_service.port')}"
        cls.execution_service_url = f"http://{cls.config_manager.get('services.execution_service.host')}:{cls.config_manager.get('services.execution_service.port')}"

    @patch("requests.get")
    def test_data_service_to_ai_engine(self, mock_get):
        """Test data flow from Data Service to AI Engine"""
        # Mock market data response
        market_data_response = {
            "symbol": "AAPL",
            "timeframe": "1d",
            "data": [
                {
                    "timestamp": "2023-01-01T00:00:00Z",
                    "open": 100.0,
                    "high": 105.0,
                    "low": 95.0,
                    "close": 102.0,
                    "volume": 1000,
                },
                {
                    "timestamp": "2023-01-02T00:00:00Z",
                    "open": 102.0,
                    "high": 107.0,
                    "low": 100.0,
                    "close": 105.0,
                    "volume": 1200,
                },
            ],
        }

        # Mock requests.get for market data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = market_data_response
        mock_get.return_value = mock_response

        # Import prediction service
        from ai_engine.prediction_service import PredictionService

        # Create prediction service
        prediction_service = PredictionService(
            self.config_manager, self.db_manager, MagicMock()
        )

        # Mock model manager predict
        prediction_service.model_manager.predict.return_value = {
            "symbol": "AAPL",
            "timeframe": "1d",
            "predictions": [
                {"timestamp": "2023-01-03T00:00:00Z", "value": 108.0},
                {"timestamp": "2023-01-04T00:00:00Z", "value": 110.0},
            ],
        }

        # Generate prediction
        result = prediction_service.generate_prediction(
            model_id="model1", symbol="AAPL", timeframe="1d", period="1mo", horizon=2
        )

        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result["symbol"], "AAPL")
        self.assertEqual(result["model_id"], "model1")
        self.assertTrue("prediction" in result)
        self.assertTrue("average" in result["prediction"])
        self.assertTrue("direction" in result["prediction"])

        # Check requests.get was called with correct URL
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith(self.data_service_url))

    @patch("requests.get")
    def test_ai_engine_to_risk_service(self, mock_get):
        """Test data flow from AI Engine to Risk Service"""
        # Mock prediction response
        prediction_response = {
            "symbol": "AAPL",
            "model_id": "model1",
            "latest_price": 105.0,
            "prediction": {
                "average": 109.0,
                "minimum": 108.0,
                "maximum": 110.0,
                "change": 4.0,
                "change_percent": 3.81,
                "direction": "bullish",
            },
            "predictions": [
                {"timestamp": "2023-01-03T00:00:00Z", "value": 108.0},
                {"timestamp": "2023-01-04T00:00:00Z", "value": 110.0},
            ],
        }

        # Mock requests.get for prediction
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = prediction_response
        mock_get.return_value = mock_response

        # Import risk calculator
        from risk_service.risk_calculator import RiskCalculator

        # Create risk calculator
        risk_calculator = RiskCalculator(self.config_manager, self.db_manager)

        # Sample portfolio
        portfolio = {
            "id": "portfolio1",
            "name": "Test Portfolio",
            "positions": [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "entry_price": 100.0,
                    "current_price": 105.0,
                }
            ],
            "cash": 10000.0,
        }

        # Calculate portfolio value with prediction
        result = risk_calculator.calculate_portfolio_value_with_prediction(
            portfolio=portfolio, model_id="model1"
        )

        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result["portfolio_id"], "portfolio1")
        self.assertTrue("current_value" in result)
        self.assertTrue("predicted_value" in result)
        self.assertTrue("change" in result)
        self.assertTrue("change_percent" in result)

        # Check current value calculation
        expected_current_value = 100 * 105.0 + 10000.0
        self.assertEqual(result["current_value"], expected_current_value)

        # Check predicted value calculation
        expected_predicted_value = 100 * 109.0 + 10000.0
        self.assertEqual(result["predicted_value"], expected_predicted_value)

        # Check requests.get was called with correct URL
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith(self.ai_engine_url))

    @patch("requests.get")
    @patch("requests.post")
    def test_risk_service_to_execution_service(self, mock_post, mock_get):
        """Test data flow from Risk Service to Execution Service"""
        # Mock risk assessment response
        risk_assessment_response = {
            "portfolio_id": "portfolio1",
            "symbol": "AAPL",
            "max_position_size": 200,
            "max_order_value": 20000.0,
            "risk_level": "medium",
        }

        # Mock requests.get for risk assessment
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = risk_assessment_response
        mock_get.return_value = mock_get_response

        # Mock order creation response
        order_response = {
            "id": "order1",
            "portfolio_id": "portfolio1",
            "symbol": "AAPL",
            "order_type": "market",
            "side": "buy",
            "quantity": 100,
            "price": None,
            "time_in_force": "day",
            "status": "new",
        }

        # Mock requests.post for order creation
        mock_post_response = MagicMock()
        mock_post_response.status_code = 201
        mock_post_response.json.return_value = order_response
        mock_post.return_value = mock_post_response

        # Import order manager
        from execution_service.order_manager import OrderManager

        # Create order manager
        order_manager = OrderManager(self.config_manager, self.db_manager)

        # Create order with risk check
        order_data = {
            "portfolio_id": "portfolio1",
            "symbol": "AAPL",
            "order_type": "market",
            "side": "buy",
            "quantity": 100,
            "price": None,
            "time_in_force": "day",
        }

        result = order_manager.create_order_with_risk_check(order_data)

        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "order1")
        self.assertEqual(result["portfolio_id"], "portfolio1")
        self.assertEqual(result["symbol"], "AAPL")
        self.assertEqual(result["quantity"], 100)
        self.assertEqual(result["status"], "new")

        # Check requests.get was called with correct URL
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith(self.risk_service_url))

    @patch("requests.get")
    def test_execution_service_to_data_service(self, mock_get):
        """Test data flow from Execution Service to Data Service"""
        # Mock market data response
        market_data_response = {
            "symbol": "AAPL",
            "last_price": 160.0,
            "bid": 159.95,
            "ask": 160.05,
            "volume": 1000000,
        }

        # Mock requests.get for market data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = market_data_response
        mock_get.return_value = mock_response

        # Import broker integration
        from execution_service.broker_integration import BrokerIntegration

        # Create broker integration
        broker_integration = BrokerIntegration(self.config_manager, self.db_manager)

        # Get market data
        result = broker_integration.get_market_data("AAPL")

        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result["symbol"], "AAPL")
        self.assertEqual(result["last_price"], 160.0)
        self.assertEqual(result["bid"], 159.95)
        self.assertEqual(result["ask"], 160.05)

        # Check requests.get was called with correct URL
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith(self.data_service_url))

    @patch("requests.post")
    def test_end_to_end_trading_flow(self, mock_post):
        """Test end-to-end trading flow"""

        # Mock all service responses
        def mock_service_response(*args, **kwargs):
            url = args[0]

            if "/market-data/" in url:
                # Market data response
                return MagicMock(
                    status_code=200,
                    json=lambda: {
                        "symbol": "AAPL",
                        "data": [
                            {
                                "timestamp": "2023-01-01T00:00:00Z",
                                "open": 100.0,
                                "high": 105.0,
                                "low": 95.0,
                                "close": 102.0,
                                "volume": 1000,
                            }
                        ],
                    },
                )
            elif "/predict/" in url:
                # Prediction response
                return MagicMock(
                    status_code=200,
                    json=lambda: {
                        "symbol": "AAPL",
                        "prediction": {"direction": "bullish", "change_percent": 3.0},
                    },
                )
            elif "/risk/" in url:
                # Risk assessment response
                return MagicMock(
                    status_code=200,
                    json=lambda: {"symbol": "AAPL", "max_position_size": 200},
                )
            elif "/orders/" in url:
                # Order creation response
                return MagicMock(
                    status_code=201,
                    json=lambda: {
                        "id": "order1",
                        "symbol": "AAPL",
                        "quantity": 100,
                        "status": "new",
                    },
                )
            elif "/broker/" in url:
                # Broker response
                return MagicMock(
                    status_code=200,
                    json=lambda: {
                        "broker_order_id": "broker_order1",
                        "status": "filled",
                    },
                )
            else:
                return MagicMock(status_code=404)

        mock_post.side_effect = mock_service_response

        # Import trading service
        from execution_service.trading_service import TradingService

        # Create trading service
        trading_service = TradingService(self.config_manager, self.db_manager)

        # Execute trade based on signal
        signal = {
            "symbol": "AAPL",
            "type": "buy",
            "strength": 0.8,
            "price": 160.0,
            "model_id": "model1",
        }

        portfolio_id = "portfolio1"

        result = trading_service.execute_trade_from_signal(signal, portfolio_id)

        # Check result
        self.assertIsInstance(result, dict)
        self.assertTrue("order_id" in result)
        self.assertTrue("status" in result)
        self.assertTrue("execution_details" in result)


class TestDatabaseIntegration(unittest.TestCase):
    """Integration tests for database operations"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Initialize config manager
        cls.config_manager = ConfigManager()

        # Initialize database manager
        cls.db_manager = DatabaseManager(cls.config_manager)

    def test_postgres_connection(self):
        """Test PostgreSQL connection"""
        # Get session
        session = self.db_manager.get_postgres_session()

        # Check session
        self.assertIsNotNone(session)

        # Execute simple query
        result = session.execute("SELECT 1 as test")
        row = result.fetchone()

        # Check result
        self.assertEqual(row[0], 1)

        # Close session
        session.close()

    def test_timescale_connection(self):
        """Test TimescaleDB connection"""
        # Get session
        session = self.db_manager.get_timescale_session()

        # Check session
        self.assertIsNotNone(session)

        # Execute simple query
        result = session.execute("SELECT 1 as test")
        row = result.fetchone()

        # Check result
        self.assertEqual(row[0], 1)

        # Close session
        session.close()

    def test_redis_connection(self):
        """Test Redis connection"""
        # Get Redis client
        redis_client = self.db_manager.get_redis_client()

        # Check client
        self.assertIsNotNone(redis_client)

        # Set and get value
        redis_client.set("test_key", "test_value")
        value = redis_client.get("test_key")

        # Check result
        self.assertEqual(value.decode("utf-8"), "test_value")

        # Clean up
        redis_client.delete("test_key")

    def test_kafka_connection(self):
        """Test Kafka connection"""
        # Get Kafka producer
        producer = self.db_manager.get_kafka_producer()

        # Check producer
        self.assertIsNotNone(producer)

        # Get Kafka consumer
        consumer = self.db_manager.get_kafka_consumer(["test_topic"])

        # Check consumer
        self.assertIsNotNone(consumer)


class TestAPIEndpoints(unittest.TestCase):
    """Integration tests for API endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Initialize config manager
        cls.config_manager = ConfigManager()

        # Service URLs
        cls.data_service_url = f"http://{cls.config_manager.get('services.data_service.host')}:{cls.config_manager.get('services.data_service.port')}"
        cls.ai_engine_url = f"http://{cls.config_manager.get('services.ai_engine.host')}:{cls.config_manager.get('services.ai_engine.port')}"
        cls.risk_service_url = f"http://{cls.config_manager.get('services.risk_service.host')}:{cls.config_manager.get('services.risk_service.port')}"
        cls.execution_service_url = f"http://{cls.config_manager.get('services.execution_service.host')}:{cls.config_manager.get('services.execution_service.port')}"

    @patch("requests.get")
    def test_data_service_market_data_endpoint(self, mock_get):
        """Test Data Service market data endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "symbol": "AAPL",
            "timeframe": "1d",
            "data": [
                {
                    "timestamp": "2023-01-01T00:00:00Z",
                    "open": 100.0,
                    "high": 105.0,
                    "low": 95.0,
                    "close": 102.0,
                    "volume": 1000,
                }
            ],
        }
        mock_get.return_value = mock_response

        # Call endpoint
        response = requests.get(
            f"{self.data_service_url}/api/market-data/AAPL?timeframe=1d&period=1mo"
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["symbol"], "AAPL")
        self.assertTrue("data" in data)
        self.assertTrue(len(data["data"]) > 0)

    @patch("requests.post")
    def test_ai_engine_predict_endpoint(self, mock_post):
        """Test AI Engine predict endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "symbol": "AAPL",
            "model_id": "model1",
            "prediction": {"direction": "bullish", "change_percent": 3.0},
        }
        mock_post.return_value = mock_response

        # Call endpoint
        response = requests.post(
            f"{self.ai_engine_url}/api/predict",
            json={"model_id": "model1", "symbol": "AAPL", "timeframe": "1d"},
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["symbol"], "AAPL")
        self.assertTrue("prediction" in data)
        self.assertEqual(data["prediction"]["direction"], "bullish")

    @patch("requests.get")
    def test_risk_service_portfolio_risk_endpoint(self, mock_get):
        """Test Risk Service portfolio risk endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "portfolio_id": "portfolio1",
            "var": 5000.0,
            "var_percent": 5.0,
            "sharpe_ratio": 1.2,
        }
        mock_get.return_value = mock_response

        # Call endpoint
        response = requests.get(
            f"{self.risk_service_url}/api/risk/portfolio/portfolio1"
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["portfolio_id"], "portfolio1")
        self.assertTrue("var" in data)
        self.assertTrue("sharpe_ratio" in data)

    @patch("requests.post")
    def test_execution_service_orders_endpoint(self, mock_post):
        """Test Execution Service orders endpoint"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "order1",
            "portfolio_id": "portfolio1",
            "symbol": "AAPL",
            "order_type": "market",
            "side": "buy",
            "quantity": 100,
            "status": "new",
        }
        mock_post.return_value = mock_response

        # Call endpoint
        response = requests.post(
            f"{self.execution_service_url}/api/orders",
            json={
                "portfolio_id": "portfolio1",
                "symbol": "AAPL",
                "order_type": "market",
                "side": "buy",
                "quantity": 100,
            },
        )

        # Check response
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["symbol"], "AAPL")
        self.assertEqual(data["quantity"], 100)
        self.assertEqual(data["status"], "new")


if __name__ == "__main__":
    unittest.main()
