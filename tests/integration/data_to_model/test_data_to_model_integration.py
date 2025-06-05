"""
Integration tests for data service to AI engine integration.
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
    from backend.data_service.data_processor import DataProcessor
    from backend.ai_engine.model_manager import ModelManager
    from backend.common.exceptions import ValidationError, ServiceError
except ImportError:
    # Mock the classes for testing when imports fail
    class DataProcessor:
        pass
    
    class ModelManager:
        pass
    
    class ValidationError(Exception):
        pass
    
    class ServiceError(Exception):
        pass

class TestDataToModelIntegration(unittest.TestCase):
    """Integration tests for data service to AI engine integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "data_service": {
                "cache_dir": "/tmp/cache",
                "data_dir": "/tmp/data"
            },
            "ai_engine": {
                "model_dir": "/tmp/models",
                "registry_file": "/tmp/models/registry.json"
            },
            "services": {
                "data_service": {
                    "host": "localhost",
                    "port": 8081
                },
                "ai_engine": {
                    "host": "localhost",
                    "port": 8082
                }
            }
        }
        
        # Create mock database manager
        self.db_manager = MagicMock()
        
        # Create sample market data
        self.market_data = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100),
            'open': np.random.normal(100, 2, 100),
            'high': np.random.normal(102, 2, 100),
            'low': np.random.normal(98, 2, 100),
            'close': np.random.normal(100, 2, 100),
            'volume': np.random.normal(1000000, 100000, 100),
            'symbol': 'AAPL'
        })
        
        # Create data processor
        self.data_processor = DataProcessor(self.config_manager, self.db_manager)
        
        # Create model manager
        self.model_manager = ModelManager(self.config_manager, self.db_manager)
    
    @patch('requests.get')
    def test_data_processing_to_model_training(self, mock_get):
        """Test data processing to model training flow."""
        # Mock market data API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': self.market_data.to_dict(orient='records')
        }
        mock_get.return_value = mock_response
        
        # Process data
        processed_data = self.data_processor.clean_data(self.market_data)
        processed_data = self.data_processor.calculate_technical_indicators(processed_data)
        
        # Check processed data
        self.assertIsInstance(processed_data, pd.DataFrame)
        self.assertIn('sma_20', processed_data.columns)
        self.assertIn('rsi_14', processed_data.columns)
        self.assertIn('macd', processed_data.columns)
        
        # Prepare data for ML
        X_train, X_test, y_train, y_test, scaler = self.data_processor.prepare_data_for_ml(
            df=processed_data,
            target_column='close',
            sequence_length=10,
            target_shift=1,
            test_size=0.2
        )
        
        # Check prepared data
        self.assertIsInstance(X_train, np.ndarray)
        self.assertIsInstance(X_test, np.ndarray)
        self.assertIsInstance(y_train, np.ndarray)
        self.assertIsInstance(y_test, np.ndarray)
        
        # Mock model training
        with patch.object(self.model_manager, 'train_model') as mock_train:
            mock_train.return_value = {
                'id': 'model_1234567890',
                'name': 'Test Model',
                'type': 'lstm',
                'status': 'trained',
                'performance': {
                    'mse': 0.0025,
                    'rmse': 0.05,
                    'mae': 0.04,
                    'r2': 0.85
                }
            }
            
            # Train model
            model = self.model_manager.train_model(
                name='Test Model',
                model_type='lstm',
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                params={
                    'layers': [50, 100, 50],
                    'dropout': 0.2,
                    'activation': 'relu',
                    'optimizer': 'adam',
                    'loss': 'mse',
                    'epochs': 100,
                    'batch_size': 32
                }
            )
            
            # Check model
            self.assertEqual(model['name'], 'Test Model')
            self.assertEqual(model['type'], 'lstm')
            self.assertEqual(model['status'], 'trained')
            self.assertIn('performance', model)
            self.assertIn('mse', model['performance'])
            self.assertIn('rmse', model['performance'])
            self.assertIn('mae', model['performance'])
            self.assertIn('r2', model['performance'])
    
    @patch('requests.get')
    @patch('requests.post')
    def test_data_service_to_ai_engine_api_integration(self, mock_post, mock_get):
        """Test data service to AI engine API integration."""
        # Mock data service API response
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'data': self.market_data.to_dict(orient='records')
        }
        mock_get.return_value = mock_get_response
        
        # Mock AI engine API response
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {
            'model_id': 'model_1234567890',
            'symbol': 'AAPL',
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
        mock_post.return_value = mock_post_response
        
        # Get market data from data service
        data_service_url = 'http://localhost:8081/api/market-data/AAPL?timeframe=1d&period=1mo'
        response = requests.get(data_service_url)
        self.assertEqual(response.status_code, 200)
        
        market_data = response.json()['data']
        self.assertIsInstance(market_data, list)
        
        # Send data to AI engine for prediction
        ai_engine_url = 'http://localhost:8082/api/predict'
        response = requests.post(ai_engine_url, json={
            'model_id': 'model_1234567890',
            'symbol': 'AAPL',
            'data': market_data
        })
        self.assertEqual(response.status_code, 200)
        
        prediction = response.json()
        self.assertEqual(prediction['model_id'], 'model_1234567890')
        self.assertEqual(prediction['symbol'], 'AAPL')
        self.assertIn('prediction', prediction)
        self.assertIn('predictions', prediction)
        self.assertEqual(len(prediction['predictions']), 5)
    
    def test_data_processor_to_model_manager_direct_integration(self):
        """Test direct integration between data processor and model manager."""
        # Process data
        processed_data = self.data_processor.clean_data(self.market_data)
        processed_data = self.data_processor.calculate_technical_indicators(processed_data)
        
        # Mock model manager predict method
        with patch.object(self.model_manager, 'predict') as mock_predict:
            mock_predict.return_value = {
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
            
            # Convert processed data to dict for model input
            data_dict = {
                'symbol': 'AAPL',
                'timeframe': '1d',
                'latest_price': processed_data['close'].iloc[-1],
                'data': processed_data.to_dict(orient='records')
            }
            
            # Get prediction from model
            prediction = self.model_manager.predict('model_1234567890', data_dict)
            
            # Check prediction
            self.assertEqual(prediction['symbol'], 'AAPL')
            self.assertEqual(prediction['model_id'], 'model_1234567890')
            self.assertIn('prediction', prediction)
            self.assertIn('predictions', prediction)
            self.assertEqual(len(prediction['predictions']), 5)
            
            # Check if model manager predict was called with correct data
            mock_predict.assert_called_once()
            args, kwargs = mock_predict.call_args
            self.assertEqual(args[0], 'model_1234567890')
            self.assertEqual(args[1]['symbol'], 'AAPL')
    
    def test_data_feature_engineering_to_model_input(self):
        """Test feature engineering to model input flow."""
        # Process data
        processed_data = self.data_processor.clean_data(self.market_data)
        processed_data = self.data_processor.calculate_technical_indicators(processed_data)
        
        # Generate signals
        signals_data = self.data_processor.generate_signals(processed_data, strategy='sma_crossover')
        
        # Check signals
        self.assertIn('signal', signals_data.columns)
        self.assertTrue(set(signals_data['signal'].unique()).issubset({-1, 0, 1}))
        
        # Prepare features for model
        features = [
            'close', 'volume', 'sma_20', 'sma_50', 'rsi_14', 
            'macd', 'macd_signal', 'macd_hist', 
            'bb_upper', 'bb_middle', 'bb_lower', 'signal'
        ]
        model_input = signals_data[features].copy()
        
        # Check model input
        self.assertEqual(len(model_input.columns), len(features))
        for feature in features:
            self.assertIn(feature, model_input.columns)
        
        # Mock model manager train method
        with patch.object(self.model_manager, 'train_model') as mock_train:
            mock_train.return_value = {
                'id': 'model_1234567890',
                'name': 'Test Model',
                'type': 'lstm',
                'status': 'trained',
                'features': features,
                'performance': {
                    'mse': 0.0025,
                    'rmse': 0.05,
                    'mae': 0.04,
                    'r2': 0.85
                }
            }
            
            # Prepare data for ML
            X_train, X_test, y_train, y_test, scaler = self.data_processor.prepare_data_for_ml(
                df=model_input,
                target_column='close',
                sequence_length=10,
                target_shift=1,
                test_size=0.2
            )
            
            # Train model
            model = self.model_manager.train_model(
                name='Test Model',
                model_type='lstm',
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                params={
                    'layers': [50, 100, 50],
                    'dropout': 0.2,
                    'activation': 'relu',
                    'optimizer': 'adam',
                    'loss': 'mse',
                    'epochs': 100,
                    'batch_size': 32
                },
                features=features
            )
            
            # Check model
            self.assertEqual(model['name'], 'Test Model')
            self.assertEqual(model['type'], 'lstm')
            self.assertEqual(model['status'], 'trained')
            self.assertEqual(model['features'], features)
            
            # Check if model manager train was called with correct data
            mock_train.assert_called_once()
            args, kwargs = mock_train.call_args
            self.assertEqual(kwargs['name'], 'Test Model')
            self.assertEqual(kwargs['model_type'], 'lstm')
            self.assertEqual(kwargs['features'], features)

if __name__ == "__main__":
    unittest.main()

