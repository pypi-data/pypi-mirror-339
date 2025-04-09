"""
Data loading and processing utilities for the recommendation system.

This module provides utilities for loading and processing data for
training and evaluating recommendation models.
"""

import csv
import gzip
import json
import logging
import os
import pickle
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from llama_recommender.utils.logging import get_logger


class DataLoader:
    """
    Data loader for recommendation datasets.

    This class provides methods for loading and preprocessing data
    for training and evaluating recommendation models.
    """

    def __init__(
        self,
        cache_dir: str = "cache",
        use_cache: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the data loader.

        Args:
            cache_dir: Directory for caching data
            use_cache: Whether to use cached data
            logger: Logger instance
        """
        self.cache_dir = cache_dir
        self.use_cache = use_cache
        self.logger = logger or get_logger(self.__class__.__name__)

        # Create cache directory if it doesn't exist
        if use_cache:
            os.makedirs(cache_dir, exist_ok=True)

    def load_csv(
        self,
        path: str,
        delimiter: str = ",",
        header: bool = True,
        dtypes: Optional[Dict[str, type]] = None,
        cache_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Load data from a CSV file.

        Args:
            path: Path to CSV file
            delimiter: Field delimiter
            header: Whether the file has a header row
            dtypes: Dictionary mapping column names to types
            cache_key: Key for caching the data (if None, no caching)

        Returns:
            Dictionary with data and metadata
        """
        # Check if cached version exists
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "rb") as f:
                        data = pickle.load(f)
                    self.logger.info(f"Loaded cached data from {cache_path}")
                    return data
                except Exception as e:
                    self.logger.warning(f"Error loading cached data: {e}")

        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # Load data from CSV
        rows = []

        # Determine if file is gzipped
        open_func = gzip.open if path.endswith(".gz") else open

        with open_func(path, "rt", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=delimiter)

            # Read header if present
            if header:
                headers = next(reader)
            else:
                # Generate numeric column names
                headers = [f"col{i}" for i in range(len(next(reader)))]
                # Reset file pointer
                f.seek(0)

            # Read data rows
            for row in reader:
                # Convert to dictionary
                row_dict = {}
                for i, value in enumerate(row):
                    if i < len(headers):
                        col_name = headers[i]

                        # Convert to specified type if provided
                        if dtypes and col_name in dtypes:
                            try:
                                value = dtypes[col_name](value)
                            except (ValueError, TypeError):
                                # Keep as string if conversion fails
                                pass

                        row_dict[col_name] = value

                rows.append(row_dict)

        # Prepare result
        result = {
            "data": rows,
            "headers": headers,
            "metadata": {"file_path": path, "delimiter": delimiter, "row_count": len(rows)},
        }

        # Cache data if requested
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            try:
                with open(cache_path, "wb") as f:
                    pickle.dump(result, f)
                self.logger.info(f"Cached data to {cache_path}")
            except Exception as e:
                self.logger.warning(f"Error caching data: {e}")

        self.logger.info(f"Loaded {len(rows)} rows from {path}")
        return result

    def load_json(self, path: str, cache_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Load data from a JSON file.

        Args:
            path: Path to JSON file
            cache_key: Key for caching the data (if None, no caching)

        Returns:
            Dictionary with data and metadata
        """
        # Check if cached version exists
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "rb") as f:
                        data = pickle.load(f)
                    self.logger.info(f"Loaded cached data from {cache_path}")
                    return data
                except Exception as e:
                    self.logger.warning(f"Error loading cached data: {e}")

        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # Determine if file is gzipped
        open_func = gzip.open if path.endswith(".gz") else open

        # Load data from JSON
        with open_func(path, "rt", encoding="utf-8") as f:
            data = json.load(f)

        # Prepare result
        result = {"data": data, "metadata": {"file_path": path}}

        # Add additional metadata based on data structure
        if isinstance(data, list):
            result["metadata"]["item_count"] = len(data)
        elif isinstance(data, dict):
            result["metadata"]["key_count"] = len(data)

        # Cache data if requested
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            try:
                with open(cache_path, "wb") as f:
                    pickle.dump(result, f)
                self.logger.info(f"Cached data to {cache_path}")
            except Exception as e:
                self.logger.warning(f"Error caching data: {e}")

        self.logger.info(f"Loaded data from {path}")
        return result

    def load_numpy(self, path: str, cache_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Load data from a NumPy file.

        Args:
            path: Path to NumPy file
            cache_key: Key for caching the data (if None, no caching)

        Returns:
            Dictionary with data and metadata
        """
        # Check if cached version exists
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "rb") as f:
                        data = pickle.load(f)
                    self.logger.info(f"Loaded cached data from {cache_path}")
                    return data
                except Exception as e:
                    self.logger.warning(f"Error loading cached data: {e}")

        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # Load data from NumPy file
        try:
            data = np.load(path, allow_pickle=True)
        except Exception as e:
            raise ValueError(f"Error loading NumPy file: {e}")

        # Prepare result
        result = {
            "data": data,
            "metadata": {
                "file_path": path,
                "shape": data.shape if hasattr(data, "shape") else None,
                "dtype": str(data.dtype) if hasattr(data, "dtype") else None,
            },
        }

        # Cache data if requested
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            try:
                with open(cache_path, "wb") as f:
                    pickle.dump(result, f)
                self.logger.info(f"Cached data to {cache_path}")
            except Exception as e:
                self.logger.warning(f"Error caching data: {e}")

        self.logger.info(f"Loaded data from {path}")
        return result

    def load_embeddings(
        self, path: str, entity_type: str = "user", cache_key: Optional[str] = None
    ) -> Dict[str, np.ndarray]:
        """
        Load embeddings from a file.

        Args:
            path: Path to embeddings file
            entity_type: Type of entities ('user' or 'item')
            cache_key: Key for caching the data (if None, no caching)

        Returns:
            Dictionary mapping entity IDs to embeddings
        """
        # Check if cached version exists
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "rb") as f:
                        embeddings = pickle.load(f)
                    self.logger.info(f"Loaded cached embeddings from {cache_path}")
                    return embeddings
                except Exception as e:
                    self.logger.warning(f"Error loading cached embeddings: {e}")

        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # Load embeddings based on file type
        if path.endswith(".npy") or path.endswith(".npz"):
            # Load from NumPy file
            embeddings = np.load(path, allow_pickle=True)

            # Convert to dictionary if array
            if isinstance(embeddings, np.ndarray):
                if embeddings.ndim == 2:
                    # Assume row index corresponds to entity ID
                    embeddings = {
                        f"{entity_type}_{i}": embeddings[i] for i in range(embeddings.shape[0])
                    }
            elif not isinstance(embeddings, dict):
                self.logger.warning(f"Unexpected embeddings format from {path}")
                embeddings = {}

        elif path.endswith(".json") or path.endswith(".json.gz"):
            # Load from JSON file
            open_func = gzip.open if path.endswith(".gz") else open
            with open_func(path, "rt", encoding="utf-8") as f:
                embeddings_data = json.load(f)

            # Convert to NumPy arrays
            embeddings = {}
            for entity_id, embedding in embeddings_data.items():
                embeddings[entity_id] = np.array(embedding, dtype=np.float32)

        elif path.endswith(".pickle") or path.endswith(".pkl"):
            # Load from pickle file
            with open(path, "rb") as f:
                embeddings = pickle.load(f)

            # Check format
            if not isinstance(embeddings, dict):
                self.logger.warning(f"Unexpected embeddings format from {path}")
                embeddings = {}

        else:
            # Try to infer format from content
            try:
                embeddings = self.load_numpy(path)["data"]

                # Convert to dictionary if array
                if isinstance(embeddings, np.ndarray) and embeddings.ndim == 2:
                    embeddings = {
                        f"{entity_type}_{i}": embeddings[i] for i in range(embeddings.shape[0])
                    }
                elif not isinstance(embeddings, dict):
                    self.logger.warning(f"Unexpected embeddings format from {path}")
                    embeddings = {}

            except Exception:
                self.logger.warning(f"Failed to load embeddings from {path}")
                embeddings = {}

        # Cache embeddings if requested
        if self.use_cache and cache_key and embeddings:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            try:
                with open(cache_path, "wb") as f:
                    pickle.dump(embeddings, f)
                self.logger.info(f"Cached embeddings to {cache_path}")
            except Exception as e:
                self.logger.warning(f"Error caching embeddings: {e}")

        self.logger.info(f"Loaded {len(embeddings)} embeddings from {path}")
        return embeddings

    def load_interactions(
        self,
        path: str,
        user_col: str = "user_id",
        item_col: str = "item_id",
        rating_col: Optional[str] = "rating",
        timestamp_col: Optional[str] = "timestamp",
        delimiter: str = ",",
        cache_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Load user-item interactions from a file.

        Args:
            path: Path to interactions file
            user_col: Name of user ID column
            item_col: Name of item ID column
            rating_col: Name of rating column (if None, all interactions are 1.0)
            timestamp_col: Name of timestamp column (if None, ignored)
            delimiter: Field delimiter for CSV files
            cache_key: Key for caching the data (if None, no caching)

        Returns:
            Dictionary with interactions data and metadata
        """
        # Check if cached version exists
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, "rb") as f:
                        interactions = pickle.load(f)
                    self.logger.info(f"Loaded cached interactions from {cache_path}")
                    return interactions
                except Exception as e:
                    self.logger.warning(f"Error loading cached interactions: {e}")

        # Load data based on file type
        if (
            path.endswith(".csv")
            or path.endswith(".csv.gz")
            or path.endswith(".txt")
            or path.endswith(".txt.gz")
        ):
            # Load from CSV file
            data = self.load_csv(
                path=path,
                delimiter=delimiter,
                header=True,
                dtypes=(
                    {
                        rating_col: float if rating_col else None,
                        timestamp_col: int if timestamp_col else None,
                    }
                    if rating_col or timestamp_col
                    else None
                ),
            )

            # Extract interactions
            interactions = []
            for row in data["data"]:
                # Check for required columns
                if user_col not in row or item_col not in row:
                    continue

                user_id = row[user_col]
                item_id = row[item_col]

                # Extract rating if available
                rating = 1.0
                if rating_col and rating_col in row:
                    try:
                        rating = float(row[rating_col])
                    except (ValueError, TypeError):
                        rating = 1.0

                # Extract timestamp if available
                timestamp = None
                if timestamp_col and timestamp_col in row:
                    try:
                        timestamp = int(row[timestamp_col])
                    except (ValueError, TypeError):
                        timestamp = None

                # Create interaction
                interaction = {"user_id": user_id, "item_id": item_id, "rating": rating}

                if timestamp is not None:
                    interaction["timestamp"] = timestamp

                interactions.append(interaction)

            # Create result
            unique_users = set(interaction["user_id"] for interaction in interactions)
            unique_items = set(interaction["item_id"] for interaction in interactions)

            result = {
                "interactions": interactions,
                "metadata": {
                    "file_path": path,
                    "interaction_count": len(interactions),
                    "user_count": len(unique_users),
                    "item_count": len(unique_items),
                    "density": (
                        len(interactions) / (len(unique_users) * len(unique_items))
                        if unique_users and unique_items
                        else 0
                    ),
                },
            }

        elif path.endswith(".json") or path.endswith(".json.gz"):
            # Load from JSON file
            data = self.load_json(path)

            # Check format
            if isinstance(data["data"], list):
                # List of interactions
                interactions = []
                for item in data["data"]:
                    # Check for required fields
                    if not isinstance(item, dict) or user_col not in item or item_col not in item:
                        continue

                    user_id = item[user_col]
                    item_id = item[item_col]

                    # Extract rating if available
                    rating = 1.0
                    if rating_col and rating_col in item:
                        try:
                            rating = float(item[rating_col])
                        except (ValueError, TypeError):
                            rating = 1.0

                    # Extract timestamp if available
                    timestamp = None
                    if timestamp_col and timestamp_col in item:
                        try:
                            timestamp = int(item[timestamp_col])
                        except (ValueError, TypeError):
                            timestamp = None

                    # Create interaction
                    interaction = {"user_id": user_id, "item_id": item_id, "rating": rating}

                    if timestamp is not None:
                        interaction["timestamp"] = timestamp

                    interactions.append(interaction)

            elif isinstance(data["data"], dict):
                # Dictionary of user -> items
                interactions = []
                for user_id, items in data["data"].items():
                    if isinstance(items, list):
                        # List of items
                        for item_entry in items:
                            if isinstance(item_entry, dict):
                                # Dictionary with item information
                                if item_col not in item_entry:
                                    continue

                                item_id = item_entry[item_col]

                                # Extract rating if available
                                rating = 1.0
                                if rating_col and rating_col in item_entry:
                                    try:
                                        rating = float(item_entry[rating_col])
                                    except (ValueError, TypeError):
                                        rating = 1.0

                                # Extract timestamp if available
                                timestamp = None
                                if timestamp_col and timestamp_col in item_entry:
                                    try:
                                        timestamp = int(item_entry[timestamp_col])
                                    except (ValueError, TypeError):
                                        timestamp = None

                            elif isinstance(item_entry, str):
                                # Item ID only
                                item_id = item_entry
                                rating = 1.0
                                timestamp = None

                            else:
                                # Unknown format
                                continue

                            # Create interaction
                            interaction = {"user_id": user_id, "item_id": item_id, "rating": rating}

                            if timestamp is not None:
                                interaction["timestamp"] = timestamp

                            interactions.append(interaction)

                    elif isinstance(items, dict):
                        # Dictionary of item IDs to ratings
                        for item_id, rating_value in items.items():
                            rating = 1.0
                            if isinstance(rating_value, (int, float)):
                                rating = float(rating_value)
                            elif (
                                isinstance(rating_value, dict)
                                and rating_col
                                and rating_col in rating_value
                            ):
                                try:
                                    rating = float(rating_value[rating_col])
                                except (ValueError, TypeError):
                                    rating = 1.0

                            # Extract timestamp if available
                            timestamp = None
                            if (
                                isinstance(rating_value, dict)
                                and timestamp_col
                                and timestamp_col in rating_value
                            ):
                                try:
                                    timestamp = int(rating_value[timestamp_col])
                                except (ValueError, TypeError):
                                    timestamp = None

                            # Create interaction
                            interaction = {"user_id": user_id, "item_id": item_id, "rating": rating}

                            if timestamp is not None:
                                interaction["timestamp"] = timestamp

                            interactions.append(interaction)

            else:
                # Unknown format
                self.logger.warning(f"Unknown interactions format in {path}")
                interactions = []

            # Create result
            unique_users = set(interaction["user_id"] for interaction in interactions)
            unique_items = set(interaction["item_id"] for interaction in interactions)

            result = {
                "interactions": interactions,
                "metadata": {
                    "file_path": path,
                    "interaction_count": len(interactions),
                    "user_count": len(unique_users),
                    "item_count": len(unique_items),
                    "density": (
                        len(interactions) / (len(unique_users) * len(unique_items))
                        if unique_users and unique_items
                        else 0
                    ),
                },
            }

        else:
            # Unknown format
            self.logger.warning(f"Unsupported file format for interactions: {path}")
            result = {
                "interactions": [],
                "metadata": {
                    "file_path": path,
                    "interaction_count": 0,
                    "user_count": 0,
                    "item_count": 0,
                    "density": 0,
                },
            }

        # Cache interactions if requested
        if self.use_cache and cache_key:
            cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
            try:
                with open(cache_path, "wb") as f:
                    pickle.dump(result, f)
                self.logger.info(f"Cached interactions to {cache_path}")
            except Exception as e:
                self.logger.warning(f"Error caching interactions: {e}")

        self.logger.info(
            f"Loaded {result['metadata']['interaction_count']} interactions from {path} "
            f"({result['metadata']['user_count']} users, {result['metadata']['item_count']} items)"
        )

        return result

    def create_train_test_split(
        self,
        interactions: List[Dict[str, Any]],
        test_ratio: float = 0.2,
        validation_ratio: float = 0.1,
        seed: Optional[int] = None,
        by_user: bool = True,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Create train/test/validation splits from interactions.

        Args:
            interactions: List of interaction dictionaries
            test_ratio: Proportion of data to use for the test set.
            validation_ratio: Proportion of data to use for the validation set.
            seed: Random seed for reproducibility.
            by_user: If True, split data per user to avoid data leakage.

        Returns:
            Dictionary containing 'train', 'test', and 'validation' sets.
        """

        if (
            not (0 < test_ratio < 1)
            or not (0 < validation_ratio < 1)
            or (test_ratio + validation_ratio >= 1)
        ):
            raise ValueError(
                "Test and validation ratios must be between 0 and 1, "
                "and their sum must be less than 1."
            )

        if by_user:
            # Group interactions by user
            user_interactions = {}
            for interaction in interactions:
                user_id = interaction["user_id"]
                if user_id not in user_interactions:
                    user_interactions[user_id] = []
                user_interactions[user_id].append(interaction)

            # Split each user's interactions
            train_test_split = {}
            for user_id, user_interactions in user_interactions.items():
                train_test_split[user_id] = self._split_interactions(
                    user_interactions, test_ratio, validation_ratio, seed
                )

            return train_test_split
        else:
            # Split interactions as a single group
            return self._split_interactions(interactions, test_ratio, validation_ratio, seed)

    def _split_interactions(
        self,
        interactions: List[Dict[str, Any]],
        test_ratio: float,
        validation_ratio: float,
        seed: Optional[int] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Split a list of interactions into train/test/validation sets.

        Args:
            interactions: List of interaction dictionaries
            test_ratio: Proportion of data to use for the test set.
            validation_ratio: Proportion of data to use for the validation set.
            seed: Random seed for reproducibility.

        Returns:
            Dictionary containing 'train', 'test', and 'validation' sets.
        """
        import random

        if seed is not None:
            random.seed(seed)

        random.shuffle(interactions)

        split_index = int(len(interactions) * test_ratio)
        test_set = interactions[:split_index]

        split_index += int(len(interactions) * validation_ratio)
        validation_set = interactions[split_index:]

        return {"train": interactions[split_index:], "test": test_set, "validation": validation_set}
