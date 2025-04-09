import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mlxpipeline.chunker import (
    MLXEmbeddingModel,
    chunk_semantic,
    chunk_text,
    cosine_similarity,
)


class TestChunker(unittest.TestCase):
    """Test cases for chunker module functions."""

    def test_chunk_text(self):
        """Test text chunking."""
        # Test with empty text
        self.assertEqual(chunk_text(""), [])

        # Test with short text
        short_text = "This is a short test text."
        self.assertEqual(chunk_text(short_text, chunk_size=100), [short_text])

        # Test with longer text that needs chunking
        long_text = "This is the first sentence. This is the second sentence. " * 20
        chunks = chunk_text(long_text, chunk_size=100, chunk_overlap=20)

        # Check that we have multiple chunks
        self.assertGreater(len(chunks), 1)

        # Check chunk sizes
        for chunk in chunks:
            self.assertLessEqual(
                len(chunk), 100 + 20
            )  # Allow for some flexibility with sentence boundaries

        # Check that all content is preserved (approximately)
        combined = " ".join(chunks)
        self.assertGreaterEqual(
            len(combined), len(long_text) * 0.9
        )  # Allow for some whitespace differences

    @patch("mlxpipeline.chunker.MLXEmbeddingModel")
    def test_chunk_semantic(self, mock_embedding_model):
        """Test semantic chunking."""
        # Mock the embedding model
        mock_model_instance = MagicMock()
        mock_embedding_model.return_value = mock_model_instance

        # Mock the encode method to return fake embeddings
        import mlx.core as mx

        mock_model_instance.encode.return_value = mx.array(np.random.random((3, 384)))

        # Test text to chunk
        text = (
            "First paragraph about topic A. More about topic A. "
            "Second paragraph about topic B. More about topic B. "
            "Third paragraph about topic C. More about topic C."
        )

        # Call the function
        chunks = chunk_semantic(text, chunk_size=50, chunk_overlap=10)

        # Check results
        self.assertIsInstance(chunks, list)
        mock_embedding_model.assert_called_once()
        mock_model_instance.encode.assert_called_once()

    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        import mlx.core as mx

        # Test with orthogonal vectors (should be 0)
        vec1 = mx.array([1.0, 0.0, 0.0])
        vec2 = mx.array([0.0, 1.0, 0.0])
        self.assertAlmostEqual(cosine_similarity(vec1, vec2), 0.0)

        # Test with identical vectors (should be 1)
        vec3 = mx.array([0.5, 0.5, 0.5])
        self.assertAlmostEqual(cosine_similarity(vec3, vec3), 1.0)

        # Test with vectors at 45 degrees (cos 45° = 1/√2 ≈ 0.7071)
        vec4 = mx.array([1.0, 0.0])
        vec5 = mx.array([1.0, 1.0])
        self.assertAlmostEqual(cosine_similarity(vec4, vec5), 0.7071, places=4)

    @patch("mlxpipeline.chunker.COMMUNITY_AVAILABLE", False)
    @patch("mlxpipeline.chunker.mlx_load")
    @patch("transformers.AutoTokenizer.from_pretrained")
    def test_mlx_embedding_model_custom_loading(self, mock_tokenizer, mock_mlx_load):
        """Test custom loading of MLX embedding model when community package is not available."""
        # Mock the dependencies
        mock_tokenizer.return_value = MagicMock()
        mock_mlx_load.return_value = {"weights": "mock_weights"}

        # Patch os.path.join to return predictable paths
        with patch("os.path.join", lambda *args: "/".join(args)):
            # This should not raise an exception
            with patch("mlxpipeline.chunker.SimpleEmbeddingModel") as mock_simple_model:
                mock_simple_model.return_value = MagicMock()
                model = MLXEmbeddingModel("/path/to/model")

                # Check that the model was loaded
                self.assertIsNotNone(model.model)
                self.assertIsNotNone(model.tokenizer)

                # Check that the right functions were called
                mock_tokenizer.assert_called_once_with("/path/to/model")
                mock_simple_model.assert_called_once()


if __name__ == "__main__":
    unittest.main()
