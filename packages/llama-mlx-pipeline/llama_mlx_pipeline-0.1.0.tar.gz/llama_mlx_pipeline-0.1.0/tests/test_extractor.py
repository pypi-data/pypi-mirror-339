import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mlxpipeline.extract import (
    MLXModelManager,
    extract_from_chunk,
    extract_json_from_response,
)


class TestExtractor(unittest.TestCase):
    """Test cases for extract module functions."""

    def test_extract_json_from_response(self):
        """Test JSON extraction from model response."""
        # Test with JSON in markdown code block
        md_response = """
        Here's the extracted information:
        ```json
        {
            "name": "John Smith",
            "age": 42,
            "occupation": "Software Engineer"
        }
        ```
        """
        json_str = extract_json_from_response(md_response)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["name"], "John Smith")
        self.assertEqual(parsed["age"], 42)

        # Test with raw JSON
        raw_response = """
        {
            "name": "Jane Doe",
            "age": 35,
            "occupation": "Data Scientist"
        }
        """
        json_str = extract_json_from_response(raw_response)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["name"], "Jane Doe")
        self.assertEqual(parsed["age"], 35)

        # Test with invalid JSON
        invalid_response = "This is not JSON"
        json_str = extract_json_from_response(invalid_response)
        self.assertEqual(json_str, invalid_response)

    @patch("mlxpipeline.extract.MLXModelManager")
    @patch("mlx.lm.generate")
    def test_extract_from_chunk(self, mock_generate, mock_model_manager):
        """Test extraction from text chunk."""
        # Create a mock model and tokenizer
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_tokenizer.encode.return_value = [1, 2, 3]
        mock_tokenizer.decode.return_value = '{"name": "Test", "age": 25}'

        # Set up the mock model manager
        mock_manager_instance = MagicMock()
        mock_model_manager.return_value = mock_manager_instance
        mock_manager_instance.get_llm.return_value = (mock_model, mock_tokenizer)

        # Create a test schema and chunk
        schema = '{"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "number"}}}'
        chunk = "This is a test chunk about Test who is 25 years old."

        # Call the function
        result = extract_from_chunk(chunk, schema)

        # Verify expected behavior
        mock_manager_instance.get_llm.assert_called_once()
        mock_tokenizer.encode.assert_called_once()
        mock_generate.assert_called_once()
        mock_tokenizer.decode.assert_called_once()

        # Check the result
        parsed = json.loads(result)
        self.assertEqual(parsed["name"], "Test")
        self.assertEqual(parsed["age"], 25)

    def test_mlx_model_manager_singleton(self):
        """Test that MLXModelManager is a singleton."""
        manager1 = MLXModelManager()
        manager2 = MLXModelManager()

        # Verify both instances are the same object
        self.assertIs(manager1, manager2)


if __name__ == "__main__":
    unittest.main()
