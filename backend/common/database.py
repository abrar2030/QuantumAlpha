"""
Database connection utilities for QuantumAlpha services.
Provides connections to PostgreSQL, InfluxDB, MongoDB, and Redis.
"""
import os
import logging
from typing import Dict, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from influxdb_client import InfluxDBClient
from pymongo import MongoClient
import redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

class DatabaseManager:
    """Manager for database connections"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize database connections
        
        Args:
            config: Configuration dictionary with database connection parameters
        """
        self.config = config
        self._postgres_engine = None
        self._postgres_session_factory = None
        self._influxdb_client = None
        self._mongodb_client = None
        self._redis_client = None
        
        logger.info("Database manager initialized")
    
    def get_postgres_session(self) -> Session:
        """Get a PostgreSQL session
        
        Returns:
            SQLAlchemy session
        """
        if self._postgres_engine is None:
            db_url = f"postgresql://{self.config['postgres']['username']}:{self.config['postgres']['password']}@{self.config['postgres']['host']}:{self.config['postgres']['port']}/{self.config['postgres']['database']}"
            self._postgres_engine = create_engine(db_url)
            self._postgres_session_factory = sessionmaker(bind=self._postgres_engine)
            logger.info("PostgreSQL engine initialized")
        
        return self._postgres_session_factory()
    
    def get_influxdb_client(self) -> InfluxDBClient:
        """Get an InfluxDB client
        
        Returns:
            InfluxDB client
        """
        if self._influxdb_client is None:
            self._influxdb_client = InfluxDBClient(
                url=self.config['influxdb']['url'],
                token=self.config['influxdb']['token'],
                org=self.config['influxdb']['org']
            )
            logger.info("InfluxDB client initialized")
        
        return self._influxdb_client
    
    def get_mongodb_client(self) -> MongoClient:
        """Get a MongoDB client
        
        Returns:
            MongoDB client
        """
        if self._mongodb_client is None:
            mongo_url = f"mongodb://{self.config['mongodb']['username']}:{self.config['mongodb']['password']}@{self.config['mongodb']['host']}:{self.config['mongodb']['port']}"
            self._mongodb_client = MongoClient(mongo_url)
            logger.info("MongoDB client initialized")
        
        return self._mongodb_client
    
    def get_redis_client(self) -> redis.Redis:
        """Get a Redis client
        
        Returns:
            Redis client
        """
        if self._redis_client is None:
            self._redis_client = redis.Redis(
                host=self.config['redis']['host'],
                port=self.config['redis']['port'],
                db=self.config['redis'].get('db', 0),
                password=self.config['redis'].get('password')
            )
            logger.info("Redis client initialized")
        
        return self._redis_client
    
    def create_tables(self) -> None:
        """Create all tables in PostgreSQL"""
        if self._postgres_engine is None:
            db_url = f"postgresql://{self.config['postgres']['username']}:{self.config['postgres']['password']}@{self.config['postgres']['host']}:{self.config['postgres']['port']}/{self.config['postgres']['database']}"
            self._postgres_engine = create_engine(db_url)
            logger.info("PostgreSQL engine initialized")
        
        Base.metadata.create_all(self._postgres_engine)
        logger.info("PostgreSQL tables created")
    
    def close_connections(self) -> None:
        """Close all database connections"""
        if self._influxdb_client is not None:
            self._influxdb_client.close()
            logger.info("InfluxDB connection closed")
        
        if self._mongodb_client is not None:
            self._mongodb_client.close()
            logger.info("MongoDB connection closed")
        
        if self._redis_client is not None:
            self._redis_client.close()
            logger.info("Redis connection closed")
        
        if self._postgres_engine is not None:
            self._postgres_engine.dispose()
            logger.info("PostgreSQL connection closed")


# Singleton instance
_db_manager: Optional[DatabaseManager] = None

def get_db_manager(config: Optional[Dict[str, Any]] = None) -> DatabaseManager:
    """Get the database manager singleton
    
    Args:
        config: Configuration dictionary with database connection parameters
        
    Returns:
        Database manager instance
    """
    global _db_manager
    if _db_manager is None:
        if config is None:
            raise ValueError("Config must be provided for first initialization")
        _db_manager = DatabaseManager(config)
    
    return _db_manager

