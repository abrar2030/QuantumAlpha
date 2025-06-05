"""
Unit tests for the Execution Service's Order Manager.
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
from typing import List, Dict, Any, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import module to test
try:
    from backend.execution_service.order_manager import OrderManager
    from backend.common.exceptions import NotFoundError, ValidationError, ServiceError
    from backend.common.models import Order, Execution
except ImportError:
    # Mock the classes for testing when imports fail
    class OrderManager:
        pass
    
    class Order:
        pass
    
    class Execution:
        pass
    
    class NotFoundError(Exception):
        pass
    
    class ValidationError(Exception):
        pass
    
    class ServiceError(Exception):
        pass

class TestOrderManager(unittest.TestCase):
    """Unit tests for OrderManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_config.return_value = {
            "execution_service": {
                "default_broker": "test_broker",
                "order_timeout": 60
            }
        }
        
        # Create mock database manager
        self.db_manager = MagicMock()
        
        # Create mock session
        self.session = MagicMock()
        self.db_manager.get_postgres_session.return_value = self.session
        
        # Create mock broker integration
        self.broker_integration = MagicMock()
        
        # Create order manager
        self.order_manager = OrderManager(self.config_manager, self.db_manager, self.broker_integration)
    
    def test_init(self):
        """Test OrderManager initialization."""
        order_manager = OrderManager(self.config_manager, self.db_manager, self.broker_integration)
        
        # Check attributes
        self.assertEqual(order_manager.config_manager, self.config_manager)
        self.assertEqual(order_manager.db_manager, self.db_manager)
        self.assertEqual(order_manager.broker_integration, self.broker_integration)
        self.assertEqual(order_manager.default_broker, "test_broker")
        self.assertEqual(order_manager.order_timeout, 60)
    
    def test_create_order(self):
        """Test order creation."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.id = "order_1234567890"
        mock_order.to_dict.return_value = {
            "id": "order_1234567890",
            "user_id": "user_1234567890",
            "portfolio_id": "portfolio_1234567890",
            "symbol": "AAPL",
            "side": "buy",
            "type": "market",
            "status": "created",
            "quantity": 100,
            "price": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Mock Order class
        with patch("backend.common.models.Order") as MockOrder:
            MockOrder.return_value = mock_order
            
            # Create order
            order = self.order_manager.create_order(
                user_id="user_1234567890",
                portfolio_id="portfolio_1234567890",
                symbol="AAPL",
                side="buy",
                order_type="market",
                quantity=100
            )
            
            # Check result
            self.assertEqual(order["id"], "order_1234567890")
            self.assertEqual(order["user_id"], "user_1234567890")
            self.assertEqual(order["portfolio_id"], "portfolio_1234567890")
            self.assertEqual(order["symbol"], "AAPL")
            self.assertEqual(order["side"], "buy")
            self.assertEqual(order["type"], "market")
            self.assertEqual(order["status"], "created")
            self.assertEqual(order["quantity"], 100)
            
            # Check if order was added and committed
            self.session.add.assert_called_once()
            self.session.commit.assert_called_once()
    
    def test_create_order_invalid_side(self):
        """Test order creation with invalid side."""
        # Create order with invalid side
        with self.assertRaises(ValidationError):
            self.order_manager.create_order(
                user_id="user_1234567890",
                portfolio_id="portfolio_1234567890",
                symbol="AAPL",
                side="invalid",
                order_type="market",
                quantity=100
            )
    
    def test_create_order_invalid_type(self):
        """Test order creation with invalid type."""
        # Create order with invalid type
        with self.assertRaises(ValidationError):
            self.order_manager.create_order(
                user_id="user_1234567890",
                portfolio_id="portfolio_1234567890",
                symbol="AAPL",
                side="buy",
                order_type="invalid",
                quantity=100
            )
    
    def test_create_order_invalid_quantity(self):
        """Test order creation with invalid quantity."""
        # Create order with invalid quantity
        with self.assertRaises(ValidationError):
            self.order_manager.create_order(
                user_id="user_1234567890",
                portfolio_id="portfolio_1234567890",
                symbol="AAPL",
                side="buy",
                order_type="market",
                quantity=0
            )
    
    def test_create_order_missing_price(self):
        """Test order creation with missing price for limit order."""
        # Create limit order without price
        with self.assertRaises(ValidationError):
            self.order_manager.create_order(
                user_id="user_1234567890",
                portfolio_id="portfolio_1234567890",
                symbol="AAPL",
                side="buy",
                order_type="limit",
                quantity=100
            )
    
    def test_get_order(self):
        """Test getting order by ID."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.to_dict.return_value = {
            "id": "order_1234567890",
            "user_id": "user_1234567890",
            "portfolio_id": "portfolio_1234567890",
            "symbol": "AAPL",
            "side": "buy",
            "type": "market",
            "status": "filled",
            "quantity": 100,
            "price": None,
            "filled_quantity": 100,
            "average_fill_price": 150.0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        self.session.query().filter().first.return_value = mock_order
        
        # Get order
        order = self.order_manager.get_order("order_1234567890")
        
        # Check result
        self.assertEqual(order["id"], "order_1234567890")
        self.assertEqual(order["user_id"], "user_1234567890")
        self.assertEqual(order["portfolio_id"], "portfolio_1234567890")
        self.assertEqual(order["symbol"], "AAPL")
        self.assertEqual(order["side"], "buy")
        self.assertEqual(order["type"], "market")
        self.assertEqual(order["status"], "filled")
        self.assertEqual(order["quantity"], 100)
        self.assertEqual(order["filled_quantity"], 100)
        self.assertEqual(order["average_fill_price"], 150.0)
    
    def test_get_order_not_found(self):
        """Test getting non-existent order."""
        # Set up mock order query
        self.session.query().filter().first.return_value = None
        
        # Get non-existent order
        with self.assertRaises(NotFoundError):
            self.order_manager.get_order("nonexistent")
    
    def test_get_orders(self):
        """Test getting orders with filters."""
        # Set up mock orders
        mock_order1 = MagicMock()
        mock_order1.to_dict.return_value = {
            "id": "order_1",
            "user_id": "user_1234567890",
            "portfolio_id": "portfolio_1234567890",
            "symbol": "AAPL",
            "side": "buy",
            "type": "market",
            "status": "filled",
            "quantity": 100,
            "price": None,
            "filled_quantity": 100,
            "average_fill_price": 150.0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        mock_order2 = MagicMock()
        mock_order2.to_dict.return_value = {
            "id": "order_2",
            "user_id": "user_1234567890",
            "portfolio_id": "portfolio_1234567890",
            "symbol": "MSFT",
            "side": "sell",
            "type": "limit",
            "status": "created",
            "quantity": 50,
            "price": 260.0,
            "filled_quantity": 0,
            "average_fill_price": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        self.session.query().filter().all.return_value = [mock_order1, mock_order2]
        
        # Get orders
        orders = self.order_manager.get_orders(
            user_id="user_1234567890",
            portfolio_id="portfolio_1234567890"
        )
        
        # Check result
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]["id"], "order_1")
        self.assertEqual(orders[0]["symbol"], "AAPL")
        self.assertEqual(orders[0]["side"], "buy")
        self.assertEqual(orders[0]["status"], "filled")
        self.assertEqual(orders[1]["id"], "order_2")
        self.assertEqual(orders[1]["symbol"], "MSFT")
        self.assertEqual(orders[1]["side"], "sell")
        self.assertEqual(orders[1]["status"], "created")
    
    def test_submit_order(self):
        """Test order submission."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.id = "order_1234567890"
        mock_order.user_id = "user_1234567890"
        mock_order.portfolio_id = "portfolio_1234567890"
        mock_order.symbol = "AAPL"
        mock_order.side = "buy"
        mock_order.type = "market"
        mock_order.status = "created"
        mock_order.quantity = 100
        mock_order.price = None
        mock_order.filled_quantity = 0
        mock_order.average_fill_price = None
        mock_order.created_at = datetime.utcnow()
        mock_order.updated_at = datetime.utcnow()
        mock_order.to_dict.return_value = {
            "id": "order_1234567890",
            "user_id": "user_1234567890",
            "portfolio_id": "portfolio_1234567890",
            "symbol": "AAPL",
            "side": "buy",
            "type": "market",
            "status": "submitted",
            "quantity": 100,
            "price": None,
            "filled_quantity": 0,
            "average_fill_price": None,
            "created_at": mock_order.created_at.isoformat(),
            "updated_at": mock_order.updated_at.isoformat(),
            "broker_order_id": "broker_1234567890"
        }
        self.session.query().filter().first.return_value = mock_order
        
        # Mock broker integration
        self.broker_integration.submit_order.return_value = {
            "broker_order_id": "broker_1234567890",
            "status": "submitted"
        }
        
        # Submit order
        order = self.order_manager.submit_order("order_1234567890")
        
        # Check result
        self.assertEqual(order["id"], "order_1234567890")
        self.assertEqual(order["status"], "submitted")
        self.assertEqual(order["broker_order_id"], "broker_1234567890")
        
        # Check if broker integration was called
        self.broker_integration.submit_order.assert_called_once()
        
        # Check if order was updated and committed
        self.assertEqual(mock_order.status, "submitted")
        self.assertEqual(mock_order.broker_order_id, "broker_1234567890")
        self.session.commit.assert_called_once()
    
    def test_submit_order_not_found(self):
        """Test submitting non-existent order."""
        # Set up mock order query
        self.session.query().filter().first.return_value = None
        
        # Submit non-existent order
        with self.assertRaises(NotFoundError):
            self.order_manager.submit_order("nonexistent")
    
    def test_submit_order_already_submitted(self):
        """Test submitting already submitted order."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.status = "submitted"
        self.session.query().filter().first.return_value = mock_order
        
        # Submit already submitted order
        with self.assertRaises(ValidationError):
            self.order_manager.submit_order("order_1234567890")
    
    def test_cancel_order(self):
        """Test order cancellation."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.id = "order_1234567890"
        mock_order.status = "submitted"
        mock_order.broker_order_id = "broker_1234567890"
        mock_order.to_dict.return_value = {
            "id": "order_1234567890",
            "status": "cancelled",
            "broker_order_id": "broker_1234567890"
        }
        self.session.query().filter().first.return_value = mock_order
        
        # Mock broker integration
        self.broker_integration.cancel_order.return_value = {
            "broker_order_id": "broker_1234567890",
            "status": "cancelled"
        }
        
        # Cancel order
        order = self.order_manager.cancel_order("order_1234567890")
        
        # Check result
        self.assertEqual(order["id"], "order_1234567890")
        self.assertEqual(order["status"], "cancelled")
        
        # Check if broker integration was called
        self.broker_integration.cancel_order.assert_called_once()
        
        # Check if order was updated and committed
        self.assertEqual(mock_order.status, "cancelled")
        self.session.commit.assert_called_once()
    
    def test_cancel_order_not_found(self):
        """Test cancelling non-existent order."""
        # Set up mock order query
        self.session.query().filter().first.return_value = None
        
        # Cancel non-existent order
        with self.assertRaises(NotFoundError):
            self.order_manager.cancel_order("nonexistent")
    
    def test_cancel_order_not_cancellable(self):
        """Test cancelling non-cancellable order."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.status = "filled"
        self.session.query().filter().first.return_value = mock_order
        
        # Cancel non-cancellable order
        with self.assertRaises(ValidationError):
            self.order_manager.cancel_order("order_1234567890")
    
    def test_update_order_status(self):
        """Test order status update."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.id = "order_1234567890"
        mock_order.status = "submitted"
        mock_order.to_dict.return_value = {
            "id": "order_1234567890",
            "status": "filled",
            "broker_order_id": "broker_1234567890"
        }
        self.session.query().filter().first.return_value = mock_order
        
        # Update order status
        order = self.order_manager.update_order_status(
            order_id="order_1234567890",
            status="filled",
            broker_order_id="broker_1234567890"
        )
        
        # Check result
        self.assertEqual(order["id"], "order_1234567890")
        self.assertEqual(order["status"], "filled")
        self.assertEqual(order["broker_order_id"], "broker_1234567890")
        
        # Check if order was updated and committed
        self.assertEqual(mock_order.status, "filled")
        self.assertEqual(mock_order.broker_order_id, "broker_1234567890")
        self.session.commit.assert_called_once()
    
    def test_update_order_status_not_found(self):
        """Test updating status of non-existent order."""
        # Set up mock order query
        self.session.query().filter().first.return_value = None
        
        # Update status of non-existent order
        with self.assertRaises(NotFoundError):
            self.order_manager.update_order_status(
                order_id="nonexistent",
                status="filled"
            )
    
    def test_update_order_status_invalid_status(self):
        """Test updating order with invalid status."""
        # Set up mock order
        mock_order = MagicMock()
        self.session.query().filter().first.return_value = mock_order
        
        # Update order with invalid status
        with self.assertRaises(ValidationError):
            self.order_manager.update_order_status(
                order_id="order_1234567890",
                status="invalid"
            )
    
    def test_add_execution(self):
        """Test adding execution to order."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.id = "order_1234567890"
        mock_order.status = "submitted"
        mock_order.quantity = 100
        mock_order.filled_quantity = 0
        self.session.query(Order).filter().first.return_value = mock_order
        
        # Set up mock execution query
        self.session.query(Execution).filter().all.return_value = []
        
        # Set up mock execution
        mock_execution = MagicMock()
        mock_execution.id = "execution_1234567890"
        mock_execution.order_id = "order_1234567890"
        mock_execution.price = 150.0
        mock_execution.quantity = 100
        mock_execution.timestamp = datetime.utcnow()
        mock_execution.broker_execution_id = "broker_execution_1234567890"
        mock_execution.to_dict.return_value = {
            "id": "execution_1234567890",
            "order_id": "order_1234567890",
            "price": 150.0,
            "quantity": 100,
            "timestamp": mock_execution.timestamp.isoformat(),
            "broker_execution_id": "broker_execution_1234567890"
        }
        
        # Mock Execution class
        with patch("backend.common.models.Execution") as MockExecution:
            MockExecution.return_value = mock_execution
            
            # Add execution
            execution = self.order_manager.add_execution(
                order_id="order_1234567890",
                price=150.0,
                quantity=100,
                timestamp=datetime.utcnow(),
                broker_execution_id="broker_execution_1234567890"
            )
            
            # Check result
            self.assertEqual(execution["id"], "execution_1234567890")
            self.assertEqual(execution["order_id"], "order_1234567890")
            self.assertEqual(execution["price"], 150.0)
            self.assertEqual(execution["quantity"], 100)
            self.assertEqual(execution["broker_execution_id"], "broker_execution_1234567890")
            
            # Check if execution was added and committed
            self.session.add.assert_called_once()
            self.session.commit.assert_called_once()
            
            # Check if order was updated
            self.assertEqual(mock_order.status, "filled")
            self.assertEqual(mock_order.filled_quantity, 100)
    
    def test_add_execution_order_not_found(self):
        """Test adding execution to non-existent order."""
        # Set up mock order query
        self.session.query().filter().first.return_value = None
        
        # Add execution to non-existent order
        with self.assertRaises(NotFoundError):
            self.order_manager.add_execution(
                order_id="nonexistent",
                price=150.0,
                quantity=100,
                timestamp=datetime.utcnow()
            )
    
    def test_add_execution_partial_fill(self):
        """Test adding partial execution to order."""
        # Set up mock order
        mock_order = MagicMock()
        mock_order.id = "order_1234567890"
        mock_order.status = "submitted"
        mock_order.quantity = 100
        mock_order.filled_quantity = 0
        self.session.query(Order).filter().first.return_value = mock_order
        
        # Set up mock execution query
        self.session.query(Execution).filter().all.return_value = []
        
        # Set up mock execution
        mock_execution = MagicMock()
        mock_execution.id = "execution_1234567890"
        mock_execution.order_id = "order_1234567890"
        mock_execution.price = 150.0
        mock_execution.quantity = 50  # Partial fill
        mock_execution.timestamp = datetime.utcnow()
        mock_execution.broker_execution_id = "broker_execution_1234567890"
        mock_execution.to_dict.return_value = {
            "id": "execution_1234567890",
            "order_id": "order_1234567890",
            "price": 150.0,
            "quantity": 50,
            "timestamp": mock_execution.timestamp.isoformat(),
            "broker_execution_id": "broker_execution_1234567890"
        }
        
        # Mock Execution class
        with patch("backend.common.models.Execution") as MockExecution:
            MockExecution.return_value = mock_execution
            
            # Add execution
            execution = self.order_manager.add_execution(
                order_id="order_1234567890",
                price=150.0,
                quantity=50,
                timestamp=datetime.utcnow(),
                broker_execution_id="broker_execution_1234567890"
            )
            
            # Check result
            self.assertEqual(execution["id"], "execution_1234567890")
            self.assertEqual(execution["order_id"], "order_1234567890")
            self.assertEqual(execution["price"], 150.0)
            self.assertEqual(execution["quantity"], 50)
            
            # Check if order was updated
            self.assertEqual(mock_order.status, "partially_filled")
            self.assertEqual(mock_order.filled_quantity, 50)
    
    def test_get_executions(self):
        """Test getting executions with filters."""
        # Set up mock executions
        mock_execution1 = MagicMock()
        mock_execution1.to_dict.return_value = {
            "id": "execution_1",
            "order_id": "order_1234567890",
            "price": 150.0,
            "quantity": 50,
            "timestamp": datetime.utcnow().isoformat(),
            "broker_execution_id": "broker_execution_1"
        }
        
        mock_execution2 = MagicMock()
        mock_execution2.to_dict.return_value = {
            "id": "execution_2",
            "order_id": "order_1234567890",
            "price": 151.0,
            "quantity": 50,
            "timestamp": datetime.utcnow().isoformat(),
            "broker_execution_id": "broker_execution_2"
        }
        
        self.session.query().all.return_value = [mock_execution1, mock_execution2]
        
        # Get executions
        executions = self.order_manager.get_executions(
            order_id="order_1234567890"
        )
        
        # Check result
        self.assertEqual(len(executions), 2)
        self.assertEqual(executions[0]["id"], "execution_1")
        self.assertEqual(executions[0]["order_id"], "order_1234567890")
        self.assertEqual(executions[0]["price"], 150.0)
        self.assertEqual(executions[0]["quantity"], 50)
        self.assertEqual(executions[1]["id"], "execution_2")
        self.assertEqual(executions[1]["order_id"], "order_1234567890")
        self.assertEqual(executions[1]["price"], 151.0)
        self.assertEqual(executions[1]["quantity"], 50)

if __name__ == "__main__":
    unittest.main()

