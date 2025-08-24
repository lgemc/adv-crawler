"""
Logging configuration for the crawler
"""

import logging
import sys
from typing import Optional


def setup_logger(level: int = logging.INFO, log_file: Optional[str] = None) -> logging.Logger:
    """Setup and configure the logger"""
    
    # Create logger
    logger = logging.getLogger('crawler')
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Set crawlee logger level
    crawlee_logger = logging.getLogger('crawlee')
    crawlee_logger.setLevel(logging.WARNING)  # Reduce crawlee verbosity
    
    return logger