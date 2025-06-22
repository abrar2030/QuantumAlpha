"""
Comprehensive Input Validation Framework for QuantumAlpha
Implements robust validation, sanitization, and security controls for all inputs
"""

import re
import json
import html
import bleach
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional, Union, Callable
from functools import wraps
from flask import request, jsonify
from marshmallow import Schema, fields, validate, ValidationError, pre_load, post_load
from marshmallow.decorators import validates, validates_schema
import structlog

logger = structlog.get_logger(__name__)

class ValidationConfig:
    """Validation configuration constants"""
    
    # String limits
    MAX_STRING_LENGTH = 1000
    MAX_TEXT_LENGTH = 10000
    MAX_EMAIL_LENGTH = 255
    MAX_NAME_LENGTH = 100
    
    # Numeric limits
    MAX_DECIMAL_PLACES = 8
    MAX_PRICE = Decimal('1000000000')  # $1B max price
    MAX_QUANTITY = Decimal('1000000000')  # 1B max quantity
    MIN_PRICE = Decimal('0.0001')
    MIN_QUANTITY = Decimal('0.0001')
    
    # Security patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\s+['\"].*['\"])",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>.*?</iframe>",
    ]
    
    # Allowed HTML tags for rich text
    ALLOWED_HTML_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li']
    ALLOWED_HTML_ATTRIBUTES = {}

class ValidationError(Exception):
    """Custom validation exception"""
    def __init__(self, message: str, field: str = None, code: str = None):
        self.message = message
        self.field = field
        self.code = code
        super().__init__(message)

class SecurityValidator:
    """Security-focused input validation"""
    
    @staticmethod
    def check_sql_injection(value: str) -> bool:
        """Check for SQL injection patterns"""
        if not isinstance(value, str):
            return False
        
        value_lower = value.lower()
        for pattern in ValidationConfig.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value_lower, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def check_xss(value: str) -> bool:
        """Check for XSS patterns"""
        if not isinstance(value, str):
            return False
        
        for pattern in ValidationConfig.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False
    
    @staticmethod
    def sanitize_html(value: str) -> str:
        """Sanitize HTML content"""
        if not isinstance(value, str):
            return str(value)
        
        return bleach.clean(
            value,
            tags=ValidationConfig.ALLOWED_HTML_TAGS,
            attributes=ValidationConfig.ALLOWED_HTML_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def escape_html(value: str) -> str:
        """Escape HTML entities"""
        if not isinstance(value, str):
            return str(value)
        return html.escape(value)
    
    @staticmethod
    def validate_safe_string(value: str, field_name: str = "field") -> str:
        """Validate and sanitize a string for safety"""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        # Check for security threats
        if SecurityValidator.check_sql_injection(value):
            raise ValidationError(f"{field_name} contains potentially malicious content", code="sql_injection")
        
        if SecurityValidator.check_xss(value):
            raise ValidationError(f"{field_name} contains potentially malicious content", code="xss_attempt")
        
        # Sanitize and return
        return SecurityValidator.escape_html(value.strip())

class FinancialValidator:
    """Financial data validation"""
    
    @staticmethod
    def validate_price(value: Union[str, float, Decimal]) -> Decimal:
        """Validate and normalize price values"""
        try:
            if isinstance(value, str):
                # Remove currency symbols and whitespace
                cleaned = re.sub(r'[^\d.-]', '', value)
                price = Decimal(cleaned)
            else:
                price = Decimal(str(value))
            
            # Check bounds
            if price < ValidationConfig.MIN_PRICE:
                raise ValidationError(f"Price must be at least {ValidationConfig.MIN_PRICE}")
            
            if price > ValidationConfig.MAX_PRICE:
                raise ValidationError(f"Price cannot exceed {ValidationConfig.MAX_PRICE}")
            
            # Check decimal places
            if price.as_tuple().exponent < -ValidationConfig.MAX_DECIMAL_PLACES:
                raise ValidationError(f"Price cannot have more than {ValidationConfig.MAX_DECIMAL_PLACES} decimal places")
            
            return price
            
        except (InvalidOperation, ValueError) as e:
            raise ValidationError(f"Invalid price format: {value}")
    
    @staticmethod
    def validate_quantity(value: Union[str, float, Decimal]) -> Decimal:
        """Validate and normalize quantity values"""
        try:
            if isinstance(value, str):
                cleaned = re.sub(r'[^\d.-]', '', value)
                quantity = Decimal(cleaned)
            else:
                quantity = Decimal(str(value))
            
            # Check bounds
            if quantity <= 0:
                raise ValidationError("Quantity must be positive")
            
            if quantity > ValidationConfig.MAX_QUANTITY:
                raise ValidationError(f"Quantity cannot exceed {ValidationConfig.MAX_QUANTITY}")
            
            return quantity
            
        except (InvalidOperation, ValueError) as e:
            raise ValidationError(f"Invalid quantity format: {value}")
    
    @staticmethod
    def validate_symbol(value: str) -> str:
        """Validate stock symbol format"""
        if not isinstance(value, str):
            raise ValidationError("Symbol must be a string")
        
        symbol = value.upper().strip()
        
        # Basic symbol format validation
        if not re.match(r'^[A-Z]{1,10}$', symbol):
            raise ValidationError("Symbol must be 1-10 uppercase letters")
        
        return symbol
    
    @staticmethod
    def validate_currency(value: str) -> str:
        """Validate currency code"""
        if not isinstance(value, str):
            raise ValidationError("Currency must be a string")
        
        currency = value.upper().strip()
        
        # ISO 4217 currency code format
        if not re.match(r'^[A-Z]{3}$', currency):
            raise ValidationError("Currency must be a 3-letter ISO code")
        
        return currency

class UserValidator:
    """User data validation"""
    
    @staticmethod
    def validate_email(value: str) -> str:
        """Validate email format and security"""
        if not isinstance(value, str):
            raise ValidationError("Email must be a string")
        
        email = value.lower().strip()
        
        # Length check
        if len(email) > ValidationConfig.MAX_EMAIL_LENGTH:
            raise ValidationError(f"Email cannot exceed {ValidationConfig.MAX_EMAIL_LENGTH} characters")
        
        # Format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("Invalid email format")
        
        # Security check
        SecurityValidator.validate_safe_string(email, "email")
        
        return email
    
    @staticmethod
    def validate_password(value: str) -> str:
        """Validate password strength"""
        if not isinstance(value, str):
            raise ValidationError("Password must be a string")
        
        # Length check
        if len(value) < 12:
            raise ValidationError("Password must be at least 12 characters long")
        
        if len(value) > 128:
            raise ValidationError("Password cannot exceed 128 characters")
        
        # Complexity checks
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least one number")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character")
        
        # Common password check (simplified)
        common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
        if value.lower() in common_passwords:
            raise ValidationError("Password is too common")
        
        return value
    
    @staticmethod
    def validate_name(value: str) -> str:
        """Validate user name"""
        if not isinstance(value, str):
            raise ValidationError("Name must be a string")
        
        name = value.strip()
        
        # Length check
        if len(name) < 1:
            raise ValidationError("Name cannot be empty")
        
        if len(name) > ValidationConfig.MAX_NAME_LENGTH:
            raise ValidationError(f"Name cannot exceed {ValidationConfig.MAX_NAME_LENGTH} characters")
        
        # Character validation
        if not re.match(r'^[a-zA-Z\s\'-]+$', name):
            raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes")
        
        return SecurityValidator.validate_safe_string(name, "name")

