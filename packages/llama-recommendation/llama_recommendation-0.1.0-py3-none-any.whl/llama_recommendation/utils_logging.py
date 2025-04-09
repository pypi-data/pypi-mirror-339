"""
Logging utilities for the recommendation system.

This module provides utilities for setting up and managing logging
throughout the recommendation system.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    console: bool = True,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger
        level: Logging level
        log_file: Path to log file (if None, no file logging)
        log_format: Logging format string
        console: Whether to log to console
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set format
    if log_format is None:
        log_format = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"

    formatter = logging.Formatter(log_format)

    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler if log file specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def configure_root_logger(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    console: bool = True,
) -> None:
    """
    Configure the root logger.

    Args:
        level: Logging level
        log_file: Path to log file (if None, no file logging)
        log_format: Logging format string
        console: Whether to log to console
    """
    logger = get_logger(
        name="",  # Root logger
        level=level,
        log_file=log_file,
        log_format=log_format,
        console=console,
    )

    # Set as root logger
    logging.root = logger


class LoggingManager:
    """Manager for handling logging across the application."""

    def __init__(
        self,
        default_level: int = logging.INFO,
        default_format: str = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        log_dir: str = "logs",
    ):
        """
        Initialize the logging manager.

        Args:
            default_level: Default logging level
            default_format: Default log format
            log_dir: Directory for log files
        """
        self.default_level = default_level
        self.default_format = default_format
        self.log_dir = log_dir

        # Create log directory
        os.makedirs(log_dir, exist_ok=True)

        # Configure root logger
        configure_root_logger(
            level=default_level,
            log_file=os.path.join(log_dir, "app.log"),
            log_format=default_format,
            console=True,
        )

        # Keep track of module loggers
        self.loggers: Dict[str, logging.Logger] = {}

    def get_logger(self, name: str, level: Optional[int] = None) -> logging.Logger:
        """
        Get a logger for a specific module.

        Args:
            name: Module name
            level: Logging level (if None, use default)

        Returns:
            Configured logger instance
        """
        if name in self.loggers:
            return self.loggers[name]

        log_file = os.path.join(self.log_dir, f"{name.replace('.', '_')}.log")
        logger = get_logger(
            name=name,
            level=level or self.default_level,
            log_file=log_file,
            log_format=self.default_format,
            console=True,
        )

        self.loggers[name] = logger
        return logger

    def set_level(self, name: str, level: int) -> None:
        """
        Set the logging level for a specific module.

        Args:
            name: Module name
            level: Logging level
        """
        if name in self.loggers:
            self.loggers[name].setLevel(level)
        else:
            logger = self.get_logger(name)
            logger.setLevel(level)

    def enable_debug(self, name: Optional[str] = None) -> None:
        """
        Enable debug logging for a module or all modules.

        Args:
            name: Module name (if None, enable for all)
        """
        if name:
            self.set_level(name, logging.DEBUG)
        else:
            # Enable for all existing loggers
            for logger_name in self.loggers:
                self.set_level(logger_name, logging.DEBUG)

            # Set default level for future loggers
            self.default_level = logging.DEBUG

            # Update root logger
            logging.getLogger().setLevel(logging.DEBUG)

    def disable_console(self, name: Optional[str] = None) -> None:
        """
        Disable console logging for a module or all modules.

        Args:
            name: Module name (if None, disable for all)
        """
        if name:
            if name in self.loggers:
                logger = self.loggers[name]
                for handler in logger.handlers[:]:
                    if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                        logger.removeHandler(handler)
        else:
            # Disable for all loggers
            for logger in self.loggers.values():
                for handler in logger.handlers[:]:
                    if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                        logger.removeHandler(handler)

    def capture_warnings(self, capture: bool = True) -> None:
        """
        Capture warnings with the logging system.

        Args:
            capture: Whether to capture warnings
        """
        logging.captureWarnings(capture)


class MetricsLogger:
    """Logger for tracking and logging metrics."""

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        log_file: Optional[str] = None,
        console: bool = True,
    ):
        """
        Initialize the metrics logger.

        Args:
            logger: Logger instance
            log_file: Path to log file (if None, no file logging)
            console: Whether to log to console
        """
        self.logger = logger or get_logger(name="metrics", log_file=log_file, console=console)

        # Initialize metrics store
        self.metrics: Dict[str, Any] = {}

    def log_metric(self, name: str, value: Any, tags: Optional[Dict[str, str]] = None) -> None:
        """
        Log a metric value.

        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags for the metric
        """
        # Store metric
        if name not in self.metrics:
            self.metrics[name] = []

        metric_entry = {"value": value, "tags": tags or {}}

        self.metrics[name].append(metric_entry)

        # Log metric
        tags_str = ""
        if tags:
            tags_str = ", ".join(f"{k}={v}" for k, v in tags.items())
            tags_str = f" [{tags_str}]"

        self.logger.info(f"Metric: {name}={value}{tags_str}")

    def get_metrics(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get logged metrics.

        Args:
            name: Metric name (if None, get all metrics)

        Returns:
            Dictionary of metrics
        """
        if name:
            return self.metrics.get(name, [])
        else:
            return self.metrics

    def reset_metrics(self, name: Optional[str] = None) -> None:
        """
        Reset logged metrics.

        Args:
            name: Metric name (if None, reset all metrics)
        """
        if name:
            self.metrics[name] = []
        else:
            self.metrics = {}

    def aggregate_metrics(self, name: str, aggregation: str = "mean") -> Optional[float]:
        """
        Aggregate metric values.

        Args:
            name: Metric name
            aggregation: Aggregation method ('mean', 'sum', 'min', 'max', 'count')

        Returns:
            Aggregated value or None if no metrics found
        """
        if name not in self.metrics or not self.metrics[name]:
            return None

        values = [entry["value"] for entry in self.metrics[name]]

        if aggregation == "mean":
            return sum(values) / len(values)
        elif aggregation == "sum":
            return sum(values)
        elif aggregation == "min":
            return min(values)
        elif aggregation == "max":
            return max(values)
        elif aggregation == "count":
            return len(values)
        else:
            raise ValueError(f"Unknown aggregation method: {aggregation}")

    def log_aggregated_metrics(self, aggregation: str = "mean") -> None:
        """
        Log aggregated metrics.

        Args:
            aggregation: Aggregation method ('mean', 'sum', 'min', 'max', 'count')
        """
        for name in self.metrics:
            agg_value = self.aggregate_metrics(name, aggregation)
            if agg_value is not None:
                self.logger.info(f"Aggregated {aggregation}({name}) = {agg_value}")
