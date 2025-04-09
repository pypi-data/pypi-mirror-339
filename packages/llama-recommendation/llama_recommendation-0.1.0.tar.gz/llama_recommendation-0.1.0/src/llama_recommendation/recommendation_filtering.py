"""
Filtering module for the recommendation system.

This module provides methods for filtering recommendation candidates
based on ethical guidelines, user preferences, and other constraints.
"""

import logging
from typing import Any, Dict, List, Optional

import numpy as np
from llama_recommender.utils.logging import get_logger


class EthicalFilter:
    """
    Filter recommendations based on ethical guidelines.

    This class provides methods for filtering recommendation candidates
    to ensure they meet ethical standards and guidelines.
    """

    def __init__(
        self,
        threshold: float = 0.7,
        fairness_weight: float = 0.3,
        content_safety_weight: float = 0.4,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the ethical filter.

        Args:
            threshold: Minimum ethical score threshold (0-1)
            fairness_weight: Weight for fairness component (0-1)
            content_safety_weight: Weight for content safety component (0-1)
            logger: Logger instance
        """
        self.threshold = threshold
        self.fairness_weight = fairness_weight
        self.content_safety_weight = content_safety_weight
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize ethics components
        self._init_ethics_components()

    def _init_ethics_components(self) -> None:
        """Initialize ethics evaluation components."""
        try:
            from llama_recommender.ethics.guidelines import (
                ContentSafetyChecker,
                EthicalGuidelines,
            )

            self.ethical_guidelines = EthicalGuidelines(minimum_ethical_score=self.threshold)

            self.content_safety_checker = ContentSafetyChecker()

            self.logger.info("Initialized ethics components")
        except ImportError as e:
            self.logger.warning(f"Could not initialize ethics components: {e}")
            self.ethical_guidelines = None
            self.content_safety_checker = None

    def filter(
        self,
        user_id: str,
        items: List[Dict[str, Any]],
        attributes: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Filter items based on ethical guidelines.

        Args:
            user_id: User identifier
            items: List of items to filter
            attributes: Additional attributes for filtering

        Returns:
            List of filtered items
        """
        if not items:
            return []

        # Get user attributes
        user_attributes = attributes.get("user", {}) if attributes else {}

        # Initialize filtered items
        filtered_items = []
        filtered_out = []

        # Apply ethical filtering
        for item in items:
            # Extract item metadata
            item_id = item["item_id"]
            item_metadata = attributes.get("items", {}).get(item_id, {}) if attributes else {}

            # Check if item is appropriate for user age
            if "age" in user_attributes and "min_age" in item_metadata:
                if user_attributes["age"] < item_metadata["min_age"]:
                    filtered_out.append(item)
                    self.logger.info(f"Filtered out item {item_id} due to age restriction")
                    continue

            # Apply ethical guidelines if available
            if self.ethical_guidelines:
                try:
                    # Evaluate item against ethical guidelines
                    evaluation = self.ethical_guidelines.evaluate_item(
                        item_id, item_metadata, user_id, user_attributes
                    )

                    # Add ethical score to item
                    item_with_ethics = item.copy()
                    item_with_ethics["ethical_score"] = evaluation["ethical_score"]
                    item_with_ethics["ethical_issues"] = evaluation["issues"]

                    # Filter based on ethical score
                    if evaluation["allowed"]:
                        filtered_items.append(item_with_ethics)
                    else:
                        filtered_out.append(item_with_ethics)
                        self.logger.info(
                            f"Filtered out item {item_id} with ethical score {evaluation['ethical_score']}"
                        )

                except Exception as e:
                    # In case of error, include the item but log the error
                    self.logger.warning(f"Error in ethical evaluation of item {item_id}: {e}")
                    filtered_items.append(item)

            else:
                # If ethical guidelines not available, apply basic filtering
                filtered_items.append(item)

        # Apply content safety check if available
        if self.content_safety_checker and attributes and "items" in attributes:
            safe_items = []

            for item in filtered_items:
                item_id = item["item_id"]
                item_metadata = attributes["items"].get(item_id, {})

                try:
                    # Check content safety
                    safety_result = self.content_safety_checker.check_item_metadata(item_metadata)

                    # Add safety score to item
                    item_with_safety = item.copy()
                    item_with_safety["safety_score"] = safety_result["overall_safety_score"]
                    item_with_safety["safety_issues"] = safety_result["content_issues"]

                    # Filter based on safety
                    if safety_result["is_safe"]:
                        safe_items.append(item_with_safety)
                    else:
                        filtered_out.append(item_with_safety)
                        self.logger.info(f"Filtered out item {item_id} due to safety concerns")

                except Exception as e:
                    # In case of error, include the item but log the error
                    self.logger.warning(f"Error in safety check of item {item_id}: {e}")
                    safe_items.append(item)

            filtered_items = safe_items

        # Apply fairness check
        has_fairness_metrics = (
            any("fairness_" in key for key in attributes.keys()) if attributes else False
        )

        if has_fairness_metrics and attributes:
            # Apply fairness constraints
            try:
                from llama_recommender.ethics.fairness import FairnessConstraint

                fairness_constraint = FairnessConstraint(
                    constraint_type="demographic_parity", threshold=0.1
                )

                # Extract group memberships
                group_memberships = {}
                for key, value in attributes.items():
                    if key.startswith("fairness_"):
                        attribute_name = key[9:]  # Remove 'fairness_' prefix
                        group_memberships[attribute_name] = value

                # Check if we have any group memberships
                if group_memberships:
                    # Extract prediction scores
                    predictions = np.array([item.get("score", 0.5) for item in filtered_items])

                    # Apply fairness constraint
                    adjusted_predictions = fairness_constraint.apply_constraint(
                        predictions, group_memberships
                    )

                    # Update scores with adjusted predictions
                    for i, item in enumerate(filtered_items):
                        item["original_score"] = item["score"]
                        item["score"] = float(adjusted_predictions[i])
                        item["fairness_adjusted"] = True

            except Exception as e:
                self.logger.warning(f"Error applying fairness constraints: {e}")

        # Sort by score
        filtered_items.sort(key=lambda x: x["score"], reverse=True)

        self.logger.info(f"Filtered {len(filtered_out)} of {len(items)} items for user {user_id}")

        return filtered_items

    def get_explanation(self, item: Dict[str, Any]) -> str:
        """
        Get an explanation for why an item was filtered or allowed.

        Args:
            item: Item with ethical scores

        Returns:
            Human-readable explanation
        """
        # Check if item has ethical scores
        if "ethical_score" not in item:
            return "This item has not been evaluated for ethical considerations."

        # Check if item has ethical issues
        if "ethical_issues" in item and item["ethical_issues"]:
            issues = item["ethical_issues"]
            issue_descriptions = []

            for issue in issues:
                issue_type = issue.get("type", "unknown")

                if issue_type == "banned_category":
                    categories = issue.get("categories", [])
                    issue_descriptions.append(
                        f"This item contains banned content categories: {', '.join(categories)}."
                    )

                elif issue_type == "age_restricted_content":
                    categories = issue.get("categories", [])
                    issue_descriptions.append(
                        f"This item contains age-restricted content: {', '.join(categories)}."
                    )

                elif issue_type == "sensitive_attributes":
                    attributes = issue.get("attributes", [])
                    issue_descriptions.append(
                        f"This item contains potentially sensitive content related to: {', '.join(attributes)}."
                    )

                else:
                    issue_descriptions.append(
                        f"This item has an ethical concern of type: {issue_type}."
                    )

            if issue_descriptions:
                return " ".join(issue_descriptions)

        # Check if item has safety issues
        if "safety_issues" in item and item["safety_issues"]:
            issues = item["safety_issues"]
            issue_descriptions = []

            for issue in issues:
                issue_type = issue.get("type", "unknown")

                if issue_type == "hate_speech":
                    issue_descriptions.append(
                        "This item may contain hate speech or discriminatory language."
                    )
                elif issue_type == "violence":
                    issue_descriptions.append(
                        "This item may contain violent themes or glorify violence."
                    )
                elif issue_type == "sexual_content":
                    issue_descriptions.append("This item may contain explicit sexual material.")
                elif issue_type == "harassment":
                    issue_descriptions.append("This item may contain harassment or bullying.")
                elif issue_type == "self_harm":
                    issue_descriptions.append("This item may reference self-harm or suicide.")
                elif issue_type == "misinformation":
                    issue_descriptions.append(
                        "This item may contain misinformation or false claims."
                    )
                else:
                    issue_descriptions.append(
                        f"This item has a safety concern of type: {issue_type}."
                    )

            if issue_descriptions:
                return " ".join(issue_descriptions)

        # If no specific issues were found
        ethical_score = item.get("ethical_score", 0)
        if ethical_score >= 0.9:
            return "This item meets high ethical standards."
        elif ethical_score >= 0.7:
            return "This item meets acceptable ethical standards."
        else:
            return "This item may not fully meet our ethical guidelines."


class UserPreferenceFilter:
    """
    Filter recommendations based on user preferences.

    This class provides methods for filtering recommendation candidates
    based on explicit and implicit user preferences.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the user preference filter.

        Args:
            logger: Logger instance
        """
        self.logger = logger or get_logger(self.__class__.__name__)

    def filter(
        self, user_id: str, items: List[Dict[str, Any]], preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Filter items based on user preferences.

        Args:
            user_id: User identifier
            items: List of items to filter
            preferences: User preferences

        Returns:
            List of filtered items
        """
        if not items:
            return []

        # Extract preference components
        exclude_categories = preferences.get("exclude_categories", [])
        preferred_categories = preferences.get("preferred_categories", [])
        min_rating = preferences.get("min_rating", 0)
        max_length = preferences.get("max_length")
        min_length = preferences.get("min_length")
        exclude_languages = preferences.get("exclude_languages", [])
        preferred_languages = preferences.get("preferred_languages", [])
        exclude_creators = preferences.get("exclude_creators", [])
        preferred_creators = preferences.get("preferred_creators", [])

        # Apply filters
        filtered_items = items.copy()

        # Filter by excluded categories
        if exclude_categories:
            filtered_items = [
                item
                for item in filtered_items
                if not any(
                    category in exclude_categories for category in item.get("categories", [])
                )
            ]

        # Filter by minimum rating
        if min_rating > 0:
            filtered_items = [
                item for item in filtered_items if item.get("rating", 0) >= min_rating
            ]

        # Filter by length constraints
        if max_length is not None:
            filtered_items = [
                item for item in filtered_items if item.get("length", 0) <= max_length
            ]

        if min_length is not None:
            filtered_items = [
                item for item in filtered_items if item.get("length", 0) >= min_length
            ]

        # Filter by excluded languages
        if exclude_languages:
            filtered_items = [
                item for item in filtered_items if item.get("language") not in exclude_languages
            ]

        # Filter by excluded creators
        if exclude_creators:
            filtered_items = [
                item for item in filtered_items if item.get("creator") not in exclude_creators
            ]

        # Boost items with preferred categories
        if preferred_categories:
            for item in filtered_items:
                item_categories = item.get("categories", [])
                category_matches = sum(
                    category in preferred_categories for category in item_categories
                )

                if category_matches > 0:
                    boost_factor = 0.05 * category_matches
                    item["score"] = item["score"] * (1 + boost_factor)
                    item["boosted_by_category"] = True

        # Boost items with preferred languages
        if preferred_languages:
            for item in filtered_items:
                if item.get("language") in preferred_languages:
                    item["score"] = item["score"] * 1.1
                    item["boosted_by_language"] = True

        # Boost items with preferred creators
        if preferred_creators:
            for item in filtered_items:
                if item.get("creator") in preferred_creators:
                    item["score"] = item["score"] * 1.15
                    item["boosted_by_creator"] = True

        # Sort by score
        filtered_items.sort(key=lambda x: x["score"], reverse=True)

        self.logger.info(
            f"Filtered {len(items) - len(filtered_items)} of {len(items)} items "
            f"based on user preferences for user {user_id}"
        )

        return filtered_items

    def get_explanation(self, item: Dict[str, Any], preferences: Dict[str, Any]) -> str:
        """
        Get an explanation for how user preferences affected an item.

        Args:
            item: Item with preference adjustments
            preferences: User preferences

        Returns:
            Human-readable explanation
        """
        explanations = []

        # Check for category boost
        if item.get("boosted_by_category", False):
            preferred_categories = preferences.get("preferred_categories", [])
            matching_categories = [
                category
                for category in item.get("categories", [])
                if category in preferred_categories
            ]

            if matching_categories:
                explanations.append(
                    f"This item matches your preferred categories: {', '.join(matching_categories)}"
                )

        # Check for language boost
        if item.get("boosted_by_language", False):
            language = item.get("language", "")
            explanations.append(f"This item is in your preferred language: {language}")

        # Check for creator boost
        if item.get("boosted_by_creator", False):
            creator = item.get("creator", "")
            explanations.append(f"This item is by your preferred creator: {creator}")

        if explanations:
            return " ".join(explanations)
        else:
            return "This item was recommended based on your general preferences."


class DiversityFilter:
    """
    Filter to ensure diverse recommendations.

    This class provides methods for filtering and reranking recommendations
    to ensure diversity across different dimensions.
    """

    def __init__(
        self,
        diversity_dimensions: Optional[List[str]] = None,
        category_weight: float = 0.3,
        creator_weight: float = 0.2,
        recency_weight: float = 0.1,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the diversity filter.

        Args:
            diversity_dimensions: List of dimensions to diversify ('category', 'creator', 'recency')
            category_weight: Weight for category diversity (0-1)
            creator_weight: Weight for creator diversity (0-1)
            recency_weight: Weight for recency diversity (0-1)
            logger: Logger instance
        """
        self.diversity_dimensions = diversity_dimensions or [
            "category",
            "creator",
            "recency",
        ]
        self.category_weight = category_weight
        self.creator_weight = creator_weight