# Marshmallow schemas for API validation
class BaseSchema(Schema):
    """Base schema with common validation"""
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        """Strip whitespace from string fields"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data
    
    @validates_schema
    def validate_security(self, data, **kwargs):
        """Validate data for security threats"""
        for field, value in data.items():
            if isinstance(value, str):
                try:
                    SecurityValidator.validate_safe_string(value, field)
                except ValidationError as e:
                    raise ValidationError({field: e.message})

class UserRegistrationSchema(BaseSchema):
    """User registration validation schema"""
    
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, validate=validate.Length(min=12, max=128))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    terms_accepted = fields.Bool(required=True)
    
    @validates('email')
    def validate_email_security(self, value):
        return UserValidator.validate_email(value)
    
    @validates('password')
    def validate_password_strength(self, value):
        return UserValidator.validate_password(value)
    
    @validates('name')
    def validate_name_format(self, value):
        return UserValidator.validate_name(value)
    
    @validates('terms_accepted')
    def validate_terms(self, value):
        if not value:
            raise ValidationError("Terms and conditions must be accepted")

class UserLoginSchema(BaseSchema):
    """User login validation schema"""
    
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    mfa_token = fields.Str(required=False, validate=validate.Length(equal=6))
    remember_me = fields.Bool(required=False, default=False)
    
    @validates('email')
    def validate_email_format(self, value):
        return UserValidator.validate_email(value)

class OrderSchema(BaseSchema):
    """Order validation schema"""
    
    symbol = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    side = fields.Str(required=True, validate=validate.OneOf(['buy', 'sell']))
    order_type = fields.Str(required=True, validate=validate.OneOf(['market', 'limit', 'stop', 'stop_limit']))
    quantity = fields.Decimal(required=True, places=8)
    price = fields.Decimal(required=False, places=8, allow_none=True)
    stop_price = fields.Decimal(required=False, places=8, allow_none=True)
    time_in_force = fields.Str(required=False, validate=validate.OneOf(['day', 'gtc', 'ioc', 'fok']), default='day')
    
    @validates('symbol')
    def validate_symbol_format(self, value):
        return FinancialValidator.validate_symbol(value)
    
    @validates('quantity')
    def validate_quantity_value(self, value):
        return FinancialValidator.validate_quantity(value)
    
    @validates('price')
    def validate_price_value(self, value):
        if value is not None:
            return FinancialValidator.validate_price(value)
    
    @validates('stop_price')
    def validate_stop_price_value(self, value):
        if value is not None:
            return FinancialValidator.validate_price(value)
    
    @validates_schema
    def validate_order_logic(self, data, **kwargs):
        """Validate order business logic"""
        order_type = data.get('order_type')
        price = data.get('price')
        stop_price = data.get('stop_price')
        
        if order_type in ['limit', 'stop_limit'] and price is None:
            raise ValidationError({'price': 'Price is required for limit orders'})
        
        if order_type in ['stop', 'stop_limit'] and stop_price is None:
            raise ValidationError({'stop_price': 'Stop price is required for stop orders'})
        
        if order_type == 'market' and price is not None:
            raise ValidationError({'price': 'Price should not be specified for market orders'})

class PortfolioSchema(BaseSchema):
    """Portfolio validation schema"""
    
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(required=False, validate=validate.Length(max=1000))
    initial_cash = fields.Decimal(required=True, places=2)
    max_position_size = fields.Decimal(required=False, places=4, allow_none=True)
    max_leverage = fields.Decimal(required=False, places=2, allow_none=True)
    
    @validates('name')
    def validate_name_security(self, value):
        return SecurityValidator.validate_safe_string(value, "name")
    
    @validates('description')
    def validate_description_security(self, value):
        if value:
            return SecurityValidator.validate_safe_string(value, "description")
    
    @validates('initial_cash')
    def validate_initial_cash_value(self, value):
        if value <= 0:
            raise ValidationError("Initial cash must be positive")
        if value > 1000000000:  # $1B limit
            raise ValidationError("Initial cash cannot exceed $1 billion")
        return value

# Validation decorators
def validate_json(schema_class: Schema):
    """Decorator to validate JSON request data"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Get JSON data
                if not request.is_json:
                    return jsonify({'error': 'Content-Type must be application/json'}), 400
                
                json_data = request.get_json()
                if json_data is None:
                    return jsonify({'error': 'Invalid JSON data'}), 400
                
                # Validate with schema
                schema = schema_class()
                validated_data = schema.load(json_data)
                
                # Add validated data to kwargs
                kwargs['validated_data'] = validated_data
                
                return func(*args, **kwargs)
                
            except ValidationError as e:
                logger.warning(f"Validation error: {e.messages}")
                return jsonify({
                    'error': 'Validation failed',
                    'details': e.messages
                }), 400
            except Exception as e:
                logger.error(f"Validation decorator error: {e}")
                return jsonify({'error': 'Internal validation error'}), 500
        
        return wrapper
    return decorator

