import unittest
import subprocess
import time
import requests
import os
import signal
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestEndToEndTrading(unittest.TestCase):
    """End-to-end system tests for the QuantumAlpha trading platform"""
    
    @classmethod
    def setUpClass(cls):
        """Start all required services before running tests"""
        print("Starting services for end-to-end testing...")
        
        # Start services using docker-compose
        cls.docker_process = subprocess.Popen(
            ["docker-compose", "-f", "../infrastructure/docker-compose.yml", "up", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for services to be ready
        print("Waiting for services to be ready...")
        time.sleep(30)  # Give services time to start
        
        # Check if services are running
        cls._check_services_health()
    
    @classmethod
    def tearDownClass(cls):
        """Stop all services after tests are complete"""
        print("Stopping services...")
        
        # Stop services using docker-compose
        subprocess.run(
            ["docker-compose", "-f", "../infrastructure/docker-compose.yml", "down"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    @classmethod
    def _check_services_health(cls):
        """Check if all required services are healthy"""
        services = [
            {"name": "Data Service", "url": "http://localhost:8081/health"},
            {"name": "AI Engine", "url": "http://localhost:8082/health"},
            {"name": "Risk Service", "url": "http://localhost:8083/health"},
            {"name": "Execution Service", "url": "http://localhost:8084/health"}
        ]
        
        for service in services:
            try:
                response = requests.get(service["url"], timeout=5)
                if response.status_code == 200:
                    print(f"{service['name']} is healthy")
                else:
                    print(f"Warning: {service['name']} returned status code {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"Warning: Could not connect to {service['name']}")
    
    def test_full_trading_workflow(self):
        """Test the complete trading workflow from data to execution"""
        # Step 1: Get market data
        print("Fetching market data...")
        data_response = requests.get("http://localhost:8081/api/market-data/AAPL?timeframe=1d&period=1mo")
        self.assertEqual(data_response.status_code, 200)
        market_data = data_response.json()
        
        # Step 2: Generate trading signals
        print("Generating trading signals...")
        signal_response = requests.post(
            "http://localhost:8082/api/generate-signals",
            json={"symbol": "AAPL", "data": market_data["data"]}
        )
        self.assertEqual(signal_response.status_code, 200)
        signals = signal_response.json()
        
        # Step 3: Calculate position size based on risk parameters
        print("Calculating position size...")
        risk_response = requests.post(
            "http://localhost:8083/api/calculate-position",
            json={
                "symbol": "AAPL",
                "signal_strength": signals["strength"],
                "portfolio_value": 100000,
                "risk_tolerance": "medium"
            }
        )
        self.assertEqual(risk_response.status_code, 200)
        position = risk_response.json()
        
        # Step 4: Place order
        print("Placing order...")
        order_response = requests.post(
            "http://localhost:8084/api/place-order",
            json={
                "symbol": "AAPL",
                "side": signals["direction"],
                "quantity": position["size"],
                "order_type": "market"
            }
        )
        self.assertEqual(order_response.status_code, 200)
        order = order_response.json()
        
        # Step 5: Verify order status
        print("Verifying order status...")
        status_response = requests.get(f"http://localhost:8084/api/order-status/{order['order_id']}")
        self.assertEqual(status_response.status_code, 200)
        status = status_response.json()
        
        # Verify the complete workflow
        self.assertIn("status", status)
        print(f"Order status: {status['status']}")

if __name__ == '__main__':
    unittest.main()
