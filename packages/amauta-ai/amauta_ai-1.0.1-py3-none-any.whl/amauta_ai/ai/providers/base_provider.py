"""
Base provider for AMAUTA.

This module defines the abstract base class for all AI providers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Optional, Set

from amauta_ai.config.models import ProviderCapability


class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    
    All provider implementations should inherit from this class
    to ensure a consistent interface across different providers.
    """
    
    def __init__(self):
        """Initialize the base provider."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the provider name."""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> Set[ProviderCapability]:
        """Get the provider capabilities."""
        pass
    
    @property
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available.
        
        Returns:
            True if the provider is available and properly configured, False otherwise
        """
        pass
    
    @abstractmethod
    def initialize(self, api_key: str, default_model: Optional[str] = None) -> bool:
        """
        Initialize the provider with API key and optional model.
        
        Args:
            api_key: The API key for the provider
            default_model: Optional default model to use
            
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """
        Query the AI provider.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional arguments for the provider
            
        Returns:
            The generated response as a string
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        pass
    
    @abstractmethod
    def stream_query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        """
        Stream a response from the AI provider.
        
        Args:
            prompt: The user prompt to send
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional arguments for the provider
            
        Yields:
            Chunks of the generated response as they become available
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        pass
    
    @abstractmethod
    def get_supported_models(self) -> List[str]:
        """
        Get a list of supported models.
        
        Returns:
            List of model identifiers
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the provider.
        
        Returns:
            Dict containing provider metadata
        """
        pass 