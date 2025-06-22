"""
Enhanced QuantumAlpha Backend Application
Comprehensive financial trading platform with enterprise-grade security and compliance
"""

import os
import sys
import asyncio
import signal
from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
import structlog
import traceback

# Import enhanced modules
from common.database import initialize_database, cleanup_database, db_manager
from common.auth import auth_manager, require_auth, require_role, require_permission
from common.validation import (
    validate_json, UserRegistrationSchema, UserLoginSchema, 
    OrderSchema, PortfolioSchema, ValidationError
)
from common.audit import audit_logger, log_security_event
from common.monitoring import (
    monitoring_service, create_monitoring_blueprint, 
    create_request_monitoring_middleware
)
from services.portfolio_service import portfolio_service
from services.trading_engine import trading_engine, OrderRequest, OrderSide, OrderType

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

class QuantumAlphaApp:
    """Enhanced QuantumAlpha application class"""
    
    def __init__(self):
        self.app = None
        self.jwt = None
        self.shutdown_handlers = []
    
    def create_app(self) -> Flask:
        """Create and configure Flask application"""
        app = Flask(__name__)
        
        # Load configuration
        self._load_config(app)
        
        # Initialize extensions
        self._init_extensions(app)
        
        # Register error handlers
        self._register_error_handlers(app)
        
        # Register request handlers
        self._register_request_handlers(app)
        
        # Register blueprints
        self._register_blueprints(app)
        
        # Register API routes
        self._register_routes(app)
        
        self.app = app
        return app
    
    def _load_config(self, app: Flask):
        """Load application configuration"""
        # Basic Flask configuration
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
        app.config['TESTING'] = os.getenv('FLASK_TESTING', 'false').lower() == 'true'
        
        # JWT configuration
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['SECRET_KEY'])
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Managed by auth module
        
        # CORS configuration
        app.config['CORS_ORIGINS'] = os.getenv('CORS_ORIGINS', '*')
        
        logger.info("Application configuration loaded")
    
    def _init_extensions(self, app: Flask):
        """Initialize Flask extensions"""
        # CORS
        CORS(app, origins=app.config['CORS_ORIGINS'])
        
        # JWT
        self.jwt = JWTManager(app)
        auth_manager.init_app(app)
        
        logger.info("Flask extensions initialized")
    
    def _register_error_handlers(self, app: Flask):
        """Register global error handlers"""
        
        @app.errorhandler(ValidationError)
        def handle_validation_error(error):
            """Handle validation errors"""
            logger.warning(f"Validation error: {error}")
            return jsonify({
                'error': 'Validation failed',
                'message': str(error),
                'code': 'VALIDATION_ERROR'
            }), 400
        
        @app.errorhandler(PermissionError)
        def handle_permission_error(error):
            """Handle permission errors"""
            logger.warning(f"Permission error: {error}")
            log_security_event('permission_denied', {
                'user_id': get_jwt_identity() if request.headers.get('Authorization') else None,
                'endpoint': request.endpoint,
                'error': str(error)
            })
            return jsonify({
                'error': 'Permission denied',
                'message': 'Insufficient permissions for this operation',
                'code': 'PERMISSION_DENIED'
            }), 403
        
        @app.errorhandler(404)
        def handle_not_found(error):
            """Handle 404 errors"""
            return jsonify({
                'error': 'Not found',
                'message': 'The requested resource was not found',
                'code': 'NOT_FOUND'
            }), 404
        
        @app.errorhandler(500)
        def handle_internal_error(error):
            """Handle internal server errors"""
            error_id = f"error_{int(datetime.now(timezone.utc).timestamp())}"
            logger.error(f"Internal server error [{error_id}]: {error}", exc_info=True)
            
            # Log to audit system
            audit_logger.log_event(
                action='error',
                resource_type='system',
                metadata={
                    'error_id': error_id,
                    'error_type': 'internal_server_error',
                    'endpoint': request.endpoint,
                    'method': request.method
                }
            )
            
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred',
                'code': 'INTERNAL_ERROR',
                'error_id': error_id
            }), 500
        
        @app.errorhandler(Exception)
        def handle_unexpected_error(error):
            """Handle unexpected errors"""
            error_id = f"error_{int(datetime.now(timezone.utc).timestamp())}"
            logger.error(f"Unexpected error [{error_id}]: {error}", exc_info=True)
            
            return jsonify({
                'error': 'Unexpected error',
                'message': 'An unexpected error occurred',
                'code': 'UNEXPECTED_ERROR',
                'error_id': error_id
            }), 500
    
    def _register_request_handlers(self, app: Flask):
        """Register request handlers for monitoring and security"""
        before_request, after_request = create_request_monitoring_middleware()
        
        @app.before_request
        def before_request_handler():
            """Before request handler"""
            # Set request start time for monitoring
            before_request()
            
            # Set user context for audit logging
            try:
                if request.headers.get('Authorization'):
                    verify_jwt_in_request(optional=True)
                    user_id = get_jwt_identity()
                    if user_id:
                        g.current_user_id = user_id
            except:
                pass  # JWT verification will be handled by route decorators
        
        @app.after_request
        def after_request_handler(response):
            """After request handler"""
            return after_request(response)
    
    def _register_blueprints(self, app: Flask):
        """Register Flask blueprints"""
        # Monitoring blueprint
        monitoring_bp = create_monitoring_blueprint()
        app.register_blueprint(monitoring_bp)
        
        logger.info("Blueprints registered")
    
    def _register_routes(self, app: Flask):
        """Register API routes"""
        
        # Health check endpoint (public)
        @app.route('/health', methods=['GET'])
        def health_check():
            """Public health check endpoint"""
            return jsonify({
                'status': 'ok',
                'service': 'quantumalpha-backend',
                'version': '2.0.0',
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        
        # Authentication routes
        @app.route('/api/auth/register', methods=['POST'])
        @validate_json(UserRegistrationSchema)
        def register(validated_data):
            """User registration endpoint"""
            try:
                # Check if user already exists
                from common.database import get_db_session
                from common.models import User
                
                with get_db_session() as session:
                    existing_user = session.query(User).filter(
                        User.email == validated_data['email']
                    ).first()
                    
                    if existing_user:
                        return jsonify({
                            'error': 'User already exists',
                            'code': 'USER_EXISTS'
                        }), 409
                    
                    # Create new user
                    user = User(
                        email=validated_data['email'],
                        password_hash=auth_manager.hash_password(validated_data['password']),
                        name=validated_data['name'],
                        is_verified=False,
                        terms_accepted_at=datetime.now(timezone.utc)
                    )
                    
                    session.add(user)
                    session.commit()
                    session.refresh(user)
                    
                    # Log registration
                    audit_logger.log_event(
                        action='create',
                        resource_type='user',
                        resource_id=str(user.id),
                        new_values={'email': user.email, 'name': user.name},
                        user_id=user.id
                    )
                    
                    return jsonify({
                        'message': 'User registered successfully',
                        'user_id': user.id
                    }), 201
                    
            except Exception as e:
                logger.error(f"Registration error: {e}")
                return jsonify({
                    'error': 'Registration failed',
                    'message': str(e)
                }), 500
        
        @app.route('/api/auth/login', methods=['POST'])
        @validate_json(UserLoginSchema)
        def login(validated_data):
            """User login endpoint"""
            try:
                user = auth_manager.authenticate_user(
                    email=validated_data['email'],
                    password=validated_data['password'],
                    mfa_token=validated_data.get('mfa_token')
                )
                
                if not user:
                    return jsonify({
                        'error': 'Invalid credentials',
                        'code': 'INVALID_CREDENTIALS'
                    }), 401
                
                # Create session
                session_data = auth_manager.create_session(
                    user=user,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent', '')
                )
                
                return jsonify({
                    'message': 'Login successful',
                    'data': session_data
                }), 200
                
            except Exception as e:
                logger.error(f"Login error: {e}")
                return jsonify({
                    'error': 'Login failed',
                    'message': str(e)
                }), 500
        
        @app.route('/api/auth/logout', methods=['POST'])
        @require_auth
        def logout():
            """User logout endpoint"""
            try:
                from flask_jwt_extended import get_jwt
                
                token = get_jwt()
                user_id = get_jwt_identity()
                
                auth_manager.logout(token['jti'], user_id)
                
                return jsonify({
                    'message': 'Logout successful'
                }), 200
                
            except Exception as e:
                logger.error(f"Logout error: {e}")
                return jsonify({
                    'error': 'Logout failed',
                    'message': str(e)
                }), 500
        
        @app.route('/api/auth/user', methods=['GET'])
        @require_auth
        def get_current_user():
            """Get current user information"""
            try:
                user_id = get_jwt_identity()
                
                from common.database import get_db_session
                from common.models import User
                
                with get_db_session() as session:
                    user = session.query(User).filter(User.id == user_id).first()
                    
                    if not user:
                        return jsonify({
                            'error': 'User not found',
                            'code': 'USER_NOT_FOUND'
                        }), 404
                    
                    return jsonify({
                        'data': {
                            'id': user.id,
                            'email': user.email,
                            'name': user.name,
                            'role': user.role.value,
                            'mfa_enabled': user.mfa_enabled,
                            'last_login': user.last_login.isoformat() if user.last_login else None
                        }
                    }), 200
                    
            except Exception as e:
                logger.error(f"Get user error: {e}")
                return jsonify({
                    'error': 'Failed to get user information',
                    'message': str(e)
                }), 500
        
        # Portfolio routes
        @app.route('/api/portfolios', methods=['GET'])
        @require_auth
        def get_portfolios():
            """Get user portfolios"""
            try:
                user_id = get_jwt_identity()
                portfolios = portfolio_service.get_user_portfolios(user_id)
                
                return jsonify({
                    'data': [portfolio.to_dict() for portfolio in portfolios]
                }), 200
                
            except Exception as e:
                logger.error(f"Get portfolios error: {e}")
                return jsonify({
                    'error': 'Failed to get portfolios',
                    'message': str(e)
                }), 500
        
        @app.route('/api/portfolios', methods=['POST'])
        @require_auth
        @validate_json(PortfolioSchema)
        def create_portfolio(validated_data):
            """Create new portfolio"""
            try:
                user_id = get_jwt_identity()
                
                portfolio = portfolio_service.create_portfolio(
                    user_id=user_id,
                    name=validated_data['name'],
                    description=validated_data.get('description'),
                    initial_cash=validated_data['initial_cash']
                )
                
                return jsonify({
                    'message': 'Portfolio created successfully',
                    'data': portfolio.to_dict()
                }), 201
                
            except Exception as e:
                logger.error(f"Create portfolio error: {e}")
                return jsonify({
                    'error': 'Failed to create portfolio',
                    'message': str(e)
                }), 500
        
        @app.route('/api/portfolios/<int:portfolio_id>', methods=['GET'])
        @require_auth
        def get_portfolio(portfolio_id):
            """Get portfolio details"""
            try:
                user_id = get_jwt_identity()
                portfolio = portfolio_service.get_portfolio(portfolio_id, user_id)
                
                if not portfolio:
                    return jsonify({
                        'error': 'Portfolio not found',
                        'code': 'PORTFOLIO_NOT_FOUND'
                    }), 404
                
                # Get portfolio metrics
                metrics = asyncio.run(portfolio_service.calculate_portfolio_metrics(portfolio_id))
                
                return jsonify({
                    'data': {
                        'portfolio': portfolio.to_dict(),
                        'metrics': metrics.__dict__ if metrics else None
                    }
                }), 200
                
            except Exception as e:
                logger.error(f"Get portfolio error: {e}")
                return jsonify({
                    'error': 'Failed to get portfolio',
                    'message': str(e)
                }), 500
        
        # Trading routes
        @app.route('/api/orders', methods=['POST'])
        @require_auth
        @require_permission('order.create')
        @validate_json(OrderSchema)
        def place_order(validated_data):
            """Place a new order"""
            try:
                user_id = get_jwt_identity()
                
                # Create order request
                order_request = OrderRequest(
                    portfolio_id=validated_data['portfolio_id'],
                    symbol=validated_data['symbol'],
                    side=OrderSide(validated_data['side']),
                    order_type=OrderType(validated_data['order_type']),
                    quantity=validated_data['quantity'],
                    price=validated_data.get('price'),
                    stop_price=validated_data.get('stop_price'),
                    time_in_force=validated_data.get('time_in_force', 'day'),
                    user_id=user_id
                )
                
                # Place order
                order = asyncio.run(trading_engine.place_order(order_request))
                
                return jsonify({
                    'message': 'Order placed successfully',
                    'data': order.to_dict()
                }), 201
                
            except Exception as e:
                logger.error(f"Place order error: {e}")
                return jsonify({
                    'error': 'Failed to place order',
                    'message': str(e)
                }), 500
        
        @app.route('/api/orders/<int:order_id>', methods=['DELETE'])
        @require_auth
        @require_permission('order.cancel')
        def cancel_order(order_id):
            """Cancel an order"""
            try:
                user_id = get_jwt_identity()
                
                success = trading_engine.cancel_order(order_id, user_id)
                
                if not success:
                    return jsonify({
                        'error': 'Order not found or cannot be cancelled',
                        'code': 'ORDER_NOT_CANCELLABLE'
                    }), 404
                
                return jsonify({
                    'message': 'Order cancelled successfully'
                }), 200
                
            except Exception as e:
                logger.error(f"Cancel order error: {e}")
                return jsonify({
                    'error': 'Failed to cancel order',
                    'message': str(e)
                }), 500
        
        @app.route('/api/orders', methods=['GET'])
        @require_auth
        def get_orders():
            """Get user orders"""
            try:
                user_id = get_jwt_identity()
                portfolio_id = request.args.get('portfolio_id', type=int)
                
                orders = trading_engine.get_order_history(user_id, portfolio_id)
                
                return jsonify({
                    'data': [order.to_dict() for order in orders]
                }), 200
                
            except Exception as e:
                logger.error(f"Get orders error: {e}")
                return jsonify({
                    'error': 'Failed to get orders',
                    'message': str(e)
                }), 500
        
        logger.info("API routes registered")
    
    def run(self, host='0.0.0.0', port=8001, debug=False):
        """Run the application"""
        try:
            # Initialize database
            logger.info("Initializing database...")
            initialize_database()
            
            # Start monitoring
            logger.info("Starting monitoring services...")
            monitoring_service.start()
            
            # Register shutdown handlers
            self._register_shutdown_handlers()
            
            logger.info(f"Starting QuantumAlpha backend on {host}:{port}")
            self.app.run(host=host, port=port, debug=debug)
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            self.shutdown()
            sys.exit(1)
    
    def _register_shutdown_handlers(self):
        """Register graceful shutdown handlers"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down gracefully...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def shutdown(self):
        """Graceful shutdown"""
        try:
            logger.info("Shutting down QuantumAlpha backend...")
            
            # Stop monitoring
            monitoring_service.stop()
            
            # Cleanup database connections
            cleanup_database()
            
            # Run custom shutdown handlers
            for handler in self.shutdown_handlers:
                try:
                    handler()
                except Exception as e:
                    logger.error(f"Error in shutdown handler: {e}")
            
            logger.info("Shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

# Create application instance
def create_app():
    """Application factory"""
    app_instance = QuantumAlphaApp()
    return app_instance.create_app()

# Main entry point
if __name__ == '__main__':
    app_instance = QuantumAlphaApp()
    app = app_instance.create_app()
    
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8001))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    # Run application
    app_instance.run(host=host, port=port, debug=debug)

