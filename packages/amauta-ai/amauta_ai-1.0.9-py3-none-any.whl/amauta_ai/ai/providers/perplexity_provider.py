"""
Perplexity provider for AMAUTA.

This module provides the implementation for the Perplexity AI provider.
"""

import logging
from typing import Any, Dict, Generator, List, Optional, Set, Union

from amauta_ai.ai.providers.base_provider import AIProvider
from amauta_ai.config.models import ProviderCapability

# Configure logging
logger = logging.getLogger(__name__)

class PerplexityWrapper:
    """
    Wrapper for the PerplexiPy client providing a standardized interface.
    
    This wrapper abstracts the perplexipy library and provides consistent
    error handling, response formatting, and streaming support.
    """
    
    def __init__(self) -> None:
        """Initialize the PerplexiPy wrapper."""
        self._client = None
        self._available = False
        self._default_model = None
        
        # Check if PerplexiPy is available
        try:
            import perplexipy
            from perplexipy import PerplexityClient, PERPLEXITY_DEFAULT_MODEL
            self._available = True
            self._default_model = PERPLEXITY_DEFAULT_MODEL
        except ImportError:
            logger.warning("PerplexiPy package not available. Install with: pip install perplexipy>=1.2.0")
            self._available = False
    
    def initialize(self, api_key: str, model: Optional[str] = None) -> bool:
        """
        Initialize the PerplexiPy client.
        
        Args:
            api_key: The Perplexity API key
            model: Optional model to use (defaults to PERPLEXITY_DEFAULT_MODEL)
            
        Returns:
            True if initialization was successful, False otherwise
        """
        if not self._available:
            logger.warning("Cannot initialize PerplexiPy: package not available")
            return False
            
        try:
            from perplexipy import PerplexityClient
            
            # Initialize the client
            self._client = PerplexityClient(key=api_key)
            
            # Set the model if provided
            if model:
                try:
                    self._client.model = model
                    self._default_model = model
                except Exception as e:
                    logger.warning(f"Could not set model to {model}: {str(e)}")
                    logger.info(f"Using default model: {self._client.model}")
                    self._default_model = self._client.model
            else:
                self._default_model = self._client.model
                
            logger.info(f"PerplexityWrapper initialized with model: {self._default_model}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize PerplexiPy client: {str(e)}")
            return False
    
    @property
    def is_available(self) -> bool:
        """Check if the wrapper and client are available."""
        return self._available and self._client is not None
    
    @property
    def model(self) -> str:
        """Get the current model."""
        if self._client:
            return self._client.model
        return self._default_model if self._default_model else "unknown"
    
    @model.setter
    def model(self, model_name: str) -> None:
        """
        Set the model.
        
        Args:
            model_name: The model name to use
            
        Raises:
            RuntimeError: If the client is not initialized or the model is invalid
        """
        if not self._client:
            raise RuntimeError("PerplexiPy client not initialized")
            
        try:
            self._client.model = model_name
            self._default_model = model_name
            logger.info(f"Set PerplexiPy model to: {model_name}")
        except Exception as e:
            logger.error(f"Failed to set model to {model_name}: {str(e)}")
            raise RuntimeError(f"Invalid model {model_name}: {str(e)}")
    
    def query(self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any) -> str:
        """
        Query the Perplexity API.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt to guide the model's behavior
            **kwargs: Additional arguments for the provider
            
        Returns:
            The generated response as a string
            
        Raises:
            RuntimeError: If the client is not initialized or the query fails
        """
        if not self._client:
            raise RuntimeError("PerplexiPy client not initialized")
            
        try:
            # Combine system prompt and user prompt if both provided
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Make the API call
            response = self._client.query(full_prompt)
            
            return response
        except Exception as e:
            logger.error(f"Error querying Perplexity: {str(e)}")
            raise RuntimeError(f"Perplexity query failed: {str(e)}")
    
    def stream_query(self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any) -> Generator[str, None, None]:
        """
        Query the Perplexity API with streaming.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt to guide the model's behavior
            **kwargs: Additional arguments for the provider
            
        Yields:
            Chunks of the generated response as they become available
            
        Raises:
            RuntimeError: If the client is not initialized or the query fails
        """
        if not self._client:
            raise RuntimeError("PerplexiPy client not initialized")
            
        try:
            # Combine system prompt and user prompt if both provided
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Make the streaming API call
            for chunk in self._client.queryStreamable(full_prompt):
                if chunk is not None:  # Ensure we don't yield None values
                    yield chunk
                    
        except Exception as e:
            logger.error(f"Error streaming from Perplexity: {str(e)}")
            raise RuntimeError(f"Perplexity streaming query failed: {str(e)}")
    
    def get_supported_models(self) -> List[str]:
        """
        Get a list of supported models.
        
        Returns:
            List of model identifiers
        """
        if not self._client:
            # Return a default list if client isn't initialized
            return [
                "sonar-reasoning-pro",
                "sonar-reasoning",
                "sonar-pro",
                "sonar",
                "r1-1776",
            ]
        
        try:
            # Get models from the client
            return list(self._client.models.keys())
        except Exception as e:
            logger.warning(f"Failed to get supported models: {str(e)}")
            # Return fallback list
            return [
                "sonar-reasoning-pro",
                "sonar-reasoning",
                "sonar-pro",
                "sonar",
                "r1-1776",
            ]


