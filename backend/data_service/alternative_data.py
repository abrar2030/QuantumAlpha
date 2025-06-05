"""
Alternative data service for QuantumAlpha Data Service.
Handles alternative data collection, processing, and retrieval.
"""
import os
import logging
import uuid
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import requests
from pymongo import MongoClient

# Add parent directory to path to import common modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import (
    setup_logger,
    ServiceError,
    ValidationError,
    NotFoundError,
    RateLimiter,
    SimpleCache
)

# Configure logging
logger = setup_logger('alternative_data_service', logging.INFO)

class AlternativeDataService:
    """Alternative data service"""
    
    def __init__(self, config_manager, db_manager):
        """Initialize alternative data service
        
        Args:
            config_manager: Configuration manager
            db_manager: Database manager
        """
        self.config_manager = config_manager
        self.db_manager = db_manager
        
        # Initialize data sources
        self.data_sources = {
            'news_api': {
                'api_key': config_manager.get('api_keys.news_api'),
                'base_url': 'https://newsapi.org/v2',
                'rate_limiter': RateLimiter(0.1)  # 1 call per 10 seconds
            },
            'twitter': {
                'api_key': config_manager.get('api_keys.twitter'),
                'base_url': 'https://api.twitter.com/2',
                'rate_limiter': RateLimiter(1.0)  # 1 call per second
            },
            'sec_filings': {
                'base_url': 'https://www.sec.gov/Archives/edgar/data',
                'rate_limiter': RateLimiter(0.1)  # 1 call per 10 seconds (SEC rate limit)
            }
        }
        
        # Initialize cache
        self.cache = SimpleCache(max_size=1000, ttl=300)  # 5 minutes TTL
        
        logger.info("Alternative data service initialized")
    
    def get_alternative_data(
        self,
        source: str,
        symbol: Optional[str] = None,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None
    ) -> Dict[str, Any]:
        """Get alternative data from a source
        
        Args:
            source: Data source (e.g., news, twitter, sec)
            symbol: Filter by symbol (optional)
            start_date: Start date (optional)
            end_date: End date (optional)
            
        Returns:
            Alternative data
            
        Raises:
            ValidationError: If parameters are invalid
            NotFoundError: If data is not found
            ServiceError: If there is an error getting data
        """
        logger.info(f"Getting alternative data from {source}")
        
        # Validate parameters
        if not source:
            raise ValidationError("Source is required")
        
        # Parse dates
        if start_date and isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        
        if end_date and isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=7)
        
        if not end_date:
            end_date = datetime.utcnow()
        
        # Check if data is in cache
        cache_key = f"alternative_data:{source}:{symbol or 'all'}:{start_date.isoformat()}:{end_date.isoformat()}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            logger.debug(f"Using cached data for {source}")
            return cached_data
        
        # Check if data is in database
        data = self._get_data_from_db(source, symbol, start_date, end_date)
        
        if data and len(data['data']) > 0:
            logger.debug(f"Using database data for {source}")
            self.cache.set(cache_key, data)
            return data
        
        # Get data from external source
        if source == 'news':
            data = self._get_data_from_news_api(symbol, start_date, end_date)
        elif source == 'twitter':
            data = self._get_data_from_twitter(symbol, start_date, end_date)
        elif source == 'sec':
            data = self._get_data_from_sec_filings(symbol, start_date, end_date)
        else:
            raise ValidationError(f"Unsupported data source: {source}")
        
        # Store data in database
        self._store_data_in_db(source, data)
        
        # Cache data
        self.cache.set(cache_key, data)
        
        return data
    
    def _get_data_from_db(
        self,
        source: str,
        symbol: Optional[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get alternative data from database
        
        Args:
            source: Data source
            symbol: Filter by symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            Alternative data
        """
        try:
            # Get MongoDB client
            mongodb_client = self.db_manager.get_mongodb_client()
            db = mongodb_client[self.config_manager.get('mongodb.database')]
            
            # Determine collection based on source
            collection_map = {
                'news': 'news',
                'twitter': 'social_media',
                'sec': 'sec_filings'
            }
            
            if source not in collection_map:
                return {
                    'source': source,
                    'data': []
                }
            
            collection = db[collection_map[source]]
            
            # Build query
            query = {
                'published_at': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
            
            if symbol:
                query['symbols'] = symbol
            
            # Execute query
            cursor = collection.find(query)
            
            # Process results
            data_points = []
            
            for document in cursor:
                # Remove MongoDB ID
                if '_id' in document:
                    del document['_id']
                
                data_points.append(document)
            
            # Sort by timestamp
            data_points.sort(key=lambda x: x['published_at'])
            
            return {
                'source': source,
                'data': data_points
            }
        
        except Exception as e:
            logger.error(f"Error getting data from database: {e}")
            return {
                'source': source,
                'data': []
            }
    
    def _store_data_in_db(self, source: str, data: Dict[str, Any]) -> None:
        """Store alternative data in database
        
        Args:
            source: Data source
            data: Alternative data to store
        """
        try:
            # Get MongoDB client
            mongodb_client = self.db_manager.get_mongodb_client()
            db = mongodb_client[self.config_manager.get('mongodb.database')]
            
            # Determine collection based on source
            collection_map = {
                'news': 'news',
                'twitter': 'social_media',
                'sec': 'sec_filings'
            }
            
            if source not in collection_map:
                logger.warning(f"Unsupported data source for database storage: {source}")
                return
            
            collection = db[collection_map[source]]
            
            # Process data points
            for point in data['data']:
                # Add created_at timestamp if not present
                if 'created_at' not in point:
                    point['created_at'] = datetime.utcnow()
                
                # Insert or update document
                collection.update_one(
                    {'url': point.get('url')} if 'url' in point else {'id': point.get('id')},
                    {'$set': point},
                    upsert=True
                )
            
            logger.debug(f"Stored {len(data['data'])} data points in database")
        
        except Exception as e:
            logger.error(f"Error storing data in database: {e}")
    
    def _get_data_from_news_api(
        self,
        symbol: Optional[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get news data from News API
        
        Args:
            symbol: Filter by symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            News data
            
        Raises:
            ServiceError: If there is an error getting data
        """
        try:
            # Check if API key is available
            if not self.data_sources['news_api']['api_key']:
                raise ServiceError("News API key not configured")
            
            # Apply rate limiting
            self.data_sources['news_api']['rate_limiter'].wait()
            
            # Build query
            query = symbol if symbol else "stock market OR finance OR investing"
            
            # Format dates
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Make request
            url = f"{self.data_sources['news_api']['base_url']}/everything"
            
            response = requests.get(url, params={
                'q': query,
                'from': start_date_str,
                'to': end_date_str,
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': self.data_sources['news_api']['api_key']
            })
            
            if response.status_code != 200:
                raise ServiceError(f"Error getting data from News API: {response.text}")
            
            # Parse response
            response_data = response.json()
            
            # Check for error
            if response_data.get('status') != 'ok':
                raise ServiceError(f"News API error: {response_data.get('message')}")
            
            # Process articles
            data_points = []
            
            for article in response_data.get('articles', []):
                # Parse published date
                published_at = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                
                # Extract symbols from title and description
                symbols = []
                if symbol:
                    symbols.append(symbol)
                
                # Create data point
                data_point = {
                    'headline': article['title'],
                    'source': article['source']['name'],
                    'url': article['url'],
                    'content': article['content'],
                    'symbols': symbols,
                    'published_at': published_at.isoformat(),
                    'created_at': datetime.utcnow().isoformat()
                }
                
                # Add sentiment analysis (placeholder)
                data_point['sentiment'] = 0.0
                
                data_points.append(data_point)
            
            return {
                'source': 'news',
                'data': data_points
            }
        
        except Exception as e:
            logger.error(f"Error getting data from News API: {e}")
            raise ServiceError(f"Error getting data from News API: {str(e)}")
    
    def _get_data_from_twitter(
        self,
        symbol: Optional[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get Twitter data
        
        Args:
            symbol: Filter by symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            Twitter data
            
        Raises:
            ServiceError: If there is an error getting data
        """
        # This is a placeholder implementation
        # In a real implementation, you would use the Twitter API
        
        logger.warning("Twitter API integration not implemented")
        
        # Return empty data
        return {
            'source': 'twitter',
            'data': []
        }
    
    def _get_data_from_sec_filings(
        self,
        symbol: Optional[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get SEC filings data
        
        Args:
            symbol: Filter by symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            SEC filings data
            
        Raises:
            ServiceError: If there is an error getting data
        """
        # This is a placeholder implementation
        # In a real implementation, you would use the SEC EDGAR API
        
        logger.warning("SEC filings API integration not implemented")
        
        # Return empty data
        return {
            'source': 'sec',
            'data': []
        }

