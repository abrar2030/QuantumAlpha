"""
Prediction service for QuantumAlpha AI Engine.
Handles predictions and signal generation.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import requests
import json

# Add parent directory to path to import common modules
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import setup_logger, ServiceError, ValidationError, NotFoundError

# Configure logging
logger = setup_logger("prediction_service", logging.INFO)


class PredictionService:
    """Prediction service"""

    def __init__(self, config_manager, db_manager, model_manager):
        """Initialize prediction service

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
            model_manager: Model manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.model_manager = model_manager

        # Initialize data service URL
        self.data_service_url = f"http://{config_manager.get('services.data_service.host')}:{config_manager.get('services.data_service.port')}"

        logger.info("Prediction service initialized")

    def generate_prediction(
        self,
        model_id: str,
        symbol: str,
        timeframe: str = "1d",
        period: str = "1mo",
        horizon: int = 5,
    ) -> Dict[str, Any]:
        """Generate prediction

        Args:
            model_id: Model ID
            symbol: Symbol
            timeframe: Timeframe
            period: Period
            horizon: Prediction horizon

        Returns:
            Prediction result

        Raises:
            NotFoundError: If model is not found
            ValidationError: If parameters are invalid
            ServiceError: If there is an error generating prediction
        """
        try:
            logger.info(f"Generating prediction for {symbol} using model {model_id}")

            # Validate parameters
            if not model_id:
                raise ValidationError("Model ID is required")

            if not symbol:
                raise ValidationError("Symbol is required")

            # Get prediction from model manager
            prediction = self.model_manager.predict(
                model_id=model_id,
                data={"symbol": symbol, "timeframe": timeframe, "period": period},
            )

            # Get latest predictions
            latest_predictions = prediction["predictions"][-horizon:]

            # Get latest market data
            market_data = self._get_market_data(
                symbol=symbol, timeframe=timeframe, period="1d"
            )

            # Get latest price
            latest_price = market_data[-1]["close"]

            # Calculate prediction metrics
            prediction_values = [p["value"] for p in latest_predictions]
            avg_prediction = sum(prediction_values) / len(prediction_values)
            min_prediction = min(prediction_values)
            max_prediction = max(prediction_values)

            # Calculate change
            change = avg_prediction - latest_price
            change_percent = (change / latest_price) * 100

            # Determine direction
            if change_percent > 1:
                direction = "bullish"
            elif change_percent < -1:
                direction = "bearish"
            else:
                direction = "neutral"

            # Create response
            response = {
                "symbol": symbol,
                "model_id": model_id,
                "latest_price": latest_price,
                "prediction": {
                    "average": avg_prediction,
                    "minimum": min_prediction,
                    "maximum": max_prediction,
                    "change": change,
                    "change_percent": change_percent,
                    "direction": direction,
                },
                "horizon": horizon,
                "timeframe": timeframe,
                "predictions": latest_predictions,
                "generated_at": datetime.utcnow().isoformat(),
            }

            return response

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error generating prediction: {e}")
            raise ServiceError(f"Error generating prediction: {str(e)}")

    def generate_signals(
        self,
        symbols: List[str],
        model_id: Optional[str] = None,
        timeframe: str = "1d",
        period: str = "1mo",
        strategy: str = "prediction",
    ) -> Dict[str, Any]:
        """Generate trading signals

        Args:
            symbols: List of symbols
            model_id: Model ID (optional)
            timeframe: Timeframe
            period: Period
            strategy: Signal generation strategy

        Returns:
            Trading signals

        Raises:
            ValidationError: If parameters are invalid
            ServiceError: If there is an error generating signals
        """
        try:
            logger.info(f"Generating signals for {len(symbols)} symbols")

            # Validate parameters
            if not symbols:
                raise ValidationError("Symbols are required")

            # Generate signals based on strategy
            if strategy == "prediction":
                return self._generate_prediction_signals(
                    symbols, model_id, timeframe, period
                )
            elif strategy == "technical":
                return self._generate_technical_signals(symbols, timeframe, period)
            elif strategy == "ensemble":
                return self._generate_ensemble_signals(
                    symbols, model_id, timeframe, period
                )
            else:
                raise ValidationError(f"Unsupported strategy: {strategy}")

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            raise ServiceError(f"Error generating signals: {str(e)}")

    def _generate_prediction_signals(
        self, symbols: List[str], model_id: Optional[str], timeframe: str, period: str
    ) -> Dict[str, Any]:
        """Generate signals based on predictions

        Args:
            symbols: List of symbols
            model_id: Model ID
            timeframe: Timeframe
            period: Period

        Returns:
            Trading signals

        Raises:
            ValidationError: If parameters are invalid
        """
        # Validate model ID
        if not model_id:
            raise ValidationError("Model ID is required for prediction signals")

        # Generate signals for each symbol
        signals = []

        for symbol in symbols:
            try:
                # Generate prediction
                prediction = self.generate_prediction(
                    model_id=model_id, symbol=symbol, timeframe=timeframe, period=period
                )

                # Determine signal strength based on change percent
                change_percent = prediction["prediction"]["change_percent"]

                if change_percent > 5:
                    strength = 1.0
                elif change_percent > 3:
                    strength = 0.8
                elif change_percent > 1:
                    strength = 0.6
                elif change_percent > 0:
                    strength = 0.4
                elif change_percent > -1:
                    strength = 0.2
                elif change_percent > -3:
                    strength = 0.0
                else:
                    strength = 0.0

                # Determine signal type
                if change_percent > 1:
                    signal_type = "buy"
                elif change_percent < -1:
                    signal_type = "sell"
                else:
                    signal_type = "hold"

                # Create signal
                signal = {
                    "symbol": symbol,
                    "type": signal_type,
                    "strength": strength,
                    "price": prediction["latest_price"],
                    "prediction": prediction["prediction"],
                    "model_id": model_id,
                    "strategy": "prediction",
                    "generated_at": datetime.utcnow().isoformat(),
                }

                signals.append(signal)

            except Exception as e:
                logger.error(f"Error generating signal for {symbol}: {e}")
                continue

        # Create response
        response = {
            "signals": signals,
            "count": len(signals),
            "strategy": "prediction",
            "model_id": model_id,
            "generated_at": datetime.utcnow().isoformat(),
        }

        return response

    def _generate_technical_signals(
        self, symbols: List[str], timeframe: str, period: str
    ) -> Dict[str, Any]:
        """Generate signals based on technical analysis

        Args:
            symbols: List of symbols
            timeframe: Timeframe
            period: Period

        Returns:
            Trading signals
        """
        # Generate signals for each symbol
        signals = []

        for symbol in symbols:
            try:
                # Get market data
                market_data = self._get_market_data(
                    symbol=symbol, timeframe=timeframe, period=period
                )

                # Convert to DataFrame
                df = pd.DataFrame(market_data)

                # Get data processor from data service
                from data_service.data_processor import DataProcessor

                # Initialize data processor
                data_processor = DataProcessor(self.config_manager, self.db_manager)

                # Generate signals
                df = data_processor.generate_signals(df, strategy="sma_crossover")

                # Get latest signal
                latest_signal = df["signal"].iloc[-1]

                # Determine signal type
                if latest_signal > 0:
                    signal_type = "buy"
                    strength = 0.8
                elif latest_signal < 0:
                    signal_type = "sell"
                    strength = 0.8
                else:
                    signal_type = "hold"
                    strength = 0.0

                # Create signal
                signal = {
                    "symbol": symbol,
                    "type": signal_type,
                    "strength": strength,
                    "price": market_data[-1]["close"],
                    "strategy": "technical",
                    "generated_at": datetime.utcnow().isoformat(),
                }

                signals.append(signal)

            except Exception as e:
                logger.error(f"Error generating signal for {symbol}: {e}")
                continue

        # Create response
        response = {
            "signals": signals,
            "count": len(signals),
            "strategy": "technical",
            "generated_at": datetime.utcnow().isoformat(),
        }

        return response

    def _generate_ensemble_signals(
        self, symbols: List[str], model_id: Optional[str], timeframe: str, period: str
    ) -> Dict[str, Any]:
        """Generate signals based on ensemble of strategies

        Args:
            symbols: List of symbols
            model_id: Model ID
            timeframe: Timeframe
            period: Period

        Returns:
            Trading signals

        Raises:
            ValidationError: If parameters are invalid
        """
        # Validate model ID
        if not model_id:
            raise ValidationError("Model ID is required for ensemble signals")

        # Generate prediction signals
        prediction_signals = self._generate_prediction_signals(
            symbols=symbols, model_id=model_id, timeframe=timeframe, period=period
        )

        # Generate technical signals
        technical_signals = self._generate_technical_signals(
            symbols=symbols, timeframe=timeframe, period=period
        )

        # Combine signals
        signals = []

        for symbol in symbols:
            try:
                # Find prediction signal
                prediction_signal = next(
                    (s for s in prediction_signals["signals"] if s["symbol"] == symbol),
                    None,
                )

                # Find technical signal
                technical_signal = next(
                    (s for s in technical_signals["signals"] if s["symbol"] == symbol),
                    None,
                )

                if prediction_signal and technical_signal:
                    # Determine signal type
                    if prediction_signal["type"] == technical_signal["type"] == "buy":
                        signal_type = "buy"
                        strength = (
                            prediction_signal["strength"] + technical_signal["strength"]
                        ) / 2
                    elif (
                        prediction_signal["type"] == technical_signal["type"] == "sell"
                    ):
                        signal_type = "sell"
                        strength = (
                            prediction_signal["strength"] + technical_signal["strength"]
                        ) / 2
                    elif (
                        prediction_signal["type"] == "buy"
                        and technical_signal["type"] == "sell"
                    ):
                        signal_type = "hold"
                        strength = 0.0
                    elif (
                        prediction_signal["type"] == "sell"
                        and technical_signal["type"] == "buy"
                    ):
                        signal_type = "hold"
                        strength = 0.0
                    else:
                        signal_type = "hold"
                        strength = 0.0

                    # Create signal
                    signal = {
                        "symbol": symbol,
                        "type": signal_type,
                        "strength": strength,
                        "price": prediction_signal["price"],
                        "prediction": prediction_signal.get("prediction"),
                        "model_id": model_id,
                        "strategy": "ensemble",
                        "generated_at": datetime.utcnow().isoformat(),
                    }

                    signals.append(signal)

            except Exception as e:
                logger.error(f"Error generating ensemble signal for {symbol}: {e}")
                continue

        # Create response
        response = {
            "signals": signals,
            "count": len(signals),
            "strategy": "ensemble",
            "model_id": model_id,
            "generated_at": datetime.utcnow().isoformat(),
        }

        return response

    def _get_market_data(
        self, symbol: str, timeframe: str, period: str
    ) -> List[Dict[str, Any]]:
        """Get market data from data service

        Args:
            symbol: Symbol
            timeframe: Timeframe
            period: Period

        Returns:
            Market data

        Raises:
            ServiceError: If there is an error getting market data
        """
        try:
            # Get market data from data service
            response = requests.get(
                f"{self.data_service_url}/api/market-data/{symbol}",
                params={"timeframe": timeframe, "period": period},
            )

            if response.status_code != 200:
                raise ServiceError(f"Error getting market data: {response.text}")

            # Parse response
            data = response.json()

            return data["data"]

        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            raise ServiceError(f"Error getting market data: {str(e)}")

    def get_prediction_history(
        self,
        model_id: str,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get prediction history

        Args:
            model_id: Model ID
            symbol: Symbol
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            Prediction history

        Raises:
            NotFoundError: If model is not found
            ValidationError: If parameters are invalid
            ServiceError: If there is an error getting prediction history
        """
        try:
            logger.info(
                f"Getting prediction history for {symbol} using model {model_id}"
            )

            # Validate parameters
            if not model_id:
                raise ValidationError("Model ID is required")

            if not symbol:
                raise ValidationError("Symbol is required")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Build query
            query = """
                SELECT *
                FROM prediction_history
                WHERE model_id = %s AND symbol = %s
            """

            params = [model_id, symbol]

            if start_date:
                query += " AND timestamp >= %s"
                params.append(start_date)

            if end_date:
                query += " AND timestamp <= %s"
                params.append(end_date)

            query += " ORDER BY timestamp ASC"

            # Execute query
            result = session.execute(query, params)

            # Convert to list of dictionaries
            predictions = []

            for row in result:
                predictions.append(
                    {
                        "id": row["id"],
                        "model_id": row["model_id"],
                        "symbol": row["symbol"],
                        "timestamp": row["timestamp"].isoformat(),
                        "prediction": row["prediction"],
                        "actual": row["actual"],
                        "error": row["error"],
                    }
                )

            # Create response
            response = {
                "model_id": model_id,
                "symbol": symbol,
                "predictions": predictions,
                "count": len(predictions),
            }

            return response

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error getting prediction history: {e}")
            raise ServiceError(f"Error getting prediction history: {str(e)}")

        finally:
            session.close()

    def save_prediction(
        self,
        model_id: str,
        symbol: str,
        timestamp: str,
        prediction: float,
        actual: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Save prediction to history

        Args:
            model_id: Model ID
            symbol: Symbol
            timestamp: Timestamp
            prediction: Prediction value
            actual: Actual value (optional)

        Returns:
            Saved prediction

        Raises:
            ValidationError: If parameters are invalid
            ServiceError: If there is an error saving prediction
        """
        try:
            logger.info(f"Saving prediction for {symbol} using model {model_id}")

            # Validate parameters
            if not model_id:
                raise ValidationError("Model ID is required")

            if not symbol:
                raise ValidationError("Symbol is required")

            if not timestamp:
                raise ValidationError("Timestamp is required")

            # Calculate error if actual value is provided
            error = None

            if actual is not None:
                error = actual - prediction

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Insert prediction
            query = """
                INSERT INTO prediction_history
                (model_id, symbol, timestamp, prediction, actual, error)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """

            result = session.execute(
                query, [model_id, symbol, timestamp, prediction, actual, error]
            )

            # Get inserted ID
            prediction_id = result.fetchone()[0]

            # Commit changes
            session.commit()

            # Create response
            response = {
                "id": prediction_id,
                "model_id": model_id,
                "symbol": symbol,
                "timestamp": timestamp,
                "prediction": prediction,
                "actual": actual,
                "error": error,
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error saving prediction: {e}")
            raise ServiceError(f"Error saving prediction: {str(e)}")

        finally:
            session.close()

    def update_prediction(self, prediction_id: str, actual: float) -> Dict[str, Any]:
        """Update prediction with actual value

        Args:
            prediction_id: Prediction ID
            actual: Actual value

        Returns:
            Updated prediction

        Raises:
            NotFoundError: If prediction is not found
            ValidationError: If parameters are invalid
            ServiceError: If there is an error updating prediction
        """
        try:
            logger.info(f"Updating prediction {prediction_id}")

            # Validate parameters
            if not prediction_id:
                raise ValidationError("Prediction ID is required")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get prediction
            query = """
                SELECT *
                FROM prediction_history
                WHERE id = %s
            """

            result = session.execute(query, [prediction_id])
            row = result.fetchone()

            if not row:
                raise NotFoundError(f"Prediction not found: {prediction_id}")

            # Calculate error
            error = actual - row["prediction"]

            # Update prediction
            query = """
                UPDATE prediction_history
                SET actual = %s, error = %s
                WHERE id = %s
            """

            session.execute(query, [actual, error, prediction_id])

            # Commit changes
            session.commit()

            # Create response
            response = {
                "id": prediction_id,
                "model_id": row["model_id"],
                "symbol": row["symbol"],
                "timestamp": row["timestamp"].isoformat(),
                "prediction": row["prediction"],
                "actual": actual,
                "error": error,
            }

            return response

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error updating prediction: {e}")
            raise ServiceError(f"Error updating prediction: {str(e)}")

        finally:
            session.close()

    def get_model_performance(
        self,
        model_id: str,
        symbol: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get model performance metrics

        Args:
            model_id: Model ID
            symbol: Symbol (optional)
            start_date: Start date (optional)
            end_date: End date (optional)

        Returns:
            Model performance metrics

        Raises:
            NotFoundError: If model is not found
            ValidationError: If parameters are invalid
            ServiceError: If there is an error getting model performance
        """
        try:
            logger.info(f"Getting performance metrics for model {model_id}")

            # Validate parameters
            if not model_id:
                raise ValidationError("Model ID is required")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Build query
            query = """
                SELECT
                    model_id,
                    symbol,
                    COUNT(*) as count,
                    AVG(error) as avg_error,
                    AVG(ABS(error)) as avg_abs_error,
                    STDDEV(error) as std_error,
                    MIN(error) as min_error,
                    MAX(error) as max_error
                FROM prediction_history
                WHERE model_id = %s AND actual IS NOT NULL
            """

            params = [model_id]

            if symbol:
                query += " AND symbol = %s"
                params.append(symbol)

            if start_date:
                query += " AND timestamp >= %s"
                params.append(start_date)

            if end_date:
                query += " AND timestamp <= %s"
                params.append(end_date)

            if symbol:
                query += " GROUP BY model_id, symbol"
            else:
                query += " GROUP BY model_id"

            # Execute query
            result = session.execute(query, params)

            # Convert to list of dictionaries
            metrics = []

            for row in result:
                metrics.append(
                    {
                        "model_id": row["model_id"],
                        "symbol": row["symbol"] if symbol else None,
                        "count": row["count"],
                        "avg_error": (
                            float(row["avg_error"]) if row["avg_error"] else None
                        ),
                        "avg_abs_error": (
                            float(row["avg_abs_error"])
                            if row["avg_abs_error"]
                            else None
                        ),
                        "std_error": (
                            float(row["std_error"]) if row["std_error"] else None
                        ),
                        "min_error": (
                            float(row["min_error"]) if row["min_error"] else None
                        ),
                        "max_error": (
                            float(row["max_error"]) if row["max_error"] else None
                        ),
                    }
                )

            # Create response
            response = {
                "model_id": model_id,
                "symbol": symbol,
                "metrics": metrics[0] if metrics else None,
            }

            return response

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error getting model performance: {e}")
            raise ServiceError(f"Error getting model performance: {str(e)}")

        finally:
            session.close()
