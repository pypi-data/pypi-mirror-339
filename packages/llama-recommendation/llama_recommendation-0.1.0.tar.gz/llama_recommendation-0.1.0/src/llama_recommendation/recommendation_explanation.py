"""
Explanation generation for the recommendation system.

This module provides methods for generating human-readable explanations
for recommendations to increase transparency and user trust.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from llama_recommender.utils.logging import get_logger


class ExplanationGenerator:
    """
    Generate explanations for recommendations.

    This class provides methods for generating human-readable explanations
    for why items were recommended to users.
    """

    def __init__(
        self,
        model: "BaseModel",
        explanation_types: Optional[List[str]] = None,
        explanation_style: str = "natural",
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the explanation generator.

        Args:
            model: Recommendation model
            explanation_types: List of explanation types to generate
            explanation_style: Style of explanations ('natural', 'technical', or 'mixed')
            logger: Logger instance
        """
        self.model = model
        self.explanation_types = explanation_types or [
            "similarity",
            "popularity",
            "category",
            "collaborative",
            "diversity",
            "fairness",
            "trending",
        ]
        self.explanation_style = explanation_style
        self.logger = logger or get_logger(self.__class__.__name__)

    def generate(self, user_id: str, item_id: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an explanation for a recommendation.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Human-readable explanation
        """
        context = context or {}

        # Get item metadata
        item_metadata = context.get("item_metadata", {}).get(item_id, {})

        # Collect explanation components
        explanation_components = []

        # Apply each explanation type
        for exp_type in self.explanation_types:
            try:
                if exp_type == "similarity":
                    component = self._generate_similarity_explanation(user_id, item_id, context)
                elif exp_type == "popularity":
                    component = self._generate_popularity_explanation(item_id, item_metadata)
                elif exp_type == "category":
                    component = self._generate_category_explanation(user_id, item_id, context)
                elif exp_type == "collaborative":
                    component = self._generate_collaborative_explanation(user_id, item_id, context)
                elif exp_type == "diversity":
                    component = self._generate_diversity_explanation(user_id, item_id, context)
                elif exp_type == "fairness":
                    component = self._generate_fairness_explanation(user_id, item_id, context)
                elif exp_type == "trending":
                    component = self._generate_trending_explanation(item_id, item_metadata)
                elif exp_type == "causal":
                    component = self._generate_causal_explanation(user_id, item_id, context)
                else:
                    self.logger.warning(f"Unknown explanation type: {exp_type}")
                    component = None

                if component:
                    explanation_components.append(component)

            except Exception as e:
                self.logger.warning(f"Error generating {exp_type} explanation: {e}")

        # Combine explanation components based on style
        if not explanation_components:
            return "This item was recommended based on your preferences and past interactions."

        if self.explanation_style == "natural":
            return self._format_natural_explanation(explanation_components)
        elif self.explanation_style == "technical":
            return self._format_technical_explanation(explanation_components)
        else:  # mixed
            return self._format_mixed_explanation(explanation_components)

    def _generate_similarity_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on user-item similarity.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Explanation component or None
        """
        # Get user and item embeddings
        user_embedding = self.model.encode_user(user_id, context)
        item_embedding = self.model.encode_item(item_id)

        # Calculate similarity
        similarity = self._cosine_similarity(user_embedding, item_embedding)

        # Generate explanation based on similarity
        if similarity > 0.8:
            return "This item closely matches your preferences"
        elif similarity > 0.6:
            return "This item aligns well with your interests"
        elif similarity > 0.4:
            return "This item matches some of your preferences"
        else:
            return None

    def _generate_popularity_explanation(
        self, item_id: str, item_metadata: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on item popularity.

        Args:
            item_id: Item identifier
            item_metadata: Item metadata

        Returns:
            Explanation component or None
        """
        # Check if popularity information is available
        popularity = item_metadata.get("popularity")
        if popularity is None:
            return None

        # Generate explanation based on popularity
        if popularity > 0.9:
            return "This is one of our most popular items"
        elif popularity > 0.7:
            return "This is a popular item among users"
        elif popularity > 0.5:
            return "This item has been enjoyed by many users"
        else:
            return None

    def _generate_category_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on category preferences.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Explanation component or None
        """
        # Get item categories
        item_metadata = context.get("item_metadata", {}).get(item_id, {})
        item_categories = item_metadata.get("categories", [])

        if not item_categories:
            return None

        # Get user preferences
        user_preferences = context.get("user_preferences", {})
        preferred_categories = user_preferences.get("preferred_categories", [])

        # Find matching categories
        matching_categories = [cat for cat in item_categories if cat in preferred_categories]

        if matching_categories:
            if len(matching_categories) == 1:
                return f"This is in the '{matching_categories[0]}' category, which you've shown interest in"
            elif len(matching_categories) == 2:
                return f"This is in the '{matching_categories[0]}' and '{matching_categories[1]}' categories, which match your interests"
            else:
                return f"This matches several categories you're interested in, including {', '.join(matching_categories[:3])}"
        else:
            # Check if this is a diversification recommendation
            if context.get("diversify_categories", False):
                return f"This introduces you to the '{item_categories[0]}' category, which might broaden your interests"

            return None

    def _generate_collaborative_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on collaborative filtering.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Explanation component or None
        """
        # Check if collaborative filtering info is available
        cf_info = context.get("collaborative_info", {})

        similar_users = cf_info.get("similar_users", [])

        if similar_users:
            user_count = len(similar_users)

            if "anonymous" in context.get("privacy_settings", []):
                return f"Users with similar tastes have enjoyed this item"
            else:
                if user_count == 1:
                    return f"User {similar_users[0]} with similar preferences enjoyed this item"
                elif user_count <= 3:
                    return f"Several users with similar tastes, including {', '.join(similar_users[:3])}, enjoyed this item"
                else:
                    return f"Many users with similar preferences to yours enjoyed this item"
        else:
            return None

    def _generate_diversity_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on diversity considerations.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Explanation component or None
        """
        # Check if diversity info is available
        diversity_contribution = context.get("diversity_contribution", {}).get(item_id)

        if diversity_contribution is not None and diversity_contribution > 0.5:
            return "This adds variety to your recommendations"
        else:
            return None

    def _generate_fairness_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on fairness considerations.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Explanation component or None
        """
        # Check if fairness adjustment was applied
        fairness_adjusted = context.get("fairness_adjusted", False)

        if fairness_adjusted:
            return "This contributes to a balanced set of recommendations"
        else:
            return None

    def _generate_trending_explanation(
        self, item_id: str, item_metadata: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on trending status.

        Args:
            item_id: Item identifier
            item_metadata: Item metadata

        Returns:
            Explanation component or None
        """
        # Check if trending information is available
        trending_score = item_metadata.get("trending")
        if trending_score is None:
            return None

        # Generate explanation based on trending score
        if trending_score > 0.9:
            return "This is currently trending"
        elif trending_score > 0.7:
            return "This is gaining popularity right now"
        elif trending_score > 0.5:
            return "This has been growing in popularity recently"
        else:
            return None

    def _generate_causal_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate an explanation based on causal effects.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Explanation component or None
        """
        # Check if causal effect information is available
        causal_effects = context.get("causal_effects", {})
        treatment_effect = causal_effects.get(item_id)

        if treatment_effect is not None:
            if treatment_effect > 0.2:
                return "Our analysis shows you're likely to find this item particularly valuable"
            elif treatment_effect > 0.1:
                return "Our analysis indicates this item might be especially relevant for you"
            else:
                return None
        else:
            return None

    def _format_natural_explanation(self, components: List[str]) -> str:
        """
        Format explanation components in a natural language style.

        Args:
            components: List of explanation components

        Returns:
            Natural language explanation
        """
        if not components:
            return "This item was recommended based on your preferences and past interactions."

        # Select top components
        top_components = components[:3]

        if len(top_components) == 1:
            return f"{top_components[0]}."
        elif len(top_components) == 2:
            return f"{top_components[0]} and {top_components[1].lower()}."
        else:
            return f"{top_components[0]}, {top_components[1].lower()}, and {top_components[2].lower()}."

    def _format_technical_explanation(self, components: List[str]) -> str:
        """
        Format explanation components in a technical style.

        Args:
            components: List of explanation components

        Returns:
            Technical explanation
        """
        if not components:
            return "Item recommended based on user preference analysis."

        # Format as bullet points
        formatted = "Recommendation factors:\n"
        for component in components:
            formatted += f"- {component}\n"

        return formatted.strip()

    def _format_mixed_explanation(self, components: List[str]) -> str:
        """
        Format explanation components in a mixed style.

        Args:
            components: List of explanation components

        Returns:
            Mixed style explanation
        """
        if not components:
            return "This item was recommended based on your preferences."

        # Combine first component naturally, then add technical details
        primary = components[0]
        secondary = components[1:3] if len(components) > 1 else []

        if secondary:
            details = ", ".join(secondary)
            return f"{primary}. Additional factors: {details}."
        else:
            return f"{primary}."

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity (between -1 and 1)
        """
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0

        dot_product = np.dot(vec1, vec2)
        similarity = dot_product / (norm1 * norm2)

        return float(similarity)

    def generate_batch_explanations(
        self, user_id: str, item_ids: List[str], context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Generate explanations for multiple recommendations.

        Args:
            user_id: User identifier
            item_ids: List of item identifiers
            context: Contextual information

        Returns:
            Dictionary mapping item IDs to explanations
        """
        context = context or {}
        explanations = {}

        for item_id in item_ids:
            explanation = self.generate(user_id, item_id, context)
            explanations[item_id] = explanation

        return explanations

    def set_explanation_style(self, style: str) -> None:
        """
        Set the explanation style.

        Args:
            style: Explanation style ('natural', 'technical', or 'mixed')
        """
        valid_styles = ["natural", "technical", "mixed"]
        if style not in valid_styles:
            raise ValueError(
                f"Invalid explanation style: {style}. "
                f"Valid options are: {', '.join(valid_styles)}"
            )

        self.explanation_style = style

    def personalize_explanations(self, user_id: str, context: Dict[str, Any]) -> None:
        """
        Personalize explanation settings for a user.

        Args:
            user_id: User identifier
            context: User preferences and settings
        """
        # Get user preferences
        user_preferences = context.get("user_preferences", {})

        # Set explanation style based on user preference
        preferred_style = user_preferences.get("explanation_style")
        if preferred_style in ["natural", "technical", "mixed"]:
            self.explanation_style = preferred_style

        # Set explanation types based on user preference
        preferred_types = user_preferences.get("explanation_types")
        if preferred_types:
            self.explanation_types = preferred_types

    def get_counterfactual_explanation(
        self, user_id: str, item_id: str, context: Dict[str, Any]
    ) -> str:
        """
        Generate a counterfactual explanation for a recommendation.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Contextual information

        Returns:
            Counterfactual explanation
        """
        try:
            # Try to use causal module for counterfactual explanations
            from llama_recommender.causal.counterfactual import CounterfactualExplainer

            counterfactual_explainer = CounterfactualExplainer(base_model=self.model)

            explanation = counterfactual_explainer.generate_explanation(
                user_id=user_id, item_id=item_id, context=context, target_outcome="positive"
            )

            if "explanation" in explanation:
                return explanation["explanation"]
            else:
                return "If certain features were different, the recommendation might change."
        except Exception as e:
            self.logger.warning(f"Error generating counterfactual explanation: {e}")
            return "If certain features were different, the recommendation might change."
