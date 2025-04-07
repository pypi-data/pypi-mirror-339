"""
Exports for the AI module.

This module provides exports of AI services for use by other modules.
"""

from typing import Any, Dict, List, Optional, Set, Union

from amauta_ai.ai.providers.base_provider import AIProvider
from amauta_ai.ai.service import AiService
from amauta_ai.ai.provider_selection import ProviderSelectionService
from amauta_ai.config.models import ProviderCapability
from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)
from amauta_ai.config.service import ConfigService

__all__ = [
    "AiService",
    "ProviderSelectionService",
    "AIProvider",
    "ProviderCapability",
]

# Get the export manager instance
export_manager = ExportManager.get_instance()

# Register classes
export_class(AiService)
export_class(AIProvider)
export_class(ProviderSelectionService)

# Register methods from AiService as standalone functions
export_function(AiService.query)
export_function(AiService.query_with_tools)
export_function(AiService.query_task)

# Initialize services
config_service = ConfigService()
ai_service = AiService(config_service=config_service)

def query(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    provider_name: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    stream: bool = False,
    json_mode: bool = False,
    **kwargs: Any,
) -> Union[str, Any]:
    """
    Query an AI provider with the given prompt.

    Args:
        prompt: The prompt to send to the AI
        system_prompt: Optional system prompt to guide the AI
        model: Optional specific model to use
        provider_name: Optional preferred provider name
        history: Optional conversation history
        max_tokens: Maximum tokens to generate
        temperature: Temperature for response generation (0.0-1.0)
        stream: Whether to stream the response
        json_mode: Whether to request a JSON response
        **kwargs: Additional arguments to pass to the provider

    Returns:
        The AI's response as a string or a generator if streaming
    """
    return ai_service.query(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        provider_name=provider_name,
        history=history,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
        json_mode=json_mode,
        **kwargs,
    )

def query_with_tools(
    prompt: str,
    tools: List[Dict[str, Any]],
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    provider_name: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Query an AI provider with tools.

    Args:
        prompt: The prompt to send to the AI
        tools: List of tool definitions
        system_prompt: Optional system prompt to guide the AI
        model: Optional specific model to use
        provider_name: Optional preferred provider name
        history: Optional conversation history
        max_tokens: Maximum tokens to generate
        temperature: Temperature for response generation (0.0-1.0)
        **kwargs: Additional arguments to pass to the provider

    Returns:
        Dictionary containing the response text and any tool calls
    """
    return ai_service.query_with_tools(
        prompt=prompt,
        tools=tools,
        system_prompt=system_prompt,
        model=model,
        provider_name=provider_name,
        history=history,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )

def query_task(
    prompt: str,
    task_type: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    provider_name: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Perform a task-specific AI operation.

    Args:
        prompt: The prompt describing the task
        task_type: Type of task operation (create, update, expand, etc.)
        system_prompt: Optional system prompt to guide the AI
        model: Optional specific model to use
        provider_name: Optional preferred provider name
        max_tokens: Maximum tokens to generate
        temperature: Temperature for response generation (0.0-1.0)
        **kwargs: Additional arguments to pass to the provider

    Returns:
        Dictionary containing the task operation results
    """
    return ai_service.query_task(
        prompt=prompt,
        task_type=task_type,
        system_prompt=system_prompt,
        model=model,
        provider_name=provider_name,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )
