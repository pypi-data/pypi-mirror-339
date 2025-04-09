"""
Graph Convolutional Network for graph-based recommendations.

This module provides implementations of graph convolutional networks (GCNs)
for learning node representations in user-item interaction graphs.
"""

import logging
from typing import List, Optional

import mlx.core as mx
import mlx.nn as nn
import numpy as np
from llama_recommender.utils.logging import get_logger


class GraphConvLayer(nn.Module):
    """
    Graph Convolutional Layer implementation.

    This layer performs message passing between nodes in a graph
    through a graph convolution operation.
    """

    def __init__(
        self,
        in_features: int,
        out_features: int,
        activation: str = "relu",
        dropout: float = 0.0,
    ):
        """
        Initialize the graph convolutional layer.

        Args:
            in_features: Input feature dimensionality
            out_features: Output feature dimensionality
            activation: Activation function ('relu', 'tanh', or 'none')
            dropout: Dropout probability
        """
        super().__init__()

        # Weight matrix for transformation
        self.weight = nn.Linear(in_features, out_features, bias=False)

        # Bias term
        self.bias = mx.zeros((1, out_features))

        # Activation function
        if activation == "relu":
            self.activation = nn.ReLU()
        elif activation == "tanh":
            self.activation = nn.Tanh()
        else:
            self.activation = None

        # Dropout
        self.dropout = dropout

    def __call__(self, x: mx.array, adj: mx.array, training: bool = False) -> mx.array:
        """
        Forward pass through the graph convolutional layer.

        Args:
            x: Input node features (N x F)
            adj: Adjacency matrix (N x N)
            training: Whether the model is in training mode

        Returns:
            Updated node features (N x F')
        """
        # Feature transformation
        x = self.weight(x)

        # Apply graph convolution
        x = mx.matmul(adj, x)

        # Add bias
        x = x + self.bias

        # Apply activation function
        if self.activation is not None:
            x = self.activation(x)

        # Apply dropout during training
        if training and self.dropout > 0:
            mask = mx.random.uniform(0, 1, x.shape) > self.dropout
            x = x * mask / (1 - self.dropout)

        return x


class GCN(nn.Module):
    """
    Graph Convolutional Network for learning node representations.

    This model applies multiple graph convolutional layers to learn
    representations of nodes in a user-item interaction graph.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        num_layers: int = 2,
        hidden_dims: Optional[List[int]] = None,
        dropout: float = 0.1,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the GCN model.

        Args:
            embedding_dim: Dimensionality of embeddings
            num_layers: Number of graph convolutional layers
            hidden_dims: Dimensions of hidden layers (if None, use embedding_dim)
            dropout: Dropout probability
            logger: Logger instance
        """
        super().__init__()

        self.embedding_dim = embedding_dim
        self.num_layers = num_layers
        self.logger = logger or get_logger(self.__class__.__name__)

        # Set hidden dimensions if not provided
        if hidden_dims is None:
            hidden_dims = [embedding_dim] * num_layers

        # Ensure number of hidden dimensions matches number of layers
        if len(hidden_dims) != num_layers:
            raise ValueError(
                f"Number of hidden dimensions ({len(hidden_dims)}) "
                f"must match number of layers ({num_layers})"
            )

        # Create graph convolutional layers
        self.layers = []
        in_dim = embedding_dim

        for i in range(num_layers):
            out_dim = hidden_dims[i]
            activation = "relu" if i < num_layers - 1 else "none"

            layer = GraphConvLayer(
                in_features=in_dim,
                out_features=out_dim,
                activation=activation,
                dropout=dropout if i < num_layers - 1 else 0,
            )

            self.layers.append(layer)
            in_dim = out_dim

    def __call__(self, adj: mx.array, features: mx.array, training: bool = False) -> mx.array:
        """
        Forward pass through the GCN model.

        Args:
            adj: Adjacency matrix (N x N)
            features: Node features (N x F)
            training: Whether the model is in training mode

        Returns:
            Updated node representations (N x F')
        """
        x = features

        # Apply graph convolutional layers
        for layer in self.layers:
            x = layer(x, adj, training=training)

        return x

    def forward(
        self,
        adj_matrix: np.ndarray,
        user_embeddings: List[np.ndarray],
        item_embeddings: List[np.ndarray],
    ) -> List[np.ndarray]:
        """
        Forward pass with NumPy inputs and outputs.

        Args:
            adj_matrix: Adjacency matrix (NumPy array)
            user_embeddings: List of user embedding vectors
            item_embeddings: List of item embedding vectors

        Returns:
            List of updated embeddings for all nodes
        """
        # Convert to MLX arrays
        adj_mx = mx.array(adj_matrix)

        # Concatenate user and item embeddings
        node_embeddings = np.vstack([np.stack(user_embeddings), np.stack(item_embeddings)])
        features_mx = mx.array(node_embeddings)

        # Forward pass
        with mx.eval_mode():
            output_mx = self(adj_mx, features_mx)

        # Convert back to NumPy
        output = np.array(output_mx)

        # Split back into separate embeddings
        num_users = len(user_embeddings)
        output_embeddings = [output[i] for i in range(output.shape[0])]

        return output_embeddings


class LightGCN(nn.Module):
    """
    LightGCN implementation for efficient graph-based recommendations.

    LightGCN simplifies GCN by removing feature transformation and non-linear
    activation, focusing purely on neighborhood aggregation.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        num_layers: int = 3,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the LightGCN model.

        Args:
            embedding_dim: Dimensionality of embeddings
            num_layers: Number of graph convolutional layers
            logger: Logger instance
        """
        super().__init__()

        self.embedding_dim = embedding_dim
        self.num_layers = num_layers
        self.logger = logger or get_logger(self.__class__.__name__)

    def __call__(self, adj: mx.array, features: mx.array) -> mx.array:
        """
        Forward pass through the LightGCN model.

        Args:
            adj: Normalized adjacency matrix (N x N)
            features: Node features (N x F)

        Returns:
            Updated node representations (N x F)
        """
        # Initial embeddings
        embeddings = [features]

        # Apply graph convolutional layers
        for _ in range(self.num_layers):
            # Message passing: x = A * x
            next_emb = mx.matmul(adj, embeddings[-1])
            embeddings.append(next_emb)

        # Layer combination (average across layers)
        final_emb = mx.mean(mx.stack(embeddings), axis=0)

        return final_emb

    def forward(
        self,
        adj_matrix: np.ndarray,
        user_embeddings: List[np.ndarray],
        item_embeddings: List[np.ndarray],
    ) -> List[np.ndarray]:
        """
        Forward pass with NumPy inputs and outputs.

        Args:
            adj_matrix: Adjacency matrix (NumPy array)
            user_embeddings: List of user embedding vectors
            item_embeddings: List of item embedding vectors

        Returns:
            List of updated embeddings for all nodes
        """
        # Convert to MLX arrays
        adj_mx = mx.array(adj_matrix)

        # Concatenate user and item embeddings
        node_embeddings = np.vstack([np.stack(user_embeddings), np.stack(item_embeddings)])
        features_mx = mx.array(node_embeddings)

        # Forward pass
        with mx.eval_mode():
            output_mx = self(adj_mx, features_mx)

        # Convert back to NumPy
        output = np.array(output_mx)

        # Split back into separate embeddings
        output_embeddings = [output[i] for i in range(output.shape[0])]

        return output_embeddings
