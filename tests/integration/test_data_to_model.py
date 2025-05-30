import unittest
from unittest.mock import patch, MagicMock
import requests
import json
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDataToModelIntegration(unittest.TestCase):
    """Integration tests for data service to AI model pipeline"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data_service_url = "http://localhost:8081"
        self.ai_engine_url = "http://localhost:8082"
        
        # Mock data
        self.test_symbol = "AAPL"
        self.test_timeframe = "1d"
        self.test_period = "1mo"
    
    @patch('requests.get')
    def test_data_retrieval_and_prediction(self, mock_get):
        """Test that data from data service can be used by AI engine for predictions"""
        # Mock the data service response
        mock_data_response = {
            "symbol": self.test_symbol,
            "timeframe": self.test_timeframe,
            "data": [
                {"timestamp": "2023-01-01", "open": 150.0, "high": 152.0, "low": 149.0, "close": 151.0, "volume": 1000000},
                {"timestamp": "2023-01-02", "open": 151.0, "high": 153.0, "low": 150.0, "close": 152.0, "volume": 1100000},
                # More data points...
            ]
        }
        
        # Mock the AI engine response
        mock_prediction_response = {
            "symbol": self.test_symbol,
            "predictions": [
                {"timestamp": "2023-01-03", "predicted_close": 153.5, "confidence": 0.85},
                {"timestamp": "2023-01-04", "predicted_close": 154.2, "confidence": 0.82},
                # More predictions...
            ]
        }
        
        # Configure the mock to return different responses for different URLs
        def mock_get_side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            mock_response.status_code = 200
            
            if url.startswith(f"{self.data_service_url}/api/market-data"):
                mock_response.json.return_value = mock_data_response
            elif url.startswith(f"{self.ai_engine_url}/api/predict"):
                mock_response.json.return_value = mock_prediction_response
            
            return mock_response
        
        mock_get.side_effect = mock_get_side_effect
        
        # Step 1: Get market data from data service
        data_url = f"{self.data_service_url}/api/market-data/{self.test_symbol}?timeframe={self.test_timeframe}&period={self.test_period}"
        data_response = requests.get(data_url)
        self.assertEqual(data_response.status_code, 200)
        market_data = data_response.json()
        
        # Step 2: Send market data to AI engine for prediction
        prediction_url = f"{self.ai_engine_url}/api/predict/{self.test_symbol}"
        prediction_response = requests.get(prediction_url, params={"data": json.dumps(market_data["data"])})
        self.assertEqual(prediction_response.status_code, 200)
        predictions = prediction_response.json()
        
        # Verify the integration
        self.assertEqual(predictions["symbol"], self.test_symbol)
        self.assertTrue(len(predictions["predictions"]) > 0)
        self.assertIn("predicted_close", predictions["predictions"][0])
        self.assertIn("confidence", predictions["predictions"][0])

if __name__ == '__main__':
    unittest.main()
