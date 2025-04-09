"""
Main RecommenderSystem class that orchestrates the recommendation pipeline.
"""

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from llama_recommender.core.embeddings import EmbeddingManager
from llama_recommender.core.models import BaseModel, MultiModalModel
from llama_recommender.recommendation.candidate import CandidateGenerator
from llama_recommender.recommendation.explanation import ExplanationGenerator
from llama_recommender.recommendation.filtering import EthicalFilter
from llama_recommender.recommendation.ranking import Ranker
from llama_recommender.utils.logging import get_logger


@dataclass
class Recommendation:
    """A single recommendation with metadata."""

    item_id: str
    score: float
    explanation: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    ethical_score: Optional[float] = None
    diversity_contribution: Optional[float] = None
    confidence: Optional[float] = None
    treatment_effect: Optional[float] = None


class RecommenderSystem:
    """
    Privacy-preserving multi-modal recommendation system.

    This class orchestrates the entire recommendation pipeline, including:
    1. Candidate generation
    2. Scoring and ranking
    3. Ethical filtering
    4. Explanation generation

    Attributes:
        model: The underlying recommendation model
        embedding_manager: Manager for user and item embeddings
        candidate_generator: Component for generating candidate items
        ranker: Component for scoring and ranking items
        ethical_filter: Component for filtering based on ethical considerations
        explanation_generator: Component for generating explanations
        logger: Logger instance
    """

    def __init__(
        self,
        model: Optional[BaseModel] = None,
        embedding_path: Optional[str] = None,
        ethical_threshold: Optional[float] = None,
        diversity_weight: float = 0.2,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the recommendation system.

        Args:
            model: The underlying recommendation model. If None, a MultiModalModel
                is created.
            embedding_path: Path to pre-trained embeddings. If None, embeddings
                will be initialized from scratch.
            ethical_threshold: Minimum ethical score threshold for recommendations.
                If None, uses the value from LLAMA_ETHICS_THRESHOLD environment
                variable or defaults to 0.7.
            diversity_weight: Weight for diversity in recommendation ranking (0-1).
            logger: Logger instance. If None, a default logger is created.
        """
        self.logger = logger or get_logger(__name__)

        # Initialize model
        self.model = model or MultiModalModel()
        self.logger.info(f"Initialized model: {self.model.__class__.__name__}")

        # Initialize embedding manager
        self.embedding_manager = EmbeddingManager(embedding_path=embedding_path)

        # Set ethical threshold
        self.ethical_threshold = ethical_threshold or float(
            os.getenv("LLAMA_ETHICS_THRESHOLD", "0.7")
        )

        # Initialize pipeline components
        self.candidate_generator = CandidateGenerator(
            model=self.model, embedding_manager=self.embedding_manager
        )

        self.ranker = Ranker(model=self.model, diversity_weight=diversity_weight)

        self.ethical_filter = EthicalFilter(threshold=self.ethical_threshold)

        self.explanation_generator = ExplanationGenerator(model=self.model)

        self.logger.info("RecommenderSystem initialized successfully")

    def recommend(
        self,
        user_id: str,
        k: int = 10,
        context: Optional[Dict[str, Any]] = None,
        filter_attributes: Optional[Dict[str, Any]] = None,
        explain: bool = False,
        causal_estimation: bool = False,
    ) -> List[Recommendation]:
        """
        Generate recommendations for a user.

        Args:
            user_id: The user ID to generate recommendations for
            k: Number of recommendations to return
            context: Contextual information for the recommendation request
            filter_attributes: Attributes to filter candidates by
            explain: Whether to generate explanations for recommendations
            causal_estimation: Whether to estimate causal treatment effects

        Returns:
            A list of Recommendation objects
        """
        self.logger.info(f"Generating recommendations for user {user_id}")

        # Step 1: Generate candidates
        candidates = self.candidate_generator.generate(
            user_id=user_id,
            context=context or {},
            limit=k * 5,  # Get more candidates than needed for filtering
        )
        self.logger.debug(f"Generated {len(candidates)} candidates")

        # Step 2: Score and rank candidates
        ranked_items = self.ranker.rank(
            user_id=user_id,
            candidates=candidates,
            context=context or {},
            causal_estimation=causal_estimation,
        )
        self.logger.debug(f"Ranked {len(ranked_items)} candidates")

        # Step 3: Apply ethical filter
        filtered_items = self.ethical_filter.filter(
            user_id=user_id, items=ranked_items, attributes=filter_attributes or {}
        )
        self.logger.debug(f"Filtered to {len(filtered_items)} items")

        # Step 4: Generate explanations if requested
        recommendations = []
        for item in filtered_items[:k]:
            explanation = None
            if explain:
                explanation = self.explanation_generator.generate(
                    user_id=user_id, item_id=item.item_id, context=context or {}
                )

            recommendations.append(
                Recommendation(
                    item_id=item.item_id,
                    score=item.score,
                    explanation=explanation,
                    features=item.features,
                    ethical_score=item.ethical_score,
                    diversity_contribution=item.diversity_contribution,
                    confidence=item.confidence,
                    treatment_effect=(item.treatment_effect if causal_estimation else None),
                )
            )

        self.logger.info(f"Returning {len(recommendations)} recommendations")
        return recommendations

    def train(
        self,
        train_data: str,
        validation_data: Optional[str] = None,
        epochs: int = 10,
        batch_size: int = 32,
        learning_rate: float = 0.001,
        use_differential_privacy: bool = True,
        dp_epsilon: Optional[float] = None,
        dp_delta: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Train the underlying recommendation model.

        Args:
            train_data: Path to training data
            validation_data: Path to validation data
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate for optimization
            use_differential_privacy: Whether to use differential privacy during training
            dp_epsilon: Epsilon parameter for differential privacy
            dp_delta: Delta parameter for differential privacy

        Returns:
            Dictionary of training metrics
        """
        from llama_recommender.core.privacy import DPTrainer

        self.logger.info(
            f"Training model with {'DP' if use_differential_privacy else 'standard'} training"
        )

        if use_differential_privacy:
            dp_epsilon = dp_epsilon or float(os.getenv("LLAMA_DP_EPSILON", "1.0"))
            dp_delta = dp_delta or float(os.getenv("LLAMA_DP_DELTA", "1e-5"))

            trainer = DPTrainer(model=self.model, epsilon=dp_epsilon, delta=dp_delta)
        else:
            from llama_recommender.core.models import Trainer

            trainer = Trainer(model=self.model)

        metrics = trainer.train(
            train_data=train_data,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
        )

        # Update embeddings after training
        self.embedding_manager.update_embeddings(self.model)

        self.logger.info(f"Training completed with metrics: {metrics}")
        return metrics

    def save(self, path: str) -> None:
        """
        Save the recommendation system to disk.

        Args:
            path: Directory path to save the system
        """
        import os
        import pickle

        os.makedirs(path, exist_ok=True)

        # Save model
        model_path = os.path.join(path, "model")
        self.model.save(model_path)

        # Save embeddings
        embedding_path = os.path.join(path, "embeddings")
        self.embedding_manager.save(embedding_path)

        # Save configuration
        config = {
            "ethical_threshold": self.ethical_threshold,
            "diversity_weight": self.ranker.diversity_weight,
        }

        with open(os.path.join(path, "config.pkl"), "wb") as f:
            pickle.dump(config, f)

        self.logger.info(f"Saved recommendation system to {path}")

    @classmethod
    def load(cls, path: str) -> "RecommenderSystem":
        """
        Load a recommendation system from disk.

        Args:
            path: Directory path to load the system from

        Returns:
            Loaded RecommenderSystem instance
        """
        import os
        import pickle

        from llama_recommender.core.models import BaseModel

        # Load model
        model_path = os.path.join(path, "model")
        model = BaseModel.load(model_path)

        # Load embeddings path
        embedding_path = os.path.join(path, "embeddings")

        # Load configuration
        with open(os.path.join(path, "config.pkl"), "rb") as f:
            config = pickle.load(f)

        # Create recommender system
        recommender = cls(
            model=model,
            embedding_path=embedding_path,
            ethical_threshold=config.get("ethical_threshold"),
            diversity_weight=config.get("diversity_weight", 0.2),
        )

        return recommender
