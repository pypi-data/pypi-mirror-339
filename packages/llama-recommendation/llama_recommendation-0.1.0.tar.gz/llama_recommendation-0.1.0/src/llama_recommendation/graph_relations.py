"""
Utilities for building and processing relationship graphs.

This module provides functions for constructing and manipulating graphs
representing relationships between users and items in the recommendation system.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import scipy.sparse as sp
from llama_recommender.utils.logging import get_logger


def build_adjacency_matrix(
    interactions: List[Tuple[str, str, float]],
    user_ids: List[str],
    item_ids: List[str],
    normalize: bool = True,
    self_loops: bool = True,
    logger: Optional[logging.Logger] = None,
) -> np.ndarray:
    """
    Build an adjacency matrix for a user-item interaction graph.

    Args:
        interactions: List of (user_id, item_id, weight) tuples
        user_ids: List of all user IDs
        item_ids: List of all item IDs
        normalize: Whether to normalize the adjacency matrix
        self_loops: Whether to add self-loops to the graph
        logger: Logger instance

    Returns:
        Adjacency matrix as a NumPy array
    """
    logger = logger or get_logger("graph_relations")

    # Create mappings for user and item IDs
    user_map = {user_id: i for i, user_id in enumerate(user_ids)}
    item_map = {item_id: i + len(user_ids) for i, item_id in enumerate(item_ids)}

    # Total number of nodes
    num_nodes = len(user_ids) + len(item_ids)

    # Create sparse adjacency matrix
    row = []
    col = []
    data = []

    # Add edges for interactions
    for user_id, item_id, weight in interactions:
        if user_id not in user_map or item_id not in item_map:
            continue

        user_idx = user_map[user_id]
        item_idx = item_map[item_id]

        # Add user -> item edge
        row.append(user_idx)
        col.append(item_idx)
        data.append(weight)

        # Add item -> user edge (symmetric)
        row.append(item_idx)
        col.append(user_idx)
        data.append(weight)

    # Create sparse matrix
    adj = sp.coo_matrix((data, (row, col)), shape=(num_nodes, num_nodes))

    # Add self-loops
    if self_loops:
        adj = adj + sp.eye(num_nodes)

    # Convert to CSR format for efficient operations
    adj = adj.tocsr()

    # Normalize adjacency matrix (symmetric normalization)
    if normalize:
        adj = normalize_adjacency(adj)

    logger.info(f"Built adjacency matrix of shape {adj.shape} with {len(data)} edges")

    # Convert to dense matrix for MLX compatibility
    return adj.toarray()


def normalize_adjacency(adj: sp.spmatrix) -> sp.spmatrix:
    """
    Normalize adjacency matrix with symmetric normalization.

    A_norm = D^(-1/2) * A * D^(-1/2)

    Args:
        adj: Adjacency matrix as a sparse matrix

    Returns:
        Normalized adjacency matrix
    """
    # Calculate node degrees
    degrees = np.array(adj.sum(1)).flatten()

    # Calculate D^(-1/2)
    d_inv_sqrt = np.power(degrees, -0.5)
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0  # Handle zero degrees
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)

    # Calculate normalized adjacency: D^(-1/2) * A * D^(-1/2)
    return d_mat_inv_sqrt.dot(adj).dot(d_mat_inv_sqrt)
