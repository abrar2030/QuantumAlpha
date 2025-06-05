"""
Common data models for QuantumAlpha services.
Defines SQLAlchemy models for PostgreSQL database.
"""
import uuid
import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """User model"""
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: f"user_{uuid.uuid4().hex}")
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default="user")  # user, admin, analyst
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    portfolios = relationship("Portfolio", back_populates="user")
    api_keys = relationship("ApiKey", back_populates="user")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Portfolio(Base):
    """Portfolio model"""
    
    __tablename__ = "portfolios"
    
    id = Column(String, primary_key=True, default=lambda: f"portfolio_{uuid.uuid4().hex}")
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    initial_balance = Column(Float, nullable=False)
    current_balance = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")
    orders = relationship("Order", back_populates="portfolio")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'currency': self.currency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Position(Base):
    """Position model"""
    
    __tablename__ = "positions"
    
    id = Column(String, primary_key=True, default=lambda: f"position_{uuid.uuid4().hex}")
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('portfolio_id', 'symbol', name='uix_portfolio_symbol'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'entry_price': self.entry_price,
            'current_price': self.current_price,
            'market_value': self.quantity * self.current_price,
            'unrealized_pl': self.quantity * (self.current_price - self.entry_price),
            'unrealized_pl_percent': (self.current_price - self.entry_price) / self.entry_price if self.entry_price else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Order(Base):
    """Order model"""
    
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=lambda: f"order_{uuid.uuid4().hex}")
    portfolio_id = Column(String, ForeignKey("portfolios.id"), nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy, sell
    quantity = Column(Float, nullable=False)
    order_type = Column(String, nullable=False)  # market, limit, stop, stop_limit
    price = Column(Float)  # Required for limit orders
    stop_price = Column(Float)  # Required for stop orders
    time_in_force = Column(String, default="day")  # day, gtc, ioc
    status = Column(String, default="pending")  # pending, filled, partially_filled, canceled
    filled_quantity = Column(Float, default=0.0)
    average_price = Column(Float)
    broker = Column(String, nullable=False)  # alpaca, interactive_brokers
    broker_order_id = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="orders")
    executions = relationship("Execution", back_populates="order")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'symbol': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'order_type': self.order_type,
            'price': self.price,
            'stop_price': self.stop_price,
            'time_in_force': self.time_in_force,
            'status': self.status,
            'filled_quantity': self.filled_quantity,
            'average_price': self.average_price,
            'broker': self.broker,
            'broker_order_id': self.broker_order_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Execution(Base):
    """Execution model"""
    
    __tablename__ = "executions"
    
    id = Column(String, primary_key=True, default=lambda: f"exec_{uuid.uuid4().hex}")
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="executions")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'order_id': self.order_id,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class Strategy(Base):
    """Strategy model"""
    
    __tablename__ = "strategies"
    
    id = Column(String, primary_key=True, default=lambda: f"strategy_{uuid.uuid4().hex}")
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(String, nullable=False)  # ml, rule_based, hybrid
    status = Column(String, default="inactive")  # active, inactive, backtest
    config = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    models = relationship("Model", back_populates="strategy")
    signals = relationship("Signal", back_populates="strategy")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'status': self.status,
            'config': self.config,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Model(Base):
    """Model model"""
    
    __tablename__ = "models"
    
    id = Column(String, primary_key=True, default=lambda: f"model_{uuid.uuid4().hex}")
    strategy_id = Column(String, ForeignKey("strategies.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # lstm, transformer, reinforcement
    status = Column(String, default="training")  # training, active, inactive
    config = Column(JSON, nullable=False)
    performance = Column(JSON)
    registry_path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_trained = Column(DateTime)
    
    # Relationships
    strategy = relationship("Strategy", back_populates="models")
    signals = relationship("Signal", back_populates="model")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'config': self.config,
            'performance': self.performance,
            'registry_path': self.registry_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_trained': self.last_trained.isoformat() if self.last_trained else None
        }


class Signal(Base):
    """Signal model"""
    
    __tablename__ = "signals"
    
    id = Column(String, primary_key=True, default=lambda: f"signal_{uuid.uuid4().hex}")
    strategy_id = Column(String, ForeignKey("strategies.id"), nullable=False)
    model_id = Column(String, ForeignKey("models.id"), nullable=False)
    symbol = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # buy, sell
    strength = Column(Float, nullable=False)  # 0.0 to 1.0
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    target_price = Column(Float)
    stop_loss = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    expiration = Column(DateTime)
    
    # Relationships
    strategy = relationship("Strategy", back_populates="signals")
    model = relationship("Model", back_populates="signals")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'strategy_id': self.strategy_id,
            'model_id': self.model_id,
            'symbol': self.symbol,
            'direction': self.direction,
            'strength': self.strength,
            'confidence': self.confidence,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'expiration': self.expiration.isoformat() if self.expiration else None
        }


class ApiKey(Base):
    """API key model"""
    
    __tablename__ = "api_keys"
    
    id = Column(String, primary_key=True, default=lambda: f"key_{uuid.uuid4().hex}")
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False, unique=True)
    secret = Column(String, nullable=False)
    permissions = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)
    last_used_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'key': self.key,
            'permissions': self.permissions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None
        }

