"""
Ranking module for the recommendation system.

This module provides methods for scoring and ranking candidate items
for recommendation to users.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from llama_recommender.utils.logging import get_logger


class Ranker:
    """
    Score and rank candidate items for recommendation.

    This class provides methods for scoring and ranking candidate items
    based on relevance, diversity, and other factors.
    """

    def __init__(
        self,
        model: "BaseModel",
        diversity_weight: float = 0.2,
        novelty_weight: float = 0.1,
        trending_weight: float = 0.1,
        position_bias_correction: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the ranker.

        Args:
            model: Recommendation model
            diversity_weight: Weight for diversity (0-1)
            novelty_weight: Weight for novelty (0-1)
            trending_weight: Weight for trending items (0-1)
            position_bias_correction: Whether to correct for position bias
            logger: Logger instance
        """
        self.model = model
        self.diversity_weight = diversity_weight
        self.novelty_weight = novelty_weight
        self.trending_weight = trending_weight
        self.position_bias_correction = position_bias_correction
        self.logger = logger or get_logger(self.__class__.__name__)

    def rank(
        self,
        user_id: str,
        candidates: List[Dict[str, Any]],
        context: Dict[str, Any],
        causal_estimation: bool = False,
        diversity_method: str = "mmr",
    ) -> List[Dict[str, Any]]:
        """
        Rank candidate items for recommendation.

        Args:
            user_id: User identifier
            candidates: List of candidate items
            context: Contextual information
            causal_estimation: Whether to estimate treatment effects
            diversity_method: Method for diversity promotion ('mmr' or 'dpp')

        Returns:
            List of ranked items
        """
        if not candidates:
            self.logger.warning(f"No candidates to rank for user {user_id}")
            return []

        # Step 1: Score candidates
        scored_items = self._score_candidates(user_id, candidates, context, causal_estimation)

        # Step 2: Apply diversity
        if self.diversity_weight > 0:
            diversified_items = self._apply_diversity(
                scored_items, diversity_method=diversity_method
            )
        else:
            diversified_items = scored_items

        # Step 3: Adjust for position bias
        if self.position_bias_correction:
            ranked_items = self._correct_position_bias(diversified_items)
        else:
            # Sort by final score
            ranked_items = sorted(diversified_items, key=lambda x: x["score"], reverse=True)

        self.logger.info(f"Ranked {len(ranked_items)} items for user {user_id}")

        return ranked_items

    def _score_candidates(
        self,
        user_id: str,
        candidates: List[Dict[str, Any]],
        context: Dict[str, Any],
        causal_estimation: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Score candidate items using the recommendation model.

        Args:
            user_id: User identifier
            candidates: List of candidate items
            context: Contextual information
            causal_estimation: Whether to estimate treatment effects

        Returns:
            List of scored items
        """
        # Get item IDs
        item_ids = [candidate["item_id"] for candidate in candidates]

        # Get base predictions from model
        base_scores = self.model.predict(user_id, item_ids, context)

        # Get treatment effects if requested
        treatment_effects = None
        if causal_estimation:
            from llama_recommender.core.models import CausalModel

            if isinstance(self.model, CausalModel):
                # Use causal model to estimate treatment effects
                _, treatment_effects = self.model.predict(
                    user_id, item_ids, context, estimate_uplift=True
                )
            else:
                self.logger.warning(
                    "Causal estimation requested but model is not a CausalModel. "
                    "Treatment effects will not be estimated."
                )

        # Apply scoring adjustments
        scored_items = []
        for i, candidate in enumerate(candidates):
            item_id = candidate["item_id"]

            # Base relevance score
            relevance = float(base_scores[i])

            # Apply novelty adjustment
            novelty = candidate.get("novelty", 0)

            # Apply trending adjustment
            trending_score = candidate.get("trending", 0)

            # Calculate final score
            final_score = relevance

            # Apply novelty and trending weights
            if self.novelty_weight > 0:
                final_score += self.novelty_weight * novelty

            if self.trending_weight > 0:
                final_score += self.trending_weight * trending_score

            # Create scored item
            scored_item = candidate.copy()
            scored_item["score"] = final_score
            scored_item["relevance"] = relevance

            # Add treatment effect if available
            if treatment_effects is not None:
                treatment_effect = float(treatment_effects[i])
                scored_item["treatment_effect"] = treatment_effect

            scored_items.append(scored_item)

        return scored_items

    def _apply_diversity(
        self, items: List[Dict[str, Any]], diversity_method: str = "mmr"
    ) -> List[Dict[str, Any]]:
        """
        Apply diversity promotion to ranked items.

        Args:
            items: List of scored items
            diversity_method: Method for diversity promotion ('mmr' or 'dpp')

        Returns:
            List of items with diversity promotion
        """
        if len(items) <= 1:
            return items

        if diversity_method == "mmr":
            return self._apply_mmr_diversity(items)
        elif diversity_method == "dpp":
            return self._apply_dpp_diversity(items)
        else:
            self.logger.warning(f"Unknown diversity method: {diversity_method}")
            return items

    def _apply_mmr_diversity(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply maximal marginal relevance for diversity.

        Args:
            items: List of scored items

        Returns:
            List of items reranked for diversity
        """
        # Sort items by score
        sorted_items = sorted(items, key=lambda x: x["score"], reverse=True)

        # Extract item IDs and embeddings
        item_ids = [item["item_id"] for item in sorted_items]
        item_embeddings = {}

        for item_id in item_ids:
            embedding = self.model.encode_item(item_id)
            item_embeddings[item_id] = embedding

        # Apply maximal marginal relevance
        selected = [sorted_items[0]]  # Start with the highest-scoring item
        remaining = sorted_items[1:]

        while remaining:
            # Find the next item with the best combination of relevance and diversity
            best_mmr_score = -float("inf")
            best_item_idx = -1

            for i, item in enumerate(remaining):
                item_id = item["item_id"]
                relevance = item["score"]

                # Calculate maximum similarity to already selected items
                max_similarity = 0
                for sel in selected:
                    sel_id = sel["item_id"]
                    similarity = self._cosine_similarity(
                        item_embeddings[item_id], item_embeddings[sel_id]
                    )
                    max_similarity = max(max_similarity, similarity)

                # Calculate MMR score
                mmr_score = (
                    1 - self.diversity_weight
                ) * relevance - self.diversity_weight * max_similarity

                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_item_idx = i

            # Add the best item to the selected list
            if best_item_idx >= 0:
                best_item = remaining[best_item_idx]

                # Calculate diversity contribution
                avg_similarity = 0
                if len(selected) > 0:
                    similarities = []
                    for sel in selected:
                        sel_id = sel["item_id"]
                        similarity = self._cosine_similarity(
                            item_embeddings[best_item["item_id"]], item_embeddings[sel_id]
                        )
                        similarities.append(similarity)
                    avg_similarity = np.mean(similarities)

                # Add diversity contribution to item
                best_item_copy = best_item.copy()
                best_item_copy["diversity_contribution"] = 1 - avg_similarity

                selected.append(best_item_copy)
                remaining.pop(best_item_idx)
            else:
                break

        return selected

    def _apply_dpp_diversity(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply determinantal point process for diversity.

        Args:
            items: List of scored items

        Returns:
            List of items reranked for diversity
        """
        try:
            # Extract item IDs and scores
            item_ids = [item["item_id"] for item in items]
            item_scores = [item["score"] for item in items]

            # Extract item embeddings
            item_embeddings = []
            for item_id in item_ids:
                embedding = self.model.encode_item(item_id)
                item_embeddings.append(embedding)

            # Calculate similarity matrix
            n_items = len(items)
            similarity_matrix = np.zeros((n_items, n_items))

            for i in range(n_items):
                for j in range(i, n_items):
                    similarity = self._cosine_similarity(item_embeddings[i], item_embeddings[j])
                    similarity_matrix[i, j] = similarity
                    similarity_matrix[j, i] = similarity

            # Calculate quality vector (relevance scores)
            quality = np.array(item_scores)

            # Create DPP kernel
            L = np.zeros((n_items, n_items))
            for i in range(n_items):
                for j in range(n_items):
                    L[i, j] = quality[i] * similarity_matrix[i, j] * quality[j]

            # Apply greedy DPP algorithm
            selected_indices = self._greedy_dpp(L, n_items)

            # Create reranked items
            reranked_items = []
            for idx in selected_indices:
                item = items[idx].copy()

                # Calculate diversity contribution
                avg_similarity = 0
                if len(reranked_items) > 0:
                    selected_so_far = [i for i in range(len(reranked_items))]
                    similarities = [similarity_matrix[idx, i] for i in selected_so_far]
                    avg_similarity = np.mean(similarities)

                item["diversity_contribution"] = 1 - avg_similarity
                reranked_items.append(item)

            return reranked_items

        except Exception as e:
            self.logger.warning(f"Error applying DPP diversity: {e}")
            # Fall back to MMR
            return self._apply_mmr_diversity(items)

    def _greedy_dpp(self, kernel: np.ndarray, k: int) -> List[int]:
        """
        Greedy algorithm for k-DPP.

        Args:
            kernel: DPP kernel matrix
            k: Number of items to select

        Returns:
            List of selected indices
        """
        n = kernel.shape[0]
        k = min(k, n)

        # Initialize selected set
        selected = []

        # Initialize determinants for all single-element subsets
        det_single = np.diag(kernel).copy()

        # Greedy selection
        for _ in range(k):
            # If all remaining determinants are zero, break
            if np.all(det_single <= 0):
                break

            # Select item with largest determinant
            i = np.argmax(det_single)
            selected.append(i)

            # Update determinants
            if len(selected) < k:
                # Get submatrix for selected items
                Y = kernel[np.ix_(selected, selected)]

                # Compute inverse of Y
                try:
                    Y_inv = np.linalg.inv(Y)
                except np.linalg.LinAlgError:
                    # If Y is singular, use pseudoinverse
                    Y_inv = np.linalg.pinv(Y)

                # Update determinants for remaining items
                for j in range(n):
                    if j not in selected:
                        # Compute contribution of adding item j
                        y_j = kernel[selected, j]
                        det_ratio = kernel[j, j] - y_j.T @ Y_inv @ y_j
                        det_single[j] = max(0, det_ratio)  # Ensure non-negative
                    else:
                        det_single[j] = 0  # Mark as selected

        return selected

    def _correct_position_bias(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Correct for position bias in ranked items.

        Args:
            items: List of scored items

        Returns:
            List of items with position bias correction
        """
        # Simple position bias correction using a modification of the Inverse Propensity Scoring approach
        position_discount = lambda pos: 1.0 / np.log2(pos + 2)  # Logarithmic discount

        # Sort items by score
        sorted_items = sorted(items, key=lambda x: x["score"], reverse=True)

        # Apply position bias correction
        corrected_items = []
        for i, item in enumerate(sorted_items):
            position = i + 1  # 1-based position
            discount = position_discount(position)

            # Apply discount based on position
            corrected_item = item.copy()
            corrected_item["position_discount"] = discount

            # Calculate confidence
            confidence = 1.0 - (i / len(sorted_items) * 0.5)  # Higher ranks have higher confidence
            corrected_item["confidence"] = confidence

            corrected_items.append(corrected_item)

        return corrected_items

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score
        """
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)

        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0

        return dot_product / (norm_vec1 * norm_vec2)
