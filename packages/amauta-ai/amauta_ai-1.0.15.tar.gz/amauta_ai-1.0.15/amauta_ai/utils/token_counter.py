"""
Token counting utilities for AI APIs.

This module provides functions to estimate token counts for different AI providers.
"""

import logging
import re
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

# Check if tiktoken is available for accurate OpenAI token counting
try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning(
        "tiktoken not available. Using approximate token counting for OpenAI."
    )


def count_openai_tokens(
    messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo"
) -> int:
    """
    Count tokens for OpenAI chat API messages.

    Args:
        messages: A list of message dictionaries with 'role' and 'content' keys
        model: The model name to count tokens for

    Returns:
        Estimated token count
    """
    if TIKTOKEN_AVAILABLE:
        return count_openai_tokens_with_tiktoken(messages, model)
    else:
        return count_tokens_approximate(messages)


def count_openai_tokens_with_tiktoken(
    messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo"
) -> int:
    """
    Count tokens for OpenAI chat API messages using tiktoken for accuracy.

    Args:
        messages: A list of message dictionaries with 'role' and 'content' keys
        model: The model name to count tokens for

    Returns:
        Accurate token count
    """
    try:
        # Model selection logic
        encoding_name = "cl100k_base"  # Default for chat models

        # Get the encoding based on the model name
        encoding = tiktoken.get_encoding(encoding_name)

        # Following the OpenAI counting approach as described in their documentation
        num_tokens = 0

        # Every message follows <im_start>{role/name}\n{content}<im_end>\n
        tokens_per_message = 4

        # If a name is present, the role is omitted
        tokens_per_name = -1  # Role is 1 token, so having a name saves 1 token

        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(str(value)))
                if key == "name":
                    num_tokens += tokens_per_name

        # Every reply is primed with <im_start>assistant
        num_tokens += 2

        return num_tokens

    except Exception as e:
        logger.warning(f"Error using tiktoken for token counting: {str(e)}")
        # Fall back to approximate counting
        return count_tokens_approximate(messages)


def count_tokens_approximate(messages: List[Dict[str, str]]) -> int:
    """
    Approximate token counting based on word count.

    Args:
        messages: A list of message dictionaries with 'role' and 'content' keys

    Returns:
        Estimated token count
    """
    token_count = 0

    for message in messages:
        # Count approximately 4 tokens for message overhead
        token_count += 4

        content = message.get("content", "")
        # Approximate: Tokens tend to be ~4 characters on average in English
        token_count += len(content) // 4

        # Add tokens for spaces and punctuation
        token_count += len(re.findall(r"\s+", content))
        token_count += len(re.findall(r'[,.;:!?()[\]{}"\'-]', content))

    # Add a small overhead
    token_count += 3

    return token_count


def count_anthropic_tokens(prompt: str, system_prompt: str = "") -> int:
    """
    Estimate token count for Anthropic Claude models.

    Args:
        prompt: The user prompt
        system_prompt: The system prompt

    Returns:
        Estimated token count
    """
    try:
        import anthropic

        if hasattr(anthropic, "Anthropic") and hasattr(
            anthropic.Anthropic, "count_tokens"
        ):
            # Use the official token counter if available
            client = anthropic.Anthropic()
            return client.count_tokens(system_prompt + "\n\n" + prompt)
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not use Anthropic token counter: {str(e)}")

    # Fall back to approximate counting
    return count_tokens_approximate(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    )


def trim_messages_to_token_limit(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 4096,
    response_tokens: int = 1000,
) -> Tuple[List[Dict[str, str]], int]:
    """
    Trim messages to fit within token limit.

    Args:
        messages: A list of message dictionaries with 'role' and 'content' keys
        model: The model name to count tokens for
        max_tokens: Maximum token limit for the model
        response_tokens: Reserve this many tokens for the response

    Returns:
        Tuple of (trimmed messages, estimated token count)
    """
    # Calculate available tokens
    available_tokens = max_tokens - response_tokens

    # Count tokens in current messages
    current_tokens = count_openai_tokens(messages, model)

    # If we're already under limit, return as is
    if current_tokens <= available_tokens:
        return messages, current_tokens

    # Need to trim messages
    logger.warning(
        f"Messages exceed token limit ({current_tokens} > {available_tokens}). Trimming..."
    )

    # Always keep system and most recent user message
    system_messages = [m for m in messages if m.get("role") == "system"]
    latest_user_message = next(
        (m for m in reversed(messages) if m.get("role") == "user"), None
    )

    # Calculate tokens for these essential messages
    essential_messages = system_messages + (
        [latest_user_message] if latest_user_message else []
    )
    essential_tokens = count_openai_tokens(essential_messages, model)

    # If essential messages exceed limit, we need to trim content
    if essential_tokens > available_tokens:
        logger.warning(
            "Even essential messages exceed token limit. Trimming content..."
        )

        # Start with system messages at full length
        trimmed_messages = system_messages.copy()
        remaining_tokens = available_tokens - count_openai_tokens(
            trimmed_messages, model
        )

        # Trim the user message if we have one and need to
        if latest_user_message and remaining_tokens > 0:
            user_content = latest_user_message["content"]
            # Simple approach: keep as many characters as possible (approximate)
            chars_to_keep = int(remaining_tokens * 3.5)  # Approximate chars per token
            if chars_to_keep < len(user_content):
                logger.warning(
                    f"Trimming user message from {len(user_content)} to ~{chars_to_keep} chars"
                )
                # Keep start of message rather than end, as instructions often at beginning
                trimmed_user_content = user_content[:chars_to_keep] + "..."
                trimmed_messages.append(
                    {"role": "user", "content": trimmed_user_content}
                )
            else:
                trimmed_messages.append(latest_user_message)

        resulting_tokens = count_openai_tokens(trimmed_messages, model)
        return trimmed_messages, resulting_tokens

    # Otherwise, include as many earlier messages as will fit
    trimmed_messages = []
    remaining_tokens = available_tokens

    # Add system messages first
    for message in system_messages:
        trimmed_messages.append(message)
        remaining_tokens -= count_openai_tokens([message], model)

    # Then add messages from most recent to oldest, excluding system messages
    non_system_messages = [m for m in messages if m.get("role") != "system"]
    non_system_messages.reverse()  # Most recent first

    for message in non_system_messages:
        message_tokens = count_openai_tokens([message], model)
        if message_tokens <= remaining_tokens:
            trimmed_messages.append(message)
            remaining_tokens -= message_tokens
        else:
            # We can't fit this message, break
            break

    # Re-sort messages to original order
    trimmed_messages.sort(key=lambda m: messages.index(m))

    resulting_tokens = count_openai_tokens(trimmed_messages, model)
    return trimmed_messages, resulting_tokens


def estimate_max_tokens_for_prompt(prompt_tokens: int, model: str) -> int:
    """
    Estimate the maximum output tokens available for a given prompt size and model.

    Args:
        prompt_tokens: Number of tokens in the prompt
        model: The model name

    Returns:
        Maximum available output tokens
    """
    # Model token limits
    model_limits = {
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-4-turbo": 128000,
        "claude-2": 100000,
        "claude-instant-1": 100000,
        "claude-3-sonnet-20240229": 200000,
        "claude-3-opus-20240229": 200000,
        "claude-3-haiku-20240307": 200000,
    }

    # Get the model's token limit
    limit = model_limits.get(model, 4096)  # Default to 4096 if model not recognized

    # Leave some buffer for response formatting
    buffer = 50

    # Calculate available tokens
    available = limit - prompt_tokens - buffer

    # Ensure we don't return a negative number
    return max(0, available)
