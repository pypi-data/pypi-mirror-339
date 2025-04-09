"""
Multi-modal encoder for the recommendation system.

This module provides a multi-modal encoder that combines representations
from different modalities (text, images) into a unified representation.
"""

import logging
import os
from typing import List, Optional, Union

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from llama_recommender.encoders.image_encoder import ImageEncoder
from llama_recommender.encoders.text_encoder import TextEncoder
from llama_recommender.utils.logging import get_logger
from PIL import Image


class MultiModalEncoder:
    """
    Multi-modal encoder for combining text and image representations.

    This class combines encodings from different modalities (text, images)
    into a unified representation for multi-modal recommendation.
    """

    def __init__(
        self,
        text_encoder: Optional[TextEncoder] = None,
        image_encoder: Optional[ImageEncoder] = None,
        output_dim: int = 128,
        fusion_method: str = "concat_project",
        pretrained_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the multi-modal encoder.

        Args:
            text_encoder: Text encoder instance
            image_encoder: Image encoder instance
            output_dim: Dimensionality of the output embeddings
            fusion_method: Method for fusing modalities ('concat_project', 'sum', or 'attention')
            pretrained_path: Path to pretrained encoder weights
            logger: Logger instance
        """
        self.output_dim = output_dim
        self.fusion_method = fusion_method
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize individual encoders if not provided
        self.text_encoder = text_encoder or TextEncoder(output_dim=output_dim)
        self.image_encoder = image_encoder or ImageEncoder(output_dim=output_dim)

        # Check fusion method
        valid_fusion_methods = ["concat_project", "sum", "attention"]
        if fusion_method not in valid_fusion_methods:
            raise ValueError(
                f"Invalid fusion method: {fusion_method}. "
                f"Valid options are: {', '.join(valid_fusion_methods)}"
            )

        # Initialize fusion model
        self.model = self._create_fusion_model()

        # Load pretrained weights if provided
        if pretrained_path:
            self._load_pretrained(pretrained_path)

    def _create_fusion_model(self) -> nn.Module:
        """
        Create the MLX model for multi-modal fusion.

        Returns:
            MLX module for multi-modal fusion
        """

        class ConcatProjectFusion(nn.Module):
            """Fusion model that concatenates encodings and projects to output dimension."""

            def __init__(self, input_dim: int, output_dim: int):
                super().__init__()
                self.fc = nn.Linear(input_dim, output_dim)
                self.norm = nn.LayerNorm(output_dim)

            def __call__(self, encodings: List[mx.array]) -> mx.array:
                # Concatenate encodings
                concat = mx.concatenate(encodings, axis=1)

                # Project to output dimension
                output = self.fc(concat)
                output = self.norm(output)

                return output

        class SumFusion(nn.Module):
            """Fusion model that sums encodings."""

            def __init__(self, input_dim: int, output_dim: int):
                super().__init__()
                # Projection layers to ensure consistent dimensions
                self.projections = [nn.Linear(input_dim, output_dim) for _ in range(2)]
                self.norm = nn.LayerNorm(output_dim)

            def __call__(self, encodings: List[mx.array]) -> mx.array:
                # Project each encoding to output dimension
                projected = [proj(enc) for proj, enc in zip(self.projections, encodings)]

                # Sum projected encodings
                output = projected[0]
                for i in range(1, len(projected)):
                    output = output + projected[i]

                # Normalize
                output = self.norm(output)

                return output

        class AttentionFusion(nn.Module):
            """Fusion model that uses attention to combine encodings."""

            def __init__(self, input_dim: int, output_dim: int):
                super().__init__()
                # Projection layers to ensure consistent dimensions
                self.projections = [nn.Linear(input_dim, output_dim) for _ in range(2)]

                # Attention weights
                self.attention = nn.Linear(output_dim, 1)

                # Output normalization
                self.norm = nn.LayerNorm(output_dim)

            def __call__(self, encodings: List[mx.array]) -> mx.array:
                # Project each encoding to output dimension
                projected = [proj(enc) for proj, enc in zip(self.projections, encodings)]

                # Stack projected encodings
                stacked = mx.stack(projected, axis=1)  # (batch, num_modalities, output_dim)

                # Compute attention scores
                attention_scores = self.attention(stacked)  # (batch, num_modalities, 1)
                attention_weights = mx.softmax(
                    attention_scores, axis=1
                )  # (batch, num_modalities, 1)

                # Apply attention weights
                weighted = stacked * attention_weights  # (batch, num_modalities, output_dim)
                output = mx.sum(weighted, axis=1)  # (batch, output_dim)

                # Normalize
                output = self.norm(output)

                return output

        # Create fusion model based on specified method
        if self.fusion_method == "concat_project":
            # Input dimension is sum of individual encoder dimensions
            input_dim = self.text_encoder.output_dim + self.image_encoder.output_dim
            return ConcatProjectFusion(input_dim, self.output_dim)
        elif self.fusion_method == "sum":
            # Use consistent dimension for both encoders
            input_dim = max(self.text_encoder.output_dim, self.image_encoder.output_dim)
            return SumFusion(input_dim, self.output_dim)
        elif self.fusion_method == "attention":
            # Use consistent dimension for both encoders
            input_dim = max(self.text_encoder.output_dim, self.image_encoder.output_dim)
            return AttentionFusion(input_dim, self.output_dim)

    def _load_pretrained(self, path: str) -> None:
        """
        Load pretrained weights.

        Args:
            path: Path to pretrained weights
        """
        try:
            weights = mx.load(path)
            self.model.update(weights)
            self.logger.info(f"Loaded pretrained multi-modal encoder from {path}")
        except Exception as e:
            self.logger.warning(f"Failed to load pretrained weights: {e}")

    def encode(
        self,
        text: Optional[str] = None,
        image: Optional[Union[str, Image.Image, np.ndarray]] = None,
    ) -> np.ndarray:
        """
        Encode text and/or image into a unified vector representation.

        Args:
            text: Input text (optional)
            image: Input image (optional)

        Returns:
            Vector representation of the multi-modal input
        """
        if text is None and image is None:
            raise ValueError("At least one of text or image must be provided")

        # Encode text if provided
        text_embedding = None
        if text is not None:
            text_embedding = self.text_encoder.encode(text)

        # Encode image if provided
        image_embedding = None
        if image is not None:
            image_embedding = self.image_encoder.encode(image)

        # Handle single modality case
        if text_embedding is None:
            return image_embedding
        if image_embedding is None:
            return text_embedding

        # Convert embeddings to MLX arrays
        text_embedding_mx = mx.array(text_embedding.reshape(1, -1))
        image_embedding_mx = mx.array(image_embedding.reshape(1, -1))

        # Apply fusion model
        with mx.eval_mode():
            fused_embedding = self.model([text_embedding_mx, image_embedding_mx])

        # Convert to NumPy array
        return np.array(fused_embedding[0])

    def encode_batch(
        self,
        texts: Optional[List[str]] = None,
        images: Optional[List[Union[str, Image.Image, np.ndarray]]] = None,
    ) -> np.ndarray:
        """
        Encode batches of text and/or images into unified vector representations.

        Args:
            texts: List of input texts (optional)
            images: List of input images (optional)

        Returns:
            Matrix of multi-modal vector representations
        """
        if texts is None and images is None:
            raise ValueError("At least one of texts or images must be provided")

        # Check batch sizes
        batch_size = None
        if texts is not None:
            batch_size = len(texts)
        if images is not None:
            if batch_size is not None and len(images) != batch_size:
                raise ValueError(f"Batch size mismatch: {batch_size} texts vs {len(images)} images")
            batch_size = len(images)

        # Handle single modality case
        if texts is None:
            return self.image_encoder.encode_batch(images)
        if images is None:
            return self.text_encoder.encode_batch(texts)

        # Encode each modality
        text_embeddings = self.text_encoder.encode_batch(texts)
        image_embeddings = self.image_encoder.encode_batch(images)

        # Convert embeddings to MLX arrays
        text_embeddings_mx = mx.array(text_embeddings)
        image_embeddings_mx = mx.array(image_embeddings)

        # Apply fusion model
        with mx.eval_mode():
            fused_embeddings = self.model([text_embeddings_mx, image_embeddings_mx])

        # Convert to NumPy array
        return np.array(fused_embeddings)

    def save(self, path: str) -> None:
        """
        Save encoder to disk.

        Args:
            path: Directory path to save the encoder
        """
        os.makedirs(path, exist_ok=True)

        # Save fusion model weights
        mx.save(os.path.join(path, "fusion_model.npz"), self.model.parameters())

        # Save individual encoders
        self.text_encoder.save(os.path.join(path, "text_encoder.npz"))
        self.image_encoder.save(os.path.join(path, "image_encoder.npz"))

        # Save configuration
        import json

        config = {"output_dim": self.output_dim, "fusion_method": self.fusion_method}
        with open(os.path.join(path, "config.json"), "w") as f:
            json.dump(config, f)

        self.logger.info(f"Saved multi-modal encoder to {path}")

    @classmethod
    def load(cls, path: str) -> "MultiModalEncoder":
        """
        Load encoder from disk.

        Args:
            path: Directory path to load the encoder from

        Returns:
            Loaded MultiModalEncoder instance
        """
        # Load configuration
        import json

        with open(os.path.join(path, "config.json"), "r") as f:
            config = json.load(f)

        # Load individual encoders
        text_encoder = TextEncoder.load(
            os.path.join(path, "text_encoder.npz"), output_dim=config["output_dim"]
        )

        image_encoder = ImageEncoder.load(
            os.path.join(path, "image_encoder.npz"), output_dim=config["output_dim"]
        )

        # Create instance
        encoder = cls(
            text_encoder=text_encoder,
            image_encoder=image_encoder,
            output_dim=config["output_dim"],
            fusion_method=config["fusion_method"],
        )

        # Load fusion model weights
        encoder._load_pretrained(os.path.join(path, "fusion_model.npz"))

        return encoder

    def similarity(
        self,
        text1: Optional[str] = None,
        image1: Optional[Union[str, Image.Image, np.ndarray]] = None,
        text2: Optional[str] = None,
        image2: Optional[Union[str, Image.Image, np.ndarray]] = None,
    ) -> float:
        """
        Compute similarity between two multi-modal inputs.

        Args:
            text1: First text input (optional)
            image1: First image input (optional)
            text2: Second text input (optional)
            image2: Second image input (optional)

        Returns:
            Cosine similarity score (0-1)
        """
        # Encode inputs
        vec1 = self.encode(text=text1, image=image1)
        vec2 = self.encode(text=text2, image=image2)

        # Compute cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        return dot_product / (norm1 * norm2)
