"""
Unit tests for the Data Service's Data Processor.
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

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import module to test
try:
    from backend.data_service.data_processor import DataProcessor
    from backend.common.exceptions import ValidationError, ServiceError
except ImportError:
    # Mock the classes for testing when imports fail
    class DataProcessor:
        pass
    
    class ValidationError(Exception):
        pass
    
    class ServiceError(Exception):
        pass

class TestDataProcessor(unittest.TestCase):
    """Unit tests for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "data_service": {
                "cache_dir": "/tmp/cache",
                "data_dir": "/tmp/data"
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
    
    def test_init(self):
        """Test DataProcessor initialization."""
        data_processor = DataProcessor(self.config_manager, self.db_manager)
        
        # Check attributes
        self.assertEqual(data_processor.config_manager, self.config_manager)
        self.assertEqual(data_processor.db_manager, self.db_manager)
        self.assertEqual(data_processor.cache_dir, "/tmp/cache")
        self.assertEqual(data_processor.data_dir, "/tmp/data")
    
    def test_clean_data(self):
        """Test data cleaning."""
        # Create data with NaN values
        df = self.market_data.copy()
        df.loc[10:15, 'close'] = np.nan
        df.loc[20:25, 'volume'] = np.nan
        
        # Clean data
        cleaned_df = self.data_processor.clean_data(df)
        
        # Check result
        self.assertEqual(len(cleaned_df), len(df))
        self.assertFalse(cleaned_df['close'].isna().any())
        self.assertFalse(cleaned_df['volume'].isna().any())
    
    def test_clean_data_empty(self):
        """Test cleaning empty data."""
        # Create empty DataFrame
        df = pd.DataFrame()
        
        # Clean data and check exception
        with self.assertRaises(ValidationError):
            self.data_processor.clean_data(df)
    
    def test_clean_data_missing_columns(self):
        """Test cleaning data with missing columns."""
        # Create DataFrame with missing columns
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100),
            'close': np.random.normal(100, 2, 100),
            'symbol': 'AAPL'
        })
        
        # Clean data and check exception
        with self.assertRaises(ValidationError):
            self.data_processor.clean_data(df)
    
    def test_calculate_technical_indicators(self):
        """Test technical indicator calculation."""
        # Calculate indicators
        df = self.data_processor.calculate_technical_indicators(self.market_data)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('sma_20', df.columns)
        self.assertIn('sma_50', df.columns)
        self.assertIn('ema_20', df.columns)
        self.assertIn('rsi_14', df.columns)
        self.assertIn('macd', df.columns)
        self.assertIn('macd_signal', df.columns)
        self.assertIn('macd_hist', df.columns)
        self.assertIn('bb_upper', df.columns)
        self.assertIn('bb_middle', df.columns)
        self.assertIn('bb_lower', df.columns)
    
    def test_calculate_technical_indicators_empty(self):
        """Test calculating indicators for empty data."""
        # Create empty DataFrame
        df = pd.DataFrame()
        
        # Calculate indicators and check exception
        with self.assertRaises(ValidationError):
            self.data_processor.calculate_technical_indicators(df)
    
    def test_calculate_technical_indicators_missing_columns(self):
        """Test calculating indicators for data with missing columns."""
        # Create DataFrame with missing columns
        df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=100),
            'symbol': 'AAPL'
        })
        
        # Calculate indicators and check exception
        with self.assertRaises(ValidationError):
            self.data_processor.calculate_technical_indicators(df)
    
    def test_calculate_sma(self):
        """Test SMA calculation."""
        # Calculate SMA
        df = self.data_processor._calculate_sma(self.market_data, window=20)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('sma_20', df.columns)
        self.assertTrue(df['sma_20'].isna().sum() < len(df))
    
    def test_calculate_ema(self):
        """Test EMA calculation."""
        # Calculate EMA
        df = self.data_processor._calculate_ema(self.market_data, window=20)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('ema_20', df.columns)
        self.assertTrue(df['ema_20'].isna().sum() < len(df))
    
    def test_calculate_rsi(self):
        """Test RSI calculation."""
        # Calculate RSI
        df = self.data_processor._calculate_rsi(self.market_data, window=14)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('rsi_14', df.columns)
        self.assertTrue(df['rsi_14'].isna().sum() < len(df))
        self.assertTrue((df['rsi_14'] >= 0).all() and (df['rsi_14'] <= 100).all())
    
    def test_calculate_macd(self):
        """Test MACD calculation."""
        # Calculate MACD
        df = self.data_processor._calculate_macd(self.market_data)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('macd', df.columns)
        self.assertIn('macd_signal', df.columns)
        self.assertIn('macd_hist', df.columns)
        self.assertTrue(df['macd'].isna().sum() < len(df))
        self.assertTrue(df['macd_signal'].isna().sum() < len(df))
        self.assertTrue(df['macd_hist'].isna().sum() < len(df))
    
    def test_calculate_bollinger_bands(self):
        """Test Bollinger Bands calculation."""
        # Calculate Bollinger Bands
        df = self.data_processor._calculate_bollinger_bands(self.market_data, window=20, num_std=2)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('bb_upper', df.columns)
        self.assertIn('bb_middle', df.columns)
        self.assertIn('bb_lower', df.columns)
        self.assertTrue(df['bb_upper'].isna().sum() < len(df))
        self.assertTrue(df['bb_middle'].isna().sum() < len(df))
        self.assertTrue(df['bb_lower'].isna().sum() < len(df))
        
        # Check that upper > middle > lower
        valid_idx = ~df['bb_upper'].isna()
        self.assertTrue((df.loc[valid_idx, 'bb_upper'] >= df.loc[valid_idx, 'bb_middle']).all())
        self.assertTrue((df.loc[valid_idx, 'bb_middle'] >= df.loc[valid_idx, 'bb_lower']).all())
    
    def test_detect_anomalies(self):
        """Test anomaly detection."""
        # Detect anomalies
        df = self.data_processor.detect_anomalies(self.market_data, column='close', window=20, threshold=3.0)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('anomaly', df.columns)
        self.assertTrue(set(df['anomaly'].unique()).issubset({0, 1}))
    
    def test_detect_anomalies_invalid_column(self):
        """Test anomaly detection with invalid column."""
        # Detect anomalies with invalid column
        with self.assertRaises(ValidationError):
            self.data_processor.detect_anomalies(self.market_data, column='invalid', window=20, threshold=3.0)
    
    def test_generate_signals(self):
        """Test signal generation."""
        # Generate signals
        df = self.data_processor.generate_signals(self.market_data, strategy='sma_crossover')
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('signal', df.columns)
        self.assertTrue(set(df['signal'].unique()).issubset({-1, 0, 1}))
    
    def test_generate_signals_invalid_strategy(self):
        """Test signal generation with invalid strategy."""
        # Generate signals with invalid strategy
        with self.assertRaises(ValidationError):
            self.data_processor.generate_signals(self.market_data, strategy='invalid')
    
    def test_generate_sma_crossover_signals(self):
        """Test SMA crossover signal generation."""
        # Generate signals
        df = self.data_processor._generate_sma_crossover_signals(self.market_data)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('signal', df.columns)
        self.assertTrue(set(df['signal'].unique()).issubset({-1, 0, 1}))
    
    def test_generate_macd_signals(self):
        """Test MACD signal generation."""
        # Generate signals
        df = self.data_processor._generate_macd_signals(self.market_data)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('signal', df.columns)
        self.assertTrue(set(df['signal'].unique()).issubset({-1, 0, 1}))
    
    def test_generate_rsi_signals(self):
        """Test RSI signal generation."""
        # Generate signals
        df = self.data_processor._generate_rsi_signals(self.market_data)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('signal', df.columns)
        self.assertTrue(set(df['signal'].unique()).issubset({-1, 0, 1}))
    
    def test_generate_bollinger_bands_signals(self):
        """Test Bollinger Bands signal generation."""
        # Generate signals
        df = self.data_processor._generate_bollinger_bands_signals(self.market_data)
        
        # Check result
        self.assertEqual(len(df), len(self.market_data))
        self.assertIn('signal', df.columns)
        self.assertTrue(set(df['signal'].unique()).issubset({-1, 0, 1}))
    
    def test_prepare_data_for_ml(self):
        """Test data preparation for machine learning."""
        # Prepare data
        X_train, X_test, y_train, y_test, scaler = self.data_processor.prepare_data_for_ml(
            df=self.market_data,
            target_column='close',
            sequence_length=10,
            target_shift=1,
            test_size=0.2
        )
        
        # Check result
        self.assertIsInstance(X_train, np.ndarray)
        self.assertIsInstance(X_test, np.ndarray)
        self.assertIsInstance(y_train, np.ndarray)
        self.assertIsInstance(y_test, np.ndarray)
        self.assertIsNotNone(scaler)
        
        # Check shapes
        self.assertEqual(X_train.shape[1], 10)  # sequence_length
        self.assertEqual(X_test.shape[1], 10)  # sequence_length
        self.assertEqual(len(y_train.shape), 1)
        self.assertEqual(len(y_test.shape), 1)
        
        # Check train/test split
        total_samples = len(X_train) + len(X_test)
        self.assertAlmostEqual(len(X_test) / total_samples, 0.2, delta=0.1)  # test_size
    
    def test_prepare_data_for_ml_invalid_target(self):
        """Test data preparation with invalid target column."""
        # Prepare data with invalid target
        with self.assertRaises(ValidationError):
            self.data_processor.prepare_data_for_ml(
                df=self.market_data,
                target_column='invalid',
                sequence_length=10,
                target_shift=1,
                test_size=0.2
            )
    
    def test_prepare_data_for_ml_invalid_sequence_length(self):
        """Test data preparation with invalid sequence length."""
        # Prepare data with invalid sequence length
        with self.assertRaises(ValidationError):
            self.data_processor.prepare_data_for_ml(
                df=self.market_data,
                target_column='close',
                sequence_length=0,
                target_shift=1,
                test_size=0.2
            )
    
    def test_prepare_data_for_ml_invalid_test_size(self):
        """Test data preparation with invalid test size."""
        # Prepare data with invalid test size
        with self.assertRaises(ValidationError):
            self.data_processor.prepare_data_for_ml(
                df=self.market_data,
                target_column='close',
                sequence_length=10,
                target_shift=1,
                test_size=1.5
            )
    
    def test_create_sequences(self):
        """Test sequence creation."""
        # Create sequences
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        X, y = self.data_processor._create_sequences(data, sequence_length=3, target_shift=1)
        
        # Check result
        self.assertEqual(X.shape, (7, 3))
        self.assertEqual(y.shape, (7,))
        
        # Check first sequence
        np.testing.assert_array_equal(X[0], [1, 2, 3])
        self.assertEqual(y[0], 4)
        
        # Check last sequence
        np.testing.assert_array_equal(X[-1], [7, 8, 9])
        self.assertEqual(y[-1], 10)
    
    def test_create_sequences_invalid_length(self):
        """Test sequence creation with invalid length."""
        # Create sequences with data shorter than sequence length
        data = np.array([1, 2])
        with self.assertRaises(ValidationError):
            self.data_processor._create_sequences(data, sequence_length=3, target_shift=1)

if __name__ == "__main__":
    unittest.main()

