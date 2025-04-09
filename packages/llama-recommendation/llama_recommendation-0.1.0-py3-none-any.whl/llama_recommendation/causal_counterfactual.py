"""
Counterfactual reasoning for causal recommendation.

This module provides methods for generating and reasoning about counterfactual
scenarios for causal recommendations.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import mlx.core as mx
import numpy as np
from llama_recommender.utils.logging import get_logger


class CounterfactualExplainer:
    """
    Explainer for generating counterfactual explanations.

    This class generates counterfactual explanations for recommendations,
    explaining what would need to change for a different outcome.
    """

    def __init__(
        self,
        base_model: "BaseModel",
        embeddings_manager: Optional["EmbeddingManager"] = None,
        num_counterfactuals: int = 3,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the counterfactual explainer.

        Args:
            base_model: Base recommendation model
            embeddings_manager: Manager for user and item embeddings
            num_counterfactuals: Number of counterfactuals to generate
            logger: Logger instance
        """
        self.base_model = base_model
        self.embeddings_manager = embeddings_manager
        self.num_counterfactuals = num_counterfactuals
        self.logger = logger or get_logger(self.__class__.__name__)

    def generate_explanation(
        self,
        user_id: str,
        item_id: str,
        context: Optional[Dict[str, Any]] = None,
        target_outcome: str = "positive",
        top_k_features: int = 3,
    ) -> Dict[str, Any]:
        """
        Generate a counterfactual explanation for a recommendation.

        Args:
            user_id: User identifier
            item_id: Item identifier
            context: Optional contextual information
            target_outcome: Target outcome ("positive" or "negative")
            top_k_features: Number of top features to include in explanation

        Returns:
            Dictionary with counterfactual explanation
        """
        # Get user and item embeddings
        user_embedding = self.base_model.encode_user(user_id, context)
        item_embedding = self.base_model.encode_item(item_id)

        # Get current prediction
        prediction = self.base_model.predict(user_id, [item_id], context)[0]

        # Determine target direction (increase or decrease score)
        is_positive_target = target_outcome == "positive"
        if (prediction > 0.5 and not is_positive_target) or (
            prediction <= 0.5 and is_positive_target
        ):
            # Need to change prediction
            target_direction = 1 if is_positive_target else -1
        else:
            # Already at target outcome
            return {
                "user_id": user_id,
                "item_id": item_id,
                "current_prediction": float(prediction),
                "already_at_target": True,
                "explanation": f"The model already predicts a {target_outcome} outcome for this user-item pair.",
            }

        # Identify important features
        important_features = self._identify_important_features(
            user_embedding, item_embedding, target_direction, top_k_features
        )

        # Generate counterfactual embeddings
        counterfactual_embeddings = self._generate_counterfactuals(
            user_embedding, item_embedding, important_features, target_direction
        )

        # Evaluate counterfactuals
        counterfactual_evaluations = []
        for i, (cf_user_emb, cf_item_emb) in enumerate(counterfactual_embeddings):
            # Convert to MLX arrays for prediction
            cf_user_emb_mx = mx.array(cf_user_emb.reshape(1, -1))
            cf_item_emb_mx = mx.array(cf_item_emb.reshape(1, -1))

            # Forward pass through model
            with mx.eval_mode():
                cf_score = self.base_model._forward(cf_user_emb_mx, cf_item_emb_mx)

            # Compute change in prediction
            cf_prediction = float(cf_score[0, 0])
            pred_change = cf_prediction - prediction

            # Generate textual explanation
            explanation = self._generate_textual_explanation(
                important_features, target_direction, cf_prediction, prediction
            )

            counterfactual_evaluations.append(
                {
                    "counterfactual_id": i,
                    "prediction": cf_prediction,
                    "change": pred_change,
                    "explanation": explanation,
                }
            )

        # Sort counterfactuals by prediction change in target direction
        counterfactual_evaluations.sort(key=lambda x: target_direction * x["change"], reverse=True)

        return {
            "user_id": user_id,
            "item_id": item_id,
            "current_prediction": float(prediction),
            "target_outcome": target_outcome,
            "important_features": important_features,
            "counterfactuals": counterfactual_evaluations,
        }

    def _identify_important_features(
        self,
        user_embedding: np.ndarray,
        item_embedding: np.ndarray,
        target_direction: int,
        top_k: int,
    ) -> List[Dict[str, Any]]:
        """
        Identify important features for counterfactual generation.

        Args:
            user_embedding: User embedding vector
            item_embedding: Item embedding vector
            target_direction: Direction to change prediction (1 or -1)
            top_k: Number of top features to return

        Returns:
            List of important features with indices and sensitivities
        """
        # Compute gradient of prediction with respect to inputs
        user_emb_mx = mx.array(user_embedding.reshape(1, -1))
        item_emb_mx = mx.array(item_embedding.reshape(1, -1))

        # Function to compute prediction
        def predict(user_emb, item_emb):
            with mx.eval_mode():
                return self.base_model._forward(user_emb, item_emb)

        # Compute gradients
        user_grad, item_grad = mx.grad(predict, argnums=(0, 1))(user_emb_mx, item_emb_mx)

        # Convert to NumPy arrays
        user_grad_np = np.array(user_grad[0])
        item_grad_np = np.array(item_grad[0])

        # Compute sensitivities (gradient * value)
        user_sensitivities = user_grad_np * user_embedding
        item_sensitivities = item_grad_np * item_embedding

        # Adjust sensitivities based on target direction
        if target_direction < 0:
            user_sensitivities = -user_sensitivities
            item_sensitivities = -item_sensitivities

        # Identify important features
        important_features = []

        # User features
        user_indices = np.argsort(user_sensitivities)[::-1][:top_k]
        for i, idx in enumerate(user_indices):
            important_features.append(
                {
                    "type": "user",
                    "index": int(idx),
                    "sensitivity": float(user_sensitivities[idx]),
                    "value": float(user_embedding[idx]),
                }
            )

        # Item features
        item_indices = np.argsort(item_sensitivities)[::-1][:top_k]
        for i, idx in enumerate(item_indices):
            important_features.append(
                {
                    "type": "item",
                    "index": int(idx),
                    "sensitivity": float(item_sensitivities[idx]),
                    "value": float(item_embedding[idx]),
                }
            )

        # Sort by sensitivity
        important_features.sort(key=lambda x: x["sensitivity"], reverse=True)

        # Take top_k overall
        return important_features[:top_k]

    def _generate_counterfactuals(
        self,
        user_embedding: np.ndarray,
        item_embedding: np.ndarray,
        important_features: List[Dict[str, Any]],
        target_direction: int,
    ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Generate counterfactual embeddings by modifying important features.

        Args:
            user_embedding: User embedding vector
            item_embedding: Item embedding vector
            important_features: List of important features to modify
            target_direction: Direction to change prediction (1 or -1)

        Returns:
            List of counterfactual embedding pairs (user, item)
        """
        counterfactuals = []

        # Generate a counterfactual for each important feature
        for feature in important_features[: self.num_counterfactuals]:
            # Copy embeddings
            cf_user_emb = user_embedding.copy()
            cf_item_emb = item_embedding.copy()

            # Modify the feature
            feature_type = feature["type"]
            index = feature["index"]
            sensitivity = feature["sensitivity"]

            # Scale change based on sensitivity
            change_magnitude = 0.5 * abs(sensitivity)
            change = target_direction * change_magnitude

            if feature_type == "user":
                cf_user_emb[index] += change
            else:  # item
                cf_item_emb[index] += change

            counterfactuals.append((cf_user_emb, cf_item_emb))

        # Generate an additional counterfactual by modifying all important features
        cf_user_emb = user_embedding.copy()
        cf_item_emb = item_embedding.copy()

        for feature in important_features:
            feature_type = feature["type"]
            index = feature["index"]
            sensitivity = feature["sensitivity"]

            # Smaller change for combined counterfactual
            change_magnitude = 0.2 * abs(sensitivity)
            change = target_direction * change_magnitude

            if feature_type == "user":
                cf_user_emb[index] += change
            else:  # item
                cf_item_emb[index] += change

        counterfactuals.append((cf_user_emb, cf_item_emb))

        return counterfactuals

    def _generate_textual_explanation(
        self,
        important_features: List[Dict[str, Any]],
        target_direction: int,
        cf_prediction: float,
        original_prediction: float,
    ) -> str:
        """
        Generate a textual explanation for a counterfactual.

        Args:
            important_features: List of important features
            target_direction: Direction of desired change
            cf_prediction: Counterfactual prediction
            original_prediction: Original prediction

        Returns:
            Textual explanation
        """
        # Determine outcome description
        if target_direction > 0:
            outcome_desc = "more likely to interact with"
            if cf_prediction > 0.5 and original_prediction <= 0.5:
                threshold_desc = " (crossing the prediction threshold)"
            else:
                threshold_desc = ""
        else:
            outcome_desc = "less likely to interact with"
            if cf_prediction <= 0.5 and original_prediction > 0.5:
                threshold_desc = " (crossing the prediction threshold)"
            else:
                threshold_desc = ""

        # Format the feature changes
        feature_changes = []
        for feature in important_features:
            feature_type = feature["type"]
            index = feature["index"]

            if feature_type == "user":
                entity = "user"
            else:
                entity = "item"

            feature_changes.append(f"{entity} feature {index}")

        # Create explanation
        if len(feature_changes) == 1:
            features_text = feature_changes[0]
        elif len(feature_changes) == 2:
            features_text = f"{feature_changes[0]} and {feature_changes[1]}"
        else:
            features_text = ", ".join(feature_changes[:-1]) + f", and {feature_changes[-1]}"

        explanation = (
            f"If {features_text} were different, "
            f"the user would be {outcome_desc} this item"
            f"{threshold_desc}. "
            f"The prediction would change from {original_prediction:.2f} to {cf_prediction:.2f}."
        )

        return explanation


class CausalSimulator:
    """
    Simulator for causal scenarios and interventions.

    This class provides methods for simulating causal interventions
    and evaluating their effects on recommendations.
    """

    def __init__(self, base_model: "BaseModel", logger: Optional[logging.Logger] = None):
        """
        Initialize the causal simulator.

        Args:
            base_model: Base recommendation model
            logger: Logger instance
        """
        self.base_model = base_model
        self.logger = logger or get_logger(self.__class__.__name__)

    def simulate_intervention(
        self,
        user_id: str,
        item_ids: List[str],
        intervention: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Simulate the effect of an intervention on recommendations.

        Args:
            user_id: User identifier
            item_ids: List of item identifiers
            intervention: Dictionary describing the intervention
            context: Optional contextual information

        Returns:
            Dictionary with simulation results
        """
        # Get baseline predictions
        baseline_scores = self.base_model.predict(user_id, item_ids, context)

        # Apply intervention
        modified_context = self._apply_intervention(context or {}, intervention)

        # Get predictions with intervention
        intervention_scores = self.base_model.predict(user_id, item_ids, modified_context)

        # Compute effects
        effects = intervention_scores - baseline_scores

        # Organize results
        item_results = []
        for i, item_id in enumerate(item_ids):
            item_results.append(
                {
                    "item_id": item_id,
                    "baseline_score": float(baseline_scores[i]),
                    "intervention_score": float(intervention_scores[i]),
                    "effect": float(effects[i]),
                }
            )

        # Sort by effect magnitude
        item_results.sort(key=lambda x: abs(x["effect"]), reverse=True)

        return {
            "user_id": user_id,
            "intervention": intervention,
            "item_results": item_results,
            "average_effect": float(np.mean(effects)),
            "max_effect": float(np.max(effects)),
            "min_effect": float(np.min(effects)),
        }

    def _apply_intervention(
        self, context: Dict[str, Any], intervention: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply intervention to context.

        Args:
            context: Original context
            intervention: Intervention to apply

        Returns:
            Modified context
        """
        # Copy context to avoid modifying the original
        modified_context = context.copy()

        # Apply intervention based on type
        intervention_type = intervention.get("type", "context_modification")

        if intervention_type == "context_modification":
            # Modify context variables
            context_changes = intervention.get("changes", {})
            for key, value in context_changes.items():
                modified_context[key] = value

        elif intervention_type == "feature_modification":
            # Add feature modifications to context
            modified_context["feature_modifications"] = intervention.get("modifications", [])

        elif intervention_type == "embedding_modification":
            # Add embedding modifications to context
            modified_context["embedding_modifications"] = intervention.get("modifications", [])

        else:
            self.logger.warning(f"Unknown intervention type: {intervention_type}")

        return modified_context

    def evaluate_treatment_policy(
        self,
        policy: Dict[str, Any],
        user_ids: List[str],
        item_pool: List[str],
        num_samples: int = 100,
    ) -> Dict[str, Any]:
        """
        Evaluate a treatment policy on a sample of users and items.

        Args:
            policy: Treatment policy to evaluate
            user_ids: List of user IDs to include in evaluation
            item_pool: Pool of items to recommend from
            num_samples: Number of user-item pairs to sample

        Returns:
            Dictionary with policy evaluation results
        """
        import random

        # Sample user-item pairs
        samples = []
        for _ in range(num_samples):
            user_id = random.choice(user_ids)
            item_id = random.choice(item_pool)
            samples.append((user_id, item_id))

        # Evaluate policy on each sample
        outcomes = []
        for user_id, item_id in samples:
            # Determine if sample receives treatment according to policy
            treated = self._apply_policy(policy, user_id, item_id)

            # Get prediction with and without treatment
            if treated:
                # Context with treatment
                context = {"treatment": True}

                # Get prediction
                with_treatment = float(self.base_model.predict(user_id, [item_id], context)[0])

                # Context without treatment
                context = {"treatment": False}

                # Get prediction
                without_treatment = float(self.base_model.predict(user_id, [item_id], context)[0])

                # Compute treatment effect
                effect = with_treatment - without_treatment
            else:
                # No treatment applied
                effect = 0.0
                with_treatment = float(
                    self.base_model.predict(user_id, [item_id], {"treatment": False})[0]
                )
                without_treatment = with_treatment

            outcomes.append(
                {
                    "user_id": user_id,
                    "item_id": item_id,
                    "treated": treated,
                    "with_treatment": with_treatment,
                    "without_treatment": without_treatment,
                    "effect": effect,
                }
            )

        # Compute overall metrics
        treated_samples = [o for o in outcomes if o["treated"]]
        untreated_samples = [o for o in outcomes if not o["treated"]]

        policy_value = 0.0
        if treated_samples:
            # Average outcome with treatment for treated samples
            treated_outcomes = np.mean([o["with_treatment"] for o in treated_samples])
            policy_value += len(treated_samples) / num_samples * treated_outcomes

        if untreated_samples:
            # Average outcome without treatment for untreated samples
            untreated_outcomes = np.mean([o["without_treatment"] for o in untreated_samples])
            policy_value += len(untreated_samples) / num_samples * untreated_outcomes

        # Compute average treatment effect on the treated (ATT)
        att = 0.0
        if treated_samples:
            att = np.mean([o["effect"] for o in treated_samples])

        return {
            "policy": policy,
            "num_samples": num_samples,
            "num_treated": len(treated_samples),
            "num_untreated": len(untreated_samples),
            "policy_value": float(policy_value),
            "att": float(att),
            "sample_outcomes": outcomes,
        }

    def _apply_policy(self, policy: Dict[str, Any], user_id: str, item_id: str) -> bool:
        """
        Determine if a user-item pair receives treatment under a policy.

        Args:
            policy: Treatment policy
            user_id: User identifier
            item_id: Item identifier

        Returns:
            True if the pair receives treatment, False otherwise
        """
        policy_type = policy.get("type", "random")

        if policy_type == "random":
            # Random assignment with specified probability
            prob = policy.get("probability", 0.5)
            return np.random.random() < prob

        elif policy_type == "score_threshold":
            # Assign treatment based on predicted score
            threshold = policy.get("threshold", 0.5)
            score = float(self.base_model.predict(user_id, [item_id])[0])
            return score >= threshold

        elif policy_type == "user_group":
            # Assign treatment based on user group
            # This would require additional user metadata
            return False

        else:
            self.logger.warning(f"Unknown policy type: {policy_type}")
            return False
