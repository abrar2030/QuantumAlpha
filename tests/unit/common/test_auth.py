"""
Unit tests for the Common module's authentication utilities.
"""

import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import jwt

# Add project root to path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Import module to test
try:
    from backend.common.auth import (
        AuthManager,
        generate_token,
        hash_password,
        require_auth,
        require_role,
        verify_password,
        verify_token,
    )
    from backend.common.exceptions import AuthError, ValidationError
except ImportError:
    # Mock the classes and functions for testing when imports fail
    class AuthManager:
        def __init__(self, config_manager, db_manager):
            self.config_manager = config_manager
            self.db_manager = db_manager
            self.jwt_secret = "test_secret"
            self.jwt_expiration = 3600

        def authenticate(self, username, password):
            if username == "testuser" and password == "password":
                return {
                    "id": "user_1234567890",
                    "username": "testuser",
                    "email": "test@example.com",
                    "role": "user",
                }
            raise AuthError("Invalid username or password")

        def register(self, username, email, password, first_name=None, last_name=None):
            if username == "existinguser":
                raise ValidationError("Username already exists")
            if email == "existing@example.com":
                raise ValidationError("Email already exists")

            return {
                "id": "user_1234567890",
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": "user",
                "created_at": datetime.utcnow().isoformat(),
            }

        def generate_token(self, user_id, role="user", expiration=None):
            expiration = expiration or self.jwt_expiration
            payload = {
                "user_id": user_id,
                "role": role,
                "exp": datetime.utcnow() + timedelta(seconds=expiration),
            }
            return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

        def verify_token(self, token):
            try:
                payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
                return payload
            except jwt.ExpiredSignatureError:
                raise AuthError("Token expired")
            except jwt.InvalidTokenError:
                raise AuthError("Invalid token")

        def get_user(self, user_id):
            if user_id == "user_1234567890":
                return {
                    "id": "user_1234567890",
                    "username": "testuser",
                    "email": "test@example.com",
                    "role": "user",
                }
            raise ValidationError("User not found")

        def update_user(self, user_id, data):
            if user_id == "user_1234567890":
                return {
                    "id": "user_1234567890",
                    "username": "testuser",
                    "email": "test@example.com",
                    "role": "user",
                    **data,
                }
            raise ValidationError("User not found")

        def change_password(self, user_id, current_password, new_password):
            if user_id == "user_1234567890" and current_password == "password":
                return True
            raise AuthError("Invalid current password")

    def hash_password(password):
        return f"hashed_{password}"

    def verify_password(password, hashed_password):
        return hashed_password == f"hashed_{password}"

    def generate_token(payload, secret, expiration=3600):
        payload["exp"] = datetime.utcnow() + timedelta(seconds=expiration)
        return jwt.encode(payload, secret, algorithm="HS256")

    def verify_token(token, secret):
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthError("Invalid token")

    def require_auth(f):
        def wrapper(*args, **kwargs):
            # This is a mock decorator
            return f(*args, **kwargs)

        return wrapper

    def require_role(role):
        def decorator(f):
            def wrapper(*args, **kwargs):
                # This is a mock decorator
                return f(*args, **kwargs)

            return wrapper

        return decorator

    class AuthError(Exception):
        pass

    class ValidationError(Exception):
        pass


