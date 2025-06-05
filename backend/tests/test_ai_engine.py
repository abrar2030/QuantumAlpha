"""
Unit tests for the AI Engine.
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

from ai_engine.model_manager import ModelManager
from ai_engine.prediction_service import PredictionService
from common import ServiceError, ValidationError, NotFoundError

class TestModelManager(unittest.TestCase):
    """Test cases for ModelManager"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get.return_value = '/tmp/test_models'
        
        # Mock database manager
        self.db_manager = MagicMock()
        
        # Create model manager
        with patch('os.makedirs'):
            with patch('os.path.exists', return_value=False):
                self.model_manager = ModelManager(self.config_manager, self.db_manager)
        
        # Mock registry
        self.model_manager.model_registry = {
            'models': {}
        }
        
        # Mock save registry
        self.model_manager._save_registry = MagicMock()
    
    def test_create_model(self):
        """Test model creation"""
        # Create model
        model_data = {
            'name': 'Test Model',
            'description': 'Test model description',
            'type': 'lstm',
            'parameters': {
                'param1': 'value1',
                'param2': 'value2'
            },
            'features': ['feature1', 'feature2']
        }
        
        result = self.model_manager.create_model(model_data)
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertTrue('id' in result)
        self.assertEqual(result['name'], 'Test Model')
        self.assertEqual(result['description'], 'Test model description')
        self.assertEqual(result['type'], 'lstm')
        self.assertEqual(result['status'], 'created')
        self.assertEqual(result['parameters'], {'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result['features'], ['feature1', 'feature2'])
        
        # Check registry
        model_id = result['id']
        self.assertTrue(model_id in self.model_manager.model_registry['models'])
        self.assertEqual(self.model_manager.model_registry['models'][model_id]['name'], 'Test Model')
    
    def test_create_model_missing_name(self):
        """Test model creation with missing name"""
        # Try to create model without name
        model_data = {
            'type': 'lstm'
        }
        
        with self.assertRaises(ValidationError):
            self.model_manager.create_model(model_data)
    
    def test_create_model_missing_type(self):
        """Test model creation with missing type"""
        # Try to create model without type
        model_data = {
            'name': 'Test Model'
        }
        
        with self.assertRaises(ValidationError):
            self.model_manager.create_model(model_data)
    
    def test_get_models(self):
        """Test getting all models"""
        # Add models to registry
        self.model_manager.model_registry['models'] = {
            'model1': {
                'name': 'Model 1',
                'description': 'Model 1 description',
                'type': 'lstm',
                'status': 'created',
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T00:00:00Z'
            },
            'model2': {
                'name': 'Model 2',
                'description': 'Model 2 description',
                'type': 'cnn',
                'status': 'trained',
                'created_at': '2023-01-02T00:00:00Z',
                'updated_at': '2023-01-02T00:00:00Z',
                'metrics': {
                    'accuracy': 0.9
                }
            }
        }
        
        # Get models
        models = self.model_manager.get_models()
        
        # Check result
        self.assertIsInstance(models, list)
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]['id'], 'model1')
        self.assertEqual(models[0]['name'], 'Model 1')
        self.assertEqual(models[1]['id'], 'model2')
        self.assertEqual(models[1]['name'], 'Model 2')
        self.assertEqual(models[1]['metrics'], {'accuracy': 0.9})
    
    def test_get_model(self):
        """Test getting a specific model"""
        # Add model to registry
        self.model_manager.model_registry['models'] = {
            'model1': {
                'name': 'Model 1',
                'description': 'Model 1 description',
                'type': 'lstm',
                'status': 'created',
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T00:00:00Z',
                'parameters': {
                    'param1': 'value1'
                },
                'features': ['feature1']
            }
        }
        
        # Get model
        model = self.model_manager.get_model('model1')
        
        # Check result
        self.assertIsInstance(model, dict)
        self.assertEqual(model['id'], 'model1')
        self.assertEqual(model['name'], 'Model 1')
        self.assertEqual(model['description'], 'Model 1 description')
        self.assertEqual(model['type'], 'lstm')
        self.assertEqual(model['status'], 'created')
        self.assertEqual(model['parameters'], {'param1': 'value1'})
        self.assertEqual(model['features'], ['feature1'])
    
    def test_get_model_not_found(self):
        """Test getting a non-existent model"""
        # Try to get non-existent model
        with self.assertRaises(NotFoundError):
            self.model_manager.get_model('non_existent_model')
    
    def test_update_model(self):
        """Test updating a model"""
        # Add model to registry
        self.model_manager.model_registry['models'] = {
            'model1': {
                'name': 'Model 1',
                'description': 'Model 1 description',
                'type': 'lstm',
                'status': 'created',
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T00:00:00Z',
                'parameters': {
                    'param1': 'value1'
                },
                'features': ['feature1']
            }
        }
        
        # Update model
        update_data = {
            'name': 'Updated Model',
            'description': 'Updated description',
            'parameters': {
                'param1': 'new_value',
                'param2': 'value2'
            },
            'features': ['feature1', 'feature2']
        }
        
        result = self.model_manager.update_model('model1', update_data)
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], 'model1')
        self.assertEqual(result['name'], 'Updated Model')
        self.assertEqual(result['description'], 'Updated description')
        self.assertEqual(result['parameters'], {'param1': 'new_value', 'param2': 'value2'})
        self.assertEqual(result['features'], ['feature1', 'feature2'])
        
        # Check registry
        self.assertEqual(self.model_manager.model_registry['models']['model1']['name'], 'Updated Model')
        self.assertEqual(self.model_manager.model_registry['models']['model1']['description'], 'Updated description')
    
    def test_update_model_not_found(self):
        """Test updating a non-existent model"""
        # Try to update non-existent model
        update_data = {
            'name': 'Updated Model'
        }
        
        with self.assertRaises(NotFoundError):
            self.model_manager.update_model('non_existent_model', update_data)
    
    def test_delete_model(self):
        """Test deleting a model"""
        # Add model to registry
        self.model_manager.model_registry['models'] = {
            'model1': {
                'name': 'Model 1',
                'description': 'Model 1 description',
                'type': 'lstm',
                'status': 'created',
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-01-01T00:00:00Z'
            }
        }
        
        # Mock os.path.exists and os.remove
        with patch('os.path.exists', return_value=True):
            with patch('os.remove'):
                # Delete model
                result = self.model_manager.delete_model('model1')
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['id'], 'model1')
        self.assertEqual(result['name'], 'Model 1')
        self.assertTrue(result['deleted'])
        
        # Check registry
        self.assertFalse('model1' in self.model_manager.model_registry['models'])
    
    def test_delete_model_not_found(self):
        """Test deleting a non-existent model"""
        # Try to delete non-existent model
        with self.assertRaises(NotFoundError):
            self.model_manager.delete_model('non_existent_model')

