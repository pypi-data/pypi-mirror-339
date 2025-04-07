"""
Provider selection service for AMAUTA.

This module provides the core functionality for selecting the appropriate AI provider
based on task requirements, mode, availability, and user flags.
"""

from enum import Enum
from typing import Optional, Set, Dict, List, Any, Type, Tuple
from functools import lru_cache
import time

from amauta_ai.config.service import ConfigService
from amauta_ai.utils.logger import get_logger
from amauta_ai.config.models import ProviderCapability, AiProviderConfig, ModelMetadata
from amauta_ai.ai.providers import create_provider, get_provider_names, AIProvider

logger = get_logger(__name__)


class ProviderMode(str, Enum):
    """Provider modes for different types of operations."""
    GENERAL = "general"  # Default mode for general operations
    RESEARCH = "research"  # Research mode for operations requiring extensive knowledge
    CODE = "code"  # Code-focused operations
    ANALYSIS = "analysis"  # Analysis operations
    TASK = "task"  # Task management operations


class ProviderSelectionError(Exception):
    """Base exception for provider selection errors."""
    pass


class NoSuitableProviderError(ProviderSelectionError):
    """Exception raised when no suitable provider is found."""
    pass


class ProviderNotAvailableError(ProviderSelectionError):
    """Exception raised when a specific provider is not available."""
    pass


class ProviderCapabilityError(ProviderSelectionError):
    """Exception raised when a provider doesn't support required capabilities."""
    pass


