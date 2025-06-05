# QuantumAlpha Scripts and Configuration Documentation

This document provides an overview of the scripts and configuration files for the QuantumAlpha platform.

## Table of Contents

1. [Configuration Files](#configuration-files)
   - [Environment Configuration](#environment-configuration)
   - [Service-Specific Configuration](#service-specific-configuration)
   - [Database Configuration](#database-configuration)
   - [Logging Configuration](#logging-configuration)
2. [Environment Setup Scripts](#environment-setup-scripts)
   - [Setup Environment](#setup-environment)
   - [Database Setup](#database-setup)
   - [Start Development Environment](#start-development-environment)
   - [Stop Services](#stop-services)
   - [Start Individual Service](#start-individual-service)
3. [Testing Scripts](#testing-scripts)
   - [Run Tests](#run-tests)
4. [Deployment Scripts](#deployment-scripts)
   - [Deploy](#deploy)
   - [Kubernetes Deployment](#kubernetes-deployment)
5. [Monitoring and Maintenance Scripts](#monitoring-and-maintenance-scripts)
   - [Monitor Setup](#monitor-setup)
   - [Backup](#backup)
   - [Restore](#restore)

## Configuration Files

### Environment Configuration

Environment-specific configuration files are located in the `config` directory:

- `config/.env.dev`: Development environment configuration
- `config/.env.staging`: Staging environment configuration
- `config/.env.prod`: Production environment configuration

These files contain environment variables for different environments, including database connections, API keys, service URLs, and feature flags.

To use these files:

1. Copy the appropriate file to `config/.env` based on your environment:
   ```bash
   cp config/.env.dev config/.env
   ```

2. Edit the `.env` file to set your specific values:
   ```bash
   nano config/.env
   ```

### Service-Specific Configuration

Service-specific configuration files are located in the `config/services` directory:

- `config/services/data_service.yaml`: Configuration for the data service
- `config/services/ai_engine.yaml`: Configuration for the AI engine
- `config/services/risk_service.yaml`: Configuration for the risk service
- `config/services/execution_service.yaml`: Configuration for the execution service

These files contain detailed configuration for each service, including API settings, data sources, processing parameters, and monitoring settings.

### Database Configuration

Database configuration files are located in the `config/database` directory:

- `config/database/postgres.yaml`: PostgreSQL configuration
- `config/database/influxdb.yaml`: InfluxDB configuration

These files contain database connection settings, schema definitions, backup configurations, and performance tuning parameters.

### Logging Configuration

The logging configuration file is located at `config/logging.yaml`. It contains logging settings for different environments and services, including log levels, formats, and outputs.

## Environment Setup Scripts

### Setup Environment

The `scripts/setup_env.sh` script sets up the development environment for the QuantumAlpha platform.

Usage:
```bash
./scripts/setup_env.sh [options]
```

Options:
- `-e, --env ENV`: Set environment (dev, staging, prod). Default: dev
- `-h, --help`: Show help message

This script:
1. Checks system requirements
2. Creates and activates a Python virtual environment
3. Installs Python dependencies
4. Sets up configuration files
5. Starts database containers
6. Creates database schema
7. Installs frontend dependencies

### Database Setup

The `scripts/setup_db.py` script initializes the database schema and seeds initial data.

Usage:
```bash
python scripts/setup_db.py [options]
```

Options:
- `--env {dev,staging,prod}`: Environment (dev, staging, prod). Default: dev
- `--postgres-only`: Set up PostgreSQL only
- `--influxdb-only`: Set up InfluxDB only
- `--no-seed`: Skip seeding initial data

This script:
1. Creates databases if they don't exist
2. Executes schema creation scripts
3. Seeds initial data

### Start Development Environment

The `scripts/start_dev.sh` script starts all services for local development.

Usage:
```bash
./scripts/start_dev.sh [options]
```

Options:
- `--no-infrastructure`: Don't start infrastructure services
- `--no-backend`: Don't start backend services
- `--no-frontend`: Don't start frontend services
- `--with-monitoring`: Start monitoring services
- `-d, --detached`: Run services in detached mode
- `-h, --help`: Show help message

This script:
1. Starts infrastructure services (PostgreSQL, InfluxDB, Redis, Kafka)
2. Starts backend services (data-service, ai-engine, risk-service, execution-service)
3. Starts frontend services (web-frontend)

### Stop Services

The `scripts/stop_services.sh` script stops all running services.

Usage:
```bash
./scripts/stop_services.sh [options]
```

Options:
- `--no-infrastructure`: Don't stop infrastructure services
- `--no-backend`: Don't stop backend services
- `--no-frontend`: Don't stop frontend services
- `-h, --help`: Show help message

This script:
1. Stops backend services
2. Stops frontend services
3. Stops infrastructure services

### Start Individual Service

The `scripts/start_service.sh` script starts an individual service.

Usage:
```bash
./scripts/start_service.sh [options]
```

Options:
- `-s, --service SERVICE`: Service to start (data-service, ai-engine, risk-service, execution-service, web-frontend)
- `-e, --env ENV`: Environment (dev, staging, prod). Default: dev
- `-d, --debug`: Start service in debug mode
- `-p, --port PORT`: Override default port
- `--detached`: Run service in detached mode
- `-h, --help`: Show help message

This script:
1. Loads environment variables
2. Starts the specified service
3. Logs output to a file if running in detached mode

## Testing Scripts

### Run Tests

The `scripts/run_tests.sh` script runs tests for the QuantumAlpha platform.

Usage:
```bash
./scripts/run_tests.sh [options] [test_path]
```

Options:
- `--unit-only`: Run only unit tests
- `--integration-only`: Run only integration tests
- `--system-only`: Run only system tests
- `--with-system`: Include system tests
- `--coverage`: Generate coverage report
- `-v, --verbose`: Verbose output
- `-p, --parallel`: Run tests in parallel
- `--junit`: Generate JUnit XML reports
- `-h, --help`: Show help message

Arguments:
- `test_path`: Path to specific test file or directory

This script:
1. Runs unit tests
2. Runs integration tests
3. Runs system tests (if specified)
4. Generates coverage reports (if specified)

## Deployment Scripts

### Deploy

The `scripts/deploy.sh` script handles building, tagging, and deploying Docker images.

Usage:
```bash
./scripts/deploy.sh [options]
```

Options:
- `-e, --env ENV`: Environment to deploy to (dev, staging, prod). Default: dev
- `-s, --services SERVICES`: Services to deploy (all, data-service, ai-engine, risk-service, execution-service, web-frontend)
- `--no-build`: Skip building Docker images
- `--no-push`: Skip pushing Docker images to registry
- `--no-deploy`: Skip deploying to Kubernetes
- `-t, --tag TAG`: Image tag. Default: latest
- `-r, --registry REGISTRY`: Docker registry URL
- `-n, --namespace NS`: Kubernetes namespace. Default: quantumalpha
- `--dry-run`: Print commands without executing them
- `-h, --help`: Show help message

This script:
1. Builds Docker images
2. Pushes Docker images to registry
3. Deploys to Kubernetes

### Kubernetes Deployment

The `scripts/k8s_deploy.sh` script handles Kubernetes-specific deployment tasks.

Usage:
```bash
./scripts/k8s_deploy.sh [options]
```

Options:
- `-e, --env ENV`: Environment (dev, staging, prod). Default: dev
- `-a, --action ACTION`: Action to perform (apply, delete). Default: apply
- `-c, --components COMP`: Components to deploy (all, infrastructure, services, monitoring)
- `-n, --namespace NS`: Kubernetes namespace. If not specified, uses environment-based namespace
- `-k, --kube-context CTX`: Kubernetes context. If not specified, uses environment-based context
- `--dry-run`: Print commands without executing them
- `--no-wait`: Don't wait for resources to be ready
- `-h, --help`: Show help message

This script:
1. Creates namespace if it doesn't exist
2. Deploys infrastructure components
3. Deploys service components
4. Deploys monitoring components
5. Applies environment-specific overlays

## Monitoring and Maintenance Scripts

### Monitor Setup

The `scripts/monitor_setup.sh` script sets up monitoring and logging.

Usage:
```bash
./scripts/monitor_setup.sh [options]
```

Options:
- `-e, --env ENV`: Environment (dev, staging, prod). Default: dev
- `-c, --components COMP`: Components to set up (all, metrics, logging, dashboards)
- `-n, --namespace NS`: Kubernetes namespace. If not specified, uses environment-based namespace
- `-k, --kube-context CTX`: Kubernetes context. If not specified, uses environment-based context
- `--local`: Set up monitoring locally using Docker Compose
- `--dry-run`: Print commands without executing them
- `-h, --help`: Show help message

This script:
1. Sets up Prometheus and Grafana for metrics monitoring
2. Sets up Elasticsearch, Fluentd, and Kibana for logging
3. Sets up dashboards for monitoring

### Backup

The `scripts/backup.sh` script performs backups of databases and configurations.

Usage:
```bash
./scripts/backup.sh [options]
```

Options:
- `-e, --env ENV`: Environment (dev, staging, prod). Default: dev
- `-c, --components COMP`: Components to backup (all, postgres, influxdb, config)
- `-d, --backup-dir DIR`: Local backup directory. Default: ./backups
- `-s, --s3-bucket BUCKET`: S3 bucket for backup storage
- `-p, --s3-prefix PREFIX`: S3 prefix (folder) for backups. Default: quantumalpha-backups
- `--dry-run`: Print commands without executing them
- `-h, --help`: Show help message

This script:
1. Backs up PostgreSQL database
2. Backs up InfluxDB
3. Backs up configuration files
4. Compresses backup
5. Uploads backup to S3 (if specified)

### Restore

The `scripts/restore.sh` script restores databases and configurations from backups.

Usage:
```bash
./scripts/restore.sh [options]
```

Options:
- `-e, --env ENV`: Environment (dev, staging, prod). Default: dev
- `-c, --components COMP`: Components to restore (all, postgres, influxdb, config)
- `-f, --backup-file FILE`: Path to backup file (.tar.gz)
- `-t, --timestamp TS`: Timestamp of backup to restore (format: YYYYMMDD-HHMMSS)
- `-d, --backup-dir DIR`: Local backup directory. Default: ./backups
- `-s, --s3-bucket BUCKET`: S3 bucket for backup storage
- `-p, --s3-prefix PREFIX`: S3 prefix (folder) for backups. Default: quantumalpha-backups
- `--dry-run`: Print commands without executing them
- `--force`: Force restore without confirmation
- `-h, --help`: Show help message

This script:
1. Downloads backup from S3 (if specified)
2. Extracts backup
3. Restores PostgreSQL database
4. Restores InfluxDB
5. Restores configuration files