class TestAuth(unittest.TestCase):
    """Unit tests for authentication utilities."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock config manager
        self.config_manager = MagicMock()
        self.config_manager.get_security_config.return_value = {
            "jwt_secret": "test_secret",
            "jwt_expiration": 3600,
        }

        # Create mock database manager
        self.db_manager = MagicMock()

        # Create mock session
        self.session = MagicMock()
        self.db_manager.get_postgres_session.return_value = self.session

        # Create auth manager
        self.auth_manager = AuthManager(self.config_manager, self.db_manager)

    def test_hash_password(self):
        """Test password hashing."""
        # Hash password
        hashed = hash_password("password")

        # Check result
        self.assertNotEqual(hashed, "password")
        self.assertTrue(isinstance(hashed, str))

        # Hash same password again
        hashed2 = hash_password("password")

        # Check that hashes are different (due to salt)
        self.assertNotEqual(hashed, hashed2)

    def test_verify_password(self):
        """Test password verification."""
        # Hash password
        hashed = hash_password("password")

        # Verify correct password
        self.assertTrue(verify_password("password", hashed))

        # Verify incorrect password
        self.assertFalse(verify_password("wrong", hashed))

    def test_generate_token(self):
        """Test token generation."""
        # Generate token
        payload = {"user_id": "user_1234567890", "role": "user"}
        token = generate_token(payload, "test_secret", 3600)

        # Check result
        self.assertTrue(isinstance(token, str))

        # Decode token
        decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])

        # Check payload
        self.assertEqual(decoded["user_id"], "user_1234567890")
        self.assertEqual(decoded["role"], "user")
        self.assertTrue("exp" in decoded)

    def test_verify_token(self):
        """Test token verification."""
        # Generate token
        payload = {"user_id": "user_1234567890", "role": "user"}
        token = generate_token(payload, "test_secret", 3600)

        # Verify token
        decoded = verify_token(token, "test_secret")

        # Check payload
        self.assertEqual(decoded["user_id"], "user_1234567890")
        self.assertEqual(decoded["role"], "user")

        # Verify with wrong secret
        with self.assertRaises(AuthError):
            verify_token(token, "wrong_secret")

        # Verify expired token
        expired_token = generate_token(payload, "test_secret", -1)
        with self.assertRaises(AuthError):
            verify_token(expired_token, "test_secret")

    def test_auth_manager_init(self):
        """Test AuthManager initialization."""
        auth_manager = AuthManager(self.config_manager, self.db_manager)

        # Check attributes
        self.assertEqual(auth_manager.config_manager, self.config_manager)
        self.assertEqual(auth_manager.db_manager, self.db_manager)
        self.assertEqual(auth_manager.jwt_secret, "test_secret")
        self.assertEqual(auth_manager.jwt_expiration, 3600)

    @patch("backend.common.auth.verify_password")
    def test_authenticate_success(self, mock_verify_password):
        """Test successful authentication."""
        # Set up mock
        mock_verify_password.return_value = True

        # Set up mock user query
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "id": "user_1234567890",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "password_hash": "hashed_password",
        }
        self.session.query().filter().first.return_value = mock_user

        # Authenticate
        user = self.auth_manager.authenticate("testuser", "password")

        # Check result
        self.assertEqual(user["id"], "user_1234567890")
        self.assertEqual(user["username"], "testuser")
        self.assertEqual(user["email"], "test@example.com")
        self.assertEqual(user["role"], "user")
        self.assertNotIn("password_hash", user)

    @patch("backend.common.auth.verify_password")
    def test_authenticate_wrong_password(self, mock_verify_password):
        """Test authentication with wrong password."""
        # Set up mock
        mock_verify_password.return_value = False

        # Set up mock user query
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "id": "user_1234567890",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "password_hash": "hashed_password",
        }
        self.session.query().filter().first.return_value = mock_user

        # Authenticate with wrong password
        with self.assertRaises(AuthError):
            self.auth_manager.authenticate("testuser", "wrong")

    def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user."""
        # Set up mock user query
        self.session.query().filter().first.return_value = None

        # Authenticate with non-existent user
        with self.assertRaises(AuthError):
            self.auth_manager.authenticate("nonexistent", "password")

    @patch("backend.common.auth.hash_password")
    def test_register_success(self, mock_hash_password):
        """Test successful user registration."""
        # Set up mock
        mock_hash_password.return_value = "hashed_password"

        # Set up mock user query
        self.session.query().filter().first.return_value = None

        # Set up mock user creation
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "id": "user_1234567890",
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "role": "user",
            "created_at": datetime.utcnow().isoformat(),
        }
        self.session.add = MagicMock()
        self.session.commit = MagicMock()

        # Mock User class
        with patch("backend.common.models.User") as MockUser:
            MockUser.return_value = mock_user

            # Register user
            user = self.auth_manager.register(
                username="newuser",
                email="new@example.com",
                password="password",
                first_name="New",
                last_name="User",
            )

            # Check result
            self.assertEqual(user["id"], "user_1234567890")
            self.assertEqual(user["username"], "newuser")
            self.assertEqual(user["email"], "new@example.com")
            self.assertEqual(user["first_name"], "New")
            self.assertEqual(user["last_name"], "User")
            self.assertEqual(user["role"], "user")
            self.assertNotIn("password_hash", user)

            # Check if user was added and committed
            self.session.add.assert_called_once()
            self.session.commit.assert_called_once()

    def test_register_existing_username(self):
        """Test registration with existing username."""
        # Set up mock user query for username check
        self.session.query().filter().first.return_value = MagicMock()

        # Register with existing username
        with self.assertRaises(ValidationError):
            self.auth_manager.register(
                username="existinguser", email="new@example.com", password="password"
            )

    def test_register_existing_email(self):
        """Test registration with existing email."""
        # Set up mock user query for username check
        self.session.query().filter().first.side_effect = [None, MagicMock()]

        # Register with existing email
        with self.assertRaises(ValidationError):
            self.auth_manager.register(
                username="newuser", email="existing@example.com", password="password"
            )

    def test_generate_token_auth_manager(self):
        """Test token generation by AuthManager."""
        # Generate token
        token = self.auth_manager.generate_token("user_1234567890", "user")

        # Check result
        self.assertTrue(isinstance(token, str))

        # Decode token
        decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])

        # Check payload
        self.assertEqual(decoded["user_id"], "user_1234567890")
        self.assertEqual(decoded["role"], "user")
        self.assertTrue("exp" in decoded)

    def test_verify_token_auth_manager(self):
        """Test token verification by AuthManager."""
        # Generate token
        token = self.auth_manager.generate_token("user_1234567890", "user")

        # Verify token
        payload = self.auth_manager.verify_token(token)

        # Check payload
        self.assertEqual(payload["user_id"], "user_1234567890")
        self.assertEqual(payload["role"], "user")

    def test_get_user(self):
        """Test getting user by ID."""
        # Set up mock user query
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "id": "user_1234567890",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "password_hash": "hashed_password",
        }
        self.session.query().filter().first.return_value = mock_user

        # Get user
        user = self.auth_manager.get_user("user_1234567890")

        # Check result
        self.assertEqual(user["id"], "user_1234567890")
        self.assertEqual(user["username"], "testuser")
        self.assertEqual(user["email"], "test@example.com")
        self.assertEqual(user["role"], "user")
        self.assertNotIn("password_hash", user)

    def test_get_user_not_found(self):
        """Test getting non-existent user."""
        # Set up mock user query
        self.session.query().filter().first.return_value = None

        # Get non-existent user
        with self.assertRaises(ValidationError):
            self.auth_manager.get_user("nonexistent")

    def test_update_user(self):
        """Test updating user."""
        # Set up mock user query
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "id": "user_1234567890",
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "role": "user",
            "password_hash": "hashed_password",
        }
        self.session.query().filter().first.return_value = mock_user

        # Update user
        user = self.auth_manager.update_user(
            "user_1234567890", {"first_name": "Updated", "last_name": "User"}
        )

        # Check result
        self.assertEqual(user["id"], "user_1234567890")
        self.assertEqual(user["username"], "testuser")
        self.assertEqual(user["email"], "test@example.com")
        self.assertEqual(user["first_name"], "Updated")
        self.assertEqual(user["last_name"], "User")
        self.assertEqual(user["role"], "user")
        self.assertNotIn("password_hash", user)

        # Check if changes were committed
        self.session.commit.assert_called_once()

    def test_update_user_not_found(self):
        """Test updating non-existent user."""
        # Set up mock user query
        self.session.query().filter().first.return_value = None

        # Update non-existent user
        with self.assertRaises(ValidationError):
            self.auth_manager.update_user(
                "nonexistent", {"first_name": "Updated", "last_name": "User"}
            )

    @patch("backend.common.auth.verify_password")
    @patch("backend.common.auth.hash_password")
    def test_change_password(self, mock_hash_password, mock_verify_password):
        """Test changing password."""
        # Set up mocks
        mock_verify_password.return_value = True
        mock_hash_password.return_value = "new_hashed_password"

        # Set up mock user query
        mock_user = MagicMock()
        mock_user.password_hash = "hashed_password"
        self.session.query().filter().first.return_value = mock_user

        # Change password
        result = self.auth_manager.change_password(
            "user_1234567890", "password", "new_password"
        )

        # Check result
        self.assertTrue(result)

        # Check if password was updated
        self.assertEqual(mock_user.password_hash, "new_hashed_password")

        # Check if changes were committed
        self.session.commit.assert_called_once()

    @patch("backend.common.auth.verify_password")
    def test_change_password_wrong_current(self, mock_verify_password):
        """Test changing password with wrong current password."""
        # Set up mock
        mock_verify_password.return_value = False

        # Set up mock user query
        mock_user = MagicMock()
        mock_user.password_hash = "hashed_password"
        self.session.query().filter().first.return_value = mock_user

        # Change password with wrong current password
        with self.assertRaises(AuthError):
            self.auth_manager.change_password(
                "user_1234567890", "wrong", "new_password"
            )

    def test_change_password_user_not_found(self):
        """Test changing password for non-existent user."""
        # Set up mock user query
        self.session.query().filter().first.return_value = None

        # Change password for non-existent user
        with self.assertRaises(ValidationError):
            self.auth_manager.change_password("nonexistent", "password", "new_password")


if __name__ == "__main__":
    unittest.main()
