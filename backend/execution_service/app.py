"""
Execution Service for QuantumAlpha
This service is responsible for:
1. Order management
2. Broker integration
3. Execution strategy
4. Trade reconciliation
"""
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import traceback

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import (
    get_config_manager,
    get_db_manager,
    setup_logger,
    ServiceError,
    ValidationError,
    NotFoundError,
    AuthenticationError,
    AuthorizationError,
    validate_schema
)
from common.validation import (
    OrderRequest,
    CancelOrderRequest
)

# Import service modules
from execution_service.order_manager import OrderManager
from execution_service.broker_integration import BrokerIntegration
from execution_service.execution_strategy import ExecutionStrategy

# Configure logging
logger = setup_logger('execution_service', logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config_manager = get_config_manager(
    env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env')
)

# Initialize database manager
db_manager = get_db_manager(config_manager.get_all())

# Initialize services
broker_integration = BrokerIntegration(config_manager, db_manager)
execution_strategy = ExecutionStrategy(config_manager, db_manager)
order_manager = OrderManager(config_manager, db_manager, broker_integration, execution_strategy)

# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    """Handle errors"""
    if isinstance(error, ServiceError):
        return jsonify(error.to_dict()), error.status_code
    
    logger.error(f"Unhandled error: {error}")
    logger.error(traceback.format_exc())
    
    return jsonify({
        'error': 'Internal server error',
        'status_code': 500,
        'details': str(error)
    }), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'execution_service'
    })

# Order management endpoints
@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        # Get query parameters
        portfolio_id = request.args.get('portfolio_id')
        status = request.args.get('status')
        symbol = request.args.get('symbol')
        
        # Get orders
        orders = order_manager.get_orders(
            portfolio_id=portfolio_id,
            status=status,
            symbol=symbol
        )
        
        return jsonify({
            'orders': orders
        })
    
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order"""
    try:
        # Get order
        order = order_manager.get_order(order_id)
        
        return jsonify(order)
    
    except Exception as e:
        logger.error(f"Error getting order: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        # Get request data
        data = request.json
        
        # Validate data
        validated_data = validate_schema(data, OrderRequest)
        
        # Create order
        order = order_manager.create_order(validated_data)
        
        return jsonify(order)
    
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/orders/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order"""
    try:
        # Get request data
        data = request.json or {}
        
        # Add order ID to data
        data['order_id'] = order_id
        
        # Validate data
        validated_data = validate_schema(data, CancelOrderRequest)
        
        # Cancel order
        result = order_manager.cancel_order(validated_data['order_id'])
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error canceling order: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

# Execution strategy endpoints
@app.route('/api/execution-strategies', methods=['GET'])
def get_execution_strategies():
    """Get all execution strategies"""
    try:
        # Get execution strategies
        strategies = execution_strategy.get_strategies()
        
        return jsonify({
            'strategies': strategies
        })
    
    except Exception as e:
        logger.error(f"Error getting execution strategies: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/execution-strategies/<strategy_id>', methods=['GET'])
def get_execution_strategy(strategy_id):
    """Get a specific execution strategy"""
    try:
        # Get execution strategy
        strategy = execution_strategy.get_strategy(strategy_id)
        
        return jsonify(strategy)
    
    except Exception as e:
        logger.error(f"Error getting execution strategy: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

# Broker integration endpoints
@app.route('/api/brokers', methods=['GET'])
def get_brokers():
    """Get all brokers"""
    try:
        # Get brokers
        brokers = broker_integration.get_brokers()
        
        return jsonify({
            'brokers': brokers
        })
    
    except Exception as e:
        logger.error(f"Error getting brokers: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/brokers/<broker_id>', methods=['GET'])
def get_broker(broker_id):
    """Get a specific broker"""
    try:
        # Get broker
        broker = broker_integration.get_broker(broker_id)
        
        return jsonify(broker)
    
    except Exception as e:
        logger.error(f"Error getting broker: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/brokers/<broker_id>/accounts', methods=['GET'])
def get_broker_accounts(broker_id):
    """Get accounts for a broker"""
    try:
        # Get accounts
        accounts = broker_integration.get_accounts(broker_id)
        
        return jsonify({
            'accounts': accounts
        })
    
    except Exception as e:
        logger.error(f"Error getting broker accounts: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

@app.route('/api/brokers/<broker_id>/positions', methods=['GET'])
def get_broker_positions(broker_id):
    """Get positions for a broker"""
    try:
        # Get account ID
        account_id = request.args.get('account_id')
        
        if not account_id:
            raise ValidationError("Account ID is required")
        
        # Get positions
        positions = broker_integration.get_positions(broker_id, account_id)
        
        return jsonify({
            'positions': positions
        })
    
    except Exception as e:
        logger.error(f"Error getting broker positions: {e}")
        if isinstance(e, ServiceError):
            raise
        else:
            raise ServiceError(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

