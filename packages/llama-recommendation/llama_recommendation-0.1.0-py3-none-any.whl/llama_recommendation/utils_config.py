"""
Configuration management for the recommendation system.

This module provides utilities for loading and managing configuration
settings throughout the recommendation system.
"""

import copy
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from llama_recommender.utils.logging import get_logger


class ConfigManager:
    """
    Configuration manager for the recommendation system.

    This class provides methods for loading, validating, and accessing
    configuration settings for the recommendation system.
    """

    DEFAULT_CONFIG = {
        "model": {
            "type": "multimodal",
            "embedding_dim": 128,
            "hidden_dims": [256, 128, 64],
            "use_causal": False,
            "use_graph": False,
        },
        "training": {
            "batch_size": 32,
            "learning_rate": 0.001,
            "epochs": 10,
            "early_stopping": True,
            "patience": 3,
            "validation_split": 0.2,
        },
        "privacy": {
            "use_differential_privacy": True,
            "dp_epsilon": 1.0,
            "dp_delta": 1e-5,
            "clip_norm": 1.0,
            "secure_embeddings": True,
        },
        "recommendation": {
            "candidate_strategies": ["similarity", "popular", "collaborative"],
            "diversity_weight": 0.2,
            "novelty_weight": 0.1,
            "trending_weight": 0.1,
            "minimum_ethical_score": 0.7,
            "explanation_style": "natural",
        },
        "federated": {
            "enabled": False,
            "server_url": None,
            "aggregation_method": "fedavg",
            "min_clients": 3,
            "update_interval": 3600,
        },
        "mobile": {"enable_coreml": False, "minimum_deployment_target": "14.0"},
        "logging": {"level": "INFO", "log_to_file": True, "log_dir": "logs"},
        "data": {"embedding_path": "embeddings", "cache_dir": "cache"},
    }

    def __init__(
        self,
        config_path: Optional[str] = None,
        env_prefix: str = "LLAMA_",
        use_dotenv: bool = True,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to configuration file
            env_prefix: Prefix for environment variables
            use_dotenv: Whether to load environment variables from .env file
            logger: Logger instance
        """
        self.config_path = config_path
        self.env_prefix = env_prefix
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize configuration
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)

        # Load environment variables if requested
        if use_dotenv:
            self._load_dotenv()

        # Load configuration from file if provided
        if config_path:
            self._load_config_file()

        # Override with environment variables
        self._load_env_vars()

        # Validate configuration
        self._validate_config()

        self.logger.info("Configuration loaded successfully")

    def _load_dotenv(self) -> None:
        """Load environment variables from .env file."""
        try:
            from dotenv import load_dotenv

            load_dotenv()
            self.logger.debug("Loaded environment variables from .env file")
        except ImportError:
            self.logger.warning(
                "dotenv package not installed. Skipping .env loading. "
                "Install with: pip install python-dotenv"
            )

    def _load_config_file(self) -> None:
        """Load configuration from file."""
        if not os.path.exists(self.config_path):
            self.logger.warning(f"Configuration file not found: {self.config_path}")
            return

        try:
            with open(self.config_path, "r") as f:
                file_config = json.load(f)

            # Merge with default configuration
            self._merge_config(file_config)

            self.logger.debug(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error loading configuration file: {e}")

    def _load_env_vars(self) -> None:
        """Override configuration with environment variables."""
        # Create mapping of environment variable names to config keys
        env_mapping = self._create_env_mapping()

        # Check each environment variable
        for env_name, config_path in env_mapping.items():
            env_value = os.getenv(env_name)
            if env_value is not None:
                # Convert value to appropriate type
                try:
                    # Try to parse as JSON
                    typed_value = json.loads(env_value)
                except json.JSONDecodeError:
                    # Fallback to string
                    typed_value = env_value

                # Set in configuration
                self._set_config_value(config_path, typed_value)

                self.logger.debug(f"Overrode {config_path} with environment variable {env_name}")

    def _create_env_mapping(self) -> Dict[str, str]:
        """
        Create mapping of environment variable names to config keys.

        Returns:
            Dictionary mapping environment variable names to configuration paths
        """
        mapping = {}

        def _process_section(section_path, section_config):
            for key, value in section_config.items():
                config_path = f"{section_path}.{key}" if section_path else key

                # Create environment variable name
                env_name = self.env_prefix + config_path.replace(".", "_").upper()

                # Add to mapping
                mapping[env_name] = config_path

                # Recursively process nested sections
                if isinstance(value, dict):
                    _process_section(config_path, value)

        # Process all sections
        _process_section("", self.config)

        return mapping

    def _set_config_value(self, path: str, value: Any) -> None:
        """
        Set a value in the configuration.

        Args:
            path: Configuration path (dot-separated)
            value: Value to set
        """
        # Split path into keys
        keys = path.split(".")

        # Navigate to the correct section
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        # Set the value
        config[keys[-1]] = value

    def _get_config_value(self, path: str, default: Any = None) -> Any:
        """
        Get a value from the configuration.

        Args:
            path: Configuration path (dot-separated)
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        # Split path into keys
        keys = path.split(".")

        # Navigate to the correct section
        config = self.config
        for key in keys:
            if key not in config:
                return default
            config = config[key]

        return config

    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """
        Merge a new configuration into the current one.

        Args:
            new_config: New configuration to merge
        """

        def _merge_dicts(target, source):
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    # Recursively merge nested dictionaries
                    _merge_dicts(target[key], value)
                else:
                    # Override or add value
                    target[key] = value

        _merge_dicts(self.config, new_config)

    def _validate_config(self) -> None:
        """Validate the configuration."""
        # Perform basic validation
        errors = []

        # Check required values
        if self.config.get("model", {}).get("embedding_dim") <= 0:
            errors.append("Embedding dimension must be positive")

        if self.config.get("privacy", {}).get("dp_epsilon") <= 0:
            errors.append("Differential privacy epsilon must be positive")

        if self.config.get("privacy", {}).get("dp_delta") <= 0:
            errors.append("Differential privacy delta must be positive")

        # Log errors
        if errors:
            for error in errors:
                self.logger.error(f"Configuration error: {error}")
            raise ValueError(f"Invalid configuration: {', '.join(errors)}")

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            path: Configuration path (dot-separated)
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        return self._get_config_value(path, default)

    def set(self, path: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            path: Configuration path (dot-separated)
            value: Value to set
        """
        self._set_config_value(path, value)
        self.logger.debug(f"Set configuration {path} to {value}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.

        Returns:
            Configuration dictionary
        """
        return copy.deepcopy(self.config)

    def save(self, path: Optional[str] = None) -> None:
        """
        Save the configuration to a file.

        Args:
            path: Path to save the configuration (if None, uses config_path)
        """
        save_path = path or self.config_path
        if not save_path:
            self.logger.warning("No path specified for saving configuration")
            return

        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Save configuration
            with open(save_path, "w") as f:
                json.dump(self.config, f, indent=2)

            self.logger.info(f"Saved configuration to {save_path}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")

    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration from a dictionary.

        Args:
            config_dict: Dictionary with configuration values
        """
        self._merge_config(config_dict)
        self.logger.debug("Updated configuration from dictionary")

    def load_from_file(self, path: str) -> None:
        """
        Load configuration from a file.

        Args:
            path: Path to configuration file
        """
        old_config_path = self.config_path
        self.config_path = path
        self._load_config_file()
        self.config_path = old_config_path

    def reset(self) -> None:
        """Reset the configuration to default values."""
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)
        self.logger.info("Reset configuration to defaults")

    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration.

        Returns:
            Logging configuration dictionary
        """
        return copy.deepcopy(self.config.get("logging", {}))

    def get_model_config(self) -> Dict[str, Any]:
        """
        Get model configuration.

        Returns:
            Model configuration dictionary
        """
        return copy.deepcopy(self.config.get("model", {}))

    def get_training_config(self) -> Dict[str, Any]:
        """
        Get training configuration.

        Returns:
            Training configuration dictionary
        """
        return copy.deepcopy(self.config.get("training", {}))

    def get_privacy_config(self) -> Dict[str, Any]:
        """
        Get privacy configuration.

        Returns:
            Privacy configuration dictionary
        """
        return copy.deepcopy(self.config.get("privacy", {}))

    def get_recommendation_config(self) -> Dict[str, Any]:
        """
        Get recommendation configuration.

        Returns:
            Recommendation configuration dictionary
        """
        return copy.deepcopy(self.config.get("recommendation", {}))

    def get_federated_config(self) -> Dict[str, Any]:
        """
        Get federated learning configuration.

        Returns:
            Federated learning configuration dictionary
        """
        return copy.deepcopy(self.config.get("federated", {}))

    def get_mobile_config(self) -> Dict[str, Any]:
        """
        Get mobile deployment configuration.

        Returns:
            Mobile deployment configuration dictionary
        """
        return copy.deepcopy(self.config.get("mobile", {}))

    def get_data_config(self) -> Dict[str, Any]:
        """
        Get data configuration.

        Returns:
            Data configuration dictionary
        """
        return copy.deepcopy(self.config.get("data", {}))


class EnvironmentVariableProvider:
    """
    Provider for environment variables with defaults.

    This class provides methods for accessing environment variables
    with default values and type conversion.
    """

    def __init__(self, prefix: str = "LLAMA_"):
        """
        Initialize the environment variable provider.

        Args:
            prefix: Prefix for environment variables
        """
        self.prefix = prefix

    def get(self, name: str, default: Any = None, type_converter: Optional[callable] = None) -> Any:
        """
        Get an environment variable.

        Args:
            name: Environment variable name (without prefix)
            default: Default value if not found
            type_converter: Function to convert the value to a specific type

        Returns:
            Environment variable value or default
        """
        env_name = self.prefix + name
        env_value = os.getenv(env_name)

        if env_value is None:
            return default

        if type_converter is not None:
            try:
                return type_converter(env_value)
            except Exception:
                return default

        return env_value

    def get_int(self, name: str, default: Optional[int] = None) -> Optional[int]:
        """
        Get an integer environment variable.

        Args:
            name: Environment variable name (without prefix)
            default: Default value if not found or invalid

        Returns:
            Integer value or default
        """
        return self.get(name, default, int)

    def get_float(self, name: str, default: Optional[float] = None) -> Optional[float]:
        """
        Get a float value from environment variables.

        Args:
            name: Environment variable name (without prefix)
            default: Default value if not found or invalid

        Returns:
            Float value or default
        """
        return self.get(name, default, float)
