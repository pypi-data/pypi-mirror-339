"""
Secure aggregation for federated learning.

This module provides methods for securely aggregating model updates
from multiple clients while preserving their privacy.
"""

import logging
from typing import Dict, List, Optional

import numpy as np
from llama_recommender.utils.logging import get_logger


class SecureAggregator:
    """
    Securely aggregate model updates from multiple clients.

    This class implements secure aggregation protocols to combine model updates
    from multiple clients while preserving their privacy.
    """

    def __init__(
        self,
        secure_protocol: str = "pairwise",
        noise_scale: float = 0.1,
        dropout_rate: float = 0.0,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the secure aggregator.

        Args:
            secure_protocol: Secure aggregation protocol ('pairwise', 'threshold', 'smc')
            noise_scale: Scale of noise for secure protocols
            dropout_rate: Rate of client dropout to tolerate
            logger: Logger instance
        """
        self.secure_protocol = secure_protocol
        self.noise_scale = noise_scale
        self.dropout_rate = dropout_rate
        self.logger = logger or get_logger(self.__class__.__name__)

        # Validate protocol
        valid_protocols = ["pairwise", "threshold", "smc", "none"]
        if secure_protocol not in valid_protocols:
            self.logger.warning(
                f"Invalid secure protocol: {secure_protocol}. "
                f"Valid options are: {', '.join(valid_protocols)}. "
                f"Using 'none' instead."
            )
            self.secure_protocol = "none"

    def aggregate(
        self,
        client_updates: List[Dict[str, np.ndarray]],
        weights: Optional[List[float]] = None,
    ) -> Dict[str, np.ndarray]:
        """
        Securely aggregate client updates.

        Args:
            client_updates: List of client updates
            weights: List of weights for each client update

        Returns:
            Aggregated update
        """
        if not client_updates:
            return {}

        # Set equal weights if not provided
        if weights is None:
            weights = [1.0 / len(client_updates)] * len(client_updates)
        elif len(weights) != len(client_updates):
            self.logger.warning(
                f"Mismatch between number of updates ({len(client_updates)}) "
                f"and weights ({len(weights)}). Using equal weights."
            )
            weights = [1.0 / len(client_updates)] * len(client_updates)

        # Normalize weights
        total_weight = sum(weights)
        if total_weight <= 0:
            self.logger.warning("Total weight is non-positive. Using equal weights.")
            weights = [1.0 / len(client_updates)] * len(client_updates)
        else:
            weights = [w / total_weight for w in weights]

        # Apply secure aggregation protocol
        if self.secure_protocol == "pairwise":
            return self._pairwise_secure_aggregation(client_updates, weights)
