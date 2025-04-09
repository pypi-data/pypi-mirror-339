"""
Embedding management for the recommendation system.

This module provides utilities for managing user and item embeddings,
including loading, updating, and saving embeddings.
"""

import json
import logging
import os
from typing import Dict, Optional, Tuple

import numpy as np
from llama_recommender.security.encryption import decrypt_data, encrypt_data
from llama_recommender.utils.logging import get_logger


class EmbeddingManager:
    """
    Manager for user and item embeddings.

    This class handles loading, updating, and saving embeddings for users and items,
    with support for encryption to protect sensitive embedding data.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        embedding_path: Optional[str] = None,
        use_encryption: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the embedding manager.

        Args:
            embedding_dim: Dimensionality of embeddings
            embedding_path: Path to pre-trained embeddings
            use_encryption: Whether to encrypt embeddings when saving
            logger: Logger instance
        """
        self.embedding_dim = embedding_dim
        self.use_encryption = use_encryption
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize embeddings
        self.user_embeddings: Dict[str, np.ndarray] = {}
        self.item_embeddings: Dict[str, np.ndarray] = {}

        # Load embeddings if path provided
        if embedding_path:
            self.load(embedding_path)

    def load(self, path: str) -> None:
        """
        Load embeddings from disk.

        Args:
            path: Directory path to load the embeddings from
        """
        # Load user embeddings
        user_embeddings_path = os.path.join(path, "user_embeddings.npy")
        if os.path.exists(user_embeddings_path):
            try:
                user_data = np.load(user_embeddings_path, allow_pickle=True).item()

                if self.use_encryption:
                    # Check if embeddings are encrypted
                    metadata_path = os.path.join(path, "metadata.json")
                    if os.path.exists(metadata_path):
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)

                        if metadata.get("encrypted", False):
                            # Decrypt embeddings
                            for user_id, encrypted_embedding in user_data.items():
                                user_data[user_id] = decrypt_data(encrypted_embedding)

                self.user_embeddings = user_data
                self.logger.info(f"Loaded user embeddings for {len(self.user_embeddings)} users")
            except Exception as e:
                self.logger.warning(f"Failed to load user embeddings: {e}")

        # Load item embeddings
        item_embeddings_path = os.path.join(path, "item_embeddings.npy")
        if os.path.exists(item_embeddings_path):
            try:
                item_data = np.load(item_embeddings_path, allow_pickle=True).item()

                if self.use_encryption:
                    # Check if embeddings are encrypted
                    metadata_path = os.path.join(path, "metadata.json")
                    if os.path.exists(metadata_path):
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)

                        if metadata.get("encrypted", False):
                            # Decrypt embeddings
                            for item_id, encrypted_embedding in item_data.items():
                                item_data[item_id] = decrypt_data(encrypted_embedding)

                self.item_embeddings = item_data
                self.logger.info(f"Loaded item embeddings for {len(self.item_embeddings)} items")
            except Exception as e:
                self.logger.warning(f"Failed to load item embeddings: {e}")

    def save(self, path: str) -> None:
        """
        Save embeddings to disk.

        Args:
            path: Directory path to save the embeddings
        """
        os.makedirs(path, exist_ok=True)

        # Prepare data for saving
        user_data = self.user_embeddings.copy()
        item_data = self.item_embeddings.copy()

        # Encrypt embeddings if requested
        if self.use_encryption:
            for user_id, embedding in user_data.items():
                user_data[user_id] = encrypt_data(embedding)

            for item_id, embedding in item_data.items():
                item_data[item_id] = encrypt_data(embedding)

            # Save metadata
            metadata = {"encrypted": True, "embedding_dim": self.embedding_dim}

            with open(os.path.join(path, "metadata.json"), "w") as f:
                json.dump(metadata, f)

        # Save embeddings
        np.save(os.path.join(path, "user_embeddings.npy"), user_data)
        np.save(os.path.join(path, "item_embeddings.npy"), item_data)

        self.logger.info(f"Saved embeddings to {path} (encrypted: {self.use_encryption})")

    def get_user_embedding(self, user_id: str) -> Optional[np.ndarray]:
        """
        Get the embedding for a user.

        Args:
            user_id: User identifier

        Returns:
            User embedding vector or None if not found
        """
        return self.user_embeddings.get(user_id)

    def get_item_embedding(self, item_id: str) -> Optional[np.ndarray]:
        """
        Get the embedding for an item.

        Args:
            item_id: Item identifier

        Returns:
            Item embedding vector or None if not found
        """
        return self.item_embeddings.get(item_id)

    def set_user_embedding(self, user_id: str, embedding: np.ndarray) -> None:
        """
        Set the embedding for a user.

        Args:
            user_id: User identifier
            embedding: User embedding vector
        """
        if embedding.shape[0] != self.embedding_dim:
            raise ValueError(
                f"Embedding dimension mismatch: got {embedding.shape[0]}, "
                f"expected {self.embedding_dim}"
            )

        self.user_embeddings[user_id] = embedding

    def set_item_embedding(self, item_id: str, embedding: np.ndarray) -> None:
        """
        Set the embedding for an item.

        Args:
            item_id: Item identifier
            embedding: Item embedding vector
        """
        if embedding.shape[0] != self.embedding_dim:
            raise ValueError(
                f"Embedding dimension mismatch: got {embedding.shape[0]}, "
                f"expected {self.embedding_dim}"
            )

        self.item_embeddings[item_id] = embedding

    def update_embeddings(self, model: "BaseModel") -> None:
        """
        Update embeddings from a trained model.

        Args:
            model: Trained recommendation model
        """
        from llama_recommender.core.models import BaseModel

        if not isinstance(model, BaseModel):
            raise TypeError(f"Expected BaseModel, got {type(model).__name__}")

        # Update user embeddings
        if hasattr(model, "user_embeddings"):
            self.user_embeddings.update(model.user_embeddings)

        # Update item embeddings
        if hasattr(model, "item_embeddings"):
            self.item_embeddings.update(model.item_embeddings)

        self.logger.info(
            f"Updated embeddings: {len(self.user_embeddings)} users, "
            f"{len(self.item_embeddings)} items"
        )

    def export_embeddings(
        self,
        format: str = "numpy",
        user_path: Optional[str] = None,
        item_path: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Export embeddings in a specified format.

        Args:
            format: Export format ("numpy", "json", or "csv")
            user_path: Path to save user embeddings (optional)
            item_path: Path to save item embeddings (optional)

        Returns:
            Tuple of (user_path, item_path) where files were saved
        """
        if format not in ["numpy", "json", "csv"]:
            raise ValueError(f"Unsupported format: {format}")

        if user_path is None:
            user_path = f"user_embeddings.{format.replace('numpy', 'npy')}"

        if item_path is None:
            item_path = f"item_embeddings.{format.replace('numpy', 'npy')}"

        # Export user embeddings
        if self.user_embeddings:
            if format == "numpy":
                np.save(user_path, self.user_embeddings)
            elif format == "json":
                user_data = {
                    user_id: embedding.tolist()
                    for user_id, embedding in self.user_embeddings.items()
                }
                with open(user_path, "w") as f:
                    json.dump(user_data, f)
            elif format == "csv":
                import pandas as pd

                user_data = []
                for user_id, embedding in self.user_embeddings.items():
                    row = {"user_id": user_id}
                    for i, val in enumerate(embedding):
                        row[f"dim_{i}"] = val
                    user_data.append(row)
                pd.DataFrame(user_data).to_csv(user_path, index=False)

            self.logger.info(f"Exported user embeddings to {user_path}")
        else:
            user_path = None

        # Export item embeddings
        if self.item_embeddings:
            if format == "numpy":
                np.save(item_path, self.item_embeddings)
            elif format == "json":
                item_data = {
                    item_id: embedding.tolist()
                    for item_id, embedding in self.item_embeddings.items()
                }
                with open(item_path, "w") as f:
                    json.dump(item_data, f)
            elif format == "csv":
                import pandas as pd

                item_data = []
                for item_id, embedding in self.item_embeddings.items():
                    row = {"item_id": item_id}
                    for i, val in enumerate(embedding):
                        row[f"dim_{i}"] = val
                    item_data.append(row)
                pd.DataFrame(item_data).to_csv(item_path, index=False)

            self.logger.info(f"Exported item embeddings to {item_path}")
        else:
            item_path = None

        return user_path, item_path

    def generate_random_embeddings(
        self,
        num_users: int = 100,
        num_items: int = 1000,
        user_id_prefix: str = "user_",
        item_id_prefix: str = "item_",
    ) -> None:
        """
        Generate random embeddings for testing.

        Args:
            num_users: Number of users to generate
            num_items: Number of items to generate
            user_id_prefix: Prefix for user IDs
            item_id_prefix: Prefix for item IDs
        """
        # Generate user embeddings
        for i in range(num_users):
            user_id = f"{user_id_prefix}{i}"
            embedding = np.random.normal(0, 0.1, size=self.embedding_dim)
            self.set_user_embedding(user_id, embedding)

        # Generate item embeddings
        for i in range(num_items):
            item_id = f"{item_id_prefix}{i}"
            embedding = np.random.normal(0, 0.1, size=self.embedding_dim)
            self.set_item_embedding(item_id, embedding)

        self.logger.info(f"Generated random embeddings for {num_users} users and {num_items} items")
