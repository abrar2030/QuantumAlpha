"""
Authentication and authorization utilities for QuantumAlpha services.
Provides JWT token generation, validation, and role-based access control.
"""
import os
import logging
import time
import jwt
from typing import Dict, Any, Optional, List, Callable
from functools import wraps
from .logging_utils import AuthenticationError, AuthorizationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AuthManager:
    """Manager for authentication and authorization"""
    
    def __init__(self, secret_key: str, token_expiry: int = 86400):
        """Initialize authentication manager
        
        Args:
            secret_key: Secret key for JWT token signing
            token_expiry: Token expiry time in seconds (default: 24 hours)
        """
        self.secret_key = secret_key
        self.token_expiry = token_expiry
        logger.info("Authentication manager initialized")
    
    def generate_token(self, user_id: str, username: str, role: str) -> str:
        """Generate a JWT token
        
        Args:
            user_id: User ID
            username: Username
            role: User role
            
        Returns:
            JWT token
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': int(time.time()) + self.token_expiry
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate a JWT token
        
        Args:
            token: JWT token
            
        Returns:
            Token payload
            
        Raises:
            AuthenticationError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    
    def check_role(self, token_payload: Dict[str, Any], required_roles: List[str]) -> bool:
        """Check if user has required role
        
        Args:
            token_payload: Token payload
            required_roles: List of required roles
            
        Returns:
            True if user has required role, False otherwise
        """
        user_role = token_payload.get('role')
        return user_role in required_roles


# Decorator for role-based access control
def require_roles(auth_manager: AuthManager, required_roles: List[str]) -> Callable:
    """Decorator for role-based access control
    
    Args:
        auth_manager: Authentication manager
        required_roles: List of required roles
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract token from request
            # This implementation is framework-agnostic
            # In a real implementation, you would extract the token from the request headers
            request = kwargs.get('request') or (args[0] if args else None)
            
            if not request:
                raise AuthenticationError("No request object found")
            
            # Extract token from Authorization header
            auth_header = getattr(request, 'headers', {}).get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                raise AuthenticationError("No valid Authorization header found")
            
            token = auth_header.split(' ')[1]
            
            # Validate token
            payload = auth_manager.validate_token(token)
            
            # Check role
            if not auth_manager.check_role(payload, required_roles):
                raise AuthorizationError("Insufficient permissions")
            
            # Add user info to request
            request.user = payload
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# API key authentication
def validate_api_key(api_key: str, valid_keys: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Validate an API key
    
    Args:
        api_key: API key
        valid_keys: Dictionary of valid API keys
        
    Returns:
        API key metadata
        
    Raises:
        AuthenticationError: If API key is invalid
    """
    if api_key not in valid_keys:
        raise AuthenticationError("Invalid API key")
    
    key_data = valid_keys[api_key]
    
    # Check if key is expired
    if 'expires_at' in key_data and key_data['expires_at'] < int(time.time()):
        raise AuthenticationError("API key has expired")
    
    return key_data


# Decorator for API key authentication
def require_api_key(valid_keys: Dict[str, Dict[str, Any]]) -> Callable:
    """Decorator for API key authentication
    
    Args:
        valid_keys: Dictionary of valid API keys
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract API key from request
            # This implementation is framework-agnostic
            # In a real implementation, you would extract the API key from the request headers
            request = kwargs.get('request') or (args[0] if args else None)
            
            if not request:
                raise AuthenticationError("No request object found")
            
            # Extract API key from X-API-Key header
            api_key = getattr(request, 'headers', {}).get('X-API-Key')
            if not api_key:
                raise AuthenticationError("No API key found")
            
            # Validate API key
            key_data = validate_api_key(api_key, valid_keys)
            
            # Add API key metadata to request
            request.api_key = key_data
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

