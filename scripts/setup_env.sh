#!/bin/bash

# Setup Environment Script for QuantumAlpha
# This script sets up the development environment for the QuantumAlpha platform

set -e

echo "Setting up QuantumAlpha development environment..."

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up database
echo "Setting up database..."
if command -v docker &> /dev/null; then
    echo "Starting PostgreSQL and InfluxDB containers..."
    docker-compose -f infrastructure/docker-compose.yml up -d postgres influxdb
    
    # Wait for PostgreSQL to be ready
    echo "Waiting for PostgreSQL to be ready..."
    sleep 5
    
    echo "Creating database schema..."
    python scripts/setup_db.py
else
    echo "Docker not found. Please install Docker and Docker Compose to continue."
    exit 1
fi

# Set up configuration
echo "Setting up configuration..."
if [ ! -f config/.env ]; then
    echo "Creating .env file from example..."
    cp config/.env.example config/.env
    echo "Please update the .env file with your API keys and credentials."
fi

# Install frontend dependencies
echo "Setting up frontend dependencies..."
cd web-frontend
npm install
cd ..

cd mobile-frontend
npm install
cd ..

echo "Environment setup complete!"
echo "To start the development server, run: ./scripts/start_dev.sh"
