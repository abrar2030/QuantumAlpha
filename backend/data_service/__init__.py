"""
Data Service for QuantumAlpha
This service is responsible for:
1. Market data collection from various sources
2. Alternative data processing
3. Feature engineering
4. Data storage and retrieval
"""
from .market_data import MarketDataService
from .alternative_data import AlternativeDataService
from .feature_engineering import FeatureEngineeringService

__all__ = [
    'MarketDataService',
    'AlternativeDataService',
    'FeatureEngineeringService'
]

