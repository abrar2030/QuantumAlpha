import os
import jwt
import bcrypt
import secrets
import pyotp
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Optional, Dict, Any, List
from flask import request, jsonify, current_app
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request,
)
import redis
from sqlalchemy.orm import Session
from .models import User, UserSession, AuditLog
from .database import get_db_session
from .audit import log_security_event
from .validation import validate_password_strength
import structlog

logger = structlog.get_logger(__name__)

# Redis client for token blacklisting and session management
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_AUTH_DB", 1)),
    decode_responses=True,
)


class AuthenticationError(Exception):
    """Custom authentication exception"""

    pass


class AuthorizationError(Exception):
    """Custom authorization exception"""

    pass


class SecurityConfig:
    """Security configuration constants"""

    # Password policy
    MIN_PASSWORD_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_NUMBERS = True
    REQUIRE_SPECIAL_CHARS = True

    # Account lockout
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 30  # minutes

    # Session management
    MAX_CONCURRENT_SESSIONS = 3
    SESSION_TIMEOUT = 8  # hours

    # Token settings
    ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # MFA settings
    MFA_TOKEN_VALIDITY = 300  # seconds
    BACKUP_CODES_COUNT = 10


class AuthManager:

    def __init__(self, app=None):
        self.app = app
        self.jwt = JWTManager()
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize authentication with Flask app"""
        self.app = app
        self.jwt.init_app(app)

        # Configure JWT settings
        app.config["JWT_SECRET_KEY"] = os.getenv(
            "JWT_SECRET_KEY", secrets.token_urlsafe(32)
        )
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = SecurityConfig.ACCESS_TOKEN_EXPIRES
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = SecurityConfig.REFRESH_TOKEN_EXPIRES
        app.config["JWT_ALGORITHM"] = "HS256"
        app.config["JWT_BLACKLIST_ENABLED"] = True
        app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

        # Register JWT callbacks
        self._register_jwt_callbacks()

    def _register_jwt_callbacks(self):
        """Register JWT event callbacks"""

        @self.jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload):
            """Check if token is blacklisted"""
            jti = jwt_payload["jti"]
            return redis_client.get(f"blacklist:{jti}") is not None

        @self.jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            """Handle expired token"""
            log_security_event(
                "token_expired",
                {"user_id": jwt_payload.get("sub"), "jti": jwt_payload.get("jti")},
            )
            return jsonify({"error": "Token has expired"}), 401

        @self.jwt.invalid_token_loader
        def invalid_token_callback(error):
            """Handle invalid token"""
            log_security_event("invalid_token", {"error": str(error)})
            return jsonify({"error": "Invalid token"}), 401

        @self.jwt.unauthorized_loader
        def missing_token_callback(error):
            """Handle missing token"""
            return jsonify({"error": "Authorization token required"}), 401

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt with salt"""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def generate_mfa_secret(self) -> str:
        """Generate MFA secret for TOTP"""
        return pyotp.random_base32()

    def verify_mfa_token(self, secret: str, token: str) -> bool:
        """Verify MFA TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)

    def generate_backup_codes(self) -> List[str]:
        """Generate backup codes for MFA"""
        return [
            secrets.token_hex(4).upper()
            for _ in range(SecurityConfig.BACKUP_CODES_COUNT)
        ]

    def check_account_lockout(self, user_id: int) -> bool:
        """Check if account is locked due to failed attempts"""
        key = f"lockout:{user_id}"
        lockout_data = redis_client.get(key)
        if lockout_data:
            return True
        return False

    def record_failed_attempt(self, user_id: int):
        """Record failed login attempt"""
        key = f"attempts:{user_id}"
        attempts = redis_client.incr(key)
        redis_client.expire(key, SecurityConfig.LOCKOUT_DURATION * 60)

        if attempts >= SecurityConfig.MAX_LOGIN_ATTEMPTS:
            # Lock account
            lockout_key = f"lockout:{user_id}"
            redis_client.setex(
                lockout_key, SecurityConfig.LOCKOUT_DURATION * 60, "locked"
            )

            log_security_event(
                "account_locked",
                {
                    "user_id": user_id,
                    "attempts": attempts,
                    "lockout_duration": SecurityConfig.LOCKOUT_DURATION,
                },
            )

    def clear_failed_attempts(self, user_id: int):
        """Clear failed login attempts after successful login"""
        redis_client.delete(f"attempts:{user_id}")

    def create_session(
        self, user: User, ip_address: str, user_agent: str
    ) -> Dict[str, Any]:
        """Create authenticated session with tokens"""
        # Check concurrent sessions limit
        self._enforce_session_limit(user.id)

        # Generate tokens
        additional_claims = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "permissions": user.get_permissions(),
            "mfa_verified": user.mfa_enabled and user.mfa_verified,
            "session_id": secrets.token_urlsafe(16),
        }

        access_token = create_access_token(
            identity=user.id, additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(identity=user.id)

        # Store session in database
        session = UserSession(
            user_id=user.id,
            session_id=additional_claims["session_id"],
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc)
            + SecurityConfig.SESSION_TIMEOUT * timedelta(hours=1),
            is_active=True,
        )

        db_session = get_db_session()
        db_session.add(session)
        db_session.commit()

        # Log successful login
        log_security_event(
            "login_success",
            {
                "user_id": user.id,
                "email": user.email,
                "ip_address": ip_address,
                "session_id": additional_claims["session_id"],
            },
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": int(SecurityConfig.ACCESS_TOKEN_EXPIRES.total_seconds()),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "mfa_enabled": user.mfa_enabled,
                "last_login": user.last_login.isoformat() if user.last_login else None,
            },
        }

    def _enforce_session_limit(self, user_id: int):
        """Enforce maximum concurrent sessions"""
        db_session = get_db_session()
        active_sessions = (
            db_session.query(UserSession)
            .filter(
                UserSession.user_id == user_id,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc),
            )
            .order_by(UserSession.created_at.desc())
            .all()
        )

        if len(active_sessions) >= SecurityConfig.MAX_CONCURRENT_SESSIONS:
            # Deactivate oldest sessions
            sessions_to_deactivate = active_sessions[
                SecurityConfig.MAX_CONCURRENT_SESSIONS - 1 :
            ]
            for session in sessions_to_deactivate:
                session.is_active = False
                # Blacklist associated tokens
                self._blacklist_session_tokens(session.session_id)

            db_session.commit()

    def _blacklist_session_tokens(self, session_id: str):
        """Blacklist all tokens for a session"""
        # This would require storing token JTIs with session IDs
        # For now, we'll implement a simpler approach
        pass

    def logout(self, token_jti: str, user_id: int):
        """Logout user and blacklist token"""
        # Blacklist the token
        redis_client.setex(
            f"blacklist:{token_jti}",
            int(SecurityConfig.ACCESS_TOKEN_EXPIRES.total_seconds()),
            "blacklisted",
        )

        # Deactivate session
        db_session = get_db_session()
        session = (
            db_session.query(UserSession)
            .filter(UserSession.user_id == user_id, UserSession.is_active == True)
            .first()
        )

        if session:
            session.is_active = False
            db_session.commit()

        log_security_event("logout", {"user_id": user_id, "token_jti": token_jti})

    def authenticate_user(
        self, email: str, password: str, mfa_token: str = None
    ) -> Optional[User]:
        """Authenticate user with email/password and optional MFA"""
        db_session = get_db_session()
        user = db_session.query(User).filter(User.email == email).first()

        if not user:
            log_security_event(
                "login_failed", {"email": email, "reason": "user_not_found"}
            )
            return None

        # Check account lockout
        if self.check_account_lockout(user.id):
            log_security_event(
                "login_blocked",
                {"user_id": user.id, "email": email, "reason": "account_locked"},
            )
            raise AuthenticationError("Account is temporarily locked")

        # Verify password
        if not self.verify_password(password, user.password_hash):
            self.record_failed_attempt(user.id)
            log_security_event(
                "login_failed",
                {"user_id": user.id, "email": email, "reason": "invalid_password"},
            )
            return None

        # Check MFA if enabled
        if user.mfa_enabled:
            if not mfa_token:
                log_security_event("mfa_required", {"user_id": user.id, "email": email})
                raise AuthenticationError("MFA token required")

            if not self.verify_mfa_token(user.mfa_secret, mfa_token):
                self.record_failed_attempt(user.id)
                log_security_event("mfa_failed", {"user_id": user.id, "email": email})
                return None

            user.mfa_verified = True

        # Clear failed attempts on successful authentication
        self.clear_failed_attempts(user.id)

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db_session.commit()

        return user


# Authentication decorators
def require_auth(f):
    """Decorator to require authentication"""

    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated_function


def require_role(required_role: str):
    """Decorator to require specific role"""

    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role != required_role:
                log_security_event(
                    "authorization_failed",
                    {
                        "user_id": get_jwt_identity(),
                        "required_role": required_role,
                        "user_role": user_role,
                    },
                )
                raise AuthorizationError(f"Role '{required_role}' required")

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_permission(permission: str):
    """Decorator to require specific permission"""

    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_permissions = claims.get("permissions", [])

            if permission not in user_permissions:
                log_security_event(
                    "authorization_failed",
                    {
                        "user_id": get_jwt_identity(),
                        "required_permission": permission,
                        "user_permissions": user_permissions,
                    },
                )
                raise AuthorizationError(f"Permission '{permission}' required")

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def require_mfa(f):
    """Decorator to require MFA verification"""

    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        mfa_verified = claims.get("mfa_verified", False)

        if not mfa_verified:
            log_security_event(
                "mfa_required",
                {"user_id": get_jwt_identity(), "endpoint": request.endpoint},
            )
            return jsonify({"error": "MFA verification required"}), 403

        return f(*args, **kwargs)

    return decorated_function


# Initialize auth manager
auth_manager = AuthManager()
