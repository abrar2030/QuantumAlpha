"""
Position sizing for QuantumAlpha Risk Service.
Handles position sizing optimization.
"""

import logging
import os
# Add parent directory to path to import common modules
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import ServiceError, ValidationError, setup_logger

# Configure logging
logger = setup_logger("position_sizing", logging.INFO)


class PositionSizing:
    """Position sizing"""

    def __init__(self, config_manager, db_manager):
        """Initialize position sizing

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager

        # Initialize data service URL
        self.data_service_url = f"http://{config_manager.get('services.data_service.host')}:{config_manager.get('services.data_service.port')}"

        logger.info("Position sizing initialized")

    def calculate_position_size(
        self,
        symbol: str,
        signal_strength: float,
        portfolio_value: float,
        risk_tolerance: float,
        volatility: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Calculate optimal position size

        Args:
            symbol: Symbol
            signal_strength: Signal strength (0.0 to 1.0)
            portfolio_value: Portfolio value
            risk_tolerance: Risk tolerance (0.0 to 1.0)
            volatility: Volatility (optional)

        Returns:
            Position size recommendation

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info(f"Calculating position size for {symbol}")

            # Validate parameters
            if not symbol:
                raise ValidationError("Symbol is required")

            if signal_strength < 0 or signal_strength > 1:
                raise ValidationError("Signal strength must be between 0 and 1")

            if portfolio_value <= 0:
                raise ValidationError("Portfolio value must be positive")

            if risk_tolerance < 0 or risk_tolerance > 1:
                raise ValidationError("Risk tolerance must be between 0 and 1")

            # Get volatility if not provided
            if volatility is None:
                volatility = self._get_volatility(symbol)

            # Calculate position size using Kelly criterion
            # Kelly fraction = (edge / odds) * risk_tolerance
            # where edge = signal_strength, odds = volatility

            # Adjust signal strength to be between 0.5 and 1.0
            adjusted_signal = 0.5 + (signal_strength * 0.5)

            # Calculate edge
            edge = adjusted_signal - 0.5

            # Calculate Kelly fraction
            kelly_fraction = (edge / volatility) * risk_tolerance

            # Limit Kelly fraction to reasonable range
            kelly_fraction = max(0.01, min(0.5, kelly_fraction))

            # Calculate position size
            position_size = portfolio_value * kelly_fraction

            # Get current price
            current_price = self._get_current_price(symbol)

            # Calculate number of shares
            shares = position_size / current_price

            # Create response
            response = {
                "symbol": symbol,
                "current_price": current_price,
                "volatility": volatility,
                "kelly_fraction": kelly_fraction,
                "position_size": position_size,
                "shares": shares,
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            raise ServiceError(f"Error calculating position size: {str(e)}")

    def _get_volatility(self, symbol: str) -> float:
        """Get volatility for a symbol

        Args:
            symbol: Symbol

        Returns:
            Volatility
        """
        try:
            # Get historical data from data service
            response = requests.get(
                f"{self.data_service_url}/api/market-data/{symbol}",
                params={"timeframe": "1d", "period": "1mo"},
            )

            if response.status_code != 200:
                raise ServiceError(f"Error getting historical data: {response.text}")

            # Parse response
            data = response.json()

            # Calculate returns
            prices = [d["close"] for d in data["data"]]
            returns = np.diff(prices) / prices[:-1]

            # Calculate volatility (standard deviation of returns)
            volatility = np.std(returns)

            return float(volatility)

        except Exception as e:
            logger.error(f"Error getting volatility: {e}")

            # Return default volatility
            logger.warning("Using default volatility")
            return 0.02

    def _get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol

        Args:
            symbol: Symbol

        Returns:
            Current price
        """
        try:
            # Get latest data from data service
            response = requests.get(
                f"{self.data_service_url}/api/market-data/{symbol}",
                params={"timeframe": "1d", "period": "1d"},
            )

            if response.status_code != 200:
                raise ServiceError(f"Error getting current price: {response.text}")

            # Parse response
            data = response.json()

            # Get latest price
            current_price = data["data"][-1]["close"]

            return float(current_price)

        except Exception as e:
            logger.error(f"Error getting current price: {e}")

            # Return default price
            logger.warning("Using default price")
            return 100.0

    def optimize_portfolio(
        self,
        portfolio: List[Dict[str, Any]],
        signals: List[Dict[str, Any]],
        risk_tolerance: float,
    ) -> Dict[str, Any]:
        """Optimize portfolio based on signals

        Args:
            portfolio: Portfolio positions
            signals: Trading signals
            risk_tolerance: Risk tolerance

        Returns:
            Optimized portfolio

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info("Optimizing portfolio")

            # Validate parameters
            if not portfolio:
                raise ValidationError("Portfolio is required")

            if not signals:
                raise ValidationError("Signals are required")

            if risk_tolerance < 0 or risk_tolerance > 1:
                raise ValidationError("Risk tolerance must be between 0 and 1")

            # Calculate portfolio value
            portfolio_value = sum(
                position["quantity"] * position["entry_price"] for position in portfolio
            )

            # Calculate position sizes for each signal
            position_sizes = []

            for signal in signals:
                # Calculate position size
                position_size = self.calculate_position_size(
                    symbol=signal["symbol"],
                    signal_strength=signal["strength"],
                    portfolio_value=portfolio_value,
                    risk_tolerance=risk_tolerance,
                )

                position_sizes.append(position_size)

            # Create response
            response = {
                "portfolio_value": portfolio_value,
                "position_sizes": position_sizes,
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error optimizing portfolio: {e}")
            raise ServiceError(f"Error optimizing portfolio: {str(e)}")

    def calculate_max_position_size(
        self, symbol: str, portfolio_value: float, max_loss_percent: float
    ) -> Dict[str, Any]:
        """Calculate maximum position size based on maximum loss

        Args:
            symbol: Symbol
            portfolio_value: Portfolio value
            max_loss_percent: Maximum loss as percentage of portfolio value

        Returns:
            Maximum position size

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info(f"Calculating maximum position size for {symbol}")

            # Validate parameters
            if not symbol:
                raise ValidationError("Symbol is required")

            if portfolio_value <= 0:
                raise ValidationError("Portfolio value must be positive")

            if max_loss_percent <= 0 or max_loss_percent > 1:
                raise ValidationError("Maximum loss percent must be between 0 and 1")

            # Get volatility
            volatility = self._get_volatility(symbol)

            # Get current price
            current_price = self._get_current_price(symbol)

            # Calculate maximum position size
            # max_position_size = max_loss / (volatility * 2)
            max_loss = portfolio_value * max_loss_percent
            max_position_size = max_loss / (volatility * 2)

            # Calculate number of shares
            shares = max_position_size / current_price

            # Create response
            response = {
                "symbol": symbol,
                "current_price": current_price,
                "volatility": volatility,
                "max_loss": max_loss,
                "max_position_size": max_position_size,
                "shares": shares,
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error calculating maximum position size: {e}")
            raise ServiceError(f"Error calculating maximum position size: {str(e)}")

    def calculate_stop_loss(
        self,
        symbol: str,
        entry_price: float,
        position_size: float,
        max_loss_percent: float,
    ) -> Dict[str, Any]:
        """Calculate stop loss price

        Args:
            symbol: Symbol
            entry_price: Entry price
            position_size: Position size
            max_loss_percent: Maximum loss as percentage of position size

        Returns:
            Stop loss price

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info(f"Calculating stop loss for {symbol}")

            # Validate parameters
            if not symbol:
                raise ValidationError("Symbol is required")

            if entry_price <= 0:
                raise ValidationError("Entry price must be positive")

            if position_size <= 0:
                raise ValidationError("Position size must be positive")

            if max_loss_percent <= 0 or max_loss_percent > 1:
                raise ValidationError("Maximum loss percent must be between 0 and 1")

            # Calculate number of shares
            shares = position_size / entry_price

            # Calculate maximum loss
            max_loss = position_size * max_loss_percent

            # Calculate stop loss price
            stop_loss_price = entry_price - (max_loss / shares)

            # Create response
            response = {
                "symbol": symbol,
                "entry_price": entry_price,
                "position_size": position_size,
                "shares": shares,
                "max_loss_percent": max_loss_percent,
                "max_loss": max_loss,
                "stop_loss_price": stop_loss_price,
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error calculating stop loss: {e}")
            raise ServiceError(f"Error calculating stop loss: {str(e)}")

    def calculate_take_profit(
        self,
        symbol: str,
        entry_price: float,
        stop_loss_price: float,
        risk_reward_ratio: float,
    ) -> Dict[str, Any]:
        """Calculate take profit price

        Args:
            symbol: Symbol
            entry_price: Entry price
            stop_loss_price: Stop loss price
            risk_reward_ratio: Risk-reward ratio

        Returns:
            Take profit price

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info(f"Calculating take profit for {symbol}")

            # Validate parameters
            if not symbol:
                raise ValidationError("Symbol is required")

            if entry_price <= 0:
                raise ValidationError("Entry price must be positive")

            if stop_loss_price <= 0:
                raise ValidationError("Stop loss price must be positive")

            if risk_reward_ratio <= 0:
                raise ValidationError("Risk-reward ratio must be positive")

            # Calculate risk
            risk = entry_price - stop_loss_price

            # Calculate reward
            reward = risk * risk_reward_ratio

            # Calculate take profit price
            take_profit_price = entry_price + reward

            # Create response
            response = {
                "symbol": symbol,
                "entry_price": entry_price,
                "stop_loss_price": stop_loss_price,
                "risk": risk,
                "reward": reward,
                "risk_reward_ratio": risk_reward_ratio,
                "take_profit_price": take_profit_price,
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error calculating take profit: {e}")
            raise ServiceError(f"Error calculating take profit: {str(e)}")

    def calculate_position_adjustment(
        self,
        symbol: str,
        current_position: Dict[str, Any],
        signal: Dict[str, Any],
        portfolio_value: float,
        risk_tolerance: float,
    ) -> Dict[str, Any]:
        """Calculate position adjustment based on a new signal

        Args:
            symbol: Symbol
            current_position: Current position
            signal: New signal
            portfolio_value: Portfolio value
            risk_tolerance: Risk tolerance

        Returns:
            Position adjustment recommendation

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info(f"Calculating position adjustment for {symbol}")

            # Validate parameters
            if not symbol:
                raise ValidationError("Symbol is required")

            if not current_position:
                raise ValidationError("Current position is required")

            if not signal:
                raise ValidationError("Signal is required")

            if portfolio_value <= 0:
                raise ValidationError("Portfolio value must be positive")

            if risk_tolerance < 0 or risk_tolerance > 1:
                raise ValidationError("Risk tolerance must be between 0 and 1")

            # Get current position details
            current_quantity = current_position["quantity"]
            current_price = current_position["current_price"]
            current_value = current_quantity * current_price

            # Calculate optimal position size
            optimal_position = self.calculate_position_size(
                symbol=symbol,
                signal_strength=signal["strength"],
                portfolio_value=portfolio_value,
                risk_tolerance=risk_tolerance,
            )

            optimal_value = optimal_position["position_size"]
            optimal_quantity = optimal_position["shares"]

            # Calculate adjustment
            value_adjustment = optimal_value - current_value
            quantity_adjustment = optimal_quantity - current_quantity

            # Determine action
            if quantity_adjustment > 0:
                action = "buy"
            elif quantity_adjustment < 0:
                action = "sell"
            else:
                action = "hold"

            # Create response
            response = {
                "symbol": symbol,
                "current_position": {
                    "quantity": current_quantity,
                    "price": current_price,
                    "value": current_value,
                },
                "optimal_position": {
                    "quantity": optimal_quantity,
                    "price": current_price,
                    "value": optimal_value,
                },
                "adjustment": {
                    "action": action,
                    "quantity": abs(quantity_adjustment),
                    "value": abs(value_adjustment),
                },
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error calculating position adjustment: {e}")
            raise ServiceError(f"Error calculating position adjustment: {str(e)}")
