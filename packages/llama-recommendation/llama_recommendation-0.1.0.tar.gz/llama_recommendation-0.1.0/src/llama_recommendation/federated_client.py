"""
Federated learning client for the recommendation system.

This module provides a client implementation for federated learning,
allowing privacy-preserving model updates based on local user data.
"""

import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Union

import numpy as np
from llama_recommender.core.privacy import GaussianNoiseGenerator
from llama_recommender.utils.logging import get_logger


class FederatedClient:
    """
    Federated learning client for privacy-preserving updates.

    This class provides methods for updating a local model based on local
    data and securely submitting model updates to a federated server.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        server_url: Optional[str] = None,
        model: Optional["BaseModel"] = None,
        privacy_budget: float = 10.0,
        dp_epsilon: float = 1.0,
        dp_delta: float = 1e-5,
        local_update_rounds: int = 3,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the federated client.

        Args:
            client_id: Client identifier (if None, generates a random UUID)
            server_url: URL of the federated server
            model: Local recommendation model
            privacy_budget: Total privacy budget (epsilon)
            dp_epsilon: Epsilon parameter for differential privacy
            dp_delta: Delta parameter for differential privacy
            local_update_rounds: Number of local update rounds per global round
            logger: Logger instance
        """
        self.client_id = client_id or str(uuid.uuid4())
        self.server_url = server_url or os.getenv("LLAMA_FEDERATED_SERVER")
        self.model = model
        self.privacy_budget = privacy_budget
        self.dp_epsilon = dp_epsilon
        self.dp_delta = dp_delta
        self.local_update_rounds = local_update_rounds
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize update history
        self.update_history = []

        # Initialize noise generator
        self.noise_generator = GaussianNoiseGenerator(epsilon=dp_epsilon, delta=dp_delta)

    def update_local_model(
        self,
        local_data: Union[str, "pd.DataFrame"],
        epochs: int = 3,
        batch_size: int = 32,
        learning_rate: float = 0.001,
    ) -> Dict[str, Any]:
        """
        Update the local model using local data.

        Args:
            local_data: Path to local data file or DataFrame
            epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate for optimization

        Returns:
            Dictionary with training metrics
        """
        if self.model is None:
            self.logger.error("No local model available")
            return {"error": "No local model available"}

        try:
            # Train the local model
            from llama_recommender.core.privacy import DPTrainer

            # Compute epsilon for this update
            update_epsilon = min(self.dp_epsilon, self.privacy_budget)

            # Create DP trainer
            trainer = DPTrainer(model=self.model, epsilon=update_epsilon, delta=self.dp_delta)

            # Check if local_data is a DataFrame or path
            if isinstance(local_data, str):
                data_path = local_data
            else:
                # Save DataFrame to temporary file
                import tempfile

                import pandas as pd

                with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
                    data_path = tmp.name
                    if isinstance(local_data, pd.DataFrame):
                        local_data.to_csv(data_path, index=False)
                    else:
                        raise ValueError("local_data must be a path or DataFrame")

            # Train the model
            metrics = trainer.train(
                train_data=data_path,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
            )

            # Update privacy budget
            self.privacy_budget -= update_epsilon

            # Add update to history
            update_record = {
                "timestamp": time.time(),
                "epsilon_spent": update_epsilon,
                "remaining_budget": self.privacy_budget,
                "metrics": metrics,
            }
            self.update_history.append(update_record)

            # Clean up temporary file if needed
            if isinstance(local_data, str) is False and os.path.exists(data_path):
                os.unlink(data_path)

            self.logger.info(
                f"Updated local model with {epochs} epochs, "
                f"privacy: ε={update_epsilon}, remaining budget: {self.privacy_budget}"
            )

            return {
                "success": True,
                "metrics": metrics,
                "privacy": {
                    "epsilon_spent": update_epsilon,
                    "remaining_budget": self.privacy_budget,
                },
            }

        except Exception as e:
            self.logger.error(f"Error updating local model: {e}")
            return {"error": str(e)}

    def get_model_update(
        self,
        clip_norm: float = 1.0,
        add_noise: bool = True,
        target_epsilon: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Get the model update for federated aggregation.

        Args:
            clip_norm: Gradient clipping norm
            add_noise: Whether to add noise for differential privacy
            target_epsilon: Target epsilon for this update (if None, uses dp_epsilon)

        Returns:
            Dictionary with model update
        """
        if self.model is None:
            self.logger.error("No local model available")
            return {"error": "No local model available"}

        try:
            # Extract model parameters
            params = self._extract_model_parameters()

            # Compute update (difference from initial weights)
            if hasattr(self.model, "initial_params"):
                initial_params = self.model.initial_params
                update = {}

                for key, value in params.items():
                    if key in initial_params:
                        update[key] = value - initial_params[key]
                    else:
                        update[key] = value
            else:
                # If no initial weights, use current weights as update
                update = params
                self.logger.warning(
                    "No initial parameters available, using current parameters as update"
                )

            # Clip update by norm if requested
            if clip_norm > 0:
                update = self._clip_update(update, clip_norm)

            # Add noise for differential privacy if requested
            if add_noise:
                epsilon = target_epsilon or self.dp_epsilon

                # Check if we have enough privacy budget
                if epsilon > self.privacy_budget:
                    self.logger.warning(
                        f"Insufficient privacy budget: requested ε={epsilon}, "
                        f"remaining: {self.privacy_budget}. Using remaining budget."
                    )
                    epsilon = self.privacy_budget

                # Add noise to update
                update = self._add_noise_to_update(update, epsilon)

                # Update privacy budget
                self.privacy_budget -= epsilon

                self.logger.info(
                    f"Added noise with ε={epsilon}, remaining budget: {self.privacy_budget}"
                )

            # Create update package
            update_package = {
                "client_id": self.client_id,
                "timestamp": time.time(),
                "update": self._serialize_update(update),
                "privacy": {
                    "epsilon": epsilon if add_noise else 0,
                    "delta": self.dp_delta if add_noise else 0,
                    "clip_norm": clip_norm if clip_norm > 0 else 0,
                },
                "metadata": {
                    "model_type": self.model.__class__.__name__,
                    "embedding_dim": self.model.embedding_dim,
                },
            }

            return update_package

        except Exception as e:
            self.logger.error(f"Error creating model update: {e}")
            return {"error": str(e)}

    def _extract_model_parameters(self) -> Dict[str, np.ndarray]:
        """
        Extract parameters from the model.

        Returns:
            Dictionary of parameter name to value
        """
        # This is a placeholder implementation
        # In a real system, this would extract actual model parameters

        # For MLX models
        if hasattr(self.model, "model") and hasattr(self.model.model, "parameters"):

            # Extract parameters from MLX model
            mlx_params = self.model.model.parameters()

            # Convert MLX arrays to NumPy arrays
            params = {}
            for key, value in mlx_params.items():
                params[key] = np.array(value)

            return params

        # Fallback to model embeddings as parameters
        elif hasattr(self.model, "user_embeddings") and hasattr(self.model, "item_embeddings"):
            # Flatten embeddings into a single parameter vector
            user_embeddings = np.stack(list(self.model.user_embeddings.values()))
            item_embeddings = np.stack(list(self.model.item_embeddings.values()))

            return {
                "user_embeddings": user_embeddings,
                "item_embeddings": item_embeddings,
            }

        else:
            self.logger.warning("Could not extract model parameters, returning empty dict")
            return {}

    def _clip_update(
        self, update: Dict[str, np.ndarray], clip_norm: float
    ) -> Dict[str, np.ndarray]:
        """
        Clip update by L2 norm.

        Args:
            update: Dictionary of parameter updates
            clip_norm: Maximum L2 norm

        Returns:
            Clipped update
        """
        # Calculate total L2 norm
        squared_sum = 0
        for param in update.values():
            squared_sum += np.sum(param**2)

        total_norm = np.sqrt(squared_sum)

        # Apply clipping if norm exceeds threshold
        if total_norm > clip_norm:
            clipping_factor = clip_norm / total_norm

            clipped_update = {}
            for name, param in update.items():
                clipped_update[name] = param * clipping_factor

            self.logger.info(f"Clipped update norm from {total_norm:.4f} to {clip_norm:.4f}")

            return clipped_update

        return update

    def _add_noise_to_update(
        self, update: Dict[str, np.ndarray], epsilon: float
    ) -> Dict[str, np.ndarray]:
        """
        Add calibrated noise to update for differential privacy.

        Args:
            update: Dictionary of parameter updates
            epsilon: Epsilon parameter for this update

        Returns:
            Noisy update
        """
        # Create noise generator with specified epsilon
        noise_generator = GaussianNoiseGenerator(epsilon=epsilon, delta=self.dp_delta)

        # Add noise to each parameter
        noisy_update = {}
        for name, param in update.items():
            noisy_param = noise_generator.add_noise(param)
            noisy_update[name] = noisy_param

        return noisy_update

    def _serialize_update(self, update: Dict[str, np.ndarray]) -> Dict[str, List[float]]:
        """
        Serialize update for transmission.

        Args:
            update: Dictionary of parameter updates

        Returns:
            Serialized update
        """
        serialized = {}

        for name, param in update.items():
            # Save shape information
            shape_key = f"{name}_shape"
            serialized[shape_key] = list(param.shape)

            # Flatten and convert to list
            serialized[name] = param.flatten().tolist()

        return serialized

    def send_model_update(
        self,
        clip_norm: float = 1.0,
        add_noise: bool = True,
        target_epsilon: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Send model update to the federated server.

        Args:
            clip_norm: Gradient clipping norm
            add_noise: Whether to add noise for differential privacy
            target_epsilon: Target epsilon for this update

        Returns:
            Server response or error message
        """
        if self.server_url is None:
            self.logger.error("No server URL configured")
            return {"error": "No server URL configured"}

        try:
            # Get model update
            update = self.get_model_update(
                clip_norm=clip_norm, add_noise=add_noise, target_epsilon=target_epsilon
            )

            if "error" in update:
                return update

            # Send update to server
            import requests

            response = requests.post(
                f"{self.server_url}/api/update",
                json=update,
                headers={
                    "Content-Type": "application/json",
                    "Client-ID": self.client_id,
                },
            )

            if response.status_code == 200:
                result = response.json()
                self.logger.info("Successfully sent model update to server")
                return result
            else:
                error_msg = f"Error sending update: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            self.logger.error(f"Error sending model update: {e}")
            return {"error": str(e)}

    def pull_global_model(self) -> Dict[str, Any]:
        """
        Pull the latest global model from the federated server.

        Returns:
            Dictionary with result of the operation
        """
        if self.server_url is None:
            self.logger.error("No server URL configured")
            return {"error": "No server URL configured"}

        try:
            # Send request to server
            import requests

            response = requests.get(
                f"{self.server_url}/api/model", headers={"Client-ID": self.client_id}
            )

            if response.status_code == 200:
                # Save model to temporary file
                import tempfile

                with tempfile.NamedTemporaryFile(suffix=".npz", delete=False) as tmp:
                    tmp.write(response.content)
                    model_path = tmp.name

                # Load model
                if self.model is not None:

                    # Update current model
                    self.model._load_model_data(model_path)

                    # Save current parameters as initial parameters
                    self.model.initial_params = self._extract_model_parameters()

                    # Clean up temporary file
                    os.unlink(model_path)

                    self.logger.info("Successfully pulled global model from server")

                    return {"success": True, "message": "Model updated successfully"}
                else:
                    return {
                        "success": True,
                        "message": "Model downloaded but no local model to update",
                        "model_path": model_path,
                    }
            else:
                error_msg = f"Error pulling model: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            self.logger.error(f"Error pulling global model: {e}")
            return {"error": str(e)}

    def check_server_status(self) -> Dict[str, Any]:
        """
        Check the status of the federated server.

        Returns:
            Server status information
        """
        if self.server_url is None:
            self.logger.error("No server URL configured")
            return {"error": "No server URL configured"}

        try:
            # Send request to server
            import requests

            response = requests.get(
                f"{self.server_url}/api/status", headers={"Client-ID": self.client_id}
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_msg = (
                    f"Error checking server status: {response.status_code} - {response.text}"
                )
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            self.logger.error(f"Error checking server status: {e}")
            return {"error": str(e)}

    def get_privacy_report(self) -> Dict[str, Any]:
        """
        Get a report on privacy budget usage.

        Returns:
            Dictionary with privacy report
        """
        total_epsilon_spent = 0
        for update in self.update_history:
            total_epsilon_spent += update.get("epsilon_spent", 0)

        report = {
            "client_id": self.client_id,
            "initial_budget": self.dp_epsilon * 10,  # Assuming initial budget was 10 times epsilon
            "remaining_budget": self.privacy_budget,
            "total_spent": total_epsilon_spent,
            "update_count": len(self.update_history),
            "update_history": self.update_history,
        }

        return report
