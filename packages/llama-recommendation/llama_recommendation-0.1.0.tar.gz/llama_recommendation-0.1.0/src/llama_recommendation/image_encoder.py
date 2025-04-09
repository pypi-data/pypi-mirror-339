"""
Image encoder for the multi-modal recommendation system.

This module provides an image encoder that converts images into vector
representations for use in the recommendation system.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from llama_recommender.utils.logging import get_logger
from PIL import Image


class ImageEncoder:
    """
    Image encoder for converting images to vector representations.

    This class encodes image content into fixed-dimensional vectors
    for use in the multi-modal recommendation system.
    """

    def __init__(
        self,
        output_dim: int = 128,
        image_size: Tuple[int, int] = (224, 224),
        pretrained_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the image encoder.

        Args:
            output_dim: Dimensionality of the output embeddings
            image_size: Size to resize images to (height, width)
            pretrained_path: Path to pretrained encoder weights
            logger: Logger instance
        """
        self.output_dim = output_dim
        self.image_size = image_size
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize MLX model
        self.model = self._create_model()

        # Load pretrained weights if provided
        if pretrained_path:
            self._load_pretrained(pretrained_path)

    def _create_model(self) -> nn.Module:
        """
        Create the MLX model for image encoding.

        Returns:
            MLX module for image encoding
        """

        class ConvBlock(nn.Module):
            """Convolutional block with batch normalization and ReLU."""

            def __init__(
                self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1
            ):
                super().__init__()
                self.conv = nn.Conv2d(
                    in_channels,
                    out_channels,
                    kernel_size=kernel_size,
                    stride=stride,
                    padding=kernel_size // 2,
                )
                self.bn = nn.BatchNorm(out_channels)
                self.relu = nn.ReLU()

            def __call__(self, x: mx.array) -> mx.array:
                x = self.conv(x)
                x = self.bn(x)
                x = self.relu(x)
                return x

        class ImageEncoderModel(nn.Module):
            """MLX model for image encoding."""

            def __init__(self, output_dim: int = 128):
                super().__init__()

                # Convolutional layers
                self.conv1 = ConvBlock(3, 64, kernel_size=7, stride=2)
                self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2)

                self.conv2 = ConvBlock(64, 128, kernel_size=3, stride=1)
                self.conv3 = ConvBlock(128, 128, kernel_size=3, stride=1)
                self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

                self.conv4 = ConvBlock(128, 256, kernel_size=3, stride=1)
                self.conv5 = ConvBlock(256, 256, kernel_size=3, stride=1)
                self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

                self.conv6 = ConvBlock(256, 512, kernel_size=3, stride=1)
                self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

                # Global average pooling
                self.gap = nn.AdaptiveAvgPool2d((1, 1))

                # Output projection
                self.fc = nn.Linear(512, output_dim)

            def __call__(self, x: mx.array) -> mx.array:
                # Convolutional blocks
                x = self.conv1(x)
                x = self.pool1(x)

                x = self.conv2(x)
                x = self.conv3(x)
                x = self.pool2(x)

                x = self.conv4(x)
                x = self.conv5(x)
                x = self.pool3(x)

                x = self.conv6(x)
                x = self.pool4(x)

                # Global average pooling
                x = self.gap(x)

                # Flatten
                x = mx.reshape(x, (x.shape[0], -1))

                # Output projection
                x = self.fc(x)

                return x

        return ImageEncoderModel(output_dim=self.output_dim)

    def _load_pretrained(self, path: str) -> None:
        """
        Load pretrained weights.

        Args:
            path: Path to pretrained weights
        """
        try:
            weights = mx.load(path)
            self.model.update(weights)
            self.logger.info(f"Loaded pretrained image encoder from {path}")
        except Exception as e:
            self.logger.warning(f"Failed to load pretrained weights: {e}")

    def _preprocess_image(self, image: Union[str, Image.Image, np.ndarray]) -> np.ndarray:
        """
        Preprocess image for the encoder.

        Args:
            image: Input image (file path, PIL Image, or NumPy array)

        Returns:
            Preprocessed image as NumPy array
        """
        # Load image if path is provided
        if isinstance(image, str):
            image = Image.open(image)

        # Convert PIL Image to NumPy array
        if isinstance(image, Image.Image):
            # Resize image
            image = image.resize(self.image_size[::-1])  # PIL uses (width, height)

            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Convert to NumPy array
            image = np.array(image)

        # Ensure image shape is correct
        if image.shape[:2] != self.image_size:
            from PIL import Image as PILImage

            pil_image = PILImage.fromarray(image)
            pil_image = pil_image.resize(self.image_size[::-1])
            image = np.array(pil_image)

        # Normalize pixel values to [0, 1]
        image = image.astype(np.float32) / 255.0

        # Transpose from (H, W, C) to (C, H, W)
        image = np.transpose(image, (2, 0, 1))

        return image

    def encode(self, image: Union[str, Image.Image, np.ndarray]) -> np.ndarray:
        """
        Encode image into a vector representation.

        Args:
            image: Input image (file path, PIL Image, or NumPy array)

        Returns:
            Vector representation of the image
        """
        # Preprocess image
        processed = self._preprocess_image(image)
        processed_mx = mx.array(processed.reshape(1, *processed.shape))

        # Forward pass through model
        with mx.eval_mode():
            embedding = self.model(processed_mx)

        # Convert to NumPy array
        return np.array(embedding[0])

    def encode_batch(self, images: List[Union[str, Image.Image, np.ndarray]]) -> np.ndarray:
        """
        Encode a batch of images into vector representations.

        Args:
            images: List of input images

        Returns:
            Matrix of image vector representations
        """
        # Preprocess images
        processed = np.stack([self._preprocess_image(img) for img in images])
        processed_mx = mx.array(processed)

        # Forward pass through model
        with mx.eval_mode():
            embeddings = self.model(processed_mx)

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

        self.logger.info(f"Saved image encoder to {path}")

    @classmethod
    def load(cls, path: str, output_dim: int = 128) -> "ImageEncoder":
        """
        Load encoder from disk.

        Args:
            path: Path to load the encoder from
            output_dim: Dimensionality of the output embeddings

        Returns:
            Loaded ImageEncoder instance
        """
        encoder = cls(output_dim=output_dim)
        encoder._load_pretrained(path)
        return encoder

    def similarity(
        self,
        image1: Union[str, Image.Image, np.ndarray],
        image2: Union[str, Image.Image, np.ndarray],
    ) -> float:
        """
        Compute similarity between two images.

        Args:
            image1: First image
            image2: Second image

        Returns:
            Cosine similarity score (0-1)
        """
        # Encode images
        vec1 = self.encode(image1)
        vec2 = self.encode(image2)

        # Compute cosine similarity
        similarity_score = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        return float(similarity_score)
