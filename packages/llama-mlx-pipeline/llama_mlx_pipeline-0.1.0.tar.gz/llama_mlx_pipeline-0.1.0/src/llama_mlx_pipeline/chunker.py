import os
import re
from typing import Any, Callable, Dict, List, Optional, Tuple

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from mlx.nn import functional as F

# Attempt to import the mlx_community package for model loading
# If not available, we'll provide a custom implementation
try:
    import mlx_community.transformers

    COMMUNITY_AVAILABLE = True
except ImportError:
    COMMUNITY_AVAILABLE = False


class MLXEmbeddingModel:
    """
    A wrapper for loading and using MLX embedding models.
    This class handles loading models either via mlx_community helpers
    or directly from local files.
    """

    def __init__(self, model_path: str):
        """
        Initialize the embedding model.

        Args:
            model_path: Path to the MLX model directory
        """
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.max_length = 512

        self._load_model()

    def _load_model(self):
        """Load the MLX embedding model."""
        if COMMUNITY_AVAILABLE:
            # Use mlx_community helpers if available
            self.model, self.tokenizer = mlx_community.transformers.load_model(
                self.model_path, dtype=mx.float16
            )
        else:
            # Custom loading logic when mlx_community is not available
            # This is a simplified implementation - actual implementation depends on model format
            try:
                # Attempt to load with MLX directly
                from mlx.utils import load as mlx_load

                model_path = os.path.join(self.model_path, "model.safetensors")
                config_path = os.path.join(self.model_path, "config.json")
                tokenizer_path = os.path.join(self.model_path, "tokenizer.json")

                # Load tokenizer
                from transformers import AutoTokenizer

                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

                # Load model weights
                weights = mlx_load(model_path)

                # Stub model class - would need to be implemented based on model architecture
                self.model = SimpleEmbeddingModel(weights)
            except Exception as e:
                raise RuntimeError(f"Failed to load embedding model: {str(e)}")

    def encode(self, texts: List[str], **kwargs) -> mx.array:
        """
        Encode texts to embeddings.

        Args:
            texts: List of texts to encode
            **kwargs: Additional arguments to pass to the model

        Returns:
            mx.array: Array of embeddings
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model or tokenizer not loaded.")

        # Process each text individually and batch for efficiency
        embeddings = []

        for text in texts:
            # Tokenize input
            inputs = self.tokenizer(
                text, return_tensors="np", padding=True, truncation=True, max_length=self.max_length
            )

            # Convert to MLX arrays
            input_ids = mx.array(inputs["input_ids"])
            attention_mask = mx.array(inputs["attention_mask"])

            # Get embeddings from the model
            embedding = self._get_embedding(input_ids, attention_mask)
            embeddings.append(embedding)

        # Stack and normalize embeddings
        embeddings = mx.stack(embeddings)
        embeddings = F.normalize(embeddings, p=2, dim=1)

        return embeddings

    def _get_embedding(self, input_ids: mx.array, attention_mask: mx.array) -> mx.array:
        """
        Get embeddings from the model.

        Args:
            input_ids: Token IDs
            attention_mask: Attention mask

        Returns:
            mx.array: Embedding
        """
        # Get model outputs
        outputs = self.model(input_ids, attention_mask)

        # Mean pooling - take attention mask into account for averaging
        # Use MLX operations for the pooling
        input_mask_expanded = attention_mask.reshape(
            attention_mask.shape[0], attention_mask.shape[1], 1
        )
        sum_embeddings = mx.sum(outputs * input_mask_expanded, axis=1)
        sum_mask = mx.sum(input_mask_expanded, axis=1)

        # Handle case where sum_mask is 0
        sum_mask = mx.maximum(sum_mask, mx.array(1e-9, dtype=sum_mask.dtype))

        # Get mean embeddings
        mean_embeddings = sum_embeddings / sum_mask

        return mean_embeddings


class SimpleEmbeddingModel(nn.Module):
    """
    A simple embedding model implementation for MLX.
    This is a stub and would need to be expanded based on the actual model architecture.
    """

    def __init__(self, weights: Dict[str, mx.array]):
        super().__init__()
        self.weights = weights
        # This is a simplified implementation
        # A real implementation would define the model architecture

    def __call__(self, input_ids: mx.array, attention_mask: mx.array = None) -> mx.array:
        """
        Forward pass through the model.

        Args:
            input_ids: Token IDs
            attention_mask: Attention mask

        Returns:
            mx.array: Embeddings
        """
        # This is a placeholder - actual implementation depends on model architecture
        # For now, return a random embedding matrix
        batch_size, seq_len = input_ids.shape
        embedding_dim = 384  # Common for miniLM models

        return mx.random.normal((batch_size, seq_len, embedding_dim))


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
    """
    Split text into chunks based on character count.

    Args:
        text: Text to chunk
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Overlap between chunks in characters

    Returns:
        List[str]: List of text chunks
    """
    if not text or chunk_size <= 0:
        return []

    # Clean text by removing extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split text into sentences or paragraphs
    splits = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = []
    current_length = 0

    for split in splits:
        split_length = len(split)

        # If a single split is longer than chunk_size, further split it
        if split_length > chunk_size:
            # Add any current chunk if it exists
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                # Keep the last part for overlap if it exists
                overlap_splits = current_chunk[-1:] if chunk_overlap > 0 else []
                current_chunk = overlap_splits
                current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1

            # Split the long text
            words = split.split(" ")
            temp_chunk = []
            temp_length = 0

            for word in words:
                word_length = len(word)
                if temp_length + word_length + (1 if temp_chunk else 0) <= chunk_size:
                    temp_chunk.append(word)
                    temp_length += word_length + (1 if temp_chunk else 0)
                else:
                    if temp_chunk:
                        chunks.append(" ".join(temp_chunk))
                    temp_chunk = [word]
                    temp_length = word_length

            if temp_chunk:
                current_chunk = temp_chunk
                current_length = temp_length

        # Normal case: add split to current chunk
        elif current_length + split_length + (1 if current_chunk else 0) <= chunk_size:
            current_chunk.append(split)
            current_length += split_length + (1 if current_chunk else 0)
        else:
            # Current chunk is full, start a new one
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            # For overlap, keep some of the previous content
            if chunk_overlap > 0:
                # Calculate how many characters to keep for overlap
                overlap_chars = 0
                overlap_splits = []

                for s in reversed(current_chunk):
                    if overlap_chars + len(s) + 1 <= chunk_overlap:
                        overlap_splits.insert(0, s)
                        overlap_chars += len(s) + 1
                    else:
                        break

                current_chunk = overlap_splits + [split]
                current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1
            else:
                current_chunk = [split]
                current_length = split_length

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def cosine_similarity(a: mx.array, b: mx.array) -> float:
    """
    Calculate cosine similarity between two vectors using MLX.

    Args:
        a: First vector
        b: Second vector

    Returns:
        float: Cosine similarity
    """
    # Ensure the vectors are normalized
    a_norm = F.normalize(a, p=2, dim=0)
    b_norm = F.normalize(b, p=2, dim=0)

    # Calculate cosine similarity
    similarity = mx.sum(a_norm * b_norm)

    # Convert to float
    return float(similarity)


def chunk_semantic(
    text: str,
    chunk_size: int = 100,
    chunk_overlap: int = 20,
    embedding_model_path: Optional[str] = None,
) -> List[str]:
    """
    Chunks text based on semantic similarity using embeddings (placeholder).

    Args:
        text: The input text.
        chunk_size: Target chunk size in tokens (approximate).
        chunk_overlap: Overlap between chunks in tokens (approximate).
        embedding_model_path: Path to the embedding model.

    Returns:
        List of text chunks.
    """
    if not HAS_MLX or not embedding_model_path:
        logger.warning("MLX or embedding model not available. Using fixed-size chunking.")
        return chunk_fixed_size(text, chunk_size, chunk_overlap)

    # Placeholder for actual semantic chunking logic
    logger.info(f"Performing semantic chunking (placeholder) on text length {len(text)}")
    # In a real implementation: Load model, embed sentences/paragraphs, cluster embeddings
    # For now, fall back to fixed size
    return chunk_fixed_size(text, chunk_size, chunk_overlap)
