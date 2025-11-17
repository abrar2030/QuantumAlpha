"""
Unit tests for the Data Service.
"""

import json
import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import NotFoundError, ServiceError, ValidationError
from data_service.data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor"""

    def setUp(self):
        """Set up test environment"""
        # Mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get.return_value = "test_value"

        # Mock database manager
        self.db_manager = MagicMock()

        # Create data processor
        self.data_processor = DataProcessor(self.config_manager, self.db_manager)

        # Sample market data
        self.market_data = [
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
            {
                "timestamp": "2023-01-03T00:00:00Z",
                "open": 105.0,
                "high": 110.0,
                "low": 103.0,
                "close": 108.0,
                "volume": 1500,
            },
            {
                "timestamp": "2023-01-04T00:00:00Z",
                "open": 108.0,
                "high": 112.0,
                "low": 106.0,
                "close": 110.0,
                "volume": 1300,
            },
            {
                "timestamp": "2023-01-05T00:00:00Z",
                "open": 110.0,
                "high": 115.0,
                "low": 108.0,
                "close": 112.0,
                "volume": 1400,
            },
        ]

    def test_process_market_data_basic(self):
        """Test basic market data processing"""
        # Process data
        df = self.data_processor.process_market_data(self.market_data)

        # Check result
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)
        self.assertTrue("open" in df.columns)
        self.assertTrue("high" in df.columns)
        self.assertTrue("low" in df.columns)
        self.assertTrue("close" in df.columns)
        self.assertTrue("volume" in df.columns)

    def test_process_market_data_with_features(self):
        """Test market data processing with features"""
        # Process data with features
        df = self.data_processor.process_market_data(
            self.market_data, features=["sma", "rsi"]
        )

        # Check result
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)
        self.assertTrue("sma_20" in df.columns)
        self.assertTrue("rsi_14" in df.columns)

    def test_process_market_data_empty(self):
        """Test market data processing with empty data"""
        # Try to process empty data
        with self.assertRaises(ValidationError):
            self.data_processor.process_market_data([])

    def test_process_market_data_missing_columns(self):
        """Test market data processing with missing columns"""
        # Create data with missing columns
        data = [
            {
                "timestamp": "2023-01-01T00:00:00Z",
                "open": 100.0,
                "high": 105.0,
                "low": 95.0,
                # Missing close and volume
            }
        ]

        # Try to process data
        with self.assertRaises(ValidationError):
            self.data_processor.process_market_data(data)

    def test_normalize_data(self):
        """Test data normalization"""
        # Process data
        df = self.data_processor.process_market_data(self.market_data)

        # Normalize data
        df_normalized = self.data_processor.normalize_data(df)

        # Check result
        self.assertIsInstance(df_normalized, pd.DataFrame)
        self.assertEqual(len(df_normalized), 5)
        self.assertTrue("close_norm" in df_normalized.columns)
        self.assertTrue("volume_norm" in df_normalized.columns)

        # Check normalization
        self.assertTrue(
            0
            <= df_normalized["close_norm"].min()
            <= df_normalized["close_norm"].max()
            <= 1
        )
        self.assertTrue(
            0
            <= df_normalized["volume_norm"].min()
            <= df_normalized["volume_norm"].max()
            <= 1
        )

    def test_prepare_data_for_ml(self):
        """Test data preparation for machine learning"""
        # Process data
        df = self.data_processor.process_market_data(self.market_data)

        # Prepare data for ML
        X_train, X_test, y_train, y_test, scaler = (
            self.data_processor.prepare_data_for_ml(
                df=df,
                target_column="close",
                sequence_length=2,
                target_shift=1,
                test_size=0.5,
            )
        )

        # Check result
        self.assertIsInstance(X_train, np.ndarray)
        self.assertIsInstance(X_test, np.ndarray)
        self.assertIsInstance(y_train, np.ndarray)
        self.assertIsInstance(y_test, np.ndarray)
        self.assertEqual(X_train.shape[1], 2)  # sequence_length
        self.assertEqual(X_train.shape[2], 5)  # number of features

    def test_detect_anomalies(self):
        """Test anomaly detection"""
        # Process data
        df = self.data_processor.process_market_data(self.market_data)

        # Detect anomalies
        df_anomalies = self.data_processor.detect_anomalies(
            df=df, column="close", window=2, threshold=2.0
        )

        # Check result
        self.assertIsInstance(df_anomalies, pd.DataFrame)
        self.assertEqual(len(df_anomalies), 5)
        self.assertTrue("anomaly" in df_anomalies.columns)

    def test_generate_signals(self):
        """Test signal generation"""
        # Process data
        df = self.data_processor.process_market_data(self.market_data)

        # Generate signals
        df_signals = self.data_processor.generate_signals(
            df=df, strategy="sma_crossover"
        )

        # Check result
        self.assertIsInstance(df_signals, pd.DataFrame)
        self.assertEqual(len(df_signals), 5)
        self.assertTrue("signal" in df_signals.columns)
        self.assertTrue(df_signals["signal"].isin([-1, 0, 1]).all())


if __name__ == "__main__":
    unittest.main()
