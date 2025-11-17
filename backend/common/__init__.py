"""
Common utilities for QuantumAlpha services.
"""

from .config import get_config_manager
from .database import get_db_manager, Base
from .logging_utils import (
    setup_logger,
    ServiceError,
    ValidationError,
    NotFoundError,
    AuthenticationError,
    AuthorizationError,
    log_exceptions,
)
from .auth import AuthManager, require_roles, validate_api_key, require_api_key
from .messaging import KafkaProducer, KafkaConsumer, MessageBus
from .models import (
    User,
    Portfolio,
    Position,
    Order,
    Execution,
    Strategy,
    Model,
    Signal,
    ApiKey,
)
from .validation import validate_schema
from .utils import (
    hash_password,
    verify_password,
    parse_timeframe,
    timeframe_to_seconds,
    timeframe_to_timedelta,
    parse_period,
    to_json_serializable,
    ensure_directory,
    generate_api_key,
    RateLimiter,
    SimpleCache,
)

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
