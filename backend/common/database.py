"""
Enhanced Database Configuration and Management for QuantumAlpha
Implements robust database connections, migrations, and performance optimization
"""

import os
import time
import threading
from contextlib import contextmanager
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError
import redis
from influxdb_client import InfluxDBClient
from pymongo import MongoClient
import structlog

logger = structlog.get_logger(__name__)

class DatabaseConfig:
    """Database configuration management"""
    
    def __init__(self):
        # PostgreSQL configuration
        self.postgres_url = self._build_postgres_url()
        
        # Redis configuration
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_password = os.getenv('REDIS_PASSWORD')
        
        # InfluxDB configuration (for time-series data)
        self.influx_url = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
        self.influx_token = os.getenv('INFLUXDB_TOKEN')
        self.influx_org = os.getenv('INFLUXDB_ORG', 'quantumalpha')
        self.influx_bucket = os.getenv('INFLUXDB_BUCKET', 'market_data')
        
        # MongoDB configuration (for document storage)
        self.mongo_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        self.mongo_db = os.getenv('MONGODB_DATABASE', 'quantumalpha')
        
        # Connection pool settings
        self.pool_size = int(os.getenv('DB_POOL_SIZE', 20))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', 30))
        self.pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', 30))
        self.pool_recycle = int(os.getenv('DB_POOL_RECYCLE', 3600))
        
    def _build_postgres_url(self) -> str:
        """Build PostgreSQL connection URL"""
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5432')
        database = os.getenv('POSTGRES_DB', 'quantumalpha')
        username = os.getenv('POSTGRES_USER', 'postgres')
        password = os.getenv('POSTGRES_PASSWORD', 'password')
        
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"

