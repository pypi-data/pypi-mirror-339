"""
Core ML integration for on-device recommendation.

This module provides utilities for converting recommendation models to Core ML
format for on-device inference on Apple devices.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from llama_recommender.utils.logging import get_logger


class CoreMLConverter:
    """
    Convert recommendation models to Core ML format.

    This class provides methods for converting MLX recommendation models
    to Core ML format for on-device inference on Apple devices.
    """

    def __init__(self, model: "BaseModel", logger: Optional[logging.Logger] = None):
        """
        Initialize the Core ML converter.

        Args:
            model: Recommendation model to convert
            logger: Logger instance
        """
        self.model = model
        self.logger = logger or get_logger(self.__class__.__name__)

        # Verify coremltools is available
        try:
            import coremltools

            self.coremltools_available = True
        except ImportError:
            self.logger.warning("coremltools not available. Install with: pip install coremltools")
            self.coremltools_available = False

    def convert(
        self,
        output_path: str,
        model_type: str = "scoring",
        include_metadata: bool = True,
        minimum_deployment_target: Optional[str] = None,
    ) -> Optional[str]:
        """
        Convert the model to Core ML format.

        Args:
            output_path: Path to save the Core ML model
            model_type: Type of model to convert ('scoring', 'embedding', or 'complete')
            include_metadata: Whether to include metadata in the model
            minimum_deployment_target: Minimum deployment target version

        Returns:
            Path to the saved Core ML model or None if conversion failed
        """
        if not self.coremltools_available:
            self.logger.error("coremltools not available. Conversion failed.")
            return None

        try:
            import coremltools as ct
            from coremltools.models import MLModel

            # Create output directory
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Convert based on model type
            if model_type == "scoring":
                mlmodel = self._convert_scoring_model(ct)
            elif model_type == "embedding":
                mlmodel = self._convert_embedding_model(ct)
            elif model_type == "complete":
                mlmodel = self._convert_complete_model(ct)
            else:
                self.logger.error(f"Unknown model type: {model_type}")
                return None

            # Add metadata if requested
            if include_metadata:
                self._add_metadata(mlmodel)

            # Set minimum deployment target if specified
            if minimum_deployment_target:
                mlmodel.spec.specificationVersion = 5  # For newer deployment targets

            # Save the model
            mlmodel.save(output_path)
            self.logger.info(f"Saved Core ML model to {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Error converting model to Core ML: {e}")
            return None

    def _convert_scoring_model(self, ct) -> "MLModel":
        """
        Convert the scoring component of the model.

        Args:
            ct: coremltools module

        Returns:
            Core ML model for scoring
        """
        # Define model inputs
        inputs = [
            ct.TensorType(name="user_embedding", shape=(1, self.model.embedding_dim)),
            ct.TensorType(name="item_embedding", shape=(1, self.model.embedding_dim)),
        ]

        # Define model outputs
        outputs = [ct.TensorType(name="score", shape=(1, 1))]

        # Create a traced model
        @ct.function.trace(inputs=inputs, outputs=outputs)
        def scoring_function(user_embedding, item_embedding):
            import numpy as np

            # Convert inputs to numpy arrays
            user_embedding_np = np.array(user_embedding)
            item_embedding_np = np.array(item_embedding)

            # Concatenate embeddings
            concatenated = np.concatenate([user_embedding_np, item_embedding_np], axis=1)

            # Apply MLP layers
            # This is a placeholder for the actual model architecture
            # In a real implementation, this would match the MLX model structure
            hidden1 = np.maximum(
                0, np.dot(concatenated, np.random.randn(2 * self.model.embedding_dim, 256))
            )
            hidden2 = np.maximum(0, np.dot(hidden1, np.random.randn(256, 128)))
            output = np.dot(hidden2, np.random.randn(128, 1))

            return output

        # Convert to Core ML
        mlmodel = ct.convert(
            scoring_function,
            convert_to="mlprogram",
            compute_units=ct.ComputeUnit.CPU_AND_NE,  # Use Neural Engine if available
        )

        return mlmodel

    def _convert_embedding_model(self, ct) -> "MLModel":
        """
        Convert the embedding component of the model.

        Args:
            ct: coremltools module

        Returns:
            Core ML model for embedding extraction
        """
        # Define model inputs for user embedding
        user_inputs = [
            ct.TensorType(name="user_id", shape=(1,), dtype=np.int32),
            ct.TensorType(name="context_features", shape=(1, 10), optional=True),
        ]

        # Define model outputs for user embedding
        user_outputs = [ct.TensorType(name="user_embedding", shape=(1, self.model.embedding_dim))]

        # Create a traced model for user embedding
        @ct.function.trace(inputs=user_inputs, outputs=user_outputs)
        def user_embedding_function(user_id, context_features=None):
            import numpy as np

            # This is a placeholder for the actual embedding extraction
            # In a real implementation, this would look up the user embedding
            embedding = np.random.randn(1, self.model.embedding_dim)

            return embedding

        # Define model inputs for item embedding
        item_inputs = [ct.TensorType(name="item_id", shape=(1,), dtype=np.int32)]

        # Define model outputs for item embedding
        item_outputs = [ct.TensorType(name="item_embedding", shape=(1, self.model.embedding_dim))]

        # Create a traced model for item embedding
        @ct.function.trace(inputs=item_inputs, outputs=item_outputs)
        def item_embedding_function(item_id):
            import numpy as np

            # This is a placeholder for the actual embedding extraction
            # In a real implementation, this would look up the item embedding
            embedding = np.random.randn(1, self.model.embedding_dim)

            return embedding

        # Convert to Core ML
        user_model = ct.convert(
            user_embedding_function, convert_to="mlprogram", compute_units=ct.ComputeUnit.CPU_AND_NE
        )

        item_model = ct.convert(
            item_embedding_function, convert_to="mlprogram", compute_units=ct.ComputeUnit.CPU_AND_NE
        )

        # Combine models into a pipeline
        pipeline = ct.models.pipeline.Pipeline(
            input_features=[
                ct.TensorType(name="input_type", shape=(1,), dtype=np.int32),
                ct.TensorType(name="id", shape=(1,), dtype=np.int32),
                ct.TensorType(name="context_features", shape=(1, 10), optional=True),
            ],
            output_features=[ct.TensorType(name="embedding", shape=(1, self.model.embedding_dim))],
        )

        # Add models to pipeline
        pipeline.add_model(user_model)
        pipeline.add_model(item_model)

        # Add routing logic
        pipeline.spec.pipeline.nodes[0].branch.ifBranch.condition = "input_type == 0"
        pipeline.spec.pipeline.nodes[1].branch.ifBranch.condition = "input_type == 1"

        return pipeline

    def _convert_complete_model(self, ct) -> "MLModel":
        """
        Convert the complete recommendation model.

        Args:
            ct: coremltools module

        Returns:
            Core ML model for end-to-end recommendation
        """
        # Define model inputs
        inputs = [
            ct.TensorType(name="user_id", shape=(1,), dtype=np.int32),
            ct.TensorType(name="candidate_item_ids", shape=(ct.RangeDim(1, 100),), dtype=np.int32),
            ct.TensorType(name="context_features", shape=(1, 10), optional=True),
        ]

        # Define model outputs
        outputs = [
            ct.TensorType(name="scores", shape=(ct.RangeDim(1, 100),)),
            ct.TensorType(name="ranked_item_ids", shape=(ct.RangeDim(1, 100),), dtype=np.int32),
        ]

        # Create a traced model
        @ct.function.trace(inputs=inputs, outputs=outputs)
        def recommendation_function(user_id, candidate_item_ids, context_features=None):
            import numpy as np

            # This is a placeholder for the actual recommendation logic
            # In a real implementation, this would:
            # 1. Get user embedding
            # 2. Get item embeddings for candidates
            # 3. Calculate scores
            # 4. Rank items

            num_candidates = len(candidate_item_ids)
            scores = np.random.random(num_candidates)

            # Sort by score
            indices = np.argsort(scores)[::-1]
            ranked_item_ids = candidate_item_ids[indices]
            sorted_scores = scores[indices]

            return sorted_scores, ranked_item_ids

        # Convert to Core ML
        mlmodel = ct.convert(
            recommendation_function, convert_to="mlprogram", compute_units=ct.ComputeUnit.CPU_AND_NE
        )

        return mlmodel

    def _add_metadata(self, mlmodel) -> None:
        """
        Add metadata to the Core ML model.

        Args:
            mlmodel: Core ML model
        """
        # Add model metadata
        mlmodel.author = "llama_recommender"
        mlmodel.license = "MIT"
        mlmodel.version = "1.0"
        mlmodel.short_description = "Privacy-preserving recommendation model"

        # Add feature descriptions
        mlmodel.input_description["user_embedding"] = "User embedding vector"
        mlmodel.input_description["item_embedding"] = "Item embedding vector"
        mlmodel.output_description["score"] = "Recommendation score"

        # Add detailed description
        mlmodel.description = """
        This model provides privacy-preserving recommendations by operating on
        embedding vectors rather than raw user data. It calculates a relevance
        score for a given user-item pair.
        """


class CoreMLRecommender:
    """
    On-device recommender using Core ML models.

    This class provides methods for making recommendations using Core ML
    models on Apple devices.
    """

    def __init__(
        self,
        model_path: str,
        user_embeddings_path: Optional[str] = None,
        item_embeddings_path: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the Core ML recommender.

        Args:
            model_path: Path to the Core ML model
            user_embeddings_path: Path to user embeddings file
            item_embeddings_path: Path to item embeddings file
            logger: Logger instance
        """
        self.model_path = model_path
        self.user_embeddings_path = user_embeddings_path
        self.item_embeddings_path = item_embeddings_path
        self.logger = logger or get_logger(self.__class__.__name__)

        # Load the model
        self.model = self._load_model()

        # Load embeddings if paths provided
        self.user_embeddings = {}
        self.item_embeddings = {}

        if user_embeddings_path:
            self._load_user_embeddings()

        if item_embeddings_path:
            self._load_item_embeddings()

    def _load_model(self) -> Optional[Any]:
        """
        Load the Core ML model.

        Returns:
            Loaded Core ML model or None if loading failed
        """
        try:
            import coremltools as ct

            model = ct.models.MLModel(self.model_path)
            self.logger.info(f"Loaded Core ML model from {self.model_path}")

            return model

        except ImportError:
            self.logger.error("coremltools not available. Could not load model.")
            return None

        except Exception as e:
            self.logger.error(f"Error loading Core ML model: {e}")
            return None

    def _load_user_embeddings(self) -> None:
        """
        Load user embeddings.
        """
        try:
            self.user_embeddings = np.load(self.user_embeddings_path, allow_pickle=True).item()
            self.logger.info(f"Loaded user embeddings for {len(self.user_embeddings)} users")
        except Exception as e:
            self.logger.error(f"Error loading user embeddings: {e}")

    def _load_item_embeddings(self) -> None:
        """
        Load item embeddings.
        """
        try:
            self.item_embeddings = np.load(self.item_embeddings_path, allow_pickle=True).item()
            self.logger.info(f"Loaded item embeddings for {len(self.item_embeddings)} items")
        except Exception as e:
            self.logger.error(f"Error loading item embeddings: {e}")

    def recommend(
        self,
        user_id: str,
        candidate_items: List[str],
        context: Optional[Dict[str, Any]] = None,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations for a user.
        """
        try:
            user_embedding = self._get_user_embedding(user_id, context)

            if user_embedding is None:
                self.logger.warning(f"User embedding not found for user {user_id}")
                return []

            # Score each candidate item
            scores = []
            for item_id in candidate_items:
                item_embedding = self._get_item_embedding(item_id)
                if item_embedding is not None:
                    score = self._predict_score(user_embedding, item_embedding)
                    scores.append((item_id, float(score)))

            # Sort by score and take top-k
            scores.sort(key=lambda x: x[1], reverse=True)

            # Format output
            recommendations = [
                {"item_id": item_id, "score": score} for item_id, score in scores[:top_k]
            ]

            return recommendations
        except Exception as e:
            self.logger.error(f"Error generating recommendations for user {user_id}: {e}")
            return []
