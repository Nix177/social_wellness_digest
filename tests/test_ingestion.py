import unittest
import os
import sys

# Add parent dir to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.DataIngestionService import DataIngestionService

class TestDataIngestion(unittest.TestCase):
    def setUp(self):
        self.service = DataIngestionService(["Test_Source"])

    def test_fetch_mock_data(self):
        """Test that mock data generation returns correct structure."""
        data = self.service.fetch_mock()
        self.assertTrue(len(data) > 0)
        first_item = data[0]
        self.assertIn("id", first_item)
        self.assertIn("content", first_item)
        self.assertEqual(first_item["source"], "MockStream")

    def test_load_seeds(self):
        """Test that seeds are loaded (if file exists) or handled gracefully."""
        # This test assumes seeds.json might or might not exist in test env, 
        # but the method should return a list regardless.
        seeds = self.service.load_seeds()
        self.assertIsInstance(seeds, list)
        if len(seeds) > 0:
            self.assertIn("source", seeds[0])

    def test_standardization(self):
        """Test that data standardization works correctly."""
        raw_input = [{
            "id": "123",
            "source": "Test",
            "content": "Hello World",
            "author": "Me",
            "timestamp": 1234567890.0,
            "raw_metadata": {"foo": "bar"}
        }]
        
        standardized = self.service.standardize_data(raw_input)
        self.assertEqual(len(standardized), 1)
        item = standardized[0]
        
        self.assertEqual(item["text"], "Hello World")
        self.assertEqual(item["metadata"]["author"], "Me")
        self.assertEqual(item["metadata"]["extra"]["foo"], "bar")

if __name__ == '__main__':
    unittest.main()
