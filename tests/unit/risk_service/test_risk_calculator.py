"""
Unit tests for the Risk Service's Risk Calculator.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock

import numpy as np

# Add project root to path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import module to test
try:
    from backend.common.exceptions import ServiceError, ValidationError
    from backend.risk_service.risk_calculator import RiskCalculator
except ImportError:
    # Mock the classes for testing when imports fail
    class RiskCalculator:
        pass

    class ValidationError(Exception):
        pass

    class ServiceError(Exception):
        pass


class TestRiskCalculator(unittest.TestCase):
    """Unit tests for RiskCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "risk_service": {
                "default_risk_free_rate": 0.02,
                "default_confidence_level": 0.95,
                "max_position_size": 0.1,
                "max_portfolio_var": 0.05,
            }
        }

        # Create mock database manager
        self.db_manager = MagicMock()

        # Create sample returns
        self.sample_returns = np.array(
            [0.01, -0.02, 0.005, 0.008, -0.01, 0.02, -0.015, 0.012, -0.005, 0.018]
        )

        # Create sample equity curve
        self.sample_equity_curve = np.array(
            [100000, 101000, 99000, 99500, 100300, 99200, 101000, 99500, 100500, 102000]
        )

        # Create sample portfolio
        self.sample_portfolio = [
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
        ]

        # Create sample position returns
        self.sample_position_returns = {
            "AAPL": np.array([0.01, -0.015, 0.008, 0.012, -0.005]),
            "MSFT": np.array([0.015, -0.01, 0.005, 0.02, -0.008]),
        }

        # Create risk calculator
        self.risk_calculator = RiskCalculator(self.config_manager, self.db_manager)

    def test_init(self):
        """Test RiskCalculator initialization."""
        risk_calculator = RiskCalculator(self.config_manager, self.db_manager)

        # Check attributes
        self.assertEqual(risk_calculator.config_manager, self.config_manager)
        self.assertEqual(risk_calculator.db_manager, self.db_manager)
        self.assertEqual(risk_calculator.default_risk_free_rate, 0.02)
        self.assertEqual(risk_calculator.default_confidence_level, 0.95)
        self.assertEqual(risk_calculator.max_position_size, 0.1)
        self.assertEqual(risk_calculator.max_portfolio_var, 0.05)

    def test_calculate_portfolio_risk(self):
        """Test portfolio risk calculation."""
        # Mock _get_historical_data
        self.risk_calculator._get_historical_data = MagicMock(
            return_value=self.sample_returns
        )

        # Calculate portfolio risk
        risk = self.risk_calculator.calculate_portfolio_risk(
            portfolio_id="portfolio_1234567890",
            risk_metrics=[
                "var",
                "cvar",
                "sharpe_ratio",
                "sortino_ratio",
                "max_drawdown",
            ],
        )

        # Check result
        self.assertIsInstance(risk, dict)
        self.assertEqual(risk["portfolio_id"], "portfolio_1234567890")
        self.assertIn("var", risk)
        self.assertIn("cvar", risk)
        self.assertIn("sharpe_ratio", risk)
        self.assertIn("sortino_ratio", risk)
        self.assertIn("max_drawdown", risk)
        self.assertIn("timestamp", risk)

    def test_calculate_portfolio_risk_invalid_metrics(self):
        """Test portfolio risk calculation with invalid metrics."""
        # Calculate portfolio risk with invalid metrics
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_portfolio_risk(
                portfolio_id="portfolio_1234567890", risk_metrics=["invalid_metric"]
            )

    def test_calculate_position_risk(self):
        """Test position risk calculation."""
        # Mock _get_historical_data
        self.risk_calculator._get_historical_data = MagicMock(
            return_value=self.sample_returns
        )

        # Calculate position risk
        risk = self.risk_calculator.calculate_position_risk(
            symbol="AAPL",
            quantity=100,
            entry_price=150.0,
            current_price=155.0,
            risk_metrics=[
                "var",
                "cvar",
                "sharpe_ratio",
                "sortino_ratio",
                "max_drawdown",
            ],
        )

        # Check result
        self.assertIsInstance(risk, dict)
        self.assertEqual(risk["symbol"], "AAPL")
        self.assertEqual(risk["quantity"], 100)
        self.assertEqual(risk["entry_price"], 150.0)
        self.assertEqual(risk["current_price"], 155.0)
        self.assertIn("var", risk)
        self.assertIn("cvar", risk)
        self.assertIn("sharpe_ratio", risk)
        self.assertIn("sortino_ratio", risk)
        self.assertIn("max_drawdown", risk)
        self.assertIn("timestamp", risk)

    def test_calculate_position_risk_invalid_metrics(self):
        """Test position risk calculation with invalid metrics."""
        # Calculate position risk with invalid metrics
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_position_risk(
                symbol="AAPL",
                quantity=100,
                entry_price=150.0,
                current_price=155.0,
                risk_metrics=["invalid_metric"],
            )

    def test_calculate_position_size(self):
        """Test position size calculation."""
        # Calculate position size
        size = self.risk_calculator.calculate_position_size(
            symbol="AAPL",
            portfolio_value=100000.0,
            risk_per_trade=0.01,
            stop_loss_percent=0.05,
        )

        # Check result
        self.assertIsInstance(size, dict)
        self.assertEqual(size["symbol"], "AAPL")
        self.assertIn("size", size)
        self.assertIn("value", size)
        self.assertIn("max_loss", size)

    def test_calculate_position_size_invalid_risk(self):
        """Test position size calculation with invalid risk."""
        # Calculate position size with invalid risk
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_position_size(
                symbol="AAPL",
                portfolio_value=100000.0,
                risk_per_trade=0.5,  # Too high
                stop_loss_percent=0.05,
            )

    def test_calculate_position_size_invalid_stop_loss(self):
        """Test position size calculation with invalid stop loss."""
        # Calculate position size with invalid stop loss
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_position_size(
                symbol="AAPL",
                portfolio_value=100000.0,
                risk_per_trade=0.01,
                stop_loss_percent=0.0,  # Too low
            )

    def test_calculate_var(self):
        """Test Value at Risk calculation."""
        # Calculate VaR
        var_95 = self.risk_calculator._calculate_var(
            self.sample_returns, confidence_level=0.95
        )
        var_99 = self.risk_calculator._calculate_var(
            self.sample_returns, confidence_level=0.99
        )

        # Check result
        self.assertIsInstance(var_95, float)
        self.assertIsInstance(var_99, float)
        self.assertGreater(var_95, 0)
        self.assertGreater(var_99, 0)
        self.assertGreaterEqual(
            var_99, var_95
        )  # Higher confidence should give higher or equal VaR

    def test_calculate_cvar(self):
        """Test Conditional Value at Risk calculation."""
        # Calculate CVaR
        cvar_95 = self.risk_calculator._calculate_cvar(
            self.sample_returns, confidence_level=0.95
        )

        # Check result
        self.assertIsInstance(cvar_95, float)
        self.assertGreater(cvar_95, 0)

        # CVaR should be >= VaR
        var_95 = self.risk_calculator._calculate_var(
            self.sample_returns, confidence_level=0.95
        )
        self.assertGreaterEqual(cvar_95, var_95)

    def test_calculate_sharpe_ratio(self):
        """Test Sharpe ratio calculation."""
        # Calculate Sharpe ratio
        sharpe = self.risk_calculator._calculate_sharpe_ratio(
            self.sample_returns, risk_free_rate=0.0
        )
        sharpe_custom = self.risk_calculator._calculate_sharpe_ratio(
            self.sample_returns, risk_free_rate=0.02
        )

        # Check result
        self.assertIsInstance(sharpe, float)
        self.assertIsInstance(sharpe_custom, float)

    def test_calculate_sortino_ratio(self):
        """Test Sortino ratio calculation."""
        # Calculate Sortino ratio
        sortino = self.risk_calculator._calculate_sortino_ratio(
            self.sample_returns, risk_free_rate=0.0
        )
        sortino_custom = self.risk_calculator._calculate_sortino_ratio(
            self.sample_returns, risk_free_rate=0.02
        )

        # Check result
        self.assertIsInstance(sortino, float)
        self.assertIsInstance(sortino_custom, float)

    def test_calculate_max_drawdown(self):
        """Test maximum drawdown calculation."""
        # Calculate max drawdown
        max_dd = self.risk_calculator._calculate_max_drawdown(self.sample_returns)

        # Check result
        self.assertIsInstance(max_dd, float)
        self.assertGreaterEqual(max_dd, 0)
        self.assertLessEqual(max_dd, 1.0)

    def test_calculate_portfolio_returns(self):
        """Test portfolio returns calculation."""
        # Calculate portfolio returns
        returns = self.risk_calculator._calculate_portfolio_returns(
            portfolio=self.sample_portfolio,
            position_returns=self.sample_position_returns,
        )

        # Check result
        self.assertIsInstance(returns, np.ndarray)
        self.assertEqual(len(returns), 5)  # Length of the shortest return series

    def test_calculate_returns(self):
        """Test returns calculation."""
        # Create sample data
        data = [
            {"close": 100.0},
            {"close": 102.0},
            {"close": 101.0},
            {"close": 103.0},
            {"close": 105.0},
        ]

        # Calculate returns
        returns = self.risk_calculator._calculate_returns(data)

        # Check result
        self.assertIsInstance(returns, np.ndarray)
        self.assertEqual(len(returns), 4)  # One less than the number of data points
        np.testing.assert_almost_equal(
            returns, np.array([0.02, -0.0098, 0.0198, 0.0194]), decimal=4
        )

    def test_get_historical_data(self):
        """Test historical data retrieval."""
        # Mock database session
        mock_session = MagicMock()
        self.db_manager.get_postgres_session.return_value = mock_session

        # Mock query result
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            {"timestamp": "2023-01-01T00:00:00Z", "close": 100.0, "volume": 1000000},
            {"timestamp": "2023-01-02T00:00:00Z", "close": 102.0, "volume": 1100000},
            {"timestamp": "2023-01-03T00:00:00Z", "close": 101.0, "volume": 900000},
            {"timestamp": "2023-01-04T00:00:00Z", "close": 103.0, "volume": 1200000},
            {"timestamp": "2023-01-05T00:00:00Z", "close": 105.0, "volume": 1300000},
        ]
        mock_session.execute.return_value = mock_result

        # Get historical data
        data = self.risk_calculator._get_historical_data(symbol="AAPL", days=30)

        # Check result
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]["close"], 100.0)
        self.assertEqual(data[4]["close"], 105.0)

    def test_get_historical_data_empty(self):
        """Test historical data retrieval with empty result."""
        # Mock database session
        mock_session = MagicMock()
        self.db_manager.get_postgres_session.return_value = mock_session

        # Mock empty query result
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session.execute.return_value = mock_result

        # Get historical data and check exception
        with self.assertRaises(ValidationError):
            self.risk_calculator._get_historical_data(symbol="AAPL", days=30)

    def test_generate_synthetic_data(self):
        """Test synthetic data generation."""
        # Generate synthetic data
        data = self.risk_calculator._generate_synthetic_data(symbol="AAPL", days=30)

        # Check result
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 30)
        self.assertEqual(data[0]["symbol"], "AAPL")
        self.assertIn("timestamp", data[0])
        self.assertIn("open", data[0])
        self.assertIn("high", data[0])
        self.assertIn("low", data[0])
        self.assertIn("close", data[0])
        self.assertIn("volume", data[0])


if __name__ == "__main__":
    unittest.main()
