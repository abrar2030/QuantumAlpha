"""
Validation utilities for QuantumAlpha services.
Provides schema validation and data sanitization.
"""
import re
import logging
from typing import Dict, Any, List, Optional, Union, Type
from pydantic import BaseModel, Field, validator, ValidationError
from datetime import datetime
from .logging_utils import ValidationError as ServiceValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# User schemas
class UserCreate(BaseModel):
    """Schema for user creation"""
    
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field('user')
    
    @validator('role')
    def validate_role(cls, v):
        """Validate role"""
        if v not in ['user', 'admin', 'analyst']:
            raise ValueError('Role must be one of: user, admin, analyst')
        return v


class UserUpdate(BaseModel):
    """Schema for user update"""
    
    email: Optional[str] = Field(None, regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    password: Optional[str] = Field(None, min_length=8)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None)
    
    @validator('role')
    def validate_role(cls, v):
        """Validate role"""
        if v is not None and v not in ['user', 'admin', 'analyst']:
            raise ValueError('Role must be one of: user, admin, analyst')
        return v


# Portfolio schemas
class PortfolioCreate(BaseModel):
    """Schema for portfolio creation"""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    initial_balance: float = Field(..., gt=0)
    currency: str = Field('USD', min_length=3, max_length=3)


class PortfolioUpdate(BaseModel):
    """Schema for portfolio update"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)


# Order schemas
class OrderCreate(BaseModel):
    """Schema for order creation"""
    
    symbol: str = Field(..., min_length=1, max_length=10)
    side: str = Field(..., regex=r'^(buy|sell)$')
    quantity: float = Field(..., gt=0)
    order_type: str = Field(..., regex=r'^(market|limit|stop|stop_limit)$')
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = Field('day', regex=r'^(day|gtc|ioc)$')
    broker: str = Field(..., regex=r'^(alpaca|interactive_brokers)$')
    
    @validator('price')
    def validate_price(cls, v, values):
        """Validate price"""
        if 'order_type' in values and values['order_type'] in ['limit', 'stop_limit'] and v is None:
            raise ValueError('Price is required for limit and stop-limit orders')
        return v
    
    @validator('stop_price')
    def validate_stop_price(cls, v, values):
        """Validate stop price"""
        if 'order_type' in values and values['order_type'] in ['stop', 'stop_limit'] and v is None:
            raise ValueError('Stop price is required for stop and stop-limit orders')
        return v


# Strategy schemas
class StrategyCreate(BaseModel):
    """Schema for strategy creation"""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: str = Field(..., regex=r'^(ml|rule_based|hybrid)$')
    config: Dict[str, Any] = Field(...)


class StrategyUpdate(BaseModel):
    """Schema for strategy update"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = Field(None, regex=r'^(ml|rule_based|hybrid)$')
    status: Optional[str] = Field(None, regex=r'^(active|inactive|backtest)$')
    config: Optional[Dict[str, Any]] = None


# Model schemas
class ModelCreate(BaseModel):
    """Schema for model creation"""
    
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., regex=r'^(lstm|transformer|reinforcement)$')
    config: Dict[str, Any] = Field(...)


class ModelUpdate(BaseModel):
    """Schema for model update"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, regex=r'^(lstm|transformer|reinforcement)$')
    status: Optional[str] = Field(None, regex=r'^(training|active|inactive)$')
    config: Optional[Dict[str, Any]] = None
    performance: Optional[Dict[str, Any]] = None
    registry_path: Optional[str] = None


# Signal schemas
class SignalCreate(BaseModel):
    """Schema for signal creation"""
    
    symbol: str = Field(..., min_length=1, max_length=10)
    direction: str = Field(..., regex=r'^(buy|sell)$')
    strength: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    expiration: Optional[datetime] = None


# API key schemas
class ApiKeyCreate(BaseModel):
    """Schema for API key creation"""
    
    name: str = Field(..., min_length=1, max_length=100)
    permissions: List[str] = Field(...)
    expires_at: Optional[datetime] = None


# Market data schemas
class MarketDataRequest(BaseModel):
    """Schema for market data request"""
    
    symbol: str = Field(..., min_length=1, max_length=10)
    timeframe: str = Field(..., regex=r'^(1m|5m|15m|30m|1h|4h|1d|1wk|1mo)$')
    period: Optional[str] = Field(None, regex=r'^(1d|1wk|1mo|3mo|6mo|1y|5y|max)$')
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        """Validate end date"""
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v


# Risk calculation schemas
class RiskMetricsRequest(BaseModel):
    """Schema for risk metrics request"""
    
    portfolio: List[Dict[str, Any]] = Field(...)
    risk_metrics: List[str] = Field(...)
    confidence_level: float = Field(0.95, ge=0, le=1)
    lookback_period: int = Field(252, ge=1)
    
    @validator('risk_metrics')
    def validate_risk_metrics(cls, v):
        """Validate risk metrics"""
        valid_metrics = ['var', 'cvar', 'sharpe', 'sortino', 'max_drawdown']
        for metric in v:
            if metric not in valid_metrics:
                raise ValueError(f'Invalid risk metric: {metric}')
        return v


class StressTestRequest(BaseModel):
    """Schema for stress test request"""
    
    portfolio: List[Dict[str, Any]] = Field(...)
    scenarios: List[str] = Field(...)
    
    @validator('scenarios')
    def validate_scenarios(cls, v):
        """Validate scenarios"""
        valid_scenarios = ['2008_crisis', 'covid_crash', 'rate_hike']
        for scenario in v:
            if scenario not in valid_scenarios:
                raise ValueError(f'Invalid scenario: {scenario}')
        return v


class PositionSizeRequest(BaseModel):
    """Schema for position size request"""
    
    symbol: str = Field(..., min_length=1, max_length=10)
    signal_strength: float = Field(..., ge=0, le=1)
    portfolio_value: float = Field(..., gt=0)
    risk_tolerance: str = Field(..., regex=r'^(low|medium|high)$')
    volatility: Optional[float] = Field(None, ge=0)


# Validation functions
def validate_schema(data: Dict[str, Any], schema_class: Type[BaseModel]) -> Dict[str, Any]:
    """Validate data against schema
    
    Args:
        data: Data to validate
        schema_class: Pydantic schema class
        
    Returns:
        Validated data
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        validated_data = schema_class(**data)
        return validated_data.dict()
    except ValidationError as e:
        error_details = {}
        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            error_details[field] = error['msg']
        
        raise ServiceValidationError(
            message="Validation error",
            details=error_details
        )

