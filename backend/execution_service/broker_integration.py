"""
Broker integration for QuantumAlpha Execution Service.
Handles integration with various brokers.
"""

import logging
import os
# Add parent directory to path to import common modules
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import alpaca_trade_api as tradeapi

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import NotFoundError, ServiceError, ValidationError, setup_logger

# Configure logging
logger = setup_logger("broker_integration", logging.INFO)


class BrokerIntegration:
    """Broker integration"""

    def __init__(self, config_manager, db_manager):
        """Initialize broker integration

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager

        # Initialize brokers
        self.brokers = {
            "alpaca": {
                "name": "Alpaca",
                "description": "Alpaca Markets API",
                "api_key": config_manager.get("broker.alpaca.api_key"),
                "api_secret": config_manager.get("broker.alpaca.api_secret"),
                "endpoint": config_manager.get(
                    "broker.alpaca.endpoint", "https://paper-api.alpaca.markets"
                ),
                "status": "active",
            },
            "interactive_brokers": {
                "name": "Interactive Brokers",
                "description": "Interactive Brokers API",
                "status": "inactive",
            },
            "td_ameritrade": {
                "name": "TD Ameritrade",
                "description": "TD Ameritrade API",
                "status": "inactive",
            },
        }

        # Initialize Alpaca API
        if self.brokers["alpaca"]["api_key"] and self.brokers["alpaca"]["api_secret"]:
            self.alpaca_api = tradeapi.REST(
                key_id=self.brokers["alpaca"]["api_key"],
                secret_key=self.brokers["alpaca"]["api_secret"],
                base_url=self.brokers["alpaca"]["endpoint"],
            )
        else:
            self.alpaca_api = None
            self.brokers["alpaca"]["status"] = "inactive"

        logger.info("Broker integration initialized")

    def get_brokers(self) -> List[Dict[str, Any]]:
        """Get all brokers

        Returns:
            List of brokers
        """
        brokers = []

        for broker_id, broker in self.brokers.items():
            brokers.append(
                {
                    "id": broker_id,
                    "name": broker["name"],
                    "description": broker["description"],
                    "status": broker["status"],
                }
            )

        return brokers

    def get_broker(self, broker_id: str) -> Dict[str, Any]:
        """Get a specific broker

        Args:
            broker_id: Broker ID

        Returns:
            Broker details

        Raises:
            NotFoundError: If broker is not found
        """
        if broker_id not in self.brokers:
            raise NotFoundError(f"Broker not found: {broker_id}")

        broker = self.brokers[broker_id]

        return {
            "id": broker_id,
            "name": broker["name"],
            "description": broker["description"],
            "status": broker["status"],
        }

    def get_accounts(self, broker_id: str) -> List[Dict[str, Any]]:
        """Get accounts for a broker

        Args:
            broker_id: Broker ID

        Returns:
            List of accounts

        Raises:
            NotFoundError: If broker is not found
            ServiceError: If there is an error getting accounts
        """
        try:
            if broker_id not in self.brokers:
                raise NotFoundError(f"Broker not found: {broker_id}")

            if self.brokers[broker_id]["status"] != "active":
                raise ServiceError(f"Broker is not active: {broker_id}")

            if broker_id == "alpaca":
                return self._get_alpaca_accounts()
            else:
                raise ServiceError(f"Broker not implemented: {broker_id}")

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error getting accounts: {e}")
            raise ServiceError(f"Error getting accounts: {str(e)}")

    def get_positions(self, broker_id: str, account_id: str) -> List[Dict[str, Any]]:
        """Get positions for a broker account

        Args:
            broker_id: Broker ID
            account_id: Account ID

        Returns:
            List of positions

        Raises:
            NotFoundError: If broker is not found
            ServiceError: If there is an error getting positions
        """
        try:
            if broker_id not in self.brokers:
                raise NotFoundError(f"Broker not found: {broker_id}")

            if self.brokers[broker_id]["status"] != "active":
                raise ServiceError(f"Broker is not active: {broker_id}")

            if broker_id == "alpaca":
                return self._get_alpaca_positions(account_id)
            else:
                raise ServiceError(f"Broker not implemented: {broker_id}")

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            raise ServiceError(f"Error getting positions: {str(e)}")

    def submit_order(self, broker_id: str, order: Dict[str, Any]) -> Dict[str, Any]:
        """Submit an order to a broker

        Args:
            broker_id: Broker ID
            order: Order data

        Returns:
            Broker order details

        Raises:
            NotFoundError: If broker is not found
            ValidationError: If order data is invalid
            ServiceError: If there is an error submitting the order
        """
        try:
            if broker_id not in self.brokers:
                raise NotFoundError(f"Broker not found: {broker_id}")

            if self.brokers[broker_id]["status"] != "active":
                raise ServiceError(f"Broker is not active: {broker_id}")

            # Validate order
            if "symbol" not in order:
                raise ValidationError("Symbol is required")

            if "side" not in order:
                raise ValidationError("Side is required")

            if "type" not in order:
                raise ValidationError("Order type is required")

            if "quantity" not in order:
                raise ValidationError("Quantity is required")

            if broker_id == "alpaca":
                return self._submit_alpaca_order(order)
            else:
                raise ServiceError(f"Broker not implemented: {broker_id}")

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error submitting order: {e}")
            raise ServiceError(f"Error submitting order: {str(e)}")

    def cancel_order(self, broker_id: str, broker_order_id: str) -> Dict[str, Any]:
        """Cancel an order with a broker

        Args:
            broker_id: Broker ID
            broker_order_id: Broker order ID

        Returns:
            Cancellation result

        Raises:
            NotFoundError: If broker is not found
            ServiceError: If there is an error canceling the order
        """
        try:
            if broker_id not in self.brokers:
                raise NotFoundError(f"Broker not found: {broker_id}")

            if self.brokers[broker_id]["status"] != "active":
                raise ServiceError(f"Broker is not active: {broker_id}")

            if broker_id == "alpaca":
                return self._cancel_alpaca_order(broker_order_id)
            else:
                raise ServiceError(f"Broker not implemented: {broker_id}")

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            raise ServiceError(f"Error canceling order: {str(e)}")

    def get_order_status(self, broker_id: str, broker_order_id: str) -> Dict[str, Any]:
        """Get order status from a broker

        Args:
            broker_id: Broker ID
            broker_order_id: Broker order ID

        Returns:
            Order status

        Raises:
            NotFoundError: If broker is not found
            ServiceError: If there is an error getting order status
        """
        try:
            if broker_id not in self.brokers:
                raise NotFoundError(f"Broker not found: {broker_id}")

            if self.brokers[broker_id]["status"] != "active":
                raise ServiceError(f"Broker is not active: {broker_id}")

            if broker_id == "alpaca":
                return self._get_alpaca_order_status(broker_order_id)
            else:
                raise ServiceError(f"Broker not implemented: {broker_id}")

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            raise ServiceError(f"Error getting order status: {str(e)}")

    def _get_alpaca_accounts(self) -> List[Dict[str, Any]]:
        """Get Alpaca accounts

        Returns:
            List of accounts

        Raises:
            ServiceError: If there is an error getting accounts
        """
        try:
            if not self.alpaca_api:
                raise ServiceError("Alpaca API not initialized")

            # Get account
            account = self.alpaca_api.get_account()

            # Convert to dictionary
            account_dict = {
                "id": account.id,
                "status": account.status,
                "currency": account.currency,
                "buying_power": float(account.buying_power),
                "cash": float(account.cash),
                "portfolio_value": float(account.portfolio_value),
                "pattern_day_trader": account.pattern_day_trader,
                "trading_blocked": account.trading_blocked,
                "transfers_blocked": account.transfers_blocked,
                "account_blocked": account.account_blocked,
                "created_at": (
                    account.created_at.isoformat()
                    if hasattr(account, "created_at")
                    else None
                ),
            }

            return [account_dict]

        except Exception as e:
            logger.error(f"Error getting Alpaca accounts: {e}")
            raise ServiceError(f"Error getting Alpaca accounts: {str(e)}")

    def _get_alpaca_positions(self, account_id: str) -> List[Dict[str, Any]]:
        """Get Alpaca positions

        Args:
            account_id: Account ID

        Returns:
            List of positions

        Raises:
            ServiceError: If there is an error getting positions
        """
        try:
            if not self.alpaca_api:
                raise ServiceError("Alpaca API not initialized")

            # Get positions
            positions = self.alpaca_api.list_positions()

            # Convert to dictionaries
            position_dicts = []

            for position in positions:
                position_dict = {
                    "symbol": position.symbol,
                    "quantity": float(position.qty),
                    "side": "long" if float(position.qty) > 0 else "short",
                    "entry_price": float(position.avg_entry_price),
                    "current_price": float(position.current_price),
                    "market_value": float(position.market_value),
                    "cost_basis": float(position.cost_basis),
                    "unrealized_pl": float(position.unrealized_pl),
                    "unrealized_plpc": float(position.unrealized_plpc),
                    "exchange": position.exchange,
                }

                position_dicts.append(position_dict)

            return position_dicts

        except Exception as e:
            logger.error(f"Error getting Alpaca positions: {e}")
            raise ServiceError(f"Error getting Alpaca positions: {str(e)}")

    def _submit_alpaca_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Submit an order to Alpaca

        Args:
            order: Order data

        Returns:
            Broker order details

        Raises:
            ServiceError: If there is an error submitting the order
        """
        try:
            if not self.alpaca_api:
                raise ServiceError("Alpaca API not initialized")

            # Map order type
            order_type_map = {
                "market": "market",
                "limit": "limit",
                "stop": "stop",
                "stop_limit": "stop_limit",
            }

            alpaca_order_type = order_type_map.get(order["type"], "market")

            # Map time in force
            time_in_force_map = {
                "day": "day",
                "gtc": "gtc",
                "opg": "opg",
                "cls": "cls",
                "ioc": "ioc",
                "fok": "fok",
            }

            alpaca_time_in_force = time_in_force_map.get(
                order.get("time_in_force", "day"), "day"
            )

            # Submit order
            alpaca_order = self.alpaca_api.submit_order(
                symbol=order["symbol"],
                qty=order["quantity"],
                side=order["side"],
                type=alpaca_order_type,
                time_in_force=alpaca_time_in_force,
                limit_price=order.get("price"),
                stop_price=order.get("stop_price"),
            )

            # Convert to dictionary
            order_dict = {
                "broker_order_id": alpaca_order.id,
                "status": alpaca_order.status,
                "created_at": (
                    alpaca_order.created_at.isoformat()
                    if hasattr(alpaca_order, "created_at")
                    else None
                ),
                "updated_at": (
                    alpaca_order.updated_at.isoformat()
                    if hasattr(alpaca_order, "updated_at")
                    else None
                ),
                "submitted_at": (
                    alpaca_order.submitted_at.isoformat()
                    if hasattr(alpaca_order, "submitted_at")
                    else None
                ),
                "filled_at": (
                    alpaca_order.filled_at.isoformat()
                    if hasattr(alpaca_order, "filled_at")
                    else None
                ),
                "expired_at": (
                    alpaca_order.expired_at.isoformat()
                    if hasattr(alpaca_order, "expired_at")
                    else None
                ),
                "canceled_at": (
                    alpaca_order.canceled_at.isoformat()
                    if hasattr(alpaca_order, "canceled_at")
                    else None
                ),
                "failed_at": (
                    alpaca_order.failed_at.isoformat()
                    if hasattr(alpaca_order, "failed_at")
                    else None
                ),
                "filled_qty": (
                    float(alpaca_order.filled_qty)
                    if hasattr(alpaca_order, "filled_qty")
                    else 0
                ),
                "filled_avg_price": (
                    float(alpaca_order.filled_avg_price)
                    if hasattr(alpaca_order, "filled_avg_price")
                    and alpaca_order.filled_avg_price
                    else None
                ),
            }

            return order_dict

        except Exception as e:
            logger.error(f"Error submitting Alpaca order: {e}")
            raise ServiceError(f"Error submitting Alpaca order: {str(e)}")

    def _cancel_alpaca_order(self, broker_order_id: str) -> Dict[str, Any]:
        """Cancel an order with Alpaca

        Args:
            broker_order_id: Broker order ID

        Returns:
            Cancellation result

        Raises:
            ServiceError: If there is an error canceling the order
        """
        try:
            if not self.alpaca_api:
                raise ServiceError("Alpaca API not initialized")

            # Cancel order
            self.alpaca_api.cancel_order(broker_order_id)

            return {
                "broker_order_id": broker_order_id,
                "status": "canceled",
                "canceled_at": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error canceling Alpaca order: {e}")
            raise ServiceError(f"Error canceling Alpaca order: {str(e)}")

    def _get_alpaca_order_status(self, broker_order_id: str) -> Dict[str, Any]:
        """Get order status from Alpaca

        Args:
            broker_order_id: Broker order ID

        Returns:
            Order status

        Raises:
            ServiceError: If there is an error getting order status
        """
        try:
            if not self.alpaca_api:
                raise ServiceError("Alpaca API not initialized")

            # Get order
            alpaca_order = self.alpaca_api.get_order(broker_order_id)

            # Convert to dictionary
            order_dict = {
                "broker_order_id": alpaca_order.id,
                "status": alpaca_order.status,
                "created_at": (
                    alpaca_order.created_at.isoformat()
                    if hasattr(alpaca_order, "created_at")
                    else None
                ),
                "updated_at": (
                    alpaca_order.updated_at.isoformat()
                    if hasattr(alpaca_order, "updated_at")
                    else None
                ),
                "submitted_at": (
                    alpaca_order.submitted_at.isoformat()
                    if hasattr(alpaca_order, "submitted_at")
                    else None
                ),
                "filled_at": (
                    alpaca_order.filled_at.isoformat()
                    if hasattr(alpaca_order, "filled_at")
                    else None
                ),
                "expired_at": (
                    alpaca_order.expired_at.isoformat()
                    if hasattr(alpaca_order, "expired_at")
                    else None
                ),
                "canceled_at": (
                    alpaca_order.canceled_at.isoformat()
                    if hasattr(alpaca_order, "canceled_at")
                    else None
                ),
                "failed_at": (
                    alpaca_order.failed_at.isoformat()
                    if hasattr(alpaca_order, "failed_at")
                    else None
                ),
                "filled_qty": (
                    float(alpaca_order.filled_qty)
                    if hasattr(alpaca_order, "filled_qty")
                    else 0
                ),
                "filled_avg_price": (
                    float(alpaca_order.filled_avg_price)
                    if hasattr(alpaca_order, "filled_avg_price")
                    and alpaca_order.filled_avg_price
                    else None
                ),
            }

            return order_dict

        except Exception as e:
            logger.error(f"Error getting Alpaca order status: {e}")
            raise ServiceError(f"Error getting Alpaca order status: {str(e)}")
