"""
Risk calculator for QuantumAlpha Risk Service.
Handles portfolio risk calculation and risk monitoring.
"""

import logging
import os

# Add parent directory to path to import common modules
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
from data_service.market_data import MarketDataService

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import NotFoundError, ServiceError, ValidationError, setup_logger
from common.models import Portfolio, Position

# Configure logging
logger = setup_logger("risk_calculator", logging.INFO)


class RiskCalculator:
    """Risk calculator"""

    def __init__(self, config_manager, db_manager):
        """Initialize risk calculator

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager

        # Initialize data service URL
        data_host = config_manager.get("services.data_service.host", "localhost")
        data_port = config_manager.get("services.data_service.port", "8001")
        self.data_service_url = f"http://{data_host}:{data_port}"

        logger.info("Risk calculator initialized")

    def calculate_risk_metrics(
        self,
        portfolio: List[Dict[str, Any]],
        risk_metrics: List[str],
        confidence_level: float = 0.95,
        lookback_period: int = 252,
    ) -> Dict[str, Any]:
        """Calculate risk metrics for a portfolio

        Args:
            portfolio: Portfolio positions
            risk_metrics: List of risk metrics to calculate
            confidence_level: Confidence level for VaR calculation
            lookback_period: Lookback period in days

        Returns:
            Risk metrics

        Raises:
            ValidationError: If parameters are invalid
        """
        try:
            logger.info("Calculating risk metrics")

            # Validate parameters
            if not portfolio:
                raise ValidationError("Portfolio is required")

            if not risk_metrics:
                raise ValidationError("Risk metrics are required")

            # Calculate portfolio value
            portfolio_value = sum(
                position["quantity"] * position["entry_price"] for position in portfolio
            )

            # Get historical returns for each position
            position_returns = {}

            for position in portfolio:
                symbol = position["symbol"]

                # Get historical data from data service
                historical_data = self._get_historical_data(symbol, lookback_period)

                # Calculate returns
                returns = self._calculate_returns(historical_data)

                # Store returns
                position_returns[symbol] = returns

            # Calculate portfolio returns
            portfolio_returns = self._calculate_portfolio_returns(
                portfolio, position_returns
            )

            # Calculate risk metrics
            metrics = {}

            for metric in risk_metrics:
                if metric == "var":
                    metrics["var"] = self._calculate_var(
                        portfolio_returns, confidence_level
                    )
                    metrics["var_percent"] = metrics["var"] / portfolio_value

                elif metric == "cvar":
                    metrics["cvar"] = self._calculate_cvar(
                        portfolio_returns, confidence_level
                    )
                    metrics["cvar_percent"] = metrics["cvar"] / portfolio_value

                elif metric == "sharpe":
                    metrics["sharpe"] = self._calculate_sharpe_ratio(portfolio_returns)

                elif metric == "sortino":
                    metrics["sortino"] = self._calculate_sortino_ratio(
                        portfolio_returns
                    )

                elif metric == "max_drawdown":
                    metrics["max_drawdown"] = self._calculate_max_drawdown(
                        portfolio_returns
                    )

                elif metric == "es":
                    metrics["es"] = self._calculate_expected_shortfall(
                        portfolio_returns, confidence_level
                    )
                    metrics["es_percent"] = metrics["es"] / portfolio_value

                else:
                    logger.warning(f"Unsupported risk metric: {metric}")

            # Create response
            response = {
                "portfolio_value": portfolio_value,
                "risk_metrics": metrics,
                "calculated_at": datetime.utcnow().isoformat(),
            }

            return response

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            raise ServiceError(f"Error calculating risk metrics: {str(e)}")

    def get_portfolio_risk(self, portfolio_id: str) -> Dict[str, Any]:
        """Get risk metrics for a portfolio

        Args:
            portfolio_id: Portfolio ID

        Returns:
            Portfolio risk metrics

        Raises:
            NotFoundError: If portfolio is not found
        """
        try:
            logger.info(f"Getting risk metrics for portfolio {portfolio_id}")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get portfolio
            portfolio = (
                session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
            )

            if not portfolio:
                raise NotFoundError(f"Portfolio not found: {portfolio_id}")

            # Get positions
            positions = (
                session.query(Position)
                .filter(Position.portfolio_id == portfolio_id)
                .all()
            )

            # Convert positions to list of dictionaries
            position_dicts = [
                {
                    "symbol": position.symbol,
                    "quantity": position.quantity,
                    "entry_price": position.entry_price,
                }
                for position in positions
            ]

            # Calculate risk metrics
            risk_metrics = self.calculate_risk_metrics(
                portfolio=position_dicts,
                risk_metrics=["var", "cvar", "sharpe", "sortino", "max_drawdown"],
                confidence_level=0.95,
                lookback_period=252,
            )

            return risk_metrics

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error getting portfolio risk: {e}")
            raise ServiceError(f"Error getting portfolio risk: {str(e)}")

        finally:
            session.close()

    def get_risk_alerts(
        self, portfolio_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get risk alerts

        Args:
            portfolio_id: Portfolio ID (optional)

        Returns:
            List of risk alerts
        """
        try:
            logger.info("Getting risk alerts")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get portfolios
            if portfolio_id:
                portfolios = (
                    session.query(Portfolio).filter(Portfolio.id == portfolio_id).all()
                )
            else:
                portfolios = session.query(Portfolio).all()

            # Generate alerts
            alerts = []

            for portfolio in portfolios:
                # Get positions
                positions = (
                    session.query(Position)
                    .filter(Position.portfolio_id == portfolio.id)
                    .all()
                )

                # Skip if no positions
                if not positions:
                    continue

                # Convert positions to list of dictionaries
                position_dicts = [
                    {
                        "symbol": position.symbol,
                        "quantity": position.quantity,
                        "entry_price": position.entry_price,
                    }
                    for position in positions
                ]

                # Calculate risk metrics
                risk_metrics = self.calculate_risk_metrics(
                    portfolio=position_dicts,
                    risk_metrics=["var", "cvar", "sharpe", "sortino", "max_drawdown"],
                    confidence_level=0.95,
                    lookback_period=252,
                )

                # Check for alerts
                if risk_metrics["risk_metrics"].get("var_percent", 0) > 0.05:
                    var_percent = risk_metrics["risk_metrics"]["var_percent"]
                    alerts.append(
                        {
                            "portfolio_id": portfolio.id,
                            "portfolio_name": portfolio.name,
                            "type": "var",
                            "severity": "high",
                            "message": f"VaR exceeds 5% of portfolio value: {var_percent:.2%}",
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    )

                if risk_metrics["risk_metrics"].get("max_drawdown", 0) > 0.1:
                    max_drawdown = risk_metrics["risk_metrics"]["max_drawdown"]
                    alerts.append(
                        {
                            "portfolio_id": portfolio.id,
                            "portfolio_name": portfolio.name,
                            "type": "drawdown",
                            "severity": "medium",
                            "message": f"Maximum drawdown exceeds 10%: {max_drawdown:.2%}",
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    )

                if risk_metrics["risk_metrics"].get("sharpe", 0) < 0.5:
                    sharpe_ratio = risk_metrics["risk_metrics"]["sharpe"]
                    alerts.append(
                        {
                            "portfolio_id": portfolio.id,
                            "portfolio_name": portfolio.name,
                            "type": "sharpe",
                            "severity": "low",
                            "message": f"Sharpe ratio is below 0.5: {sharpe_ratio:.2f}",
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    )

            return alerts

        except Exception as e:
            logger.error(f"Error getting risk alerts: {e}")
            raise ServiceError(f"Error getting risk alerts: {str(e)}")

        finally:
            session.close()

    def _get_historical_data(
        self, symbol: str, lookback_period: int
    ) -> List[Dict[str, Any]]:
        """Get historical data for a symbol using MarketDataService.

        Args:
            symbol: Symbol
            lookback_period: Lookback period in days

        Returns:
            Historical data

        Raises:
            ServiceError: If there is an error getting data
        """
        try:
            market_data_service = MarketDataService(
                self.config_manager, self.db_manager
            )
            data = market_data_service.get_market_data(
                symbol=symbol, timeframe="1d", period=f"{lookback_period}d"
            )
            return data["data"]

        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            raise ServiceError(f"Error getting historical data: {str(e)}")

    def _calculate_returns(self, data: List[Dict[str, Any]]) -> np.ndarray:
        """Calculate returns from historical data

        Args:
            data: Historical data

        Returns:
            Returns
        """
        # Extract close prices
        prices = np.array([d["close"] for d in data])

        # Calculate returns
        returns = np.diff(prices) / prices[:-1]

        return returns

    def _calculate_portfolio_returns(
        self, portfolio: List[Dict[str, Any]], position_returns: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """Calculate portfolio returns

        Args:
            portfolio: Portfolio positions
            position_returns: Returns for each position

        Returns:
            Portfolio returns
        """
        # Calculate portfolio value
        portfolio_value = sum(
            position["quantity"] * position["entry_price"] for position in portfolio
        )

        # Calculate position weights
        weights = {}

        for position in portfolio:
            symbol = position["symbol"]
            weight = position["quantity"] * position["entry_price"] / portfolio_value
            weights[symbol] = weight

        # Calculate portfolio returns
        # Find the shortest return series
        min_length = min(len(returns) for returns in position_returns.values())

        # Initialize portfolio returns
        portfolio_returns = np.zeros(min_length)

        # Calculate weighted returns
        for symbol, returns in position_returns.items():
            portfolio_returns += weights[symbol] * returns[:min_length]

        return portfolio_returns

    def _calculate_var(self, returns: np.ndarray, confidence_level: float) -> float:
        """Calculate Value at Risk

        Args:
            returns: Historical returns
            confidence_level: Confidence level

        Returns:
            Value at Risk
        """
        # Sort returns
        sorted_returns = np.sort(returns)

        # Calculate index
        index = int(len(sorted_returns) * (1 - confidence_level))

        # Get VaR
        var = -sorted_returns[index]

        return float(var)

    def _calculate_cvar(self, returns: np.ndarray, confidence_level: float) -> float:
        """Calculate Conditional Value at Risk

        Args:
            returns: Historical returns
            confidence_level: Confidence level

        Returns:
            Conditional Value at Risk
        """
        # Sort returns
        sorted_returns = np.sort(returns)

        # Calculate index
        index = int(len(sorted_returns) * (1 - confidence_level))

        # Get CVaR
        cvar = -np.mean(sorted_returns[:index])

        return float(cvar)

    def _calculate_sharpe_ratio(
        self, returns: np.ndarray, risk_free_rate: float = 0.0
    ) -> float:
        """Calculate Sharpe ratio

        Args:
            returns: Historical returns
            risk_free_rate: Risk-free rate

        Returns:
            Sharpe ratio
        """
        # Calculate excess returns
        excess_returns = returns - risk_free_rate

        # Calculate Sharpe ratio
        sharpe = np.mean(excess_returns) / np.std(excess_returns)

        return float(sharpe)

    def _calculate_sortino_ratio(
        self, returns: np.ndarray, risk_free_rate: float = 0.0
    ) -> float:
        """Calculate Sortino ratio

        Args:
            returns: Historical returns
            risk_free_rate: Risk-free rate

        Returns:
            Sortino ratio
        """
        # Calculate excess returns
        excess_returns = returns - risk_free_rate

        # Calculate downside deviation
        downside_returns = excess_returns[excess_returns < 0]
        downside_deviation = (
            np.std(downside_returns) if len(downside_returns) > 0 else 0.0001
        )

        # Calculate Sortino ratio
        sortino = np.mean(excess_returns) / downside_deviation

        return float(sortino)

    def _calculate_max_drawdown(self, returns: np.ndarray) -> float:
        """Calculate maximum drawdown

        Args:
            returns: Historical returns

        Returns:
            Maximum drawdown
        """
        # Calculate cumulative returns
        cum_returns = np.cumprod(1 + returns)

        # Calculate running maximum
        running_max = np.maximum.accumulate(cum_returns)

        # Calculate drawdown
        drawdown = (running_max - cum_returns) / running_max

        # Get maximum drawdown
        max_drawdown = np.max(drawdown)

        return float(max_drawdown)

    def _calculate_expected_shortfall(
        self, returns: np.ndarray, confidence_level: float
    ) -> float:
        """Calculate Expected Shortfall (ES)

        Args:
            returns: Historical returns
            confidence_level: Confidence level

        Returns:
            Expected Shortfall
        """
        # Sort returns
        sorted_returns = np.sort(returns)

        # Calculate index for VaR
        var_index = int(len(sorted_returns) * (1 - confidence_level))

        # Get returns beyond VaR
        tail_returns = sorted_returns[:var_index]

        # Calculate ES (average of returns in the tail)
        es = -np.mean(tail_returns)

        return float(es)

    def implement_tail_risk_hedging(
        self, portfolio: List[Dict[str, Any]], risk_tolerance: float = 0.01
    ) -> Dict[str, Any]:
        """Implement a basic tail risk hedging strategy.
        This is a simplified example and would require more sophisticated models
        and real-time market data in a production environment.

        Args:
            portfolio: Current portfolio positions.
            risk_tolerance: Maximum acceptable VaR percentage.

        Returns:
            A dictionary indicating hedging actions taken.
        """
        logger.info("Implementing tail risk hedging.")

        # Calculate current VaR
        current_risk_metrics = self.calculate_risk_metrics(
            portfolio=portfolio, risk_metrics=["var"], confidence_level=0.95
        )
        current_var_percent = current_risk_metrics["risk_metrics"].get("var_percent", 0)

        hedging_actions = {
            "status": "no_action_needed",
            "current_var_percent": current_var_percent,
            "risk_tolerance": risk_tolerance,
            "recommendations": [],
        }

        if current_var_percent > risk_tolerance:
            logger.warning(
                f"Current VaR ({current_var_percent:.2%}) exceeds risk tolerance ({risk_tolerance:.2%}). Recommending hedging actions."
            )
            hedging_actions["status"] = "hedging_recommended"

            # Simplified hedging recommendation: reduce equity exposure or buy protective puts
            # In a real system, this would involve complex optimization and instrument selection
            hedging_actions["recommendations"].append(
                "Consider reducing exposure to high-beta equities or purchasing out-of-the-money put options on relevant indices/ETFs."
            )
            hedging_actions["recommendations"].append(
                "Evaluate adding inverse ETFs or safe-haven assets (e.g., gold, long-term government bonds) to the portfolio."
            )
        else:
            logger.info(
                f"Current VaR ({current_var_percent:.2%}) is within risk tolerance ({risk_tolerance:.2%}). No hedging action needed."
            )

        return hedging_actions
