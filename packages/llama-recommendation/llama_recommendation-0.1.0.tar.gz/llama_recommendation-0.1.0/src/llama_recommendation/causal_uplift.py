"""
Uplift modeling for causal treatment effect estimation.

This module provides models and utilities for estimating causal treatment
effects in recommendation systems, allowing for more effective targeting.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from llama_recommender.utils.logging import get_logger


class UpliftModel:
    """
    Uplift model for estimating treatment effects in recommendations.

    This model estimates the causal effect of recommending an item to a user,
    allowing for more effective personalization.
    """

    def __init__(
        self,
        base_model: "BaseModel",
        embedding_dim: int = 128,
        hidden_dims: List[int] = [256, 128, 64],
        propensity_model: Optional["PropensityModel"] = None,
        meta_learner_type: str = "s-learner",
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the uplift model.

        Args:
            base_model: Base recommendation model
            embedding_dim: Dimensionality of embeddings
            hidden_dims: Hidden layer dimensions for uplift estimation
            propensity_model: Model for estimating propensity scores
            meta_learner_type: Meta-learner type ('s-learner', 't-learner' or 'x-learner')
            logger: Logger instance
        """
        self.base_model = base_model
        self.embedding_dim = embedding_dim
        self.logger = logger or get_logger(self.__class__.__name__)

        # Create uplift estimator model
        self.model = self._create_model(hidden_dims)

        # Initialize propensity model if not provided
        self.propensity_model = propensity_model
        if self.propensity_model is None:
            self.propensity_model = PropensityModel(embedding_dim=embedding_dim)

        # Check meta-learner type
        valid_meta_learners = ["s-learner", "t-learner", "x-learner"]
        if meta_learner_type not in valid_meta_learners:
            raise ValueError(
                f"Invalid meta-learner type: {meta_learner_type}. "
                f"Valid options are: {', '.join(valid_meta_learners)}"
            )

        self.meta_learner_type = meta_learner_type

    def _create_model(self, hidden_dims: List[int]) -> nn.Module:
        """
        Create the MLX model for uplift estimation.

        Args:
            hidden_dims: Hidden layer dimensions

        Returns:
            MLX module for uplift estimation
        """

        class UpliftEstimator(nn.Module):
            """MLX model for uplift estimation."""

            def __init__(self, embedding_dim: int, hidden_dims: List[int]):
                super().__init__()

                # Input dimension is 2 * embedding_dim (user and item embeddings)
                input_dim = embedding_dim * 2

                # Create MLP layers
                layers = []
                prev_dim = input_dim

                for hidden_dim in hidden_dims:
                    layers.append(nn.Linear(prev_dim, hidden_dim))
                    layers.append(nn.ReLU())
                    prev_dim = hidden_dim

                # Final output layer (scalar uplift)
                layers.append(nn.Linear(prev_dim, 1))

                self.mlp = nn.Sequential(*layers)

            def __call__(self, user_embedding: mx.array, item_embedding: mx.array) -> mx.array:
                # Concatenate embeddings
                x = mx.concatenate([user_embedding, item_embedding], axis=1)

                # Forward pass through MLP
                return self.mlp(x)

        return UpliftEstimator(embedding_dim=self.embedding_dim, hidden_dims=hidden_dims)

    def estimate_uplift(
        self, user_id: str, item_ids: List[str], context: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """
        Estimate uplift (treatment effect) for recommending items to a user.

        Args:
            user_id: User identifier
            item_ids: List of item identifiers
            context: Optional contextual information

        Returns:
            Array of estimated uplift scores
        """
        # Encode user
        user_embedding = self.base_model.encode_user(user_id, context)
        user_embedding_mx = mx.array(user_embedding.reshape(1, -1))

        # Estimate uplift for each item
        uplifts = []
        for item_id in item_ids:
            # Encode item
            item_embedding = self.base_model.encode_item(item_id)
            item_embedding_mx = mx.array(item_embedding.reshape(1, -1))

            # Forward pass through model
            with mx.eval_mode():
                uplift = self.model(user_embedding_mx, item_embedding_mx)

            uplifts.append(float(uplift[0, 0]))

        return np.array(uplifts)

    def train(
        self,
        train_data: str,
        validation_data: Optional[str] = None,
        epochs: int = 10,
        batch_size: int = 32,
        learning_rate: float = 0.001,
    ) -> Dict[str, Any]:
        """
        Train the uplift model.

        Args:
            train_data: Path to training data
            validation_data: Path to validation data
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate for optimization

        Returns:
            Dictionary of training metrics
        """
        import pandas as pd
        from tqdm import tqdm

        # Load training data
        train_df = pd.read_csv(train_data)

        # Load validation data if provided
        val_df = None
        if validation_data:
            val_df = pd.read_csv(validation_data)

        # Create optimizer
        opt = mx.optimizers.Adam(learning_rate=learning_rate)

        # Training loop
        metrics = {
            "train_loss": [],
            "val_loss": [] if val_df is not None else None,
        }

        for epoch in range(epochs):
            # Shuffle training data
            train_df = train_df.sample(frac=1).reset_index(drop=True)

            # Training steps
            train_loss = []
            for i in tqdm(range(0, len(train_df), batch_size), desc=f"Epoch {epoch + 1}/{epochs}"):
                batch = train_df.iloc[i : i + batch_size]

                # Forward pass and compute loss
                loss = self._train_step(batch, opt)
                train_loss.append(loss)

            # Validation steps
            val_loss = []
            if val_df is not None:
                for i in range(0, len(val_df), batch_size):
                    batch = val_df.iloc[i : i + batch_size]

                    # Forward pass only
                    loss = self._val_step(batch)
                    val_loss.append(loss)

            # Update metrics
            metrics["train_loss"].append(np.mean(train_loss))
            if val_df is not None:
                metrics["val_loss"].append(np.mean(val_loss))

            # Log progress
            log_msg = f"Epoch {epoch + 1}/{epochs}, Train Loss: {metrics['train_loss'][-1]:.4f}"
            if val_df is not None:
                log_msg += f", Val Loss: {metrics['val_loss'][-1]:.4f}"

            self.logger.info(log_msg)

        return metrics

    def _train_step(self, batch, optimizer) -> float:
        """
        Perform a single training step.

        Args:
            batch: Batch of training data
            optimizer: MLX optimizer

        Returns:
            Batch loss
        """
        # Extract features, treatment and outcome
        user_embeddings = []
        item_embeddings = []
        treatments = []
        outcomes = []

        for _, row in batch.iterrows():
            user_id = row["user_id"]
            item_id = row["item_id"]
            treatment = row["treatment"]  # 1 if item was recommended, 0 otherwise
            outcome = row["outcome"]  # 1 if user interacted, 0 otherwise

            # Encode user and item
            user_embedding = self.base_model.encode_user(user_id)
            item_embedding = self.base_model.encode_item(item_id)

            user_embeddings.append(user_embedding)
            item_embeddings.append(item_embedding)
            treatments.append(treatment)
            outcomes.append(outcome)

        # Convert to MLX arrays
        user_embeddings_mx = mx.array(np.stack(user_embeddings))
        item_embeddings_mx = mx.array(np.stack(item_embeddings))
        treatments_mx = mx.array(np.array(treatments).reshape(-1, 1))
        outcomes_mx = mx.array(np.array(outcomes).reshape(-1, 1))

        # Compute loss based on meta-learner type
        if self.meta_learner_type == "s-learner":
            # S-learner combines treatment and features
            loss = self._s_learner_loss(
                user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
            )
        elif self.meta_learner_type == "t-learner":
            # T-learner uses separate models for treatment and control
            loss = self._t_learner_loss(
                user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
            )
        elif self.meta_learner_type == "x-learner":
            # X-learner uses imputed outcomes
            loss = self._x_learner_loss(
                user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
            )

        # Apply gradients
        parameters, gradients = mx.grad(lambda m, u, i, t, o: loss)(
            self.model, user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
        )

        # Update parameters
        optimizer.update(parameters, gradients)

        return float(loss)

    def _val_step(self, batch) -> float:
        """
        Perform a single validation step.

        Args:
            batch: Batch of validation data

        Returns:
            Batch loss
        """
        # Extract features, treatment and outcome
        user_embeddings = []
        item_embeddings = []
        treatments = []
        outcomes = []

        for _, row in batch.iterrows():
            user_id = row["user_id"]
            item_id = row["item_id"]
            treatment = row["treatment"]
            outcome = row["outcome"]

            # Encode user and item
            user_embedding = self.base_model.encode_user(user_id)
            item_embedding = self.base_model.encode_item(item_id)

            user_embeddings.append(user_embedding)
            item_embeddings.append(item_embedding)
            treatments.append(treatment)
            outcomes.append(outcome)

        # Convert to MLX arrays
        user_embeddings_mx = mx.array(np.stack(user_embeddings))
        item_embeddings_mx = mx.array(np.stack(item_embeddings))
        treatments_mx = mx.array(np.array(treatments).reshape(-1, 1))
        outcomes_mx = mx.array(np.array(outcomes).reshape(-1, 1))

        # Compute loss based on meta-learner type
        if self.meta_learner_type == "s-learner":
            loss = self._s_learner_loss(
                user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
            )
        elif self.meta_learner_type == "t-learner":
            loss = self._t_learner_loss(
                user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
            )
        elif self.meta_learner_type == "x-learner":
            loss = self._x_learner_loss(
                user_embeddings_mx, item_embeddings_mx, treatments_mx, outcomes_mx
            )

        return float(loss)

    def _s_learner_loss(
        self,
        user_embeddings: mx.array,
        item_embeddings: mx.array,
        treatments: mx.array,
        outcomes: mx.array,
    ) -> mx.array:
        """
        Compute loss for S-learner.

        S-learner uses a single model for both treated and control groups,
        with treatment as a feature.

        Args:
            user_embeddings: User embeddings
            item_embeddings: Item embeddings
            treatments: Treatment indicators
            outcomes: Observed outcomes

        Returns:
            Loss value
        """
        # Predict outcomes
        predictions = self.model(user_embeddings, item_embeddings)

        # Compute MSE loss
        loss = mx.mean((predictions - outcomes) ** 2)

        return loss

    def _t_learner_loss(
        self,
        user_embeddings: mx.array,
        item_embeddings: mx.array,
        treatments: mx.array,
        outcomes: mx.array,
    ) -> mx.array:
        """
        Compute loss for T-learner.

        T-learner uses separate models for treated and control groups.
        This is a simplified implementation using a single model.

        Args:
            user_embeddings: User embeddings
            item_embeddings: Item embeddings
            treatments: Treatment indicators
            outcomes: Observed outcomes

        Returns:
            Loss value
        """
        # Split data into treatment and control groups
        treated_mask = treatments == 1
        control_mask = treatments == 0

        # Handle empty groups
        if mx.sum(treated_mask) == 0 or mx.sum(control_mask) == 0:
            return mx.array(0.0)

        # Compute predictions for both groups
        treated_predictions = self.model(
            user_embeddings[treated_mask], item_embeddings[treated_mask]
        )
        control_predictions = self.model(
            user_embeddings[control_mask], item_embeddings[control_mask]
        )

        # Compute MSE loss for each group
        treated_loss = mx.mean((treated_predictions - outcomes[treated_mask]) ** 2)
        control_loss = mx.mean((control_predictions - outcomes[control_mask]) ** 2)

        # Combine losses
        loss = treated_loss + control_loss

        return loss

    def _x_learner_loss(
        self,
        user_embeddings: mx.array,
        item_embeddings: mx.array,
        treatments: mx.array,
        outcomes: mx.array,
    ) -> mx.array:
        """
        Compute loss for X-learner.

        X-learner uses imputed counterfactual outcomes to improve estimation.
        This is a simplified implementation.

        Args:
            user_embeddings: User embeddings
            item_embeddings: Item embeddings
            treatments: Treatment indicators
            outcomes: Observed outcomes

        Returns:
            Loss value
        """
        # This is a simplified implementation
        # In practice, X-learner would use more sophisticated imputation

        # Predict outcomes
        predictions = self.model(user_embeddings, item_embeddings)

        # Compute MSE loss
        loss = mx.mean((predictions - outcomes) ** 2)

        # Add regularization term for uplift consistency
        uplift_loss = mx.mean(mx.abs(predictions))

        return loss + 0.1 * uplift_loss

    def save(self, path: str) -> None:
        """
        Save model to disk.

        Args:
            path: Path to save the model
        """
        import os

        os.makedirs(path, exist_ok=True)

        # Save model weights
        mx.save(os.path.join(path, "uplift_model.npz"), self.model.parameters())

        # Save metadata
        import json

        metadata = {
            "meta_learner_type": self.meta_learner_type,
            "embedding_dim": self.embedding_dim,
        }
        with open(os.path.join(path, "metadata.json"), "w") as f:
            json.dump(metadata, f)

        self.logger.info(f"Saved uplift model to {path}")

    @classmethod
    def load(cls, path: str, base_model: "BaseModel") -> "UpliftModel":
        """
        Load model from disk.

        Args:
            path: Path to load the model from
            base_model: Base recommendation model

        Returns:
            Loaded UpliftModel instance
        """
        import json
        import os

        # Load metadata
        with open(os.path.join(path, "metadata.json"), "r") as f:
            metadata = json.load(f)

        # Create instance
        model = cls(
            base_model=base_model,
            embedding_dim=metadata["embedding_dim"],
            meta_learner_type=metadata["meta_learner_type"],
        )

        # Load model weights
        weights = mx.load(os.path.join(path, "uplift_model.npz"))
        model.model.update(weights)

        return model


class PropensityModel:
    """
    Model for estimating propensity scores in causal inference.

    This model estimates the probability of treatment assignment
    given user and item features.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        hidden_dims: List[int] = [64, 32],
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the propensity model.

        Args:
            embedding_dim: Dimensionality of embeddings
            hidden_dims: Hidden layer dimensions
            logger: Logger instance
        """
        self.embedding_dim = embedding_dim
        self.logger = logger or get_logger(self.__class__.__name__)

        # Create MLX model
        self.model = self._create_model(hidden_dims)

    def _create_model(self, hidden_dims: List[int]) -> nn.Module:
        """
        Create the MLX model for propensity estimation.

        Args:
            hidden_dims: Hidden layer dimensions

        Returns:
            MLX module for propensity estimation
        """

        class PropensityEstimator(nn.Module):
            """MLX model for propensity score estimation."""

            def __init__(self, embedding_dim: int, hidden_dims: List[int]):
                super().__init__()

                # Input dimension is 2 * embedding_dim (user and item embeddings)
                input_dim = embedding_dim * 2

                # Create MLP layers
                layers = []
                prev_dim = input_dim

                for hidden_dim in hidden_dims:
                    layers.append(nn.Linear(prev_dim, hidden_dim))
                    layers.append(nn.ReLU())
                    prev_dim = hidden_dim

                # Final output layer for propensity score
                layers.append(nn.Linear(prev_dim, 1))
                layers.append(nn.Sigmoid())

                self.model = nn.Sequential(layers)

        return PropensityEstimator(embedding_dim=self.embedding_dim, hidden_dims=hidden_dims)
