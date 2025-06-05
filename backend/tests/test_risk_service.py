"""
Unit tests for the Risk Service.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from risk_service.risk_calculator import RiskCalculator
from risk_service.position_sizing import PositionSizing
from risk_service.stress_testing import StressTesting
from common import ServiceError, ValidationError, NotFoundError

class TestRiskCalculator(unittest.TestCase):
    """Test cases for RiskCalculator"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get.return_value = 'test_value'
        
        # Mock database manager
        self.db_manager = MagicMock()
        
        # Create risk calculator
        self.risk_calculator = RiskCalculator(self.config_manager, self.db_manager)
        
        # Sample portfolio data
        self.portfolio = {
            'id': 'portfolio1',
            'name': 'Test Portfolio',
            'positions': [
                {
                    'symbol': 'AAPL',
                    'quantity': 100,
                    'entry_price': 150.0,
                    'current_price': 160.0
                },
                {
                    'symbol': 'MSFT',
                    'quantity': 50,
                    'entry_price': 250.0,
                    'current_price': 260.0
                },
                {
                    'symbol': 'GOOGL',
                    'quantity': 20,
                    'entry_price': 2800.0,
                    'current_price': 2900.0
                }
            ],
            'cash': 10000.0
        }
        
        # Sample market data
        self.market_data = {
            'AAPL': pd.DataFrame({
                'date': pd.date_range(start='2023-01-01', periods=100),
                'close': np.random.normal(150, 10, 100),
                'volume': np.random.randint(1000000, 10000000, 100)
            }),
            'MSFT': pd.DataFrame({
                'date': pd.date_range(start='2023-01-01', periods=100),
                'close': np.random.normal(250, 15, 100),
                'volume': np.random.randint(1000000, 10000000, 100)
            }),
            'GOOGL': pd.DataFrame({
                'date': pd.date_range(start='2023-01-01', periods=100),
                'close': np.random.normal(2800, 100, 100),
                'volume': np.random.randint(1000000, 10000000, 100)
            })
        }
    
    def test_calculate_portfolio_value(self):
        """Test portfolio value calculation"""
        # Calculate portfolio value
        result = self.risk_calculator.calculate_portfolio_value(self.portfolio)
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('total_value' in result)
        self.assertTrue('positions_value' in result)
        self.assertTrue('cash' in result)
        
        # Check calculations
        expected_positions_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            20 * 2900.0    # GOOGL
        )
        expected_total_value = expected_positions_value + 10000.0
        
        self.assertEqual(result['positions_value'], expected_positions_value)
        self.assertEqual(result['cash'], 10000.0)
        self.assertEqual(result['total_value'], expected_total_value)
    
    def test_calculate_portfolio_returns(self):
        """Test portfolio returns calculation"""
        # Calculate portfolio returns
        result = self.risk_calculator.calculate_portfolio_returns(self.portfolio)
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('total_return' in result)
        self.assertTrue('total_return_percent' in result)
        self.assertTrue('positions_return' in result)
        
        # Check calculations
        expected_positions_return = (
            100 * (160.0 - 150.0) +  # AAPL
            50 * (260.0 - 250.0) +   # MSFT
            20 * (2900.0 - 2800.0)   # GOOGL
        )
        expected_positions_cost = (
            100 * 150.0 +  # AAPL
            50 * 250.0 +   # MSFT
            20 * 2800.0    # GOOGL
        )
        expected_total_return_percent = (expected_positions_return / expected_positions_cost) * 100
        
        self.assertEqual(result['positions_return'], expected_positions_return)
        self.assertEqual(result['total_return'], expected_positions_return)
        self.assertAlmostEqual(result['total_return_percent'], expected_total_return_percent)
    
    def test_calculate_var(self):
        """Test Value at Risk calculation"""
        # Mock _get_market_data
        self.risk_calculator._get_market_data = MagicMock(return_value=self.market_data)
        
        # Calculate VaR
        result = self.risk_calculator.calculate_var(
            portfolio=self.portfolio,
            confidence_level=0.95,
            time_horizon=1
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('var' in result)
        self.assertTrue('var_percent' in result)
        self.assertTrue('confidence_level' in result)
        self.assertTrue('time_horizon' in result)
        
        # Check values
        self.assertTrue(result['var'] > 0)
        self.assertTrue(0 < result['var_percent'] < 100)
        self.assertEqual(result['confidence_level'], 0.95)
        self.assertEqual(result['time_horizon'], 1)
    
    def test_calculate_var_invalid_confidence(self):
        """Test VaR calculation with invalid confidence level"""
        # Try to calculate VaR with invalid confidence level
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_var(
                portfolio=self.portfolio,
                confidence_level=1.5,  # Invalid: > 1
                time_horizon=1
            )
        
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_var(
                portfolio=self.portfolio,
                confidence_level=-0.1,  # Invalid: < 0
                time_horizon=1
            )
    
    def test_calculate_var_invalid_horizon(self):
        """Test VaR calculation with invalid time horizon"""
        # Try to calculate VaR with invalid time horizon
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_var(
                portfolio=self.portfolio,
                confidence_level=0.95,
                time_horizon=0  # Invalid: <= 0
            )
        
        with self.assertRaises(ValidationError):
            self.risk_calculator.calculate_var(
                portfolio=self.portfolio,
                confidence_level=0.95,
                time_horizon=-1  # Invalid: <= 0
            )
    
    def test_calculate_expected_shortfall(self):
        """Test Expected Shortfall calculation"""
        # Mock _get_market_data
        self.risk_calculator._get_market_data = MagicMock(return_value=self.market_data)
        
        # Calculate ES
        result = self.risk_calculator.calculate_expected_shortfall(
            portfolio=self.portfolio,
            confidence_level=0.95,
            time_horizon=1
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('es' in result)
        self.assertTrue('es_percent' in result)
        self.assertTrue('confidence_level' in result)
        self.assertTrue('time_horizon' in result)
        
        # Check values
        self.assertTrue(result['es'] > 0)
        self.assertTrue(0 < result['es_percent'] < 100)
        self.assertEqual(result['confidence_level'], 0.95)
        self.assertEqual(result['time_horizon'], 1)
    
    def test_calculate_sharpe_ratio(self):
        """Test Sharpe Ratio calculation"""
        # Mock _get_market_data
        self.risk_calculator._get_market_data = MagicMock(return_value=self.market_data)
        
        # Calculate Sharpe Ratio
        result = self.risk_calculator.calculate_sharpe_ratio(
            portfolio=self.portfolio,
            risk_free_rate=0.02,
            period='1y'
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('sharpe_ratio' in result)
        self.assertTrue('annualized_return' in result)
        self.assertTrue('annualized_volatility' in result)
        self.assertTrue('risk_free_rate' in result)
        
        # Check values
        self.assertTrue(isinstance(result['sharpe_ratio'], float))
        self.assertTrue(isinstance(result['annualized_return'], float))
        self.assertTrue(isinstance(result['annualized_volatility'], float))
        self.assertEqual(result['risk_free_rate'], 0.02)
    
    def test_calculate_beta(self):
        """Test Beta calculation"""
        # Mock _get_market_data
        self.risk_calculator._get_market_data = MagicMock(return_value=self.market_data)
        
        # Mock _get_benchmark_data
        benchmark_data = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=100),
            'close': np.random.normal(4000, 100, 100)
        })
        self.risk_calculator._get_benchmark_data = MagicMock(return_value=benchmark_data)
        
        # Calculate Beta
        result = self.risk_calculator.calculate_beta(
            portfolio=self.portfolio,
            benchmark='SPY',
            period='1y'
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('beta' in result)
        self.assertTrue('benchmark' in result)
        
        # Check values
        self.assertTrue(isinstance(result['beta'], float))
        self.assertEqual(result['benchmark'], 'SPY')

class TestPositionSizing(unittest.TestCase):
    """Test cases for PositionSizing"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get.return_value = 'test_value'
        
        # Mock database manager
        self.db_manager = MagicMock()
        
        # Create position sizing
        self.position_sizing = PositionSizing(self.config_manager, self.db_manager)
        
        # Sample portfolio data
        self.portfolio = {
            'id': 'portfolio1',
            'name': 'Test Portfolio',
            'positions': [
                {
                    'symbol': 'AAPL',
                    'quantity': 100,
                    'entry_price': 150.0,
                    'current_price': 160.0
                },
                {
                    'symbol': 'MSFT',
                    'quantity': 50,
                    'entry_price': 250.0,
                    'current_price': 260.0
                }
            ],
            'cash': 10000.0
        }
    
    def test_calculate_position_size_fixed(self):
        """Test fixed position size calculation"""
        # Calculate position size
        result = self.position_sizing.calculate_position_size(
            portfolio=self.portfolio,
            symbol='GOOGL',
            price=2800.0,
            method='fixed',
            params={'amount': 5000.0}
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'GOOGL')
        self.assertEqual(result['price'], 2800.0)
        self.assertEqual(result['method'], 'fixed')
        self.assertTrue('quantity' in result)
        self.assertTrue('value' in result)
        
        # Check calculations
        expected_quantity = 5000.0 / 2800.0
        expected_value = expected_quantity * 2800.0
        
        self.assertAlmostEqual(result['quantity'], expected_quantity)
        self.assertAlmostEqual(result['value'], expected_value)
    
    def test_calculate_position_size_percent(self):
        """Test percentage position size calculation"""
        # Calculate position size
        result = self.position_sizing.calculate_position_size(
            portfolio=self.portfolio,
            symbol='GOOGL',
            price=2800.0,
            method='percent',
            params={'percent': 10.0}
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'GOOGL')
        self.assertEqual(result['price'], 2800.0)
        self.assertEqual(result['method'], 'percent')
        self.assertTrue('quantity' in result)
        self.assertTrue('value' in result)
        
        # Check calculations
        portfolio_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            10000.0        # Cash
        )
        expected_value = portfolio_value * 0.1
        expected_quantity = expected_value / 2800.0
        
        self.assertAlmostEqual(result['quantity'], expected_quantity)
        self.assertAlmostEqual(result['value'], expected_value)
    
    def test_calculate_position_size_risk(self):
        """Test risk-based position size calculation"""
        # Calculate position size
        result = self.position_sizing.calculate_position_size(
            portfolio=self.portfolio,
            symbol='GOOGL',
            price=2800.0,
            method='risk',
            params={'risk_percent': 1.0, 'stop_loss_percent': 5.0}
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'GOOGL')
        self.assertEqual(result['price'], 2800.0)
        self.assertEqual(result['method'], 'risk')
        self.assertTrue('quantity' in result)
        self.assertTrue('value' in result)
        self.assertTrue('stop_loss' in result)
        
        # Check calculations
        portfolio_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            10000.0        # Cash
        )
        risk_amount = portfolio_value * 0.01
        stop_loss = 2800.0 * 0.95
        expected_quantity = risk_amount / (2800.0 - stop_loss)
        expected_value = expected_quantity * 2800.0
        
        self.assertAlmostEqual(result['quantity'], expected_quantity)
        self.assertAlmostEqual(result['value'], expected_value)
        self.assertEqual(result['stop_loss'], stop_loss)
    
    def test_calculate_position_size_kelly(self):
        """Test Kelly Criterion position size calculation"""
        # Calculate position size
        result = self.position_sizing.calculate_position_size(
            portfolio=self.portfolio,
            symbol='GOOGL',
            price=2800.0,
            method='kelly',
            params={'win_rate': 0.6, 'win_loss_ratio': 2.0}
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'GOOGL')
        self.assertEqual(result['price'], 2800.0)
        self.assertEqual(result['method'], 'kelly')
        self.assertTrue('quantity' in result)
        self.assertTrue('value' in result)
        self.assertTrue('kelly_percent' in result)
        
        # Check calculations
        portfolio_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            10000.0        # Cash
        )
        kelly_percent = 0.6 - (1 - 0.6) / 2.0
        expected_value = portfolio_value * kelly_percent
        expected_quantity = expected_value / 2800.0
        
        self.assertAlmostEqual(result['quantity'], expected_quantity)
        self.assertAlmostEqual(result['value'], expected_value)
        self.assertEqual(result['kelly_percent'], kelly_percent)
    
    def test_calculate_position_size_invalid_method(self):
        """Test position size calculation with invalid method"""
        # Try to calculate position size with invalid method
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='invalid_method',
                params={}
            )
    
    def test_calculate_position_size_missing_params(self):
        """Test position size calculation with missing parameters"""
        # Try to calculate position size with missing parameters
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='fixed',
                params={}  # Missing 'amount'
            )
        
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='percent',
                params={}  # Missing 'percent'
            )
        
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='risk',
                params={'risk_percent': 1.0}  # Missing 'stop_loss_percent'
            )
        
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='kelly',
                params={'win_rate': 0.6}  # Missing 'win_loss_ratio'
            )
    
    def test_calculate_position_size_invalid_params(self):
        """Test position size calculation with invalid parameters"""
        # Try to calculate position size with invalid parameters
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='percent',
                params={'percent': 101.0}  # Invalid: > 100
            )
        
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='risk',
                params={'risk_percent': 10.0, 'stop_loss_percent': 0.0}  # Invalid: <= 0
            )
        
        with self.assertRaises(ValidationError):
            self.position_sizing.calculate_position_size(
                portfolio=self.portfolio,
                symbol='GOOGL',
                price=2800.0,
                method='kelly',
                params={'win_rate': 1.1, 'win_loss_ratio': 2.0}  # Invalid: > 1
            )

class TestStressTesting(unittest.TestCase):
    """Test cases for StressTesting"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get.return_value = 'test_value'
        
        # Mock database manager
        self.db_manager = MagicMock()
        
        # Create stress testing
        self.stress_testing = StressTesting(self.config_manager, self.db_manager)
        
        # Sample portfolio data
        self.portfolio = {
            'id': 'portfolio1',
            'name': 'Test Portfolio',
            'positions': [
                {
                    'symbol': 'AAPL',
                    'quantity': 100,
                    'entry_price': 150.0,
                    'current_price': 160.0
                },
                {
                    'symbol': 'MSFT',
                    'quantity': 50,
                    'entry_price': 250.0,
                    'current_price': 260.0
                },
                {
                    'symbol': 'GOOGL',
                    'quantity': 20,
                    'entry_price': 2800.0,
                    'current_price': 2900.0
                }
            ],
            'cash': 10000.0
        }
    
    def test_run_historical_scenario(self):
        """Test historical scenario stress test"""
        # Mock _get_historical_data
        historical_data = {
            'AAPL': pd.DataFrame({
                'date': pd.date_range(start='2008-09-01', periods=100),
                'close': np.linspace(150, 100, 100)  # Decreasing prices
            }),
            'MSFT': pd.DataFrame({
                'date': pd.date_range(start='2008-09-01', periods=100),
                'close': np.linspace(250, 200, 100)  # Decreasing prices
            }),
            'GOOGL': pd.DataFrame({
                'date': pd.date_range(start='2008-09-01', periods=100),
                'close': np.linspace(2800, 2300, 100)  # Decreasing prices
            })
        }
        self.stress_testing._get_historical_data = MagicMock(return_value=historical_data)
        
        # Run historical scenario
        result = self.stress_testing.run_historical_scenario(
            portfolio=self.portfolio,
            scenario='financial_crisis_2008',
            start_date='2008-09-01',
            end_date='2008-12-31'
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertEqual(result['scenario'], 'financial_crisis_2008')
        self.assertTrue('initial_value' in result)
        self.assertTrue('final_value' in result)
        self.assertTrue('change' in result)
        self.assertTrue('change_percent' in result)
        self.assertTrue('positions' in result)
        
        # Check calculations
        initial_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            20 * 2900.0 +  # GOOGL
            10000.0        # Cash
        )
        final_value = (
            100 * 100.0 +  # AAPL
            50 * 200.0 +   # MSFT
            20 * 2300.0 +  # GOOGL
            10000.0        # Cash
        )
        change = final_value - initial_value
        change_percent = (change / initial_value) * 100
        
        self.assertEqual(result['initial_value'], initial_value)
        self.assertEqual(result['final_value'], final_value)
        self.assertEqual(result['change'], change)
        self.assertEqual(result['change_percent'], change_percent)
    
    def test_run_monte_carlo_simulation(self):
        """Test Monte Carlo simulation stress test"""
        # Run Monte Carlo simulation
        result = self.stress_testing.run_monte_carlo_simulation(
            portfolio=self.portfolio,
            num_simulations=100,
            time_horizon=252,  # 1 year of trading days
            confidence_level=0.95
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertEqual(result['num_simulations'], 100)
        self.assertEqual(result['time_horizon'], 252)
        self.assertEqual(result['confidence_level'], 0.95)
        self.assertTrue('initial_value' in result)
        self.assertTrue('expected_final_value' in result)
        self.assertTrue('var' in result)
        self.assertTrue('var_percent' in result)
        self.assertTrue('expected_return' in result)
        self.assertTrue('expected_volatility' in result)
        self.assertTrue('simulations' in result)
        
        # Check calculations
        initial_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            20 * 2900.0 +  # GOOGL
            10000.0        # Cash
        )
        
        self.assertEqual(result['initial_value'], initial_value)
        self.assertTrue(len(result['simulations']) == 100)
    
    def test_run_sensitivity_analysis(self):
        """Test sensitivity analysis stress test"""
        # Run sensitivity analysis
        result = self.stress_testing.run_sensitivity_analysis(
            portfolio=self.portfolio,
            factors=[
                {'name': 'market_decline', 'values': [-10, -20, -30]},
                {'name': 'interest_rate', 'values': [0.03, 0.04, 0.05]}
            ]
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertTrue('initial_value' in result)
        self.assertTrue('scenarios' in result)
        
        # Check calculations
        initial_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            20 * 2900.0 +  # GOOGL
            10000.0        # Cash
        )
        
        self.assertEqual(result['initial_value'], initial_value)
        self.assertEqual(len(result['scenarios']), 9)  # 3 market decline values * 3 interest rate values
    
    def test_run_custom_scenario(self):
        """Test custom scenario stress test"""
        # Run custom scenario
        result = self.stress_testing.run_custom_scenario(
            portfolio=self.portfolio,
            scenario_name='Custom Scenario',
            price_changes={
                'AAPL': -15.0,  # 15% decline
                'MSFT': -10.0,   # 10% decline
                'GOOGL': -20.0   # 20% decline
            }
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['portfolio_id'], 'portfolio1')
        self.assertEqual(result['scenario_name'], 'Custom Scenario')
        self.assertTrue('initial_value' in result)
        self.assertTrue('final_value' in result)
        self.assertTrue('change' in result)
        self.assertTrue('change_percent' in result)
        self.assertTrue('positions' in result)
        
        # Check calculations
        initial_value = (
            100 * 160.0 +  # AAPL
            50 * 260.0 +   # MSFT
            20 * 2900.0 +  # GOOGL
            10000.0        # Cash
        )
        final_value = (
            100 * (160.0 * (1 - 0.15)) +  # AAPL
            50 * (260.0 * (1 - 0.10)) +   # MSFT
            20 * (2900.0 * (1 - 0.20)) +  # GOOGL
            10000.0                       # Cash
        )
        change = final_value - initial_value
        change_percent = (change / initial_value) * 100
        
        self.assertEqual(result['initial_value'], initial_value)
        self.assertEqual(result['final_value'], final_value)
        self.assertEqual(result['change'], change)
        self.assertEqual(result['change_percent'], change_percent)

if __name__ == '__main__':
    unittest.main()