def validate_query_params(**param_validators):
    """Decorator to validate query parameters"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validated_params = {}
                
                for param_name, validator in param_validators.items():
                    value = request.args.get(param_name)
                    
                    if value is not None:
                        if callable(validator):
                            validated_params[param_name] = validator(value)
                        else:
                            validated_params[param_name] = value
                
                kwargs['validated_params'] = validated_params
                return func(*args, **kwargs)
                
            except ValidationError as e:
                return jsonify({
                    'error': 'Query parameter validation failed',
                    'details': str(e)
                }), 400
            except Exception as e:
                logger.error(f"Query validation error: {e}")
                return jsonify({'error': 'Internal validation error'}), 500
        
        return wrapper
    return decorator

# Rate limiting validation
class RateLimitValidator:
    """Rate limiting for API endpoints"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """
        Check if rate limit is exceeded
        
        Args:
            key: Unique identifier for rate limiting
            limit: Maximum number of requests
            window: Time window in seconds
        
        Returns:
            True if within limit, False if exceeded
        """
        try:
            current = self.redis.get(key)
            if current is None:
                self.redis.setex(key, window, 1)
                return True
            
            if int(current) >= limit:
                return False
            
            self.redis.incr(key)
            return True
            
        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            return True  # Allow on error to avoid blocking legitimate requests

# Input sanitization utilities
def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    if not isinstance(filename, str):
        raise ValidationError("Filename must be a string")
    
    # Remove path traversal attempts
    filename = filename.replace('..', '').replace('/', '').replace('\\', '')
    
    # Keep only safe characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    if not filename:
        raise ValidationError("Invalid filename")
    
    return filename

def sanitize_search_query(query: str) -> str:
    """Sanitize search query"""
    if not isinstance(query, str):
        raise ValidationError("Search query must be a string")
    
    # Remove potentially dangerous characters
    query = re.sub(r'[<>"\';\\]', '', query)
    
    # Limit length
    if len(query) > 1000:
        query = query[:1000]
    
    return query.strip()

# Export validation functions and classes
__all__ = [
    'ValidationError',
    'SecurityValidator',
    'FinancialValidator',
    'UserValidator',
    'UserRegistrationSchema',
    'UserLoginSchema',
    'OrderSchema',
    'PortfolioSchema',
    'validate_json',
    'validate_query_params',
    'RateLimitValidator',
    'sanitize_filename',
    'sanitize_search_query'
]

