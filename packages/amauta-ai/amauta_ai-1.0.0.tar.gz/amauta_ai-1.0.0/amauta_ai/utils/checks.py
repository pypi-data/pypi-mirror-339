"""Utility functions for checking environment and requirements."""

import sys
import logging

logger = logging.getLogger(__name__)

def check_python_version(min_version=(3, 8)):
    """Check that the Python version meets the minimum required.
    
    Args:
        min_version (tuple): Minimum required Python version (major, minor)
        
    Raises:
        SystemExit: If Python version is too old
    """
    if sys.version_info[:2] < min_version:
        logger.error(f"Python {min_version[0]}.{min_version[1]} or higher is required")
        print(f"Error: Python {min_version[0]}.{min_version[1]} or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    return True 