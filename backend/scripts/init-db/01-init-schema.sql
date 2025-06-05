-- Initialize TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS market_data;
CREATE SCHEMA IF NOT EXISTS ai_models;
CREATE SCHEMA IF NOT EXISTS risk_management;
CREATE SCHEMA IF NOT EXISTS execution;
CREATE SCHEMA IF NOT EXISTS auth;

-- Create market data tables
CREATE TABLE IF NOT EXISTS market_data.symbols (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100),
    exchange VARCHAR(20),
    asset_class VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS market_data.ohlcv (
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    open NUMERIC(19, 6) NOT NULL,
    high NUMERIC(19, 6) NOT NULL,
    low NUMERIC(19, 6) NOT NULL,
    close NUMERIC(19, 6) NOT NULL,
    volume NUMERIC(19, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (symbol, timestamp, timeframe),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

-- Convert OHLCV table to hypertable
SELECT create_hypertable('market_data.ohlcv', 'timestamp');

CREATE TABLE IF NOT EXISTS market_data.alternative_data (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    symbol VARCHAR(20),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

-- Convert alternative_data table to hypertable
SELECT create_hypertable('market_data.alternative_data', 'timestamp');

CREATE TABLE IF NOT EXISTS market_data.features (
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    feature_name VARCHAR(50) NOT NULL,
    value NUMERIC(19, 6) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (symbol, timestamp, timeframe, feature_name),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

-- Convert features table to hypertable
SELECT create_hypertable('market_data.features', 'timestamp');

-- Create AI model tables
CREATE TABLE IF NOT EXISTS ai_models.models (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    parameters JSONB,
    metrics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ai_models.model_versions (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(50) NOT NULL,
    version VARCHAR(20) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    parameters JSONB,
    metrics JSONB,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (model_id) REFERENCES ai_models.models(id),
    UNIQUE (model_id, version)
);

CREATE TABLE IF NOT EXISTS ai_models.prediction_history (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    prediction NUMERIC(19, 6) NOT NULL,
    actual NUMERIC(19, 6),
    error NUMERIC(19, 6),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (model_id) REFERENCES ai_models.models(id),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

-- Convert prediction_history table to hypertable
SELECT create_hypertable('ai_models.prediction_history', 'timestamp');

CREATE TABLE IF NOT EXISTS ai_models.signals (
    id SERIAL PRIMARY KEY,
    model_id VARCHAR(50),
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    signal_type VARCHAR(20) NOT NULL,
    strength NUMERIC(5, 2) NOT NULL,
    price NUMERIC(19, 6),
    parameters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (model_id) REFERENCES ai_models.models(id),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

-- Convert signals table to hypertable
SELECT create_hypertable('ai_models.signals', 'timestamp');

-- Create risk management tables
CREATE TABLE IF NOT EXISTS risk_management.portfolios (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id VARCHAR(50) NOT NULL,
    parameters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risk_management.positions (
    id SERIAL PRIMARY KEY,
    portfolio_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    quantity NUMERIC(19, 6) NOT NULL,
    entry_price NUMERIC(19, 6) NOT NULL,
    current_price NUMERIC(19, 6) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (portfolio_id) REFERENCES risk_management.portfolios(id),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol),
    UNIQUE (portfolio_id, symbol)
);

CREATE TABLE IF NOT EXISTS risk_management.risk_metrics (
    id SERIAL PRIMARY KEY,
    portfolio_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    var_95 NUMERIC(19, 6),
    var_99 NUMERIC(19, 6),
    expected_shortfall NUMERIC(19, 6),
    sharpe_ratio NUMERIC(10, 4),
    sortino_ratio NUMERIC(10, 4),
    max_drawdown NUMERIC(10, 4),
    beta NUMERIC(10, 4),
    alpha NUMERIC(10, 4),
    volatility NUMERIC(10, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (portfolio_id) REFERENCES risk_management.portfolios(id)
);

-- Convert risk_metrics table to hypertable
SELECT create_hypertable('risk_management.risk_metrics', 'timestamp');

CREATE TABLE IF NOT EXISTS risk_management.stress_tests (
    id SERIAL PRIMARY KEY,
    portfolio_id VARCHAR(50) NOT NULL,
    scenario_name VARCHAR(100) NOT NULL,
    parameters JSONB,
    results JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (portfolio_id) REFERENCES risk_management.portfolios(id)
);

-- Create execution tables
CREATE TABLE IF NOT EXISTS execution.orders (
    id VARCHAR(50) PRIMARY KEY,
    portfolio_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    order_type VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity NUMERIC(19, 6) NOT NULL,
    price NUMERIC(19, 6),
    time_in_force VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    broker_order_id VARCHAR(50),
    parameters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (portfolio_id) REFERENCES risk_management.portfolios(id),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

CREATE TABLE IF NOT EXISTS execution.trades (
    id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity NUMERIC(19, 6) NOT NULL,
    price NUMERIC(19, 6) NOT NULL,
    commission NUMERIC(19, 6) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (order_id) REFERENCES execution.orders(id),
    FOREIGN KEY (symbol) REFERENCES market_data.symbols(symbol)
);

-- Convert trades table to hypertable
SELECT create_hypertable('execution.trades', 'timestamp');

CREATE TABLE IF NOT EXISTS execution.broker_accounts (
    id VARCHAR(50) PRIMARY KEY,
    broker_name VARCHAR(50) NOT NULL,
    account_number VARCHAR(50) NOT NULL,
    api_key VARCHAR(100),
    api_secret VARCHAR(100),
    parameters JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create authentication tables
CREATE TABLE IF NOT EXISTS auth.users (
    id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auth.api_keys (
    id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    key_name VARCHAR(50) NOT NULL,
    api_key VARCHAR(100) NOT NULL UNIQUE,
    permissions JSONB,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES auth.users(id)
);

-- Create indexes
CREATE INDEX idx_ohlcv_symbol ON market_data.ohlcv(symbol);
CREATE INDEX idx_alternative_data_symbol ON market_data.alternative_data(symbol);
CREATE INDEX idx_features_symbol ON market_data.features(symbol);
CREATE INDEX idx_prediction_history_model_id ON ai_models.prediction_history(model_id);
CREATE INDEX idx_prediction_history_symbol ON ai_models.prediction_history(symbol);
CREATE INDEX idx_signals_model_id ON ai_models.signals(model_id);
CREATE INDEX idx_signals_symbol ON ai_models.signals(symbol);
CREATE INDEX idx_positions_portfolio_id ON risk_management.positions(portfolio_id);
CREATE INDEX idx_risk_metrics_portfolio_id ON risk_management.risk_metrics(portfolio_id);
CREATE INDEX idx_orders_portfolio_id ON execution.orders(portfolio_id);
CREATE INDEX idx_orders_symbol ON execution.orders(symbol);
CREATE INDEX idx_trades_order_id ON execution.trades(order_id);
CREATE INDEX idx_trades_symbol ON execution.trades(symbol);

-- Create functions for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updating timestamps
CREATE TRIGGER update_market_data_symbols_updated_at
BEFORE UPDATE ON market_data.symbols
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_ai_models_models_updated_at
BEFORE UPDATE ON ai_models.models
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_risk_management_portfolios_updated_at
BEFORE UPDATE ON risk_management.portfolios
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_risk_management_positions_updated_at
BEFORE UPDATE ON risk_management.positions
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_execution_orders_updated_at
BEFORE UPDATE ON execution.orders
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_execution_broker_accounts_updated_at
BEFORE UPDATE ON execution.broker_accounts
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_auth_users_updated_at
BEFORE UPDATE ON auth.users
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_auth_api_keys_updated_at
BEFORE UPDATE ON auth.api_keys
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

