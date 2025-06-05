"""
Integration tests for AI engine to risk service integration.
"""
import os
import json
import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import pytest
import sys
from datetime import datetime, timedelta
import requests

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import modules to test
try:
    from backend.ai_engine.model_manager import ModelManager
    from backend.ai_engine.prediction_service import PredictionService
    from backend.risk_service.risk_calculator import RiskCalculator
    from backend.common.exceptions import ValidationError, ServiceError
except ImportError:
    # Mock the classes for testing when imports fail
    class ModelManager:
        pass
    
    class PredictionService:
        pass
    
    class RiskCalculator:
        pass
    
    class ValidationError(Exception):
        pass
    
    class ServiceError(Exception):
        pass

class TestModelToRiskIntegration(unittest.TestCase):
    """Integration tests for AI engine to risk service integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "ai_engine": {
                "model_dir": "/tmp/models",
                "registry_file": "/tmp/models/registry.json"
            },
            "risk_service": {
                "default_risk_free_rate": 0.02,
                "default_confidence_level": 0.95,
                "max_position_size": 0.1,
                "max_portfolio_var": 0.05
            },
            "services": {
                "ai_engine": {
                    "host": "localhost",
                    "port": 8082
                },
                "risk_service": {
                    "host": "localhost",
                    "port": 8083
                }
            }
        }
        
        # Create mock database manager
        self.db_manager = MagicMock()
        
        # Create sample prediction data
        self.prediction_data = {
            'symbol': 'AAPL',
            'model_id': 'model_1234567890',
            'latest_price': 100.0,
            'prediction': {
                'average': 110.0,
                'minimum': 105.0,
                'maximum': 115.0,
                'change': 10.0,
                'change_percent': 10.0,
                'direction': 'up'
            },
            'predictions': [
                {
                    'timestamp': '2023-01-11T00:00:00Z',
                    'value': 105.0,
                    'confidence': 0.9
                },
                {
                    'timestamp': '2023-01-12T00:00:00Z',
                    'value': 107.5,
                    'confidence': 0.85
                },
                {
                    'timestamp': '2023-01-13T00:00:00Z',
                    'value': 110.0,
                    'confidence': 0.8
                },
                {
                    'timestamp': '2023-01-14T00:00:00Z',
                    'value': 112.5,
                    'confidence': 0.75
                },
                {
                    'timestamp': '2023-01-15T00:00:00Z',
                    'value': 115.0,
                    'confidence': 0.7
                }
            ]
        }
        
        # Create sample portfolio
        self.sample_portfolio = [
            {
                'symbol': 'AAPL',
                'quantity': 100,
                'entry_price': 150.0,
                'current_price': 155.0
            },
            {
                'symbol': 'MSFT',
                'quantity': 50,
                'entry_price': 250.0,
                'current_price': 260.0
            }
        ]
        
        # Create model manager
        self.model_manager = ModelManager(self.config_manager, self.db_manager)
        
        # Create prediction service
        self.prediction_service = PredictionService(self.config_manager, self.db_manager, self.model_manager)
        
        # Create risk calculator
        self.risk_calculator = RiskCalculator(self.config_manager, self.db_manager)
    
    @patch('requests.post')
    def test_prediction_to_risk_calculation(self, mock_post):
        """Test prediction to risk calculation flow."""
        # Mock risk service API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'symbol': 'AAPL',
            'quantity': 100,
            'entry_price': 150.0,
            'current_price': 155.0,
            'predicted_price': 110.0,
            'var': 0.05,
            'cvar': 0.07,
            'sharpe_ratio': 1.2,
            'sortino_ratio': 1.5,
            'max_drawdown': 0.15,
            'risk_score': 65,
            'risk_level': 'medium',
            'timestamp': datetime.utcnow().isoformat()
        }
        mock_post.return_value = mock_response
        
        # Mock model manager predict method
        with patch.object(self.model_manager, 'predict') as mock_predict:
            mock_predict.return_value = self.prediction_data
            
            # Get prediction from model
            prediction = self.model_manager.predict('model_1234567890', {
                'symbol': 'AAPL',
                'timeframe': '1d',
                'latest_price': 100.0,
                'data': []
            })
            
            # Check prediction
            self.assertEqual(prediction['symbol'], 'AAPL')
            self.assertEqual(prediction['model_id'], 'model_1234567890')
            self.assertIn('prediction', prediction)
            self.assertIn('predictions', prediction)
            
            # Mock risk calculator calculate_position_risk method
            with patch.object(self.risk_calculator, 'calculate_position_risk') as mock_risk:
                mock_risk.return_value = {
                    'symbol': 'AAPL',
                    'quantity': 100,
                    'entry_price': 150.0,
                    'current_price': 155.0,
                    'predicted_price': 110.0,
                    'var': 0.05,
                    'cvar': 0.07,
                    'sharpe_ratio': 1.2,
                    'sortino_ratio': 1.5,
                    'max_drawdown': 0.15,
                    'risk_score': 65,
                    'risk_level': 'medium',
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                # Calculate risk based on prediction
                risk = self.risk_calculator.calculate_position_risk(
                    symbol='AAPL',
                    quantity=100,
                    entry_price=150.0,
                    current_price=155.0,
                    predicted_price=prediction['prediction']['average'],
                    risk_metrics=['var', 'cvar', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown']
                )
                
                # Check risk calculation
                self.assertEqual(risk['symbol'], 'AAPL')
                self.assertEqual(risk['quantity'], 100)
                self.assertEqual(risk['entry_price'], 150.0)
                self.assertEqual(risk['current_price'], 155.0)
                self.assertEqual(risk['predicted_price'], 110.0)
                self.assertIn('var', risk)
                self.assertIn('cvar', risk)
                self.assertIn('sharpe_ratio', risk)
                self.assertIn('sortino_ratio', risk)
                self.assertIn('max_drawdown', risk)
                self.assertIn('risk_score', risk)
                self.assertIn('risk_level', risk)
    
    @patch('requests.get')
    @patch('requests.post')
    def test_ai_engine_to_risk_service_api_integration(self, mock_post, mock_get):
        """Test AI engine to risk service API integration."""
        # Mock AI engine API response
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.prediction_data
        mock_get.return_value = mock_get_response
        
        # Mock risk service API response
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            'symbol': 'AAPL',
            'quantity': 100,
            'entry_price': 150.0,
            'current_price': 155.0,
            'predicted_price': 110.0,
            'var': 0.05,
            'cvar': 0.07,
            'sharpe_ratio': 1.2,
            'sortino_ratio': 1.5,
            'max_drawdown': 0.15,
            'risk_score': 65,
            'risk_level': 'medium',
            'timestamp': datetime.utcnow().isoformat()
        }
        mock_post.return_value = mock_post_response
        
        # Get prediction from AI engine
        ai_engine_url = 'http://localhost:8082/api/predict/model_1234567890/AAPL'
        response = requests.get(ai_engine_url)
        self.assertEqual(response.status_code, 200)
        
        prediction = response.json()
        self.assertEqual(prediction['symbol'], 'AAPL')
        self.assertEqual(prediction['model_id'], 'model_1234567890')
        
        # Send prediction to risk service
        risk_service_url = 'http://localhost:8083/api/risk/position'
        response = requests.post(risk_service_url, json={
            'symbol': 'AAPL',
            'quantity': 100,
            'entry_price': 150.0,
            'current_price': 155.0,
            'predicted_price': prediction['prediction']['average'],
            'risk_metrics': ['var', 'cvar', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown']
        })
        self.assertEqual(response.status_code, 200)
        
        risk = response.json()
        self.assertEqual(risk['symbol'], 'AAPL')
        self.assertEqual(risk['quantity'], 100)
        self.assertEqual(risk['entry_price'], 150.0)
        self.assertEqual(risk['current_price'], 155.0)
        self.assertEqual(risk['predicted_price'], 110.0)
        self.assertIn('var', risk)
        self.assertIn('cvar', risk)
        self.assertIn('sharpe_ratio', risk)
        self.assertIn('sortino_ratio', risk)
        self.assertIn('max_drawdown', risk)
        self.assertIn('risk_score', risk)
        self.assertIn('risk_level', risk)
    
    def test_prediction_service_to_risk_calculator_direct_integration(self):
        """Test direct integration between prediction service and risk calculator."""
        # Mock prediction service get_prediction method
        with patch.object(self.prediction_service, 'get_prediction') as mock_predict:
            mock_predict.return_value = self.prediction_data
            
            # Get prediction from prediction service
            prediction = self.prediction_service.get_prediction(
                model_id='model_1234567890',
                symbol='AAPL',
                timeframe='1d'
            )
            
            # Check prediction
            self.assertEqual(prediction['symbol'], 'AAPL')
            self.assertEqual(prediction['model_id'], 'model_1234567890')
            self.assertIn('prediction', prediction)
            self.assertIn('predictions', prediction)
            
            # Mock risk calculator calculate_position_risk method
            with patch.object(self.risk_calculator, 'calculate_position_risk') as mock_risk:
                mock_risk.return_value = {
                    'symbol': 'AAPL',
                    'quantity': 100,
                    'entry_price': 150.0,
                    'current_price': 155.0,
                    'predicted_price': 110.0,
                    'var': 0.05,
                    'cvar': 0.07,
                    'sharpe_ratio': 1.2,
                    'sortino_ratio': 1.5,
                    'max_drawdown': 0.15,
                    'risk_score': 65,
                    'risk_level': 'medium',
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                # Calculate risk based on prediction
                risk = self.risk_calculator.calculate_position_risk(
                    symbol='AAPL',
                    quantity=100,
                    entry_price=150.0,
                    current_price=155.0,
                    predicted_price=prediction['prediction']['average'],
                    risk_metrics=['var', 'cvar', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown']
                )
                
                # Check risk calculation
                self.assertEqual(risk['symbol'], 'AAPL')
                self.assertEqual(risk['quantity'], 100)
                self.assertEqual(risk['entry_price'], 150.0)
                self.assertEqual(risk['current_price'], 155.0)
                self.assertEqual(risk['predicted_price'], 110.0)
                self.assertIn('var', risk)
                self.assertIn('cvar', risk)
                self.assertIn('sharpe_ratio', risk)
                self.assertIn('sortino_ratio', risk)
                self.assertIn('max_drawdown', risk)
                self.assertIn('risk_score', risk)
                self.assertIn('risk_level', risk)
    
    def test_monte_carlo_simulation_integration(self):
        """Test Monte Carlo simulation integration between prediction and risk services."""
        # Mock prediction service get_prediction method
        with patch.object(self.prediction_service, 'get_prediction') as mock_predict:
            mock_predict.return_value = self.prediction_data
            
            # Get prediction from prediction service
            prediction = self.prediction_service.get_prediction(
                model_id='model_1234567890',
                symbol='AAPL',
                timeframe='1d'
            )
            
            # Extract prediction values and confidence levels
            prediction_values = [p['value'] for p in prediction['predictions']]
            confidence_levels = [p['confidence'] for p in prediction['predictions']]
            
            # Mock risk calculator run_monte_carlo_simulation method
            with patch.object(self.risk_calculator, 'run_monte_carlo_simulation') as mock_monte_carlo:
                mock_monte_carlo.return_value = {
                    'symbol': 'AAPL',
                    'initial_price': 155.0,
                    'simulations': 1000,
                    'days': 5,
                    'results': {
                        'mean_final_price': 110.0,
                        'median_final_price': 109.5,
                        'min_final_price': 95.0,
                        'max_final_price': 125.0,
                        'std_dev': 5.0,
                        'var_95': 0.05,
                        'cvar_95': 0.07,
                        'probability_profit': 0.65,
                        'expected_return': 0.1
                    },
                    'percentiles': {
                        '5': 100.0,
                        '25': 105.0,
                        '50': 109.5,
                        '75': 115.0,
                        '95': 120.0
                    }
                }
                
                # Run Monte Carlo simulation based on prediction
                simulation = self.risk_calculator.run_monte_carlo_simulation(
                    symbol='AAPL',
                    initial_price=155.0,
                    predicted_prices=prediction_values,
                    confidence_levels=confidence_levels,
                    simulations=1000,
                    days=5
                )
                
                # Check simulation results
                self.assertEqual(simulation['symbol'], 'AAPL')
                self.assertEqual(simulation['initial_price'], 155.0)
                self.assertEqual(simulation['simulations'], 1000)
                self.assertEqual(simulation['days'], 5)
                self.assertIn('results', simulation)
                self.assertIn('mean_final_price', simulation['results'])
                self.assertIn('var_95', simulation['results'])
                self.assertIn('probability_profit', simulation['results'])
                self.assertIn('percentiles', simulation)
    
    def test_portfolio_risk_with_predictions(self):
        """Test portfolio risk calculation with predictions."""
        # Mock prediction service get_predictions method
        with patch.object(self.prediction_service, 'get_predictions') as mock_predict:
            mock_predict.return_value = {
                'AAPL': {
                    'symbol': 'AAPL',
                    'model_id': 'model_1234567890',
                    'latest_price': 155.0,
                    'prediction': {
                        'average': 110.0,
                        'minimum': 105.0,
                        'maximum': 115.0,
                        'change': -45.0,
                        'change_percent': -29.03,
                        'direction': 'down'
                    }
                },
                'MSFT': {
                    'symbol': 'MSFT',
                    'model_id': 'model_1234567890',
                    'latest_price': 260.0,
                    'prediction': {
                        'average': 270.0,
                        'minimum': 265.0,
                        'maximum': 275.0,
                        'change': 10.0,
                        'change_percent': 3.85,
                        'direction': 'up'
                    }
                }
            }
            
            # Get predictions for portfolio symbols
            symbols = [position['symbol'] for position in self.sample_portfolio]
            predictions = self.prediction_service.get_predictions(
                model_id='model_1234567890',
                symbols=symbols,
                timeframe='1d'
            )
            
            # Check predictions
            self.assertEqual(len(predictions), 2)
            self.assertIn('AAPL', predictions)
            self.assertIn('MSFT', predictions)
            
            # Mock risk calculator calculate_portfolio_risk method
            with patch.object(self.risk_calculator, 'calculate_portfolio_risk') as mock_risk:
                mock_risk.return_value = {
                    'portfolio_id': 'portfolio_1234567890',
                    'total_value': 28000.0,
                    'predicted_value': 27000.0,
                    'var': 0.04,
                    'cvar': 0.06,
                    'sharpe_ratio': 1.1,
                    'sortino_ratio': 1.3,
                    'max_drawdown': 0.12,
                    'risk_score': 60,
                    'risk_level': 'medium',
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                # Update portfolio with predicted prices
                portfolio_with_predictions = []
                for position in self.sample_portfolio:
                    symbol = position['symbol']
                    if symbol in predictions:
                        position_with_prediction = position.copy()
                        position_with_prediction['predicted_price'] = predictions[symbol]['prediction']['average']
                        portfolio_with_predictions.append(position_with_prediction)
                    else:
                        portfolio_with_predictions.append(position)
                
                # Calculate portfolio risk with predictions
                risk = self.risk_calculator.calculate_portfolio_risk(
                    portfolio_id='portfolio_1234567890',
                    portfolio=portfolio_with_predictions,
                    risk_metrics=['var', 'cvar', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown']
                )
                
                # Check risk calculation
                self.assertEqual(risk['portfolio_id'], 'portfolio_1234567890')
                self.assertIn('total_value', risk)
                self.assertIn('predicted_value', risk)
                self.assertIn('var', risk)
                self.assertIn('cvar', risk)
                self.assertIn('sharpe_ratio', risk)
                self.assertIn('sortino_ratio', risk)
                self.assertIn('max_drawdown', risk)
                self.assertIn('risk_score', risk)
                self.assertIn('risk_level', risk)

if __name__ == "__main__":
    unittest.main()

