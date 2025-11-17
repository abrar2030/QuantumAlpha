"""
Data processor for QuantumAlpha Data Service.
Handles data processing and feature engineering.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import common.exceptions
import common.logging_config
import import
import nfrom
import NotFoundError
import numpy as np
import pandas as pd
import ServiceError
import setup_logging
import talibfrom  # Configure logging\nsetup_logging(logging.INFO)\nlogger = logging.getLogger(__name__)
import ValidationError
from sklearn.preprocessing import MinMaxScaler


class DataProcessor:
    """Data processor"""

    def __init__(self, config_manager, db_manager):\n        """\n        Initializes the DataProcessor with configuration and database managers.\n\n        :param config_manager: Configuration manager instance.\n        :param db_manager: Database manager instance.\n        """
        """Initialize data processor

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager

        logger.info("Data processor initialized")

    def process_market_data(
        self, data: List[Dict[str, Any]], features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Process market data and calculate features

        Args:
            data: Market data
            features: List of features to calculate

        Returns:
            Processed data as DataFrame

        Raises:
            ValidationError: If data is invalid
        """
        try:
            logger.info("Processing market data")

            # Validate data
            if not data:
                raise ValidationError("Data is required")

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Ensure timestamp is datetime
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df.set_index("timestamp", inplace=True)

            # Check if required columns exist
            required_columns = ["open", "high", "low", "close", "volume"]

            for column in required_columns:
                if column not in df.columns:
                    raise ValidationError(f"Required column not found: {column}")

            # Calculate features
            if features:
                df = self._calculate_features(df, features)

            return df

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error processing market data: {e}")
            raise ServiceError(f"Error processing market data: {str(e)}")

    def _calculate_features(
        self, df: pd.DataFrame, features: List[str]
    ) -> pd.DataFrame:
        """Calculate features

        Args:
            df: DataFrame with market data
            features: List of features to calculate

        Returns:
            DataFrame with calculated features
        """
        # Define feature calculation functions
        feature_functions = {
            "sma": self._calculate_sma,
            "ema": self._calculate_ema,
            "rsi": self._calculate_rsi,
            "macd": self._calculate_macd,
            "bollinger_bands": self._calculate_bollinger_bands,
            "atr": self._calculate_atr,
            "obv": self._calculate_obv,
            "returns": self._calculate_returns,
            "log_returns": self._calculate_log_returns,
            "momentum": self._calculate_momentum,
            "roc": self._calculate_roc,
            "stochastic": self._calculate_stochastic,
            "williams_r": self._calculate_williams_r,
            "adx": self._calculate_adx,
            "cci": self._calculate_cci,
            "aroon": self._calculate_aroon,
            "ichimoku": self._calculate_ichimoku,
        }

        # Calculate requested features
        for feature in features:
            if feature in feature_functions:
                df = feature_functions[feature](df)
            else:
                logger.warning(f"Unsupported feature: {feature}")

        return df

    def _calculate_sma(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """Calculate Simple Moving Average

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with SMA
        """
        df[f"sma_{window}"] = talib.SMA(df["close"].values, timeperiod=window)
        return df

    def _calculate_ema(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """Calculate Exponential Moving Average

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with EMA
        """
        df[f"ema_{window}"] = talib.EMA(df["close"].values, timeperiod=window)
        return df

    def _calculate_rsi(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Relative Strength Index

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with RSI
        """
        df[f"rsi_{window}"] = talib.RSI(df["close"].values, timeperiod=window)
        return df

    def _calculate_macd(
        self,
        df: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> pd.DataFrame:
        """Calculate Moving Average Convergence Divergence

        Args:
            df: DataFrame with market data
            fast_period: Fast period
            slow_period: Slow period
            signal_period: Signal period

        Returns:
            DataFrame with MACD
        """
        macd, signal, hist = talib.MACD(
            df["close"].values,
            fastperiod=fast_period,
            slowperiod=slow_period,
            signalperiod=signal_period,
        )

        df["macd"] = macd
        df["macd_signal"] = signal
        df["macd_hist"] = hist

        return df

    def _calculate_bollinger_bands(
        self, df: pd.DataFrame, window: int = 20, num_std: float = 2.0
    ) -> pd.DataFrame:
        """Calculate Bollinger Bands

        Args:
            df: DataFrame with market data
            window: Window size
            num_std: Number of standard deviations

        Returns:
            DataFrame with Bollinger Bands
        """
        upper, middle, lower = talib.BBANDS(
            df["close"].values,
            timeperiod=window,
            nbdevup=num_std,
            nbdevdn=num_std,
            matype=0,
        )

        df["bb_upper"] = upper
        df["bb_middle"] = middle
        df["bb_lower"] = lower

        return df

    def _calculate_atr(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Average True Range

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with ATR
        """
        df[f"atr_{window}"] = talib.ATR(
            df["high"].values, df["low"].values, df["close"].values, timeperiod=window
        )

        return df

    def _calculate_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate On-Balance Volume

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with OBV
        """
        df["obv"] = talib.OBV(df["close"].values, df["volume"].values)
        return df

    def _calculate_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate returns

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with returns
        """
        df["returns"] = df["close"].pct_change()
        return df

    def _calculate_log_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate logarithmic returns

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with log returns
        """
        df["log_returns"] = np.log(df["close"] / df["close"].shift(1))
        return df

    def _calculate_momentum(self, df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """Calculate momentum

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with momentum
        """
        df[f"momentum_{window}"] = df["close"] - df["close"].shift(window)
        return df

    def _calculate_roc(self, df: pd.DataFrame, window: int = 10) -> pd.DataFrame:
        """Calculate Rate of Change

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with ROC
        """
        df[f"roc_{window}"] = talib.ROC(df["close"].values, timeperiod=window)
        return df

    def _calculate_stochastic(
        self,
        df: pd.DataFrame,
        fastk_period: int = 5,
        slowk_period: int = 3,
        slowd_period: int = 3,
    ) -> pd.DataFrame:
        """Calculate Stochastic Oscillator

        Args:
            df: DataFrame with market data
            fastk_period: Fast K period
            slowk_period: Slow K period
            slowd_period: Slow D period

        Returns:
            DataFrame with Stochastic Oscillator
        """
        slowk, slowd = talib.STOCH(
            df["high"].values,
            df["low"].values,
            df["close"].values,
            fastk_period=fastk_period,
            slowk_period=slowk_period,
            slowk_matype=0,
            slowd_period=slowd_period,
            slowd_matype=0,
        )

        df["stoch_k"] = slowk
        df["stoch_d"] = slowd

        return df

    def _calculate_williams_r(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Williams %R

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with Williams %R
        """
        df[f"williams_r_{window}"] = talib.WILLR(
            df["high"].values, df["low"].values, df["close"].values, timeperiod=window
        )

        return df

    def _calculate_adx(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Average Directional Index

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with ADX
        """
        df[f"adx_{window}"] = talib.ADX(
            df["high"].values, df["low"].values, df["close"].values, timeperiod=window
        )

        return df

    def _calculate_cci(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Commodity Channel Index

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with CCI
        """
        df[f"cci_{window}"] = talib.CCI(
            df["high"].values, df["low"].values, df["close"].values, timeperiod=window
        )

        return df

    def _calculate_aroon(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """Calculate Aroon Oscillator

        Args:
            df: DataFrame with market data
            window: Window size

        Returns:
            DataFrame with Aroon Oscillator
        """
        aroon_down, aroon_up = talib.AROON(
            df["high"].values, df["low"].values, timeperiod=window
        )

        df[f"aroon_up_{window}"] = aroon_up
        df[f"aroon_down_{window}"] = aroon_down
        df[f"aroon_osc_{window}"] = aroon_up - aroon_down

        return df

    def _calculate_ichimoku(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Ichimoku Cloud

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with Ichimoku Cloud
        """
        # Calculate Tenkan-sen (Conversion Line)
        high_9 = df["high"].rolling(window=9).max()
        low_9 = df["low"].rolling(window=9).min()
        df["tenkan_sen"] = (high_9 + low_9) / 2

        # Calculate Kijun-sen (Base Line)
        high_26 = df["high"].rolling(window=26).max()
        low_26 = df["low"].rolling(window=26).min()
        df["kijun_sen"] = (high_26 + low_26) / 2

        # Calculate Senkou Span A (Leading Span A)
        df["senkou_span_a"] = ((df["tenkan_sen"] + df["kijun_sen"]) / 2).shift(26)

        # Calculate Senkou Span B (Leading Span B)
        high_52 = df["high"].rolling(window=52).max()
        low_52 = df["low"].rolling(window=52).min()
        df["senkou_span_b"] = ((high_52 + low_52) / 2).shift(26)

        # Calculate Chikou Span (Lagging Span)
        df["chikou_span"] = df["close"].shift(-26)

        return df

    def ndef normalize_data(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:ataFrame:
        """Normalize data

        Args:
            df: DataFrame with market data
            columns: List of columns to normalize

        Returns:
            DataFrame with normalized data
        """
        # If columns not specified, normalize all numeric columns
        if not columns:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()

        # Create a copy of the DataFrame
        df_normalized = df.copy()

        # Normalize each column
        for column in columns:
            if column in df.columns:
                scaler = MinMaxScaler()
                df_normalized[f"{column}_norm"] = scaler.fit_transform(df[[column]])

        return df_normalized

    def prepare_data_for_ml(
        self,
        df: pd.DataFrame,
        target_column: str = "close",
        sequence_length: int = 60,
        target_shift: int = 1,
        test_size: float = 0.2,
    ) -> tuple:
        """Prepare data for machine learning

        Args:
            df: DataFrame with market data
            target_column: Target column
            sequence_length: Sequence length
            target_shift: Target shift
            test_size: Test size

        Returns:
            Tuple of (X_train, X_test, y_train, y_test, scaler)

        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Validate data
            if target_column not in df.columns:
                raise ValidationError(f"Target column not found: {target_column}")

            # Drop rows with NaN values
            df = df.dropna()

            # Select numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

            # Scale data
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(df[numeric_columns])

            # Create sequences
            X = []
            y = []

            for i in range(len(scaled_data) - sequence_length - target_shift):
                X.append(scaled_data[i : i + sequence_length])
                y.append(
                    scaled_data[
                        i + sequence_length + target_shift - 1,
                        numeric_columns.index(target_column),
                    ]
                )

            X = np.array(X)
            y = np.array(y)

            # Split data
            split_idx = int(len(X) * (1 - test_size))
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]

            return X_train, X_test, y_train, y_test, scaler

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error preparing data for ML: {e}")
            raise ServiceError(f"Error preparing data for ML: {str(e)}")

    def detect_anomalies(
        self,
        df: pd.DataFrame,
        column: str = "close",
        window: int = 20,
        threshold: float = 3.0,
    ) -> pd.DataFrame:
        """Detect anomalies in data

        Args:
            df: DataFrame with market data
            column: Column to detect anomalies in
            window: Window size
            threshold: Threshold in standard deviations

        Returns:
            DataFrame with anomalies

        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Validate data
            if column not in df.columns:
                raise ValidationError(f"Column not found: {column}")

            # Calculate rolling mean and standard deviation
            rolling_mean = df[column].rolling(window=window).mean()
            rolling_std = df[column].rolling(window=window).std()

            # Calculate z-score
            z_score = (df[column] - rolling_mean) / rolling_std

            # Detect anomalies
            df["anomaly"] = (z_score.abs() > threshold).astype(int)

            return df

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            raise ServiceError(f"Error detecting anomalies: {str(e)}")

    def generate_signals(
        self, df: pd.DataFrame, strategy: str = "sma_crossover"
    ) -> pd.DataFrame:
        """Generate trading signals

        Args:
            df: DataFrame with market data
            strategy: Signal generation strategy

        Returns:
            DataFrame with signals

        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Validate data
            if "close" not in df.columns:
                raise ValidationError("Close column not found")

            # Generate signals based on strategy
            if strategy == "sma_crossover":
                return self._generate_sma_crossover_signals(df)
            elif strategy == "macd":
                return self._generate_macd_signals(df)
            elif strategy == "rsi":
                return self._generate_rsi_signals(df)
            elif strategy == "bollinger_bands":
                return self._generate_bollinger_bands_signals(df)
            else:
                raise ValidationError(f"Unsupported strategy: {strategy}")

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            raise ServiceError(f"Error generating signals: {str(e)}")

    def _generate_sma_crossover_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate SMA crossover signals

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with signals
        """
        # Calculate SMAs
        df = self._calculate_sma(df, window=20)
        df = self._calculate_sma(df, window=50)

        # Generate signals
        df["signal"] = 0
        df.loc[df["sma_20"] > df["sma_50"], "signal"] = 1
        df.loc[df["sma_20"] < df["sma_50"], "signal"] = -1

        return df

    def _generate_macd_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate MACD signals

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with signals
        """
        # Calculate MACD
        df = self._calculate_macd(df)

        # Generate signals
        df["signal"] = 0
        df.loc[df["macd"] > df["macd_signal"], "signal"] = 1
        df.loc[df["macd"] < df["macd_signal"], "signal"] = -1

        return df

    def _generate_rsi_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate RSI signals

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with signals
        """
        # Calculate RSI
        df = self._calculate_rsi(df)

        # Generate signals
        df["signal"] = 0
        df.loc[df["rsi_14"] < 30, "signal"] = 1
        df.loc[df["rsi_14"] > 70, "signal"] = -1

        return df

    def _generate_bollinger_bands_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate Bollinger Bands signals

        Args:
            df: DataFrame with market data

        Returns:
            DataFrame with signals
        """
        # Calculate Bollinger Bands
        df = self._calculate_bollinger_bands(df)

        # Generate signals
        df["signal"] = 0
        df.loc[df["close"] < df["bb_lower"], "signal"] = 1
        df.loc[df["close"] > df["bb_upper"], "signal"] = -1

        return df
