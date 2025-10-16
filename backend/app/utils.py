"""Utility functions for logging and common operations."""

import logging
import sys
from pathlib import Path

from .config import get_settings

settings = get_settings()


def setup_logging() -> logging.Logger:
    """
    Configure application logging with console and file handlers.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("iot_analytics_api")
    logger.setLevel(getattr(logging, settings.log_level))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level))

    # File handler
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setLevel(getattr(logging, settings.log_level))

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Initialize logger
logger = setup_logging()