class PerplexityProvider(AIProvider):
    """Perplexity provider implementation using the perplexipy library."""
    
    def __init__(self) -> None:
        """Initialize the Perplexity provider."""
        super().__init__()
        self._wrapper = PerplexityWrapper()
        self._api_key = None
        self._model = None
    
    @property
    def name(self) -> str:
        """Get the provider name."""
        return "perplexipy"
    
    @property
    def capabilities(self) -> Set[ProviderCapability]:
        """Get the provider capabilities."""
        return {
            ProviderCapability.GENERAL,
            ProviderCapability.RESEARCH,
            ProviderCapability.CODE,
            ProviderCapability.TASK,
            ProviderCapability.ANALYSIS,
        }
    
    def initialize(self, api_key: str, default_model: Optional[str] = None) -> bool:
        """Initialize the provider with API key and optional model."""
        self._api_key = api_key
        
        # Use safe default model options that are known to be supported
        supported_models = ["sonar-reasoning-pro", "sonar-reasoning", "sonar-pro", "sonar", "r1-1776"]
        
        # If a model is provided, check if it's in our list of known supported models
        if default_model and default_model not in supported_models:
            logger.warning(f"Requested model '{default_model}' may not be supported. Falling back to 'sonar'")
            self._model = "sonar"
        else:
            self._model = default_model or "sonar"
            
        return self._wrapper.initialize(api_key, self._model)
    
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """
        Query the Perplexity API.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate (not directly supported by perplexipy)
            temperature: Sampling temperature (not directly supported by perplexipy)
            **kwargs: Additional arguments for the provider
            
        Returns:
            The generated response as a string
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        if not self._wrapper.is_available:
            raise RuntimeError("Perplexity provider not initialized or unavailable")
            
        try:
            # Note: perplexipy doesn't directly expose max_tokens or temperature parameters
            # but we keep them for API consistency
            return self._wrapper.query(
                prompt=prompt,
                system_prompt=system_prompt,
                **kwargs,
            )
        except Exception as e:
            logger.error(f"Error querying Perplexity: {str(e)}")
            raise RuntimeError(f"Perplexity query failed: {str(e)}")
    
    def stream_query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        """
        Query the Perplexity API with streaming.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate (not directly supported by perplexipy)
            temperature: Sampling temperature (not directly supported by perplexipy)
            **kwargs: Additional arguments for the provider
            
        Yields:
            Chunks of the generated response as they become available
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        if not self._wrapper.is_available:
            raise RuntimeError("Perplexity provider not initialized or unavailable")
            
        try:
            # Note: perplexipy doesn't directly expose max_tokens or temperature parameters
            # but we keep them for API consistency
            yield from self._wrapper.stream_query(
                prompt=prompt,
                system_prompt=system_prompt,
                **kwargs,
            )
        except Exception as e:
            logger.error(f"Error streaming from Perplexity: {str(e)}")
            raise RuntimeError(f"Perplexity streaming query failed: {str(e)}")
    
    @property
    def is_available(self) -> bool:
        """Check if the provider is available."""
        return self._wrapper.is_available
    
    def get_supported_models(self) -> List[str]:
        """Get a list of supported models."""
        return self._wrapper.get_supported_models()
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the provider."""
        research_models = ["sonar-reasoning-pro", "sonar-reasoning"]
        current_model = self._wrapper.model
        
        return {
            "name": self.name,
            "version": "1.2.0+",
            "default_model": current_model,
            "available_models": self.get_supported_models(),
            "capabilities": [c.value for c in self.capabilities],
            "research_optimized": current_model in research_models,
            "research_models": research_models
        } 