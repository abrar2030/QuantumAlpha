"""
Order manager for QuantumAlpha Execution Service.
Handles order management and execution.
"""

import logging
import os

# Add parent directory to path to import common modules
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import NotFoundError, ServiceError, ValidationError, setup_logger
from common.models import Execution, Order

# Configure logging
logger = setup_logger("order_manager", logging.INFO)


class OrderManager:
    """Order manager"""

    def __init__(
        self, config_manager, db_manager, broker_integration, execution_strategy
    ):
        """Initialize order manager

        Args:
            config_manager: Configuration manager
            db_manager: Database manager
            broker_integration: Broker integration
            execution_strategy: Execution strategy
        """
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.broker_integration = broker_integration
        self.execution_strategy = execution_strategy

        logger.info("Order manager initialized")

    def get_orders(
        self,
        portfolio_id: Optional[str] = None,
        status: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get orders

        Args:
            portfolio_id: Filter by portfolio ID
            status: Filter by status
            symbol: Filter by symbol

        Returns:
            List of orders
        """
        try:
            logger.info("Getting orders")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Build query
            query = session.query(Order)

            if portfolio_id:
                query = query.filter(Order.portfolio_id == portfolio_id)

            if status:
                query = query.filter(Order.status == status)

            if symbol:
                query = query.filter(Order.symbol == symbol)

            # Execute query
            orders = query.all()

            # Convert to dictionaries
            order_dicts = [order.to_dict() for order in orders]

            return order_dicts

        except Exception as e:
            logger.error(f"Error getting orders: {e}")
            raise ServiceError(f"Error getting orders: {str(e)}")

        finally:
            session.close()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get a specific order

        Args:
            order_id: Order ID

        Returns:
            Order details

        Raises:
            NotFoundError: If order is not found
        """
        try:
            logger.info(f"Getting order {order_id}")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get order
            order = session.query(Order).filter(Order.id == order_id).first()

            if not order:
                raise NotFoundError(f"Order not found: {order_id}")

            # Convert to dictionary
            order_dict = order.to_dict()

            # Get executions
            executions = (
                session.query(Execution).filter(Execution.order_id == order_id).all()
            )

            # Convert to dictionaries
            execution_dicts = [execution.to_dict() for execution in executions]

            # Add executions to order
            order_dict["executions"] = execution_dicts

            return order_dict

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error getting order: {e}")
            raise ServiceError(f"Error getting order: {str(e)}")

        finally:
            session.close()

    def create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order

        Args:
            data: Order data

        Returns:
            Created order

        Raises:
            ValidationError: If data is invalid
        """
        try:
            logger.info("Creating order")

            # Validate required fields
            if "portfolio_id" not in data:
                raise ValidationError("Portfolio ID is required")

            if "symbol" not in data:
                raise ValidationError("Symbol is required")

            if "side" not in data:
                raise ValidationError("Side is required")

            if "type" not in data:
                raise ValidationError("Order type is required")

            if "quantity" not in data:
                raise ValidationError("Quantity is required")

            # Validate side
            if data["side"] not in ["buy", "sell"]:
                raise ValidationError(f"Invalid side: {data['side']}")

            # Validate type
            if data["type"] not in ["market", "limit", "stop", "stop_limit"]:
                raise ValidationError(f"Invalid order type: {data['type']}")

            # Validate price for limit and stop_limit orders
            if data["type"] in ["limit", "stop_limit"] and "price" not in data:
                raise ValidationError(
                    "Price is required for limit and stop_limit orders"
                )

            # Validate stop price for stop and stop_limit orders
            if data["type"] in ["stop", "stop_limit"] and "stop_price" not in data:
                raise ValidationError(
                    "Stop price is required for stop and stop_limit orders"
                )

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Generate order ID
            order_id = f"order_{uuid.uuid4().hex}"

            # Create order
            order = Order(
                id=order_id,
                portfolio_id=data["portfolio_id"],
                strategy_id=data.get("strategy_id"),
                symbol=data["symbol"],
                side=data["side"],
                type=data["type"],
                quantity=data["quantity"],
                price=data.get("price"),
                stop_price=data.get("stop_price"),
                time_in_force=data.get("time_in_force", "day"),
                status="pending",
                broker_id=data.get("broker_id"),
                broker_account_id=data.get("broker_account_id"),
                execution_strategy_id=data.get("execution_strategy_id"),
                created_at=datetime.utcnow(),
            )

            # Add to session
            session.add(order)

            # Commit changes
            session.commit()

            # Get order dictionary
            order_dict = order.to_dict()

            # Submit order to broker
            if data.get("submit", True):
                self._submit_order(order_dict)

            return order_dict

        except ValidationError:
            raise

        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise ServiceError(f"Error creating order: {str(e)}")

        finally:
            session.close()

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order

        Args:
            order_id: Order ID

        Returns:
            Canceled order

        Raises:
            NotFoundError: If order is not found
            ValidationError: If order cannot be canceled
        """
        try:
            logger.info(f"Canceling order {order_id}")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get order
            order = session.query(Order).filter(Order.id == order_id).first()

            if not order:
                raise NotFoundError(f"Order not found: {order_id}")

            # Check if order can be canceled
            if order.status not in ["pending", "open", "partially_filled"]:
                raise ValidationError(f"Order cannot be canceled: {order.status}")

            # Cancel order with broker
            if order.broker_id and order.broker_order_id:
                self.broker_integration.cancel_order(
                    broker_id=order.broker_id, broker_order_id=order.broker_order_id
                )

            # Update order status
            order.status = "canceled"
            order.updated_at = datetime.utcnow()

            # Commit changes
            session.commit()

            # Convert to dictionary
            order_dict = order.to_dict()

            return order_dict

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            raise ServiceError(f"Error canceling order: {str(e)}")

        finally:
            session.close()

    def _submit_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Submit an order to a broker

        Args:
            order: Order data

        Returns:
            Updated order

        Raises:
            ValidationError: If order cannot be submitted
        """
        try:
            logger.info(f"Submitting order {order['id']}")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get order from database
            db_order = session.query(Order).filter(Order.id == order["id"]).first()

            if not db_order:
                raise NotFoundError(f"Order not found: {order['id']}")

            # Check if order can be submitted
            if db_order.status != "pending":
                raise ValidationError(f"Order cannot be submitted: {db_order.status}")

            # Get broker ID
            broker_id = db_order.broker_id

            if not broker_id:
                # Use default broker
                broker_id = self.config_manager.get(
                    "execution.default_broker_id", "alpaca"
                )

            # Get execution strategy
            execution_strategy_id = db_order.execution_strategy_id

            if not execution_strategy_id:
                # Use default execution strategy
                execution_strategy_id = self.config_manager.get(
                    "execution.default_strategy_id", "market"
                )

            # Get execution strategy
            self.execution_strategy.get_strategy(execution_strategy_id)

            # Execute strategy
            result = self.execution_strategy.execute_strategy(
                strategy_id=execution_strategy_id, order=order, broker_id=broker_id
            )

            # Update order with broker information
            db_order.broker_id = broker_id
            db_order.broker_order_id = result.get("broker_order_id")
            db_order.status = result.get("status", "open")
            db_order.updated_at = datetime.utcnow()

            # Commit changes
            session.commit()

            # Convert to dictionary
            order_dict = db_order.to_dict()

            return order_dict

        except (NotFoundError, ValidationError):
            raise

        except Exception as e:
            logger.error(f"Error submitting order: {e}")

            # Update order status to error
            try:
                db_order.status = "error"
                db_order.error_message = str(e)
                db_order.updated_at = datetime.utcnow()
                session.commit()
            except Exception:
                pass

            raise ServiceError(f"Error submitting order: {str(e)}")

        finally:
            session.close()

    def update_order_status(
        self,
        order_id: str,
        status: str,
        broker_order_id: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update order status

        Args:
            order_id: Order ID
            status: New status
            broker_order_id: Broker order ID (optional)
            error_message: Error message (optional)

        Returns:
            Updated order

        Raises:
            NotFoundError: If order is not found
        """
        try:
            logger.info(f"Updating order status: {order_id} -> {status}")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get order
            order = session.query(Order).filter(Order.id == order_id).first()

            if not order:
                raise NotFoundError(f"Order not found: {order_id}")

            # Update order
            order.status = status
            order.updated_at = datetime.utcnow()

            if broker_order_id:
                order.broker_order_id = broker_order_id

            if error_message:
                order.error_message = error_message

            # Commit changes
            session.commit()

            # Convert to dictionary
            order_dict = order.to_dict()

            return order_dict

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            raise ServiceError(f"Error updating order status: {str(e)}")

        finally:
            session.close()

    def add_execution(
        self,
        order_id: str,
        price: float,
        quantity: float,
        timestamp: datetime,
        broker_execution_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add an execution to an order

        Args:
            order_id: Order ID
            price: Execution price
            quantity: Execution quantity
            timestamp: Execution timestamp
            broker_execution_id: Broker execution ID (optional)

        Returns:
            Created execution

        Raises:
            NotFoundError: If order is not found
        """
        try:
            logger.info(f"Adding execution to order {order_id}")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Get order
            order = session.query(Order).filter(Order.id == order_id).first()

            if not order:
                raise NotFoundError(f"Order not found: {order_id}")

            # Generate execution ID
            execution_id = f"exec_{uuid.uuid4().hex}"

            # Create execution
            execution = Execution(
                id=execution_id,
                order_id=order_id,
                price=price,
                quantity=quantity,
                timestamp=timestamp,
                broker_execution_id=broker_execution_id,
                created_at=datetime.utcnow(),
            )

            # Add to session
            session.add(execution)

            # Update order status
            filled_quantity = (
                sum(
                    e.quantity
                    for e in session.query(Execution)
                    .filter(Execution.order_id == order_id)
                    .all()
                )
                + quantity
            )

            if filled_quantity >= order.quantity:
                order.status = "filled"
            else:
                order.status = "partially_filled"

            order.filled_quantity = filled_quantity
            order.updated_at = datetime.utcnow()

            # Commit changes
            session.commit()

            # Convert to dictionary
            execution_dict = execution.to_dict()

            return execution_dict

        except NotFoundError:
            raise

        except Exception as e:
            logger.error(f"Error adding execution: {e}")
            raise ServiceError(f"Error adding execution: {str(e)}")

        finally:
            session.close()

    def get_executions(
        self,
        order_id: Optional[str] = None,
        portfolio_id: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get executions

        Args:
            order_id: Filter by order ID
            portfolio_id: Filter by portfolio ID
            symbol: Filter by symbol

        Returns:
            List of executions
        """
        try:
            logger.info("Getting executions")

            # Get database session
            session = self.db_manager.get_postgres_session()

            # Build query
            query = session.query(Execution)

            if order_id:
                query = query.filter(Execution.order_id == order_id)

            if portfolio_id or symbol:
                query = query.join(Order, Execution.order_id == Order.id)

                if portfolio_id:
                    query = query.filter(Order.portfolio_id == portfolio_id)

                if symbol:
                    query = query.filter(Order.symbol == symbol)

            # Execute query
            executions = query.all()

            # Convert to dictionaries
            execution_dicts = [execution.to_dict() for execution in executions]

            return execution_dicts

        except Exception as e:
            logger.error(f"Error getting executions: {e}")
            raise ServiceError(f"Error getting executions: {str(e)}")

        finally:
            session.close()