class TestPredictionService(unittest.TestCase):
    """Test cases for PredictionService"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get.return_value = 'http://localhost:8080'
        
        # Mock database manager
        self.db_manager = MagicMock()
        
        # Mock model manager
        self.model_manager = MagicMock()
        
        # Create prediction service
        self.prediction_service = PredictionService(self.config_manager, self.db_manager, self.model_manager)
        
        # Sample market data
        self.market_data = [
            {
                'timestamp': '2023-01-01T00:00:00Z',
                'open': 100.0,
                'high': 105.0,
                'low': 95.0,
                'close': 102.0,
                'volume': 1000
            },
            {
                'timestamp': '2023-01-02T00:00:00Z',
                'open': 102.0,
                'high': 107.0,
                'low': 100.0,
                'close': 105.0,
                'volume': 1200
            },
            {
                'timestamp': '2023-01-03T00:00:00Z',
                'open': 105.0,
                'high': 110.0,
                'low': 103.0,
                'close': 108.0,
                'volume': 1500
            },
            {
                'timestamp': '2023-01-04T00:00:00Z',
                'open': 108.0,
                'high': 112.0,
                'low': 106.0,
                'close': 110.0,
                'volume': 1300
            },
            {
                'timestamp': '2023-01-05T00:00:00Z',
                'open': 110.0,
                'high': 115.0,
                'low': 108.0,
                'close': 112.0,
                'volume': 1400
            }
        ]
    
    @patch('requests.get')
    def test_generate_prediction(self, mock_get):
        """Test prediction generation"""
        # Mock model manager predict
        self.model_manager.predict.return_value = {
            'symbol': 'AAPL',
            'timeframe': '1d',
            'predictions': [
                {'timestamp': '2023-01-06T00:00:00Z', 'value': 115.0},
                {'timestamp': '2023-01-07T00:00:00Z', 'value': 118.0},
                {'timestamp': '2023-01-08T00:00:00Z', 'value': 120.0},
                {'timestamp': '2023-01-09T00:00:00Z', 'value': 122.0},
                {'timestamp': '2023-01-10T00:00:00Z', 'value': 125.0}
            ]
        }
        
        # Mock requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [self.market_data[-1]]}
        mock_get.return_value = mock_response
        
        # Generate prediction
        result = self.prediction_service.generate_prediction(
            model_id='model1',
            symbol='AAPL',
            timeframe='1d',
            period='1mo',
            horizon=5
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['symbol'], 'AAPL')
        self.assertEqual(result['model_id'], 'model1')
        self.assertEqual(result['latest_price'], 112.0)
        self.assertTrue('prediction' in result)
        self.assertTrue('average' in result['prediction'])
        self.assertTrue('minimum' in result['prediction'])
        self.assertTrue('maximum' in result['prediction'])
        self.assertTrue('change' in result['prediction'])
        self.assertTrue('change_percent' in result['prediction'])
        self.assertTrue('direction' in result['prediction'])
        self.assertEqual(len(result['predictions']), 5)
    
    def test_generate_prediction_missing_model_id(self):
        """Test prediction generation with missing model ID"""
        # Try to generate prediction without model ID
        with self.assertRaises(ValidationError):
            self.prediction_service.generate_prediction(
                model_id='',
                symbol='AAPL',
                timeframe='1d',
                period='1mo',
                horizon=5
            )
    
    def test_generate_prediction_missing_symbol(self):
        """Test prediction generation with missing symbol"""
        # Try to generate prediction without symbol
        with self.assertRaises(ValidationError):
            self.prediction_service.generate_prediction(
                model_id='model1',
                symbol='',
                timeframe='1d',
                period='1mo',
                horizon=5
            )
    
    @patch('requests.get')
    def test_generate_signals(self, mock_get):
        """Test signal generation"""
        # Mock model manager predict
        self.model_manager.predict.return_value = {
            'symbol': 'AAPL',
            'timeframe': '1d',
            'predictions': [
                {'timestamp': '2023-01-06T00:00:00Z', 'value': 115.0},
                {'timestamp': '2023-01-07T00:00:00Z', 'value': 118.0},
                {'timestamp': '2023-01-08T00:00:00Z', 'value': 120.0},
                {'timestamp': '2023-01-09T00:00:00Z', 'value': 122.0},
                {'timestamp': '2023-01-10T00:00:00Z', 'value': 125.0}
            ]
        }
        
        # Mock requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [self.market_data[-1]]}
        mock_get.return_value = mock_response
        
        # Generate signals
        result = self.prediction_service.generate_signals(
            symbols=['AAPL', 'MSFT'],
            model_id='model1',
            timeframe='1d',
            period='1mo',
            strategy='prediction'
        )
        
        # Check result
        self.assertIsInstance(result, dict)
        self.assertEqual(result['strategy'], 'prediction')
        self.assertEqual(result['model_id'], 'model1')
        self.assertTrue('signals' in result)
        self.assertTrue('count' in result)
        self.assertTrue('generated_at' in result)
        
        # Check signals
        signals = result['signals']
        self.assertIsInstance(signals, list)
        self.assertEqual(len(signals), 2)
        self.assertEqual(signals[0]['symbol'], 'AAPL')
        self.assertTrue('type' in signals[0])
        self.assertTrue('strength' in signals[0])
        self.assertTrue('price' in signals[0])
        self.assertTrue('prediction' in signals[0])
    
    def test_generate_signals_missing_symbols(self):
        """Test signal generation with missing symbols"""
        # Try to generate signals without symbols
        with self.assertRaises(ValidationError):
            self.prediction_service.generate_signals(
                symbols=[],
                model_id='model1',
                timeframe='1d',
                period='1mo',
                strategy='prediction'
            )
    
    def test_generate_signals_missing_model_id(self):
        """Test signal generation with missing model ID"""
        # Try to generate signals without model ID
        with self.assertRaises(ValidationError):
            self.prediction_service.generate_signals(
                symbols=['AAPL', 'MSFT'],
                model_id=None,
                timeframe='1d',
                period='1mo',
                strategy='prediction'
            )
    
    def test_generate_signals_invalid_strategy(self):
        """Test signal generation with invalid strategy"""
        # Try to generate signals with invalid strategy
        with self.assertRaises(ValidationError):
            self.prediction_service.generate_signals(
                symbols=['AAPL', 'MSFT'],
                model_id='model1',
                timeframe='1d',
                period='1mo',
                strategy='invalid_strategy'
            )

if __name__ == '__main__':
    unittest.main()

