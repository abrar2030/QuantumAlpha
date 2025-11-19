"""
Common utilities for QuantumAlpha services.
"""

from .auth import AuthManager, require_api_key, require_roles, validate_api_key
from .config import get_config_manager
from .database import Base, get_db_manager
from .logging_utils import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ServiceError,
    ValidationError,
    log_exceptions,
    setup_logger,
)
from .messaging import KafkaConsumer, KafkaProducer, MessageBus
from .models import (
    ApiKey,
    Execution,
    Model,
    Order,
    Portfolio,
    Position,
    Signal,
    Strategy,
    User,
)
from .utils import (
    RateLimiter,
    SimpleCache,
    ensure_directory,
    generate_api_key,
    hash_password,
    parse_period,
    parse_timeframe,
    timeframe_to_seconds,
    timeframe_to_timedelta,
    to_json_serializable,
    verify_password,
)
from .validation import validate_schema

__all__ = [
    "get_config_manager",
    "get_db_manager",
    "Base",
    "setup_logger",
    "ServiceError",
    "ValidationError",
    "NotFoundError",
    "AuthenticationError",
    "AuthorizationError",
    "log_exceptions",
    "AuthManager",
    "require_roles",
    "validate_api_key",
    "require_api_key",
    "KafkaProducer",
    "KafkaConsumer",
    "MessageBus",
    "User",
    "Portfolio",
    "Position",
    "Order",
    "Execution",
    "Strategy",
    "Model",
    "Signal",
    "ApiKey",
    "validate_schema",
    "hash_password",
    "verify_password",
    "parse_timeframe",
    "timeframe_to_seconds",
    "timeframe_to_timedelta",
    "parse_period",
    "to_json_serializable",
    "ensure_directory",
    "generate_api_key",
    "RateLimiter",
    "SimpleCache",
]
