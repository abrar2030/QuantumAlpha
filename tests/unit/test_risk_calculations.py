import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestRiskCalculations(unittest.TestCase):
    """Unit tests for risk calculation functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create sample return data for testing
        self.sample_returns = np.array([0.01, -0.02, 0.005, 0.008, -0.01, 0.02, -0.015])
        
    def test_calculate_var(self):
        """Test Value at Risk calculation"""
        from backend.risk_service.risk_calculations import calculate_var
        
        # Test with 95% confidence level
        var_95 = calculate_var(self.sample_returns, confidence_level=0.95)
        self.assertIsInstance(var_95, float)
        self.assertGreater(var_95, 0)  # VaR should be positive
        
        # Test with 99% confidence level
        var_99 = calculate_var(self.sample_returns, confidence_level=0.99)
        self.assertGreaterEqual(var_99, var_95)  # Higher confidence should give higher or equal VaR
    
    def test_calculate_cvar(self):
        """Test Conditional Value at Risk calculation"""
        from backend.risk_service.risk_calculations import calculate_cvar
        
        # Test with 95% confidence level
        cvar_95 = calculate_cvar(self.sample_returns, confidence_level=0.95)
        self.assertIsInstance(cvar_95, float)
        self.assertGreater(cvar_95, 0)  # CVaR should be positive
        
        # Test with different confidence levels
        var_95 = calculate_var(self.sample_returns, confidence_level=0.95)
        self.assertGreaterEqual(cvar_95, var_95)  # CVaR should be >= VaR
    
    def test_calculate_sharpe_ratio(self):
        """Test Sharpe ratio calculation"""
        from backend.risk_service.risk_calculations import calculate_sharpe_ratio
        
        # Test with default risk-free rate
        sharpe = calculate_sharpe_ratio(self.sample_returns)
        self.assertIsInstance(sharpe, float)
        
        # Test with custom risk-free rate
        sharpe_custom = calculate_sharpe_ratio(self.sample_returns, risk_free_rate=0.02)
        self.assertIsInstance(sharpe_custom, float)
    
    def test_calculate_max_drawdown(self):
        """Test maximum drawdown calculation"""
        from backend.risk_service.risk_calculations import calculate_max_drawdown
        
        # Create a sample equity curve
        equity_curve = np.array([1000, 1050, 1030, 1070, 1000, 1020, 1100])
        
        # Calculate max drawdown
        max_dd, max_dd_pct = calculate_max_drawdown(equity_curve)
        
        self.assertIsInstance(max_dd, float)
        self.assertIsInstance(max_dd_pct, float)
        self.assertGreaterEqual(max_dd, 0)  # Drawdown should be non-negative
        self.assertLessEqual(max_dd_pct, 1.0)  # Percentage should be <= 100%

if __name__ == '__main__':
    unittest.main()
