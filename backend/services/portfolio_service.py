"""
Enhanced Portfolio Management Service for QuantumAlpha
Implements comprehensive portfolio tracking, risk management, and performance analytics
"""

import asyncio
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from .database import get_db_session, get_redis_client
from .models import Portfolio, Position, Order, OrderStatus, User, AuditAction
from .audit import audit_logger
from .validation import FinancialValidator
import structlog
import json
import numpy as np
import pandas as pd

logger = structlog.get_logger(__name__)

@dataclass
class PortfolioMetrics:
    """Portfolio performance metrics"""
    total_value: Decimal
    cash_balance: Decimal
    invested_amount: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    total_return: Decimal
    total_return_pct: Decimal
    day_change: Decimal
    day_change_pct: Decimal
    
    # Risk metrics
    var_1d: Optional[Decimal] = None
    var_5d: Optional[Decimal] = None
    max_drawdown: Optional[Decimal] = None
    sharpe_ratio: Optional[Decimal] = None
    beta: Optional[Decimal] = None
    volatility: Optional[Decimal] = None
    
    # Allocation metrics
    sector_allocation: Optional[Dict[str, Decimal]] = None
    country_allocation: Optional[Dict[str, Decimal]] = None
    currency_allocation: Optional[Dict[str, Decimal]] = None

@dataclass
class PositionMetrics:
    """Individual position metrics"""
    symbol: str
    quantity: Decimal
    avg_cost: Decimal
    current_price: Decimal
    market_value: Decimal
    unrealized_pnl: Decimal
    unrealized_pnl_pct: Decimal
    weight: Decimal
    day_change: Decimal
    day_change_pct: Decimal
    
    # Risk metrics
    position_var: Optional[Decimal] = None
    position_beta: Optional[Decimal] = None
    
    # Metadata
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    currency: str = 'USD'

