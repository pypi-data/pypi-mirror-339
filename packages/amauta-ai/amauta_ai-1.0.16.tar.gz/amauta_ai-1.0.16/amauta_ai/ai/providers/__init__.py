"""
AI providers for AMAUTA.

This module provides implementations for various AI providers.
"""

import logging
from typing import Dict, List, Type

from amauta_ai.ai.providers.base_provider import AIProvider

# Configure logging
logger = logging.getLogger(__name__)

# Import provider implementations
try:
    from amauta_ai.ai.providers.anthropic_provider import AnthropicProvider
    ANTHROPIC_AVAILABLE = True
except ImportError:
    logger.warning("Anthropic provider unavailable. Please install the required dependencies.")
    ANTHROPIC_AVAILABLE = False

try:
    from amauta_ai.ai.providers.perplexity_provider import PerplexityProvider
    PERPLEXITY_AVAILABLE = True
except ImportError:
    logger.warning("Perplexity provider unavailable. Please install the required dependencies.")
    PERPLEXITY_AVAILABLE = False

# Provider registry
PROVIDER_REGISTRY: Dict[str, Type[AIProvider]] = {}

# Register providers if available
if ANTHROPIC_AVAILABLE:
    PROVIDER_REGISTRY["anthropic"] = AnthropicProvider

if PERPLEXITY_AVAILABLE:
    PROVIDER_REGISTRY["perplexipy"] = PerplexityProvider

def get_provider_names() -> List[str]:
    """Get a list of available provider names."""
    return list(PROVIDER_REGISTRY.keys())

def get_provider_class(provider_name: str) -> Type[AIProvider]:
    """Get a provider class by name."""
    if provider_name not in PROVIDER_REGISTRY:
        raise ValueError(f"Provider {provider_name} not found. Available providers: {', '.join(get_provider_names())}")
    return PROVIDER_REGISTRY[provider_name]

def create_provider(provider_name: str) -> AIProvider:
    """Create a provider instance by name."""
    provider_class = get_provider_class(provider_name)
    return provider_class() 