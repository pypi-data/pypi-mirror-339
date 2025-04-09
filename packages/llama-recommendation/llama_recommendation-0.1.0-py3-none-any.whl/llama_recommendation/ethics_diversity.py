"""
Diversity metrics and algorithms for recommendation systems.

This module provides utilities for measuring and improving diversity
in recommendation results to avoid filter bubbles and echo chambers.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from llama_recommender.utils.logging import get_logger
from scipy.spatial.distance import pdist, squareform


class DiversityMetrics:
    """
    Metrics for measuring diversity in recommendation lists.

    This class provides methods for calculating various diversity metrics
    for evaluating the diversity of recommendation results.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize diversity metrics calculator.

        Args:
            logger: Logger instance
        """
        self.logger = logger or get_logger(self.__class__.__name__)

    def intra_list_diversity(
        self, item_embeddings: np.ndarray, distance_metric: str = "cosine"
    ) -> float:
        """
        Calculate intra-list diversity.

        This metric measures the average pairwise distance between items
        in a recommendation list.

        Args:
            item_embeddings: Array of item embeddings (N x D)
            distance_metric: Distance metric to use

        Returns:
            Intra-list diversity score (higher is more diverse)
        """
        # Check if there are at least 2 items
        if len(item_embeddings) < 2:
            return 0.0

        # Calculate pairwise distances
        distances = pdist(item_embeddings, metric=distance_metric)

        # Return average distance
        return float(np.mean(distances))

    def coverage(self, recommended_items: List[str], all_items: List[str]) -> float:
        """
        Calculate catalog coverage.

        This metric measures the proportion of all available items that
        are recommended at least once.

        Args:
            recommended_items: List of recommended item IDs
            all_items: List of all available item IDs

        Returns:
            Coverage ratio (0-1)
        """
        # Convert to sets for efficient operations
        recommended_set = set(recommended_items)
        all_set = set(all_items)

        # Calculate coverage
        coverage_ratio = len(recommended_set) / len(all_set) if all_set else 0

        return float(coverage_ratio)

    def category_coverage(
        self, recommended_categories: List[str], all_categories: List[str]
    ) -> float:
        """
        Calculate category coverage.

        This metric measures the proportion of all available categories that
        are represented in the recommendations.

        Args:
            recommended_categories: List of categories in recommendations
            all_categories: List of all available categories

        Returns:
            Category coverage ratio (0-1)
        """
        # Convert to sets for efficient operations
        recommended_set = set(recommended_categories)
        all_set = set(all_categories)

        # Calculate coverage
        coverage_ratio = len(recommended_set) / len(all_set) if all_set else 0

        return float(coverage_ratio)

    def unexpectedness(
        self, recommendations: List[str], expected_recommendations: List[str]
    ) -> float:
        """
        Calculate unexpectedness.

        This metric measures the proportion of recommendations that are
        unexpected (not in the expected set).

        Args:
            recommendations: List of recommended item IDs
            expected_recommendations: List of expected item IDs

        Returns:
            Unexpectedness score (0-1)
        """
        # Convert to sets for efficient operations
        recommendations_set = set(recommendations)
        expected_set = set(expected_recommendations)

        # Calculate unexpectedness
        unexpected_count = len(recommendations_set - expected_set)
        unexpectedness = unexpected_count / len(recommendations_set) if recommendations_set else 0

        return float(unexpectedness)

    def novelty(self, recommendations: List[str], item_popularities: Dict[str, float]) -> float:
        """
        Calculate novelty.

        This metric measures the average unpopularity of recommended items.
        Higher novelty means recommending more niche items.

        Args:
            recommendations: List of recommended item IDs
            item_popularities: Dictionary mapping item IDs to popularity scores

        Returns:
            Novelty score (higher means more novel)
        """
        if not recommendations:
            return 0.0

        # Calculate self-information (negative log of popularity)
        novelty_scores = []
        for item_id in recommendations:
            popularity = item_popularities.get(item_id, 0)
            # Avoid log(0)
            if popularity > 0:
                # Self-information: -log(popularity)
                self_info = -np.log2(popularity)
                novelty_scores.append(self_info)
            else:
                # Maximum novelty for items with no popularity data
                novelty_scores.append(np.inf)

        # Handle case where all scores are infinite
        if all(np.isinf(score) for score in novelty_scores):
            return float(np.max(novelty_scores))

        # Filter out infinite values for the average
        finite_scores = [score for score in novelty_scores if not np.isinf(score)]

        # Return average novelty
        return float(np.mean(finite_scores)) if finite_scores else 0.0

    def serendipity(
        self,
        recommendations: List[str],
        expected_recommendations: List[str],
        item_relevance: Dict[str, float],
    ) -> float:
        """
        Calculate serendipity.

        This metric measures the unexpectedness and relevance of recommendations.
        It rewards unexpected items that are also relevant.

        Args:
            recommendations: List of recommended item IDs
            expected_recommendations: List of expected item IDs
            item_relevance: Dictionary mapping item IDs to relevance scores

        Returns:
            Serendipity score (0-1)
        """
        if not recommendations:
            return 0.0

        # Convert to sets for efficient operations
        recommendations_set = set(recommendations)
        expected_set = set(expected_recommendations)

        # Find unexpected recommendations
        unexpected_items = recommendations_set - expected_set

        # Calculate serendipity (unexpectedness * relevance)
        serendipity_scores = []
        for item_id in unexpected_items:
            relevance = item_relevance.get(item_id, 0)
            serendipity_scores.append(relevance)

        # Return average serendipity
        return float(np.mean(serendipity_scores)) if serendipity_scores else 0.0

    def evaluate_diversity(
        self,
        recommendations: List[str],
        item_embeddings: Dict[str, np.ndarray],
        all_items: List[str],
        item_categories: Optional[Dict[str, List[str]]] = None,
        all_categories: Optional[List[str]] = None,
        expected_recommendations: Optional[List[str]] = None,
        item_popularities: Optional[Dict[str, float]] = None,
        item_relevance: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Evaluate multiple diversity metrics.

        Args:
            recommendations: List of recommended item IDs
            item_embeddings: Dictionary mapping item IDs to embeddings
            all_items: List of all available item IDs
            item_categories: Dictionary mapping item IDs to categories
            all_categories: List of all available categories
            expected_recommendations: List of expected item IDs
            item_popularities: Dictionary mapping item IDs to popularity scores
            item_relevance: Dictionary mapping item IDs to relevance scores

        Returns:
            Dictionary of diversity metrics
        """
        metrics = {}

        # Calculate intra-list diversity if embeddings are available
        if item_embeddings:
            try:
                rec_embeddings = np.array(
                    [
                        item_embeddings[item_id]
                        for item_id in recommendations
                        if item_id in item_embeddings
                    ]
                )
            except KeyError as e:
                self.logger.warning(f"Missing embeddings for item: {e}")
                rec_embeddings = np.array([])