class RiskCalculator:
    """Portfolio risk calculation engine"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
    
    def calculate_var(self, returns: List[float], confidence_level: float = 0.05) -> float:
        """Calculate Value at Risk using historical simulation"""
        if not returns or len(returns) < 30:
            return 0.0
        
        returns_array = np.array(returns)
        return float(np.percentile(returns_array, confidence_level * 100))
    
    def calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        if not returns or len(returns) < 2:
            return 0.0
        
        returns_array = np.array(returns)
        excess_returns = returns_array - (risk_free_rate / 252)  # Daily risk-free rate
        
        if np.std(excess_returns) == 0:
            return 0.0
        
        return float(np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252))
    
    def calculate_max_drawdown(self, values: List[float]) -> float:
        """Calculate maximum drawdown"""
        if not values or len(values) < 2:
            return 0.0
        
        values_array = np.array(values)
        peak = np.maximum.accumulate(values_array)
        drawdown = (values_array - peak) / peak
        return float(np.min(drawdown))
    
    def calculate_beta(self, portfolio_returns: List[float], market_returns: List[float]) -> float:
        """Calculate portfolio beta against market"""
        if not portfolio_returns or not market_returns or len(portfolio_returns) != len(market_returns):
            return 1.0
        
        portfolio_array = np.array(portfolio_returns)
        market_array = np.array(market_returns)
        
        covariance = np.cov(portfolio_array, market_array)[0][1]
        market_variance = np.var(market_array)
        
        if market_variance == 0:
            return 1.0
        
        return float(covariance / market_variance)
    
    def calculate_volatility(self, returns: List[float]) -> float:
        """Calculate annualized volatility"""
        if not returns or len(returns) < 2:
            return 0.0
        
        returns_array = np.array(returns)
        return float(np.std(returns_array) * np.sqrt(252))

class MarketDataService:
    """Market data service for real-time pricing"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.cache_ttl = 60  # 1 minute cache
    
    async def get_current_price(self, symbol: str) -> Optional[Decimal]:
        """Get current market price for a symbol"""
        try:
            # Try cache first
            if self.redis_client:
                cached_price = self.redis_client.get(f"price:{symbol}")
                if cached_price:
                    return Decimal(cached_price)
            
            # Fetch from market data provider (mock implementation)
            price = await self._fetch_market_price(symbol)
            
            # Cache the result
            if self.redis_client and price:
                self.redis_client.setex(f"price:{symbol}", self.cache_ttl, str(price))
            
            return price
            
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    async def _fetch_market_price(self, symbol: str) -> Optional[Decimal]:
        """Fetch price from market data provider (mock implementation)"""
        # This would integrate with real market data providers
        # For now, return mock data
        mock_prices = {
            'AAPL': Decimal('175.50'),
            'GOOGL': Decimal('142.80'),
            'MSFT': Decimal('420.15'),
            'TSLA': Decimal('245.30'),
            'AMZN': Decimal('155.75'),
            'NVDA': Decimal('875.25'),
            'META': Decimal('485.60'),
            'SPY': Decimal('485.20')
        }
        
        # Simulate some price movement
        base_price = mock_prices.get(symbol, Decimal('100.00'))
        import random
        change_pct = Decimal(str(random.uniform(-0.02, 0.02)))  # ±2% random change
        return base_price * (1 + change_pct)
    
    async def get_historical_prices(self, symbol: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical price data"""
        try:
            # This would fetch from historical data provider
            # For now, generate mock historical data
            current_price = await self.get_current_price(symbol)
            if not current_price:
                return []
            
            historical_data = []
            for i in range(days):
                date = datetime.now(timezone.utc) - timedelta(days=days-i)
                # Generate realistic price movement
                import random
                change = random.uniform(-0.05, 0.05)  # ±5% daily change
                price = current_price * Decimal(str(1 + change))
                
                historical_data.append({
                    'date': date.date().isoformat(),
                    'close': float(price),
                    'volume': random.randint(1000000, 50000000)
                })
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return []

class PortfolioService:
    """Enhanced portfolio management service"""
    
    def __init__(self):
        self.market_data = MarketDataService()
        self.risk_calculator = RiskCalculator()
        self.redis_client = get_redis_client()
    
    def create_portfolio(self, user_id: int, name: str, description: str = None, 
                        initial_cash: Decimal = Decimal('100000')) -> Portfolio:
        """Create a new portfolio"""
        try:
            with get_db_session() as session:
                # Validate inputs
                name = FinancialValidator.validate_safe_string(name, "portfolio name")
                if description:
                    description = FinancialValidator.validate_safe_string(description, "description")
                
                # Create portfolio
                portfolio = Portfolio(
                    user_id=user_id,
                    name=name,
                    description=description,
                    total_value=initial_cash,
                    cash_balance=initial_cash,
                    invested_amount=Decimal('0'),
                    unrealized_pnl=Decimal('0'),
                    realized_pnl=Decimal('0'),
                    created_by=user_id
                )
                
                session.add(portfolio)
                session.commit()
                session.refresh(portfolio)
                
                # Log audit event
                audit_logger.log_event(
                    action=AuditAction.CREATE,
                    resource_type='portfolio',
                    resource_id=str(portfolio.id),
                    new_values=portfolio.to_dict(),
                    user_id=user_id
                )
                
                logger.info(f"Portfolio created: {portfolio.id} for user {user_id}")
                return portfolio
                
        except Exception as e:
            logger.error(f"Error creating portfolio: {e}")
            raise
    
    def get_portfolio(self, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        """Get portfolio by ID with user authorization"""
        try:
            with get_db_session() as session:
                portfolio = session.query(Portfolio).filter(
                    and_(
                        Portfolio.id == portfolio_id,
                        Portfolio.user_id == user_id,
                        Portfolio.is_deleted == False
                    )
                ).first()
                
                if portfolio:
                    # Log access
                    audit_logger.log_event(
                        action=AuditAction.READ,
                        resource_type='portfolio',
                        resource_id=str(portfolio.id),
                        user_id=user_id
                    )
                
                return portfolio
                
        except Exception as e:
            logger.error(f"Error getting portfolio {portfolio_id}: {e}")
            return None
    
    def get_user_portfolios(self, user_id: int) -> List[Portfolio]:
        """Get all portfolios for a user"""
        try:
            with get_db_session() as session:
                portfolios = session.query(Portfolio).filter(
                    and_(
                        Portfolio.user_id == user_id,
                        Portfolio.is_deleted == False
                    )
                ).order_by(Portfolio.created_at.desc()).all()
                
                return portfolios
                
        except Exception as e:
            logger.error(f"Error getting portfolios for user {user_id}: {e}")
            return []
    
    async def calculate_portfolio_metrics(self, portfolio_id: int) -> Optional[PortfolioMetrics]:
        """Calculate comprehensive portfolio metrics"""
        try:
            with get_db_session() as session:
                portfolio = session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
                if not portfolio:
                    return None
                
                positions = session.query(Position).filter(
                    Position.portfolio_id == portfolio_id
                ).all()
                
                # Update position prices
                await self._update_position_prices(positions)
                
                # Calculate basic metrics
                total_market_value = Decimal('0')
                total_unrealized_pnl = Decimal('0')
                
                for position in positions:
                    if position.current_price and position.quantity:
                        market_value = position.current_price * abs(position.quantity)
                        total_market_value += market_value
                        
                        cost_basis = position.avg_cost * abs(position.quantity)
                        unrealized_pnl = market_value - cost_basis
                        total_unrealized_pnl += unrealized_pnl
                        
                        # Update position in database
                        position.market_value = market_value
                        position.unrealized_pnl = unrealized_pnl
                
                # Calculate portfolio totals
                total_value = portfolio.cash_balance + total_market_value
                invested_amount = total_market_value
                total_return = total_unrealized_pnl + portfolio.realized_pnl
                total_return_pct = (total_return / portfolio.cash_balance * 100) if portfolio.cash_balance > 0 else Decimal('0')
                
                # Get historical data for risk calculations
                historical_returns = await self._get_portfolio_returns(portfolio_id, days=252)
                
                # Calculate risk metrics
                var_1d = None
                var_5d = None
                max_drawdown = None
                sharpe_ratio = None
                volatility = None
                
                if historical_returns:
                    var_1d = Decimal(str(self.risk_calculator.calculate_var(historical_returns, 0.05)))
                    var_5d = Decimal(str(self.risk_calculator.calculate_var(historical_returns, 0.01)))
                    sharpe_ratio = Decimal(str(self.risk_calculator.calculate_sharpe_ratio(historical_returns)))
                    volatility = Decimal(str(self.risk_calculator.calculate_volatility(historical_returns)))
                    
                    # Get historical portfolio values for max drawdown
                    historical_values = await self._get_portfolio_values(portfolio_id, days=252)
                    if historical_values:
                        max_drawdown = Decimal(str(self.risk_calculator.calculate_max_drawdown(historical_values)))
                
                # Calculate allocations
                sector_allocation = self._calculate_sector_allocation(positions)
                country_allocation = self._calculate_country_allocation(positions)
                currency_allocation = self._calculate_currency_allocation(positions)
                
                # Update portfolio in database
                portfolio.total_value = total_value
                portfolio.invested_amount = invested_amount
                portfolio.unrealized_pnl = total_unrealized_pnl
                portfolio.var_1d = var_1d
                portfolio.var_5d = var_5d
                portfolio.max_drawdown = max_drawdown
                portfolio.sharpe_ratio = sharpe_ratio
                
                session.commit()
                
                return PortfolioMetrics(
                    total_value=total_value,
                    cash_balance=portfolio.cash_balance,
                    invested_amount=invested_amount,
                    unrealized_pnl=total_unrealized_pnl,
                    realized_pnl=portfolio.realized_pnl,
                    total_return=total_return,
                    total_return_pct=total_return_pct,
                    day_change=Decimal('0'),  # Would calculate from previous day
                    day_change_pct=Decimal('0'),
                    var_1d=var_1d,
                    var_5d=var_5d,
                    max_drawdown=max_drawdown,
                    sharpe_ratio=sharpe_ratio,
                    volatility=volatility,
                    sector_allocation=sector_allocation,
                    country_allocation=country_allocation,
                    currency_allocation=currency_allocation
                )
                
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {e}")
            return None
    
    async def _update_position_prices(self, positions: List[Position]):
        """Update current prices for all positions"""
        for position in positions:
            try:
                current_price = await self.market_data.get_current_price(position.symbol)
                if current_price:
                    position.current_price = current_price
            except Exception as e:
                logger.error(f"Error updating price for {position.symbol}: {e}")
    
    async def _get_portfolio_returns(self, portfolio_id: int, days: int = 252) -> List[float]:
        """Get historical portfolio returns"""
        try:
            # This would fetch from historical data storage
            # For now, generate mock returns
            import random
            returns = []
            for _ in range(days):
                daily_return = random.gauss(0.0008, 0.02)  # Mean 0.08% daily, 2% volatility
                returns.append(daily_return)
            return returns
        except Exception as e:
            logger.error(f"Error getting portfolio returns: {e}")
            return []
    
    async def _get_portfolio_values(self, portfolio_id: int, days: int = 252) -> List[float]:
        """Get historical portfolio values"""
        try:
            # This would fetch from historical data storage
            # For now, generate mock values
            import random
            base_value = 100000.0
            values = [base_value]
            
            for _ in range(days - 1):
                change = random.gauss(0.0008, 0.02)
                new_value = values[-1] * (1 + change)
                values.append(new_value)
            
            return values
        except Exception as e:
            logger.error(f"Error getting portfolio values: {e}")
            return []
    
    def _calculate_sector_allocation(self, positions: List[Position]) -> Dict[str, Decimal]:
        """Calculate sector allocation percentages"""
        sector_values = {}
        total_value = Decimal('0')
        
        for position in positions:
            if position.market_value and position.sector:
                sector = position.sector
                if sector not in sector_values:
                    sector_values[sector] = Decimal('0')
                sector_values[sector] += position.market_value
                total_value += position.market_value
        
        # Convert to percentages
        if total_value > 0:
            return {sector: (value / total_value * 100) for sector, value in sector_values.items()}
        return {}
    
    def _calculate_country_allocation(self, positions: List[Position]) -> Dict[str, Decimal]:
        """Calculate country allocation percentages"""
        country_values = {}
        total_value = Decimal('0')
        
        for position in positions:
            if position.market_value and position.country:
                country = position.country
                if country not in country_values:
                    country_values[country] = Decimal('0')
                country_values[country] += position.market_value
                total_value += position.market_value
        
        # Convert to percentages
        if total_value > 0:
            return {country: (value / total_value * 100) for country, value in country_values.items()}
        return {}
    
    def _calculate_currency_allocation(self, positions: List[Position]) -> Dict[str, Decimal]:
        """Calculate currency allocation percentages"""
        currency_values = {}
        total_value = Decimal('0')
        
        for position in positions:
            if position.market_value:
                currency = position.currency or 'USD'
                if currency not in currency_values:
                    currency_values[currency] = Decimal('0')
                currency_values[currency] += position.market_value
                total_value += position.market_value
        
        # Convert to percentages
        if total_value > 0:
            return {currency: (value / total_value * 100) for currency, value in currency_values.items()}
        return {}
    
    def add_position(self, portfolio_id: int, symbol: str, quantity: Decimal, 
                    avg_cost: Decimal, user_id: int) -> Optional[Position]:
        """Add or update a position in the portfolio"""
        try:
            with get_db_session() as session:
                # Validate inputs
                symbol = FinancialValidator.validate_symbol(symbol)
                quantity = FinancialValidator.validate_quantity(quantity)
                avg_cost = FinancialValidator.validate_price(avg_cost)
                
                # Check if position already exists
                existing_position = session.query(Position).filter(
                    and_(
                        Position.portfolio_id == portfolio_id,
                        Position.symbol == symbol
                    )
                ).first()
                
                if existing_position:
                    # Update existing position (weighted average cost)
                    old_value = existing_position.quantity * existing_position.avg_cost
                    new_value = quantity * avg_cost
                    total_quantity = existing_position.quantity + quantity
                    
                    if total_quantity != 0:
                        new_avg_cost = (old_value + new_value) / total_quantity
                        existing_position.quantity = total_quantity
                        existing_position.avg_cost = new_avg_cost
                        position = existing_position
                    else:
                        # Position closed
                        session.delete(existing_position)
                        position = None
                else:
                    # Create new position
                    position = Position(
                        portfolio_id=portfolio_id,
                        symbol=symbol,
                        quantity=quantity,
                        avg_cost=avg_cost,
                        currency='USD',  # Default currency
                        created_by=user_id
                    )
                    session.add(position)
                
                session.commit()
                
                if position:
                    session.refresh(position)
                    
                    # Log audit event
                    audit_logger.log_event(
                        action=AuditAction.CREATE if not existing_position else AuditAction.UPDATE,
                        resource_type='position',
                        resource_id=str(position.id),
                        new_values=position.to_dict(),
                        user_id=user_id
                    )
                
                return position
                
        except Exception as e:
            logger.error(f"Error adding position: {e}")
            raise
    
    def get_portfolio_positions(self, portfolio_id: int) -> List[Position]:
        """Get all positions for a portfolio"""
        try:
            with get_db_session() as session:
                positions = session.query(Position).filter(
                    Position.portfolio_id == portfolio_id
                ).all()
                
                return positions
                
        except Exception as e:
            logger.error(f"Error getting positions for portfolio {portfolio_id}: {e}")
            return []
    
    async def get_position_metrics(self, position_id: int) -> Optional[PositionMetrics]:
        """Get detailed metrics for a specific position"""
        try:
            with get_db_session() as session:
                position = session.query(Position).filter(Position.id == position_id).first()
                if not position:
                    return None
                
                # Get current price
                current_price = await self.market_data.get_current_price(position.symbol)
                if not current_price:
                    current_price = position.current_price or position.avg_cost
                
                # Calculate metrics
                market_value = current_price * abs(position.quantity)
                cost_basis = position.avg_cost * abs(position.quantity)
                unrealized_pnl = market_value - cost_basis
                unrealized_pnl_pct = (unrealized_pnl / cost_basis * 100) if cost_basis > 0 else Decimal('0')
                
                # Get portfolio total value for weight calculation
                portfolio = session.query(Portfolio).filter(Portfolio.id == position.portfolio_id).first()
                weight = (market_value / portfolio.total_value * 100) if portfolio and portfolio.total_value > 0 else Decimal('0')
                
                return PositionMetrics(
                    symbol=position.symbol,
                    quantity=position.quantity,
                    avg_cost=position.avg_cost,
                    current_price=current_price,
                    market_value=market_value,
                    unrealized_pnl=unrealized_pnl,
                    unrealized_pnl_pct=unrealized_pnl_pct,
                    weight=weight,
                    day_change=Decimal('0'),  # Would calculate from previous day
                    day_change_pct=Decimal('0'),
                    sector=position.sector,
                    industry=position.industry,
                    country=position.country,
                    currency=position.currency
                )
                
        except Exception as e:
            logger.error(f"Error getting position metrics: {e}")
            return None

# Global portfolio service instance
portfolio_service = PortfolioService()

# Export main components
__all__ = [
    'PortfolioService',
    'PortfolioMetrics',
    'PositionMetrics',
    'RiskCalculator',
    'MarketDataService',
    'portfolio_service'
]

