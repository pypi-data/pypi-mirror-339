"""
Text encoder for the multi-modal recommendation system.

This module provides a text encoder that converts text into vector
representations for use in the recommendation system.
"""

import logging
import os
from typing import List, Optional

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from llama_recommender.utils.logging import get_logger


class TextEncoder:
    """
    Text encoder for converting text to vector representations.

    This class encodes text content into fixed-dimensional vectors
    for use in the multi-modal recommendation system.
    """

    def __init__(
        self,
        output_dim: int = 128,
        max_length: int = 512,
        pretrained_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the text encoder.

        Args:
            output_dim: Dimensionality of the output embeddings
            max_length: Maximum sequence length to process
            pretrained_path: Path to pretrained encoder weights
            logger: Logger instance
        """
        self.output_dim = output_dim
        self.max_length = max_length
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize MLX model
        self.model = self._create_model()

        # Load pretrained weights if provided
        if pretrained_path:
            self._load_pretrained(pretrained_path)

    def _create_model(self) -> nn.Module:
        """
        Create the MLX model for text encoding.

        Returns:
            MLX module for text encoding
        """

        class TextEncoderModel(nn.Module):
            """MLX model for text encoding."""

            def __init__(
                self,
                embedding_dim: int = 128,
                hidden_dim: int = 256,
                output_dim: int = 128,
            ):
                super().__init__()

                # Simple tokenizer (character-level for demonstration)
                self.vocab_size = 128  # ASCII characters

                # Embedding layer
                self.embedding = nn.Embedding(self.vocab_size, embedding_dim)

                # Processing layers
                self.conv1 = nn.Conv1d(embedding_dim, hidden_dim, kernel_size=3, padding=1)
                self.act1 = nn.ReLU()
                self.pool1 = nn.MaxPool1d(kernel_size=2, stride=2)

                self.conv2 = nn.Conv1d(hidden_dim, hidden_dim, kernel_size=3, padding=1)
                self.act2 = nn.ReLU()
                self.pool2 = nn.MaxPool1d(kernel_size=2, stride=2)

                # Output projection
                self.fc = nn.Linear(hidden_dim, output_dim)

            def __call__(self, x: mx.array) -> mx.array:
                # Embedding lookup
                x = self.embedding(x)

                # Reshape for 1D convolution (batch, seq, channels) -> (batch, channels, seq)
                x = mx.transpose(x, (0, 2, 1))

                # First conv block
                x = self.conv1(x)
                x = self.act1(x)
                x = self.pool1(x)

                # Second conv block
                x = self.conv2(x)
                x = self.act2(x)
                x = self.pool2(x)

                # Global pooling
                x = mx.mean(x, axis=2)  # (batch, channels)

                # Output projection
                x = self.fc(x)

                return x

        return TextEncoderModel(embedding_dim=128, hidden_dim=256, output_dim=self.output_dim)

    def _load_pretrained(self, path: str) -> None:
        """
        Load pretrained weights.

        Args:
            path: Path to pretrained weights
        """
        try:
            weights = mx.load(path)
            self.model.update(weights)
            self.logger.info(f"Loaded pretrained text encoder from {path}")
        except Exception as e:
            self.logger.warning(f"Failed to load pretrained weights: {e}")

    def _tokenize(self, text: str, max_length: Optional[int] = None) -> np.ndarray:
        """
        Tokenize text into character IDs.

        Args:
            text: Input text
            max_length: Maximum sequence length (if None, uses self.max_length)

        Returns:
            NumPy array of token IDs
        """
        max_length = max_length or self.max_length

        # Simple character-level tokenization (for demonstration)
        char_ids = np.array([min(ord(c), 127) for c in text[:max_length]])

        # Pad to max_length
        if len(char_ids) < max_length:
            char_ids = np.pad(
                char_ids,
                (0, max_length - len(char_ids)),
                mode="constant",
                constant_values=0,
            )

        return char_ids

    def encode(self, text: str) -> np.ndarray:
        """
        Encode text into a vector representation.

        Args:
            text: Input text

        Returns:
            Vector representation of the text
        """
        # Tokenize text
        tokens = self._tokenize(text)
        tokens_mx = mx.array(tokens.reshape(1, -1))

        # Forward pass through model
        with mx.eval_mode():
            embedding = self.model(tokens_mx)

        # Convert to NumPy array
        return np.array(embedding[0])

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """
        Encode a batch of texts into vector representations.

        Args:
            texts: List of input texts

        Returns:
            Matrix of text vector representations
        """
        # Tokenize texts
        batch_tokens = np.stack([self._tokenize(text) for text in texts])
        batch_tokens_mx = mx.array(batch_tokens)

        # Forward pass through model
        with mx.eval_mode():
            embeddings = self.model(batch_tokens_mx)

        # Convert to NumPy array
        return np.array(embeddings)

    def save(self, path: str) -> None:
        """
        Save encoder to disk.

        Args:
            path: Path to save the encoder
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Save model weights
        mx.save(path, self.model.parameters())

        self.logger.info(f"Saved text encoder to {path}")

    @classmethod
    def load(cls, path: str, output_dim: int = 128) -> "TextEncoder":
        """
        Load encoder from disk.

        Args:
            path: Path to load the encoder from
            output_dim: Dimensionality of the output embeddings

        Returns:
            Loaded TextEncoder instance
        """
        encoder = cls(output_dim=output_dim)
        encoder._load_pretrained(path)
        return encoder

    def similarity(self, text1: str, text2: str) -> float:
        """
        Compute similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity score (0-1)
        """
        # Encode texts
        vec1 = self.encode(text1)
        vec2 = self.encode(text2)

        # Compute cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        return dot_product / (norm1 * norm2)

    def initialize_with_fasttext(self, fasttext_path: str) -> None:
        """
        Initialize word embeddings with pre-trained FastText embeddings.

        Args:
            fasttext_path: Path to FastText embeddings
        """
        # This is a stub implementation
        # In a real implementation, this would load FastText embeddings
        # and initialize the embedding layer of the model
        self.logger.info(f"Initializing with FastText embeddings from {fasttext_path}")
