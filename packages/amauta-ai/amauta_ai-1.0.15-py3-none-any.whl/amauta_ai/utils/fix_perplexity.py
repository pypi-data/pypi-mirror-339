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
                kwargs['timeout'] = 240.0  # 240-second timeout (increased from 120)
            
            if 'max_retries' not in kwargs:
                kwargs['max_retries'] = 5  # 5 retries (increased from 3)
            
            # Configure exponential backoff 
            # Will help with large PRD files and complex task generation
            if 'max_retries' in kwargs and not isinstance(kwargs['max_retries'], int):
                from httpx import Timeout
                try:
                    from openai._types import NOT_GIVEN, Timeout as OpenAITimeout
                    from openai._base_client import DEFAULT_MAX_RETRIES
                    kwargs['max_retries'] = DEFAULT_MAX_RETRIES
                except ImportError:
                    kwargs['max_retries'] = 5
                
            # Call the original __init__
            original_init(self, **kwargs)
        
        # Store original __init__
        original_init = OpenAI.__init__
        
        # Apply patch
        OpenAI.__init__ = patched_init
        
        # Also patch the default request options if available
        try:
            from openai._client import OpenAI as InternalOpenAI
            if hasattr(InternalOpenAI, 'DEFAULT_REQUEST_TIMEOUT'):
                InternalOpenAI.DEFAULT_REQUEST_TIMEOUT = 240.0
        except (ImportError, AttributeError):
            pass
        
        logger.info("Successfully patched OpenAI client used by perplexipy")
        logger.info("New timeout: 240 seconds, Retries: 5")
        
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