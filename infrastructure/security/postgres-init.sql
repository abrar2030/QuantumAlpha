-- PostgreSQL initialization script for QuantumAlpha
-- Security-hardened configuration for financial services

-- Create application database if not exists
CREATE DATABASE IF NOT EXISTS quantumalpha;

-- Create application user with limited privileges
CREATE USER IF NOT EXISTS quantumalpha_app WITH PASSWORD 'changeme_in_production';

-- Grant necessary privileges
GRANT CONNECT ON DATABASE quantumalpha TO quantumalpha_app;
GRANT USAGE ON SCHEMA public TO quantumalpha_app;
GRANT CREATE ON SCHEMA public TO quantumalpha_app;

-- Create audit schema for compliance
CREATE SCHEMA IF NOT EXISTS audit;
GRANT USAGE ON SCHEMA audit TO quantumalpha_app;
GRANT CREATE ON SCHEMA audit TO quantumalpha_app;

-- Enable row level security
ALTER DATABASE quantumalpha SET row_security = on;

-- Create audit table for SOX compliance
CREATE TABLE IF NOT EXISTS audit.user_actions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(255),
    record_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Create index for audit queries
CREATE INDEX IF NOT EXISTS idx_audit_user_actions_timestamp ON audit.user_actions(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_user_actions_user_id ON audit.user_actions(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_user_actions_action ON audit.user_actions(action);

-- Create function for audit logging
CREATE OR REPLACE FUNCTION audit.log_user_action()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit.user_actions (user_id, action, table_name, record_id, old_values)
        VALUES (current_user, TG_OP, TG_TABLE_NAME, OLD.id::text, row_to_json(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit.user_actions (user_id, action, table_name, record_id, old_values, new_values)
        VALUES (current_user, TG_OP, TG_TABLE_NAME, NEW.id::text, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit.user_actions (user_id, action, table_name, record_id, new_values)
        VALUES (current_user, TG_OP, TG_TABLE_NAME, NEW.id::text, row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Security settings
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
ALTER SYSTEM SET log_checkpoints = on;
ALTER SYSTEM SET log_lock_waits = on;
ALTER SYSTEM SET log_temp_files = 0;
ALTER SYSTEM SET log_autovacuum_min_duration = 0;

-- SSL settings
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = 'server.crt';
ALTER SYSTEM SET ssl_key_file = 'server.key';
ALTER SYSTEM SET ssl_ca_file = 'ca.crt';
ALTER SYSTEM SET ssl_crl_file = 'server.crl';

-- Connection security
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
ALTER SYSTEM SET tcp_keepalives_idle = 600;
ALTER SYSTEM SET tcp_keepalives_interval = 30;
ALTER SYSTEM SET tcp_keepalives_count = 3;

-- Reload configuration
SELECT pg_reload_conf();
