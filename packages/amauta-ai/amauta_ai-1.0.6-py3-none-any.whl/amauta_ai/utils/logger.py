"""Logger configuration for AMAUTA.

This module provides a centralized logging configuration for the AMAUTA project.
It sets up logging with proper formatting and handlers for both file and console output.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

# Constants for log configuration
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_DIR = "logs"
DEFAULT_LOG_FILE = "amauta.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT = 5


def setup_logger() -> None:
    """Set up the global logging configuration.
    
    This function initializes the root logger and configures basic logging
    formatters and handlers. It should be called once at application startup.
    """
    # Get log level from environment variable if available
    log_level_name = os.environ.get("AMAUTA_LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, DEFAULT_LOG_LEVEL)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers (in case this function is called multiple times)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatters
    formatter = logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_LOG_DATE_FORMAT)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Create file handler if log directory exists or can be created
    try:
        # Create log directory if it doesn't exist
        os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            os.path.join(DEFAULT_LOG_DIR, DEFAULT_LOG_FILE),
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    
    except Exception as e:
        # Log error to console but continue without file handler
        root_logger.warning(f"Could not create file handler: {str(e)}")


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger with the given name.
    
    Args:
        name: The name of the logger
        level: Optional logging level (defaults to INFO or from environment)
        
    Returns:
        A configured logger
    """
    # Get the default log level from environment or use INFO
    if level is None:
        log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
        try:
            level = getattr(logging, log_level_str)
        except AttributeError:
            level = logging.INFO
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create console handler if not already set up
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger


def set_log_level(level: int) -> None:
    """Set the log level for all handlers of all loggers.

    Args:
        level (int): The log level to set (e.g., logging.DEBUG, logging.INFO)
    """
    # Update root logger
    logging.getLogger().setLevel(level)

    # Update all existing loggers
    for name in logging.root.manager.loggerDict:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)


def get_log_level() -> int:
    """Get the current log level of the root logger.

    Returns:
        int: The current log level
    """
    return logging.getLogger().getEffectiveLevel()


# Initialize root logger with default configuration
root_logger = get_logger("root")

# Export commonly used log levels
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
