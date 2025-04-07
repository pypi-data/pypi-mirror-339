"""
Utility to patch perplexipy's OpenAI client for better timeout handling.

This module patches the underlying OpenAI client used by perplexipy
to handle timeout errors gracefully and adjust timeout settings.
"""

import logging
import importlib.util
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

def patch_perplexipy():
    """
    Patch perplexipy to use more robust timeout settings with the OpenAI client.
    
    This function attempts to:
    1. Determine if perplexipy is installed
    2. Patch the OpenAI client timeout settings used by perplexipy
    3. Log the outcome of the patching process
    
    Returns:
        bool: True if patching was successful, False otherwise
    """
    # Check if perplexipy is available
    perplexipy_spec = importlib.util.find_spec("perplexipy")
    if not perplexipy_spec:
        logger.warning("perplexipy package not found. Cannot apply patches.")
        return False
    
    # Check if openai is available
    openai_spec = importlib.util.find_spec("openai")
    if not openai_spec:
        logger.warning("openai package not found. Cannot apply patches.")
        return False
    
    try:
        import openai
        from openai import OpenAI
        
        # Get original OpenAI client
        original_client = OpenAI
        
        # Create a patched version with longer timeouts
        def patched_init(self, **kwargs):
            # Ensure timeout settings are included and set to appropriate values
            if 'timeout' not in kwargs:
                kwargs['timeout'] = 120.0  # 120-second timeout
            
            if 'max_retries' not in kwargs:
                kwargs['max_retries'] = 3  # 3 retries
                
            # Call the original __init__
            original_init(self, **kwargs)
        
        # Store original __init__
        original_init = OpenAI.__init__
        
        # Apply patch
        OpenAI.__init__ = patched_init
        
        logger.info("Successfully patched OpenAI client used by perplexipy")
        logger.info("New timeout: 120 seconds, Retries: 3")
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to patch perplexipy OpenAI client: {e}")
        return False

def get_perplexipy_version() -> Optional[str]:
    """
    Get the installed version of perplexipy.
    
    Returns:
        Optional[str]: The version string if perplexipy is installed, None otherwise
    """
    try:
        import perplexipy
        version = getattr(perplexipy, "__VERSION__", "unknown")
        return version
    except ImportError:
        return None
    except Exception as e:
        logger.error(f"Error checking perplexipy version: {e}")
        return None 