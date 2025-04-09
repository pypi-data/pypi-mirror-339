"""
Federated learning server for the recommendation system.

This module provides a server implementation for federated learning,
aggregating model updates from clients while preserving privacy.
"""

import logging
import os
import threading
import time
from typing import Any, Dict, List, Optional, Union

import numpy as np
from llama_recommender.utils.logging import get_logger


class FederatedServer:
    """
    Federated learning server for aggregating model updates.

    This class provides methods for securely aggregating model updates
    from federated clients while preserving privacy.
    """

    def __init__(
        self,
        model: "BaseModel",
        aggregation_method: str = "fedavg",
        min_clients: int = 3,
        update_threshold: float = 0.01,
        max_staleness: int = 5,
        model_save_path: Optional[str] = None,
        update_interval: int = 3600,  # 1 hour
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the federated server.

        Args:
            model: Global recommendation model
            aggregation_method: Method for aggregating updates ('fedavg', 'fedmedian', 'fedprox')
            min_clients: Minimum number of clients required for aggregation
            update_threshold: Threshold for model updates
            max_staleness: Maximum allowed staleness of client updates in aggregation rounds
            model_save_path: Path to save the global model
            update_interval: Interval between global model updates (in seconds)
            logger: Logger instance
        """
        self.model = model
        self.aggregation_method = aggregation_method
        self.min_clients = min_clients
        self.update_threshold = update_threshold
        self.max_staleness = max_staleness
        self.model_save_path = model_save_path
        self.update_interval = update_interval
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize update buffer
        self.update_buffer = []

        # Initialize client registry
        self.clients = {}

        # Initialize model version
        self.model_version = 1

        # Initialize stats
        self.stats = {
            "aggregation_rounds": 0,
            "total_updates_received": 0,
            "total_updates_applied": 0,
            "client_count": 0,
            "last_update_time": 0,
            "privacy_metrics": {"average_epsilon": 0, "average_clip_norm": 0},
        }

        # Start update thread if interval is positive
        if update_interval > 0:
            self.update_thread = threading.Thread(target=self._periodic_update_thread)
            self.update_thread.daemon = True
            self.update_thread.start()
        else:
            self.update_thread = None

        self.logger.info(
            f"Initialized federated server with {aggregation_method} aggregation, "
            f"min_clients={min_clients}, update_interval={update_interval}s"
        )

    def register_client(
        self, client_id: str, client_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a new client with the server.

        Args:
            client_id: Client identifier
            client_info: Client information

        Returns:
            Dictionary with registration result
        """
        # Create client record
        client_record = {
            "client_id": client_id,
            "registration_time": time.time(),
            "last_update_time": 0,
            "update_count": 0,
            "info": client_info or {},
        }

        # Add to client registry
        self.clients[client_id] = client_record

        # Update stats
        self.stats["client_count"] = len(self.clients)

        self.logger.info(f"Registered client {client_id}")

        # Return registration result
        return {
            "success": True,
            "client_id": client_id,
            "server_time": time.time(),
            "model_version": self.model_version,
        }

    def process_update(self, update_package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an update from a client.

        Args:
            update_package: Update package from client

        Returns:
            Dictionary with processing result
        """
        try:
            # Extract client ID
            client_id = update_package.get("client_id")
            if not client_id:
                return {"error": "Missing client ID"}

            # Check if client is registered
            if client_id not in self.clients:
                # Auto-register client
                self.register_client(client_id)

            # Update client record
            client_record = self.clients[client_id]
            client_record["last_update_time"] = time.time()
            client_record["update_count"] += 1

            # Add update to buffer
            self.update_buffer.append(
                {
                    "client_id": client_id,
                    "timestamp": time.time(),
                    "update": update_package.get("update", {}),
                    "privacy": update_package.get("privacy", {}),
                    "metadata": update_package.get("metadata", {}),
                }
            )

            # Update stats
            self.stats["total_updates_received"] += 1

            self.logger.info(f"Received update from client {client_id}")

            # Check if we should apply updates
            should_update = len(self.update_buffer) >= self.min_clients or (
                time.time() - self.stats["last_update_time"] > self.update_interval
                and len(self.update_buffer) > 0
            )

            if should_update:
                # Apply updates in a separate thread to avoid blocking
                threading.Thread(target=self._apply_updates).start()

            # Return processing result
            return {
                "success": True,
                "message": "Update received",
                "server_time": time.time(),
                "model_version": self.model_version,
                "updates_pending": len(self.update_buffer),
            }

        except Exception as e:
            self.logger.error(f"Error processing update: {e}")
            return {"error": str(e)}

    def _apply_updates(self) -> None:
        """Apply pending updates to the global model."""
        with threading.Lock():
            if not self.update_buffer:
                return

            self.logger.info(f"Applying {len(self.update_buffer)} updates to global model")

            try:
                # Deserialize updates
                updates = []
                weights = []

                for update_record in self.update_buffer:
                    # Deserialize update
                    update = self._deserialize_update(update_record["update"])
                    if update:
                        updates.append(update)

                        # Calculate weight based on client importance (equal for now)
                        weights.append(1.0)

                # Check if we have enough updates
                if len(updates) < self.min_clients:
                    self.logger.warning(
                        f"Not enough updates to apply: {len(updates)} < {self.min_clients}"
                    )
                    return

                # Aggregate updates
                aggregated_update = self._aggregate_updates(updates, weights)

                # Apply aggregated update to global model
                self._update_global_model(aggregated_update)

                # Update model version
                self.model_version += 1

                # Update stats
                self.stats["aggregation_rounds"] += 1
                self.stats["total_updates_applied"] += len(updates)
                self.stats["last_update_time"] = time.time()

                # Calculate privacy metrics
                epsilons = [record["privacy"].get("epsilon", 0) for record in self.update_buffer]
                clip_norms = [
                    record["privacy"].get("clip_norm", 0) for record in self.update_buffer
                ]

                self.stats["privacy_metrics"]["average_epsilon"] = (
                    sum(epsilons) / len(epsilons) if epsilons else 0
                )
                self.stats["privacy_metrics"]["average_clip_norm"] = (
                    sum(clip_norms) / len(clip_norms) if clip_norms else 0
                )

                # Save global model if path is provided
                if self.model_save_path:
                    self.save_global_model()

                self.logger.info(
                    f"Applied {len(updates)} updates to global model, "
                    f"new version: {self.model_version}"
                )

                # Clear update buffer
                self.update_buffer = []

            except Exception as e:
                self.logger.error(f"Error applying updates: {e}")

    def _deserialize_update(
        self, serialized_update: Dict[str, Any]
    ) -> Optional[Dict[str, np.ndarray]]:
        """
        Deserialize an update from a client.

        Args:
            serialized_update: Serialized update

        Returns:
            Deserialized update or None if invalid
        """
        try:
            deserialized = {}

            # Process each parameter
            for key, value in serialized_update.items():
                # Skip shape keys
                if key.endswith("_shape"):
                    continue

                # Get shape for this parameter
                shape_key = f"{key}_shape"
                if shape_key in serialized_update:
                    shape = tuple(serialized_update[shape_key])

                    # Reshape the flattened parameter
                    param = np.array(value)
                    param = param.reshape(shape)

                    deserialized[key] = param
                else:
                    # No shape information, keep as is
                    deserialized[key] = np.array(value)

            return deserialized

        except Exception as e:
            self.logger.error(f"Error deserializing update: {e}")
            return None

    def _aggregate_updates(
        self, updates: List[Dict[str, np.ndarray]], weights: List[float]
    ) -> Dict[str, np.ndarray]:
        """
        Aggregate updates from multiple clients.

        Args:
            updates: List of client updates
            weights: List of weights for each update

        Returns:
            Aggregated update
        """
        if not updates:
            return {}

        # Normalize weights
        total_weight = sum(weights)
        if total_weight <= 0:
            # Equal weights if total is zero
            weights = [1.0 / len(updates)] * len(updates)
        else:
            weights = [w / total_weight for w in weights]

        # Apply aggregation method
        if self.aggregation_method == "fedavg":
            return self._fedavg_aggregate(updates, weights)
        elif self.aggregation_method == "fedmedian":
            return self._fedmedian_aggregate(updates)
        elif self.aggregation_method == "fedprox":
            return self._fedprox_aggregate(updates, weights)
        else:
            self.logger.warning(f"Unknown aggregation method: {self.aggregation_method}")
            # Fall back to FedAvg
            return self._fedavg_aggregate(updates, weights)

    def _fedavg_aggregate(
        self, updates: List[Dict[str, np.ndarray]], weights: List[float]
    ) -> Dict[str, np.ndarray]:
        """
        Aggregate updates using Federated Averaging (FedAvg).

        Args:
            updates: List of client updates
            weights: List of weights for each update

        Returns:
            Aggregated update
        """
        aggregated = {}

        # Get all parameter names across updates
        all_keys = set()
        for update in updates:
            all_keys.update(update.keys())

        # Weighted average for each parameter
        for key in all_keys:
            # Collect parameter values from all updates that have this parameter
            weighted_params = []

            for i, update in enumerate(updates):
                if key in update:
                    weighted_param = update[key] * weights[i]
                    weighted_params.append(weighted_param)

            if weighted_params:
                # Sum weighted parameters
                aggregated[key] = sum(weighted_params)

        return aggregated

    def _fedmedian_aggregate(self, updates: List[Dict[str, np.ndarray]]) -> Dict[str, np.ndarray]:
        """
        Aggregate updates using coordinate-wise median.

        Args:
            updates: List of client updates

        Returns:
            Aggregated update
        """
        aggregated = {}

        # Get all parameter names across updates
        all_keys = set()
        for update in updates:
            all_keys.update(update.keys())

        # Compute median for each parameter
        for key in all_keys:
            # Collect parameter values from all updates that have this parameter
            params = []

            for update in updates:
                if key in update:
                    params.append(update[key])

            if params:
                # Stack parameters along a new axis
                stacked = np.stack(params)

                # Compute median along the first axis
                aggregated[key] = np.median(stacked, axis=0)

        return aggregated

    def _fedprox_aggregate(
        self,
        updates: List[Dict[str, np.ndarray]],
        weights: List[float],
        mu: float = 0.01,
    ) -> Dict[str, np.ndarray]:
        """
        Aggregate updates using FedProx (proximal term regularization).

        Args:
            updates: List of client updates
            weights: List of weights for each update
            mu: Proximal term coefficient

        Returns:
            Aggregated update
        """
        # For FedProx, we first compute FedAvg
        avg_update = self._fedavg_aggregate(updates, weights)

        # Then apply proximal term regularization
        # In this simplified implementation, we just scale down the update
        # to simulate the effect of proximal term regularization
        regularized = {}

        for key, value in avg_update.items():
            regularized[key] = value * (1.0 / (1.0 + mu))

        return regularized

    def _update_global_model(self, aggregated_update: Dict[str, np.ndarray]) -> None:
        """
        Update the global model with the aggregated update.

        Args:
            aggregated_update: Aggregated parameter update
        """
        # This is a placeholder implementation
        # In a real system, this would update the actual model parameters

        # For MLX models
        if hasattr(self.model, "model") and hasattr(self.model.model, "parameters"):
            import mlx.core as mx

            # Get current parameters
            current_params = self.model.model.parameters()

            # Apply updates
            new_params = {}
            for key, param in current_params.items():
                if key in aggregated_update:
                    # Convert numpy array to MLX array
                    update = mx.array(aggregated_update[key])

                    # Apply update
                    new_params[key] = param + update
                else:
                    # Keep unchanged
                    new_params[key] = param

            # Update model parameters
            self.model.model.update(new_params)

            self.logger.info("Updated MLX model parameters")

        # For embedding-based models
        elif hasattr(self.model, "user_embeddings") and hasattr(self.model, "item_embeddings"):
            if "user_embeddings" in aggregated_update:
                # Update user embeddings
                user_update = aggregated_update["user_embeddings"]

                # Get user IDs in the same order as embeddings
                user_ids = list(self.model.user_embeddings.keys())

                # Apply updates
                for i, user_id in enumerate(user_ids):
                    if i < user_update.shape[0]:
                        self.model.user_embeddings[user_id] += user_update[i]

            if "item_embeddings" in aggregated_update:
                # Update item embeddings
                item_update = aggregated_update["item_embeddings"]

                # Get item IDs in the same order as embeddings
                item_ids = list(self.model.item_embeddings.keys())

                # Apply updates
                for i, item_id in enumerate(item_ids):
                    if i < item_update.shape[0]:
                        self.model.item_embeddings[item_id] += item_update[i]

            self.logger.info("Updated embedding model parameters")

        else:
            self.logger.warning("Could not update model parameters")

    def save_global_model(self) -> Optional[str]:
        """
        Save the global model to disk.

        Returns:
            Path where the model was saved or None if failed
        """
        if not self.model_save_path:
            self.logger.warning("No model save path specified")
            return None

        try:
            # Create directories if needed
            os.makedirs(os.path.dirname(self.model_save_path), exist_ok=True)

            # Save the model
            if hasattr(self.model, "save"):
                # Use model's save method
                save_path = f"{self.model_save_path}/model_v{self.model_version}"
                self.model.save(save_path)

                # Also save a 'latest' version
                latest_path = f"{self.model_save_path}/model_latest"
                self.model.save(latest_path)

                self.logger.info(f"Saved global model to {save_path} and {latest_path}")
                return save_path
            else:
                self.logger.warning("Model does not have a save method")
                return None

        except Exception as e:
            self.logger.error(f"Error saving global model: {e}")
            return None

    def load_global_model(self, version: Optional[Union[int, str]] = None) -> bool:
        """
        Load the global model from disk.

        Args:
            version: Model version to load (if None, loads the latest)

        Returns:
            True if successful, False otherwise
        """
        if not self.model_save_path:
            self.logger.warning("No model save path specified")
            return False

        try:
            # Determine model path
            if version is None or version == "latest":
                model_path = f"{self.model_save_path}/model_latest"
            else:
                model_path = f"{self.model_save_path}/model_v{version}"

            # Check if model exists
            if not os.path.exists(model_path):
                self.logger.warning(f"Model not found at {model_path}")
                return False

            # Load the model
            if hasattr(self.model, "_load_model_data"):
                # Use model's load method
                self.model._load_model_data(model_path)

                # Update model version
                if version != "latest" and isinstance(version, int):
                    self.model_version = version

                self.logger.info(f"Loaded global model from {model_path}")
                return True
            else:
                self.logger.warning("Model does not have a load method")
                return False

        except Exception as e:
            self.logger.error(f"Error loading global model: {e}")
            return False

    def get_server_status(self) -> Dict[str, Any]:
        """
        Get the current status of the federated server.

        Returns:
            Dictionary with server status
        """
        # Count active clients (those that have updated in the last day)
        active_threshold = time.time() - 86400  # 24 hours
        active_clients = sum(
            1 for client in self.clients.values() if client["last_update_time"] > active_threshold
        )

        # Get status
        status = {
            "server_time": time.time(),
            "model_version": self.model_version,
            "clients": {"total": len(self.clients), "active": active_clients},
            "updates": {
                "pending": len(self.update_buffer),
                "total_received": self.stats["total_updates_received"],
                "total_applied": self.stats["total_updates_applied"],
            },
            "aggregation": {
                "method": self.aggregation_method,
                "rounds": self.stats["aggregation_rounds"],
                "min_clients": self.min_clients,
                "last_update_time": self.stats["last_update_time"],
            },
            "privacy": self.stats["privacy_metrics"],
        }

        return status

    def _periodic_update_thread(self) -> None:
        """Thread for periodic model updates."""
        while True:
            try:
                # Sleep for the update interval
                time.sleep(self.update_interval)

                # Check if we have any updates to apply
                if self.update_buffer:
                    self._apply_updates()

            except Exception as e:
                self.logger.error(f"Error in periodic update thread: {e}")

    def start_web_server(
        self, host: str = "0.0.0.0", port: int = 8000, api_key: Optional[str] = None
    ) -> None:
        """
        Start a web server for the federated server.

        Args:
            host: Host to bind to
            port: Port to listen on
            api_key: API key for authentication (if None, generates a random key)
        """
        try:
            import uvicorn
            from fastapi import Depends, FastAPI, Header, HTTPException
            from pydantic import BaseModel

            # Create FastAPI app
            app = FastAPI(title="Federated Learning Server", version="1.0.0")

            # Generate API key if not provided
            if api_key is None:
                import secrets

                api_key = secrets.token_hex(16)
                self.logger.info(f"Generated API key: {api_key}")

            # API key verification
            async def verify_api_key(x_api_key: str = Header(None)):
                if x_api_key != api_key:
                    raise HTTPException(status_code=401, detail="Invalid API key")
                return x_api_key

            # Define request models
            class ClientRegistration(BaseModel):
                client_id: str
                client_info: Optional[Dict[str, Any]] = None

            # Define routes
            @app.get("/api/status")
            async def get_status():
                return self.get_server_status()

            @app.post("/api/register")
            async def register_client(
                registration: ClientRegistration, api_key: str = Depends(verify_api_key)
            ):
                return self.register_client(
                    client_id=registration.client_id,
                    client_info=registration.client_info,
                )

            @app.post("/api/update")
            async def process_update(
                update_package: Dict[str, Any], api_key: str = Depends(verify_api_key)
            ):
                return self.process_update(update_package)

            @app.get("/api/model")
            async def get_model(
                version: Optional[Union[int, str]] = None,
                api_key: str = Depends(verify_api_key),
            ):
                # TODO: Implement model download
                raise HTTPException(status_code=501, detail="Not implemented")

            # Start server
            self.logger.info(f"Starting web server on {host}:{port}")
            uvicorn.run(app, host=host, port=port)

        except ImportError:
            self.logger.error(
                "Required packages not installed. " "Install with: pip install fastapi uvicorn"
            )

        except Exception as e:
            self.logger.error(f"Error starting web server: {e}")

    def set_aggregation_method(self, method: str) -> None:
        """
        Set the aggregation method.

        Args:
            method: Aggregation method ('fedavg', 'fedmedian', or 'fedprox')
        """
        valid_methods = ["fedavg", "fedmedian", "fedprox"]
        if method not in valid_methods:
            self.logger.warning(
                f"Invalid aggregation method: {method}. "
                f"Valid options are: {', '.join(valid_methods)}"
            )
            return

        self.aggregation_method = method
        self.logger.info(f"Set aggregation method to {method}")

    def set_min_clients(self, min_clients: int) -> None:
        """
        Set the minimum number of clients required for aggregation.

        Args:
            min_clients: Minimum number of clients
        """
        if min_clients < 1:
            self.logger.warning("Minimum number of clients must be at least 1")
            return

        self.min_clients = min_clients
        self.logger.info(f"Set minimum number of clients to {min_clients}")

    def set_update_interval(self, update_interval: int) -> None:
        """
        Set the update interval.

        Args:
            update_interval: Interval between global model updates (in seconds)
        """
        if update_interval < 0:
            self.logger.warning("Update interval must be non-negative")
            return

        self.update_interval = update_interval
        self.logger.info(f"Set update interval to {update_interval}s")

        # Restart update thread if needed
        if self.update_thread is not None:
            # Stop existing thread
            self.update_thread = None

        if update_interval > 0:
            # Start new thread
            self.update_thread = threading.Thread(target=self._periodic_update_thread)
            self.update_thread.daemon = True
            self.update_thread.start()

    def get_client_info(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a client.

        Args:
            client_id: Client identifier

        Returns:
            Dictionary with client information or None if not found
        """
        return self.clients.get(client_id)

    def remove_client(self, client_id: str) -> bool:
        """
        Remove a client from the registry.

        Args:
            client_id: Client identifier

        Returns:
            True if client was removed, False otherwise
        """
        if client_id in self.clients:
            del self.clients[client_id]

            # Update stats
            self.stats["client_count"] = len(self.clients)

            self.logger.info(f"Removed client {client_id}")
            return True

        return False
