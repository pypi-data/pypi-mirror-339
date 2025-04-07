import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from crm_benchmark_lib import BenchmarkClient


class TestBenchmarkClient(unittest.TestCase):
    
    def setUp(self):
        """Set up a client instance for testing."""
        self.client = BenchmarkClient("test_api_key")
    
    @patch('requests.Session.post')
    def test_authenticate(self, mock_post):
        """Test authentication endpoint."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "token": "test_token",
            "username": "test_user",
            "datasets": [{"id": "dataset_1"}, {"id": "dataset_2"}]
        }
        mock_post.return_value = mock_response
        
        # Call authenticate
        response = self.client.authenticate("TestAgent")
        
        # Verify the call
        mock_post.assert_called_once()
        self.assertEqual(self.client.auth_token, "test_token")
        self.assertEqual(self.client.username, "test_user")
        self.assertEqual(len(self.client.datasets), 2)
    
    @patch('requests.Session.post')
    def test_load_dataset(self, mock_post):
        """Test dataset loading."""
        # Set up authentication
        self.client.auth_token = "test_token"
        
        # Mock dataset response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "token": "dataset_token",
            "question": "Test question?",
            "total_questions": 5,
            "data": [{"id": 1, "name": "Test"}]
        }
        mock_post.return_value = mock_response
        
        # Call load_dataset
        response = self.client.load_dataset("dataset_1")
        
        # Verify the call
        mock_post.assert_called_once()
        self.assertIsInstance(response["data"], pd.DataFrame)
        self.assertEqual(response["question"], "Test question?")
    
    def test_simple_agent_function(self):
        """Test a simple agent function that would be used with the client."""
        def simple_agent(question, data):
            """A simple test agent that just returns a fixed answer."""
            return "This is a test answer"
        
        # Test the function
        question = "What is the test question?"
        data = pd.DataFrame({"id": [1, 2], "value": ["a", "b"]})
        answer = simple_agent(question, data)
        
        self.assertEqual(answer, "This is a test answer")


if __name__ == "__main__":
    unittest.main() 