class ProviderSelectionService:
    """Service for selecting the appropriate AI provider."""
    
    def __init__(self, config_service: ConfigService) -> None:
        """Initialize the provider selection service."""
        self.config_service = config_service
        self._availability_cache: Dict[str, tuple[bool, float]] = {}
        self._provider_instances: Dict[str, AIProvider] = {}
        self._cache_ttl = 300  # 5 minutes cache TTL
        
        # Get provider capabilities from the provider instances
        self.provider_capabilities: Dict[str, Set[ProviderCapability]] = {}
        self._initialize_provider_capabilities()
        
        logger.info("Provider Selection Service initialized")
        self._log_provider_capabilities()

    def _initialize_provider_capabilities(self) -> None:
        """Initialize provider capabilities from provider instances."""
        for provider_name in get_provider_names():
            try:
                provider = self._get_provider_instance(provider_name)
                if provider:
                    self.provider_capabilities[provider_name] = provider.capabilities
            except Exception as e:
                logger.warning(f"Failed to initialize provider {provider_name}: {str(e)}")

    def _get_provider_instance(self, provider_name: str) -> Optional[AIProvider]:
        """Get or create a provider instance."""
        if provider_name in self._provider_instances:
            return self._provider_instances[provider_name]
        
        try:
            provider = create_provider(provider_name)
            self._provider_instances[provider_name] = provider
            return provider
        except Exception as e:
            logger.warning(f"Failed to create provider instance for {provider_name}: {str(e)}")
            return None

    def _log_provider_capabilities(self) -> None:
        """Log the capabilities of each provider."""
        for provider, capabilities in self.provider_capabilities.items():
            logger.debug(f"Provider {provider} capabilities: {', '.join(str(c) for c in capabilities)}")

    def select_provider(
        self,
        mode: ProviderMode,
        research: bool = False,
        provider: Optional[str] = None,
        required_capabilities: Optional[Set[ProviderCapability]] = None,
    ) -> str:
        """
        Select the most appropriate AI provider.
        
        Args:
            mode: The operation mode
            research: Whether this is a research query
            provider: Optional explicit provider selection
            required_capabilities: Set of required provider capabilities
            
        Returns:
            The selected provider name
            
        Raises:
            ProviderSelectionError: If no suitable provider is found or other selection errors
        """
        logger.debug(f"Selecting provider for mode={mode}, research={research}, explicit_provider={provider}")
        
        try:
            # Initialize required capabilities if not provided
            if required_capabilities is None:
                required_capabilities = set()
            
            # 1. Check explicit provider override
            if provider:
                logger.debug(f"Checking explicitly selected provider: {provider}")
                if self._is_provider_available(provider):
                    if required_capabilities and not self._has_capabilities(provider, required_capabilities):
                        raise ProviderCapabilityError(
                            f"Provider {provider} does not support required capabilities: "
                            f"{', '.join(str(c) for c in required_capabilities)}"
                        )
                    logger.info(f"Using explicitly selected provider: {provider}")
                    return provider
                raise ProviderNotAvailableError(f"Explicitly selected provider {provider} is not available")

            # 2. Add RESEARCH capability if research mode
            if research:
                required_capabilities.add(ProviderCapability.RESEARCH)
                logger.debug("Added RESEARCH capability requirement")
                
                # Get additional research capabilities from config
                research_config = self.config_service.get_research_mode_config()
                for capability in research_config.required_capabilities:
                    if capability not in required_capabilities:
                        required_capabilities.add(capability)
                        logger.debug(f"Added required capability from research config: {capability}")
                
                # Use research-specific provider preferences instead of just changing the mode
                preferred_providers = research_config.preferred_providers
                logger.debug(f"Using research mode preferred providers: {preferred_providers}")
            else:
                # 3. Get preferred providers for the mode
                preferred_providers = self._get_preferred_providers(mode)
                logger.debug(f"Preferred providers for mode {mode}: {preferred_providers}")

            # 4. Filter by required capabilities
            if required_capabilities:
                preferred_providers = [
                    p for p in preferred_providers
                    if self._has_capabilities(p, required_capabilities)
                ]
                logger.debug(f"Providers with required capabilities: {preferred_providers}")
                
                # If no providers have the required capabilities, raise error
                if not preferred_providers:
                    raise NoSuitableProviderError(
                        f"No provider found with required capabilities: "
                        f"{', '.join(str(c) for c in required_capabilities)}"
                    )

            # 5. Filter by availability
            available_providers = [
                p for p in preferred_providers
                if self._is_provider_available(p)
            ]
            logger.debug(f"Available providers: {available_providers}")

            # 6. Return first available provider or raise error
            if not available_providers:
                # Try to find any available provider as fallback
                all_providers = get_provider_names()
                available_fallbacks = [p for p in all_providers if self._is_provider_available(p)]
                
                if available_fallbacks:
                    fallback = available_fallbacks[0]
                    logger.warning(
                        f"No preferred provider available for mode {mode}. "
                        f"Using fallback provider: {fallback}"
                    )
                    return fallback
                
                raise NoSuitableProviderError(
                    "No suitable provider found. Check API keys and provider availability."
                )
            
            selected = available_providers[0]
            if research:
                logger.info(f"Selected provider: {selected} (using research mode preferences)")
            else:
                logger.info(f"Selected provider: {selected}")
            return selected

        except ProviderSelectionError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during provider selection: {str(e)}")
            raise ProviderSelectionError(f"Provider selection failed: {str(e)}")

    def _get_preferred_providers(self, mode: ProviderMode) -> List[str]:
        """Get the preferred providers for a given mode."""
        config = self.config_service.get_config()
        preferences = config.provider_preferences

        # Get preferences based on mode
        if mode == ProviderMode.GENERAL:
            return preferences.general
        elif mode == ProviderMode.RESEARCH:
            return preferences.research
        elif mode == ProviderMode.CODE:
            return preferences.code
        elif mode == ProviderMode.ANALYSIS:
            return preferences.analysis
        elif mode == ProviderMode.TASK:
            return preferences.task
        
        # Default to general preferences
        logger.warning(f"Unknown mode {mode}, using general preferences")
        return preferences.general

    def _has_capabilities(
        self,
        provider: str,
        capabilities: Set[ProviderCapability],
    ) -> bool:
        """Check if a provider has all required capabilities."""
        if provider not in self.provider_capabilities:
            logger.warning(f"Unknown provider {provider}")
            return False
        
        provider_caps = self.provider_capabilities[provider]
        has_caps = all(cap in provider_caps for cap in capabilities)
        if not has_caps:
            missing = [str(c) for c in capabilities if c not in provider_caps]
            logger.debug(f"Provider {provider} missing capabilities: {', '.join(missing)}")
        return has_caps

    def _is_provider_available(self, provider: str) -> bool:
        """
        Check if a provider is available for use.
        
        This method caches results for a short period to avoid repeated API key checks.
        """
        # Check cache first
        now = time.time()
        if provider in self._availability_cache:
            available, timestamp = self._availability_cache[provider]
            if now - timestamp < self._cache_ttl:
                return available

        # Check if provider is supported
        if provider not in self.provider_capabilities:
            logger.warning(f"Unsupported provider: {provider}")
            self._availability_cache[provider] = (False, now)
            return False
            
        # Check if API key is configured
        api_key = self.config_service.get_api_key(provider)
        if not api_key:
            logger.warning(f"Provider {provider} not available: API key not found")
            self._availability_cache[provider] = (False, now)
            return False

        # Check if provider initialization works
        provider_instance = self._get_provider_instance(provider)
        if not provider_instance:
            logger.warning(f"Provider {provider} not available: could not create instance")
            self._availability_cache[provider] = (False, now)
            return False
            
        # Get provider config
        provider_config = self._get_provider_config(provider)
        default_model = provider_config.default_model if provider_config else None
            
        # Try to initialize the provider
        try:
            available = provider_instance.initialize(api_key, default_model)
            self._availability_cache[provider] = (available, now)
            if not available:
                logger.warning(f"Provider {provider} initialization failed")
            return available
        except Exception as e:
            logger.warning(f"Provider {provider} initialization error: {e}")
            self._availability_cache[provider] = (False, now)
            return False

    def _get_provider_config(self, provider: str) -> Optional[AiProviderConfig]:
        """Get the provider configuration."""
        config = self.config_service.get_config()
        return config.ai.get(provider)

    def validate_provider_config(self, provider: str) -> List[str]:
        """
        Validate the configuration for a specific provider.
        
        Args:
            provider: The provider name to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check if provider is supported
        if provider not in get_provider_names():
            errors.append(f"Provider {provider} is not supported")
            return errors
            
        # Check if provider has config
        provider_config = self._get_provider_config(provider)
        if not provider_config:
            errors.append(f"Provider {provider} has no configuration in .amautarc.yaml")
            return errors
            
        # Check if API key is set
        api_key = self.config_service.get_api_key(provider)
        if not api_key:
            env_var = provider_config.api_key_env_var
            errors.append(f"API key for {provider} not found. Set the {env_var} environment variable.")
            
        # Check if default model is set
        if not provider_config.default_model:
            errors.append(f"Default model for {provider} is not specified in configuration")
            
        return errors

    def get_provider_info(self, provider: str) -> Dict[str, Any]:
        """
        Get information about a provider.
        
        Args:
            provider: The provider name
            
        Returns:
            Dict containing provider information
        """
        provider_config = self._get_provider_config(provider)
        if not provider_config:
            return {
                "name": provider,
                "available": False,
                "reason": "No configuration found",
            }
            
        available = self._is_provider_available(provider)
        api_key_set = self.config_service.get_api_key(provider) is not None
        
        provider_instance = self._get_provider_instance(provider) if available else None
        capabilities = list(self.provider_capabilities.get(provider, set()))
        
        return {
            "name": provider,
            "available": available,
            "configured": provider_config is not None,
            "api_key_set": api_key_set,
            "default_model": provider_config.default_model if provider_config else None,
            "capabilities": capabilities,
            "metadata": provider_instance.get_metadata() if provider_instance else {},
        }

    def get_available_providers(self) -> List[str]:
        """
        Get a list of available providers.
        
        Returns:
            List of available provider names
        """
        available = []
        for provider in get_provider_names():
            if self._is_provider_available(provider):
                available.append(provider)
        return available

    def clear_cache(self) -> None:
        """Clear the availability cache."""
        self._availability_cache.clear()
        logger.debug("Provider availability cache cleared")
        
    def get_provider_for_operation(
        self,
        operation_type: str,
        research: bool = False,
        provider: Optional[str] = None,
        required_capabilities: Optional[Set[ProviderCapability]] = None,
    ) -> str:
        """
        Get the appropriate provider for a specific operation type.
        
        Args:
            operation_type: The type of operation (maps to ProviderMode)
            research: Whether this is a research operation
            provider: Optional explicit provider override
            required_capabilities: Optional set of required capabilities
            
        Returns:
            The selected provider name
            
        Raises:
            ProviderSelectionError: If no suitable provider is found
        """
        try:
            # Map operation type to provider mode
            mode = ProviderMode(operation_type)
        except ValueError:
            logger.warning(f"Unknown operation type: {operation_type}, using GENERAL mode")
            mode = ProviderMode.GENERAL
            
        return self.select_provider(
            mode=mode,
            research=research,
            provider=provider,
            required_capabilities=required_capabilities,
        ) 

    def select_model(
        self, 
        provider: str, 
        mode: ProviderMode, 
        research: bool = False,
        context_size: Optional[int] = None
    ) -> str:
        """
        Select the most appropriate model for a provider based on mode and requirements.
        
        Args:
            provider: The provider name
            mode: The operation mode
            research: Whether research mode is enabled
            context_size: Optional required context window size
            
        Returns:
            The selected model name
        """
        # Convert the mode to a string for lookup
        operation_type = mode.value
        
        # If research mode is enabled, prioritize research operation type
        if research:
            operation_type = "research"
        
        # Get recommended model based on operation type
        recommended = self.config_service.get_recommended_model(provider, operation_type)
        
        # If we don't have a context size requirement, return the recommended model
        if context_size is None or recommended is None:
            # Fall back to default model if no recommendation
            if recommended is None:
                provider_config = self.config_service.get_provider_config(provider)
                if provider_config:
                    return provider_config.default_model
            return recommended
        
        # If we have a context size requirement, find models that can handle it
        provider_config = self.config_service.get_provider_config(provider)
        if not provider_config or not provider_config.models:
            return recommended  # Fall back to recommendation
        
        # Filter models by context window size
        viable_models = []
        for model_name, metadata in provider_config.models.items():
            if metadata.context_window >= context_size:
                # Score models based on operation type match and context window efficiency
                score = 0
                if operation_type in metadata.recommended_for:
                    score += 100  # High priority for operation type match
                
                # Penalize oversized models slightly to prefer right-sized models
                # (we don't want to use a 200K token model for a 10K token task if a 32K model exists)
                efficiency = 1.0 - (metadata.context_window - context_size) / metadata.context_window
                score += efficiency * 50
                
                viable_models.append((model_name, metadata, score))
        
        if not viable_models:
            return recommended  # Fall back to recommendation
        
        # Sort by score (highest first)
        viable_models.sort(key=lambda x: x[2], reverse=True)
        return viable_models[0][0]

    def get_provider_model_for_operation(
        self,
        operation_type: str,
        research: bool = False,
        provider: Optional[str] = None,
        required_capabilities: Optional[Set[ProviderCapability]] = None,
        context_size: Optional[int] = None,
    ) -> Tuple[str, str]:
        """
        Get the appropriate provider and model for a specific operation.
        
        Args:
            operation_type: The operation type
            research: Whether research mode is enabled
            provider: Optional provider override
            required_capabilities: Optional required capabilities
            context_size: Optional required context window size
            
        Returns:
            Tuple of (provider_name, model_name)
            
        Raises:
            ProviderSelectionError: If no suitable provider is found
        """
        # First select the provider
        selected_provider = self.get_provider_for_operation(
            operation_type=operation_type,
            research=research,
            provider=provider,
            required_capabilities=required_capabilities,
        )
        
        # Now select the appropriate model
        try:
            # Map operation type to provider mode
            mode = ProviderMode(operation_type)
        except ValueError:
            logger.warning(f"Unknown operation type: {operation_type}, using GENERAL mode")
            mode = ProviderMode.GENERAL
            
        selected_model = self.select_model(
            provider=selected_provider,
            mode=mode,
            research=research,
            context_size=context_size
        )
        
        logger.info(f"Selected provider {selected_provider} with model {selected_model} for {operation_type} operation")
        return selected_provider, selected_model 