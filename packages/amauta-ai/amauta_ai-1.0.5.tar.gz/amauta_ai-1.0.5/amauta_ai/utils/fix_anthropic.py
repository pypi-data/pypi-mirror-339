"""Utility functions for working with the Anthropic client."""

import logging
import os
import re
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

# Current available models as of the latest check
AVAILABLE_MODELS = [
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
]


def get_available_models() -> List[str]:
    """
    Get a list of currently available Claude models.

    Returns:
        List of available model IDs
    """
    return AVAILABLE_MODELS


def get_best_available_model(client: Any = None) -> str:
    """
    Get the best available Claude model (most capable).

    Args:
        client: Optional Anthropic client to fetch live model information

    Returns:
        Model ID of the best available model
    """
    if client:
        try:
            models = client.models.list()
            if hasattr(models, "data") and len(models.data) > 0:
                # Update global models list
                global AVAILABLE_MODELS
                AVAILABLE_MODELS = [model.id for model in models.data]

                # Try to find a Claude-3-7 model first (newest generation)
                for model in models.data:
                    if "claude-3-7" in model.id:
                        return model.id

                # Fall back to Claude-3-5
                for model in models.data:
                    if "claude-3-5" in model.id:
                        return model.id

                # Last resort: return first available model
                return models.data[0].id
        except Exception as e:
            logger.warning(f"Error fetching models: {str(e)}")

    # If we can't get the models from the API, use our static list
    # Priorities: Claude 3.7 > Claude 3.5 > Claude Opus
    for model_prefix in ["claude-3-7", "claude-3-5", "claude-3-opus"]:
        for model in AVAILABLE_MODELS:
            if model.startswith(model_prefix):
                return model

    # Last resort: return first model in our list or a relatively safe fallback
    return AVAILABLE_MODELS[0] if AVAILABLE_MODELS else "claude-3-5-sonnet-20240620"


def create_anthropic_client(api_key: str) -> Optional[Any]:
    """
    Create an Anthropic client with the latest SDK.

    This function creates an Anthropic client using the latest SDK version.

    Args:
        api_key: The Anthropic API key to use

    Returns:
        An Anthropic client instance or None if creation fails
    """
    try:
        # Check if Anthropic module is available
        import anthropic
        import httpx
        import packaging.version

        logger.info(f"Using Anthropic version {anthropic.__version__}")

        # Clean up any environment variables that might interfere
        for env_var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
            if env_var in os.environ:
                logger.info(f"Removing {env_var} from environment for Anthropic client")
                del os.environ[env_var]

        # Get the anthropic version
        version = packaging.version.parse(anthropic.__version__)

        # In versions ≥ 0.49.0, the constructor may have changed
        if version >= packaging.version.parse("0.49.0"):
            logger.info("Using newer Anthropic client constructor (version >= 0.49.0)")
            client = anthropic.Anthropic(api_key=api_key)
        # In version 0.21.3 up to 0.49.0, even though 'proxies' shows up in constructor signature,
        # it actually causes a TypeError. Use http_client approach instead.
        else:
            logger.info("Using legacy Anthropic client constructor (version < 0.49.0)")
            http_client = httpx.Client()
            client = anthropic.Anthropic(api_key=api_key, http_client=http_client)

        logger.info("Successfully created Anthropic client")
        return client

    except Exception as e:
        logger.error(f"Failed to create Anthropic client: {str(e)}")
        return None


def extract_text_from_response(response: Any) -> str:
    """
    Extract text content from an Anthropic API response.

    Args:
        response: The response object from an Anthropic API call

    Returns:
        The extracted text content as a string
    """
    try:
        # Check for content list in modern response format
        if hasattr(response, "content") and isinstance(response.content, list):
            full_text = ""
            for content_block in response.content:
                if hasattr(content_block, "type") and content_block.type == "text":
                    if hasattr(content_block, "text"):
                        full_text += str(content_block.text)
            if full_text:
                return full_text

        # Try alternative approaches if we didn't find text content
        if hasattr(response, "content"):
            if isinstance(response.content, str):
                return response.content
            elif isinstance(response.content, list) and len(response.content) > 0:
                if (
                    isinstance(response.content[0], dict)
                    and "text" in response.content[0]
                ):
                    return str(response.content[0]["text"])
                elif isinstance(response.content[0], str):
                    return response.content[0]

        # Final fallback
        return str(response)

    except Exception as e:
        logger.warning(f"Error extracting text from response: {str(e)}")
        return str(response)


def extract_thinking_from_response(response: Any) -> str:
    """
    Extract thinking content from an Anthropic response object.

    This function handles different response formats that might occur.

    Args:
        response: The response object from Anthropic

    Returns:
        The extracted thinking content as a string
    """
    # Case 1: Try to extract from tool calls directly
    if hasattr(response, "tool_calls") and response.tool_calls:
        for call in response.tool_calls:
            if hasattr(call, "name") and call.name == "thinking":
                if (
                    hasattr(call, "input")
                    and isinstance(call.input, dict)
                    and "thinking" in call.input
                ):
                    return str(call.input["thinking"])
                elif hasattr(call, "input") and hasattr(call.input, "get"):
                    return str(call.input.get("thinking", ""))

    # Case 2: Response is a string containing the message structure
    if isinstance(response, str):
        # Try to extract thinking from the string representation using regex
        thinking_match = re.search(r"'thinking':\s*'([^']*)'", response)
        if thinking_match:
            return thinking_match.group(1).replace("\\n", "\n")

        # Try alternate format
        thinking_match = re.search(r'"thinking":\s*"([^"]*)"', response)
        if thinking_match:
            return thinking_match.group(1).replace("\\n", "\n")

    # Case 3: Response might have content that includes the thinking
    if hasattr(response, "content") and isinstance(response.content, list):
        for item in response.content:
            if hasattr(item, "type") and item.type == "tool_use":
                if (
                    hasattr(item, "input")
                    and isinstance(item.input, dict)
                    and "thinking" in item.input
                ):
                    return str(item.input["thinking"])

    # If we reach here, we couldn't extract the thinking
    return ""


def extract_answer_from_response(response: Any) -> str:
    """
    Extract the answer content from an Anthropic response object.

    Args:
        response: The response object from Anthropic

    Returns:
        The extracted answer as a string
    """
    # Case 1: Response has content with text type
    if hasattr(response, "content") and isinstance(response.content, list):
        for item in response.content:
            if hasattr(item, "type") and item.type == "text":
                if hasattr(item, "text"):
                    return item.text

    # Case 2: Response is a string
    if isinstance(response, str):
        # We have the thinking, so return a generic response
        return "I've analyzed this problem. Please see my thinking process for the solution."

    # Case 3: Response might have a content attribute that's a string
    if hasattr(response, "content") and isinstance(response.content, str):
        return response.content

    # If we reach here, return a generic message
    return "Analysis complete. See thinking process for details."
