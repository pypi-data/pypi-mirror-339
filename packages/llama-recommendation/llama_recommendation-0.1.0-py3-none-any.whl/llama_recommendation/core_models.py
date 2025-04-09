"""
Core model implementations for the recommendation system.

This module provides the base model interfaces and concrete implementations
for different recommendation approaches, including multi-modal, graph-based,
and causal recommendation models.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from llama_recommender.utils.logging import get_logger


class BaseModel(ABC):
    """
    Abstract base class for recommendation models.

    All recommendation models should inherit from this class and implement
    the required methods.
    """

    def __init__(self, embedding_dim: int = 128, logger: Optional[logging.Logger] = None):
        """
        Initialize the base model.

        Args:
            embedding_dim: Dimensionality of embeddings
            logger: Logger instance
        """
        self.embedding_dim = embedding_dim
        self.logger = logger or get_logger(self.__class__.__name__)
        self.is_trained = False

    @abstractmethod
    def predict(
        self,
        user_id: str,
        item_ids: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> np.ndarray:
        """
        Predict scores for a list of items.

        Args:
            user_id: User identifier
            item_ids: List of item identifiers
            context: Optional contextual information

        Returns:
            Array of prediction scores for each item
        """
        pass

    @abstractmethod
    def encode_user(self, user_id: str, context: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Encode a user into a vector representation.

        Args:
            user_id: User identifier
            context: Optional contextual information

        Returns:
            User embedding vector
        """
        pass

    @abstractmethod
    def encode_item(self, item_id: str) -> np.ndarray:
        """
        Encode an item into a vector representation.

        Args:
            item_id: Item identifier

        Returns:
            Item embedding vector
        """
        pass

    @abstractmethod
    def _forward(self, user_embedding: mx.array, item_embedding: mx.array) -> mx.array:
        """
        Forward pass of the model.

        Args:
            user_embedding: User embedding tensor
            item_embedding: Item embedding tensor

        Returns:
            Score tensor
        """
        pass

    def save(self, path: str) -> None:
        """
        Save model to disk.

        Args:
            path: Directory path to save the model
        """
        os.makedirs(path, exist_ok=True)

        # Save model metadata
        metadata = {
            "model_type": self.__class__.__name__,
            "embedding_dim": self.embedding_dim,
            "is_trained": self.is_trained,
        }

        with open(os.path.join(path, "metadata.json"), "w") as f:
            json.dump(metadata, f)

        self.logger.info(f"Saved model metadata to {path}")

    @classmethod
    def load(cls, path: str) -> "BaseModel":
        """
        Load model from disk.

        Args:
            path: Directory path to load the model from

        Returns:
            Loaded model instance
        """
        # Load model metadata
        with open(os.path.join(path, "metadata.json"), "r") as f:
            metadata = json.load(f)

        # Determine model class
        model_type = metadata["model_type"]
        model_classes = {
            "MultiModalModel": MultiModalModel,
            "GraphModel": GraphModel,
            "CausalModel": CausalModel,
        }

        if model_type not in model_classes:
            raise ValueError(f"Unknown model type: {model_type}")

        # Create model instance
        model_class = model_classes[model_type]
        model = model_class(embedding_dim=metadata["embedding_dim"])
        model.is_trained = metadata["is_trained"]

        # Load model-specific data (implemented by subclasses)
        model._load_model_data(path)

        return model

    @abstractmethod
    def _load_model_data(self, path: str) -> None:
        """
        Load model-specific data from disk.

        Args:
            path: Directory path to load the model data from
        """
        pass


class MLXModel(nn.Module):
    """MLX neural network module for recommendation."""

    def __init__(self, embedding_dim: int = 128, hidden_dims: List[int] = [256, 128, 64]):
        """
        Initialize the MLX model.

        Args:
            embedding_dim: Dimensionality of embeddings
            hidden_dims: List of hidden layer dimensions
        """
        super().__init__()

        # Create MLP layers
        layers = []
        input_dim = embedding_dim * 2  # Concatenated user and item embeddings

        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(input_dim, hidden_dim))
            layers.append(nn.ReLU())
            input_dim = hidden_dim

        # Final output layer
        layers.append(nn.Linear(input_dim, 1))

        self.mlp = nn.Sequential(*layers)

    def __call__(self, user_embedding: mx.array, item_embedding: mx.array) -> mx.array:
        """
        Forward pass through the model.

        Args:
            user_embedding: User embedding tensor
            item_embedding: Item embedding tensor

        Returns:
            Score tensor
        """
        # Concatenate embeddings
        x = mx.concatenate([user_embedding, item_embedding], axis=1)

        # Forward pass through MLP
        return self.mlp(x)


class MultiModalModel(BaseModel):
    """
    Multi-modal recommendation model that handles different types of content.

    This model can process and recommend items with text, images, or mixed content.
    It uses separate encoders for different modalities and combines them for scoring.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        user_embedding_path: Optional[str] = None,
        item_embedding_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the multi-modal model.

        Args:
            embedding_dim: Dimensionality of embeddings
            user_embedding_path: Path to pre-trained user embeddings
            item_embedding_path: Path to pre-trained item embeddings
            logger: Logger instance
        """
        super().__init__(embedding_dim=embedding_dim, logger=logger)

        # Initialize MLX model
        self.model = MLXModel(embedding_dim=embedding_dim)

        # Initialize embeddings
        self.user_embeddings = {}
        self.item_embeddings = {}