class DatabaseManager:
    """Enhanced database manager with connection pooling and monitoring"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._engine = None
        self._session_factory = None
        self._scoped_session = None
        self._redis_client = None
        self._influx_client = None
        self._mongo_client = None
        self._connection_stats = {
            'total_connections': 0,
            'active_connections': 0,
            'failed_connections': 0,
            'last_connection_time': None
        }
        self._lock = threading.Lock()
    
    def initialize(self):
        """Initialize all database connections"""
        try:
            self._setup_postgresql()
            self._setup_redis()
            self._setup_influxdb()
            self._setup_mongodb()
            logger.info("Database connections initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database connections: {e}")
            raise
    
    def _setup_postgresql(self):
        """Setup PostgreSQL connection with optimizations"""
        try:
            # Create engine with connection pooling
            self._engine = create_engine(
                self.config.postgres_url,
                poolclass=QueuePool,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=True,  # Validate connections before use
                echo=os.getenv('SQL_ECHO', 'false').lower() == 'true',
                connect_args={
                    "application_name": "QuantumAlpha",
                    "connect_timeout": 10,
                    "options": "-c timezone=UTC"
                }
            )
            
            # Setup session factory
            self._session_factory = sessionmaker(bind=self._engine)
            self._scoped_session = scoped_session(self._session_factory)
            
            # Register event listeners for monitoring
            self._register_postgresql_events()
            
            # Test connection
            with self._engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info("PostgreSQL connection established")
            
        except Exception as e:
            logger.error(f"Failed to setup PostgreSQL: {e}")
            raise
    
    def _register_postgresql_events(self):
        """Register SQLAlchemy event listeners for monitoring"""
        
        @event.listens_for(self._engine, "connect")
        def receive_connect(dbapi_connection, connection_record):
            with self._lock:
                self._connection_stats['total_connections'] += 1
                self._connection_stats['active_connections'] += 1
                self._connection_stats['last_connection_time'] = time.time()
        
        @event.listens_for(self._engine, "close")
        def receive_close(dbapi_connection, connection_record):
            with self._lock:
                self._connection_stats['active_connections'] -= 1
        
        @event.listens_for(self._engine, "handle_error")
        def receive_error(exception_context):
            with self._lock:
                self._connection_stats['failed_connections'] += 1
            logger.error(f"Database error: {exception_context.original_exception}")
    
    def _setup_redis(self):
        """Setup Redis connection with retry logic"""
        try:
            self._redis_client = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                password=self.config.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            self._redis_client.ping()
            logger.info("Redis connection established")
            
        except Exception as e:
            logger.error(f"Failed to setup Redis: {e}")
            # Redis is not critical, so we don't raise
    
    def _setup_influxdb(self):
        """Setup InfluxDB connection for time-series data"""
        try:
            if self.config.influx_token:
                self._influx_client = InfluxDBClient(
                    url=self.config.influx_url,
                    token=self.config.influx_token,
                    org=self.config.influx_org,
                    timeout=10000
                )
                
                # Test connection
                health = self._influx_client.health()
                if health.status == "pass":
                    logger.info("InfluxDB connection established")
                else:
                    logger.warning("InfluxDB health check failed")
            else:
                logger.info("InfluxDB token not provided, skipping connection")
                
        except Exception as e:
            logger.error(f"Failed to setup InfluxDB: {e}")
            # InfluxDB is not critical for basic operations
    
    def _setup_mongodb(self):
        """Setup MongoDB connection for document storage"""
        try:
            self._mongo_client = MongoClient(
                self.config.mongo_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test connection
            self._mongo_client.admin.command('ping')
            logger.info("MongoDB connection established")
            
        except Exception as e:
            logger.error(f"Failed to setup MongoDB: {e}")
            # MongoDB is not critical for basic operations
    
    @property
    def engine(self) -> Engine:
        """Get PostgreSQL engine"""
        if not self._engine:
            raise RuntimeError("Database not initialized")
        return self._engine
    
    @property
    def session_factory(self):
        """Get session factory"""
        if not self._session_factory:
            raise RuntimeError("Database not initialized")
        return self._session_factory
    
    @property
    def redis(self) -> Optional[redis.Redis]:
        """Get Redis client"""
        return self._redis_client
    
    @property
    def influx(self) -> Optional[InfluxDBClient]:
        """Get InfluxDB client"""
        return self._influx_client
    
    @property
    def mongo(self) -> Optional[MongoClient]:
        """Get MongoDB client"""
        return self._mongo_client
    
    def get_session(self):
        """Get a new database session"""
        if not self._scoped_session:
            raise RuntimeError("Database not initialized")
        return self._scoped_session()
    
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations"""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        with self._lock:
            stats = self._connection_stats.copy()
        
        # Add pool statistics if available
        if self._engine and hasattr(self._engine.pool, 'size'):
            stats.update({
                'pool_size': self._engine.pool.size(),
                'checked_in': self._engine.pool.checkedin(),
                'checked_out': self._engine.pool.checkedout(),
                'overflow': self._engine.pool.overflow(),
                'invalid': self._engine.pool.invalid()
            })
        
        return stats
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all database connections"""
        health_status = {
            'postgresql': {'status': 'unknown', 'error': None},
            'redis': {'status': 'unknown', 'error': None},
            'influxdb': {'status': 'unknown', 'error': None},
            'mongodb': {'status': 'unknown', 'error': None}
        }
        
        # Check PostgreSQL
        try:
            with self._engine.connect() as conn:
                conn.execute("SELECT 1")
            health_status['postgresql']['status'] = 'healthy'
        except Exception as e:
            health_status['postgresql']['status'] = 'unhealthy'
            health_status['postgresql']['error'] = str(e)
        
        # Check Redis
        if self._redis_client:
            try:
                self._redis_client.ping()
                health_status['redis']['status'] = 'healthy'
            except Exception as e:
                health_status['redis']['status'] = 'unhealthy'
                health_status['redis']['error'] = str(e)
        else:
            health_status['redis']['status'] = 'not_configured'
        
        # Check InfluxDB
        if self._influx_client:
            try:
                health = self._influx_client.health()
                health_status['influxdb']['status'] = 'healthy' if health.status == 'pass' else 'unhealthy'
            except Exception as e:
                health_status['influxdb']['status'] = 'unhealthy'
                health_status['influxdb']['error'] = str(e)
        else:
            health_status['influxdb']['status'] = 'not_configured'
        
        # Check MongoDB
        if self._mongo_client:
            try:
                self._mongo_client.admin.command('ping')
                health_status['mongodb']['status'] = 'healthy'
            except Exception as e:
                health_status['mongodb']['status'] = 'unhealthy'
                health_status['mongodb']['error'] = str(e)
        else:
            health_status['mongodb']['status'] = 'not_configured'
        
        return health_status
    
    def close_all_connections(self):
        """Close all database connections"""
        try:
            if self._scoped_session:
                self._scoped_session.remove()
            
            if self._engine:
                self._engine.dispose()
            
            if self._redis_client:
                self._redis_client.close()
            
            if self._influx_client:
                self._influx_client.close()
            
            if self._mongo_client:
                self._mongo_client.close()
            
            logger.info("All database connections closed")
            
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

class DatabaseMigrationManager:
    """Database migration management"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def create_tables(self):
        """Create all database tables"""
        try:
            from .models import Base, create_tables, init_database
            
            # Create tables
            create_tables(self.db_manager.engine)
            
            # Initialize with default data
            init_database(self.db_manager.engine)
            
            logger.info("Database tables created and initialized")
            
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def check_migration_status(self) -> Dict[str, Any]:
        """Check database migration status"""
        try:
            with self.db_manager.session_scope() as session:
                # Check if tables exist
                inspector = self.db_manager.engine.dialect.get_table_names(
                    self.db_manager.engine.connect()
                )
                
                required_tables = [
                    'users', 'user_sessions', 'audit_logs', 'portfolios',
                    'positions', 'orders', 'order_executions', 'strategies',
                    'risk_limits', 'compliance_rules', 'market_data'
                ]
                
                missing_tables = [table for table in required_tables if table not in inspector]
                
                return {
                    'tables_exist': len(missing_tables) == 0,
                    'missing_tables': missing_tables,
                    'total_tables': len(inspector)
                }
                
        except Exception as e:
            logger.error(f"Failed to check migration status: {e}")
            return {'error': str(e)}

# Global database manager instance
db_config = DatabaseConfig()
db_manager = DatabaseManager(db_config)
migration_manager = DatabaseMigrationManager(db_manager)

# Convenience functions
def get_db_session():
    """Get a database session"""
    return db_manager.get_session()

def get_redis_client():
    """Get Redis client"""
    return db_manager.redis

def get_influx_client():
    """Get InfluxDB client"""
    return db_manager.influx

def get_mongo_client():
    """Get MongoDB client"""
    return db_manager.mongo

@contextmanager
def db_session_scope():
    """Database session context manager"""
    with db_manager.session_scope() as session:
        yield session

# Database initialization function
def initialize_database():
    """Initialize all database connections"""
    try:
        db_manager.initialize()
        
        # Check if tables need to be created
        migration_status = migration_manager.check_migration_status()
        if not migration_status.get('tables_exist', False):
            logger.info("Creating database tables...")
            migration_manager.create_tables()
        
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

# Cleanup function
def cleanup_database():
    """Cleanup database connections"""
    db_manager.close_all_connections()

# Export main components
__all__ = [
    'DatabaseConfig',
    'DatabaseManager',
    'DatabaseMigrationManager',
    'db_manager',
    'migration_manager',
    'get_db_session',
    'get_redis_client',
    'get_influx_client',
    'get_mongo_client',
    'db_session_scope',
    'initialize_database',
    'cleanup_database'
]

