"""
Anthropic provider for AMAUTA.

This module provides the implementation for the Anthropic Claude AI provider.
"""

import logging
import pkg_resources
import json
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union, Callable

from amauta_ai.ai.providers.base_provider import AIProvider
from amauta_ai.config.models import ProviderCapability

# Configure logging
logger = logging.getLogger(__name__)

class AnthropicProvider(AIProvider):
    """Anthropic provider implementation."""
    
    def __init__(self) -> None:
        """Initialize the Anthropic provider."""
        super().__init__()
        self._client = None
        self._api_key = None
        self._available = False
        self._model = "claude-3-5-sonnet-latest"
        self._api_version = None
        
        # Check if Anthropic is available
        try:
            from anthropic import Anthropic
            self._detect_api_version()
            self._available = True
        except ImportError:
            logger.warning("Anthropic package not available. Install with: pip install anthropic>=0.49.0")
            self._available = False
    
    def _detect_api_version(self) -> None:
        """Detect the version of the Anthropic package."""
        try:
            version = pkg_resources.get_distribution("anthropic").version
            self._api_version = version
            logger.info(f"Detected Anthropic API version: {version}")
        except Exception as e:
            logger.warning(f"Unable to detect Anthropic API version: {str(e)}")
            self._api_version = "unknown"
    
    @property
    def name(self) -> str:
        """Get the provider name."""
        return "anthropic"
    
    @property
    def capabilities(self) -> Set[ProviderCapability]:
        """Get the provider capabilities."""
        return {
            ProviderCapability.GENERAL,
            ProviderCapability.RESEARCH,
            ProviderCapability.CODE,
            ProviderCapability.TASK,
            ProviderCapability.ANALYSIS,
            ProviderCapability.STREAMING,
            ProviderCapability.TOOL_CALLS,
            ProviderCapability.FUNCTION_CALLING,
            ProviderCapability.LONG_CONTEXT,
        }
    
    @property
    def is_available(self) -> bool:
        """Check if the provider is available."""
        return self._available and self._client is not None
    
    def initialize(self, api_key: str, default_model: Optional[str] = None) -> bool:
        """Initialize the provider with API key and optional model."""
        if not self._available:
            logger.warning("Cannot initialize Anthropic: package not available")
            return False
            
        # Validate API key before attempting to initialize
        if not api_key or not isinstance(api_key, str) or len(api_key) < 8:
            logger.error("Invalid Anthropic API key provided: API key is missing or invalid")
            return False
            
        try:
            from anthropic import Anthropic, APIError, APIConnectionError
            import time

            # Store only a reference to the API key, but not the key itself
            # This helps avoid API key logging in tracebacks or memory dumps
            self._api_key = "[API KEY SET]"
            
            # Implement retry mechanism for initial connection
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(1, max_retries + 1):
                try:
                    self._client = Anthropic(api_key=api_key)
                    
                    # Set the model if provided
                    if default_model:
                        self._model = default_model
                        
                    # Log successful initialization with sanitized info
                    logger.info(f"Initialized Anthropic provider with model: {self._model}")
                    return True
                    
                except APIConnectionError as e:
                    # Retry on connection errors
                    if attempt < max_retries:
                        logger.warning(f"Connection error initializing Anthropic (attempt {attempt}/{max_retries}): {str(e)}")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5  # Exponential backoff
                    else:
                        logger.error(f"Failed to connect to Anthropic after {max_retries} attempts: {str(e)}")
                        return False
                        
                except APIError as e:
                    # Don't retry on API errors (like authentication failures)
                    error_code = getattr(e, "status_code", None)
                    if error_code == 401:
                        logger.error("Authentication failed: Invalid Anthropic API key")
                    else:
                        logger.error(f"Anthropic API error (code: {error_code}): {str(e)}")
                    return False
                    
        except Exception as e:
            # Do not include the API key in error messages
            logger.error(f"Failed to initialize Anthropic provider: {str(e)}")
            return False
    
    def _extract_text_from_content(self, content: Any) -> str:
        """Extract text from Anthropic content blocks.
        
        Args:
            content: The content from Anthropic response, which can be in various formats
            
        Returns:
            Extracted text as a string
        """
        if not content:
            return ""
            
        # Handle string content directly
        if isinstance(content, str):
            return content
            
        # Handle list of content blocks
        if isinstance(content, list):
            text_parts = []
            for block in content:
                # Handle dict-style content blocks
                if isinstance(block, dict):
                    if block.get("type") == "text" and "text" in block:
                        text_parts.append(block["text"])
                    elif "text" in block:
                        text_parts.append(block["text"])
                # Handle object-style content blocks
                elif hasattr(block, "type") and block.type == "text" and hasattr(block, "text"):
                    text_parts.append(block.text)
                elif hasattr(block, "text"):
                    text_parts.append(block.text)
                # Handle simple string blocks
                elif isinstance(block, str):
                    text_parts.append(block)
            return "".join(text_parts)
        
        # Handle object with content attribute
        if hasattr(content, "text"):
            return content.text
            
        # Last resort: convert to string
        try:
            return str(content)
        except:
            return ""
    
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """
        Query the Anthropic API.
        
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
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        try:
            # Check if messages are provided in kwargs
            if "messages" in kwargs:
                messages = kwargs.pop("messages")
            else:
                # Create a simple message
                messages = [{"role": "user", "content": prompt}]
                
            # Create API call arguments
            api_kwargs = {
                "model": self._model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                **kwargs,
            }
            
            # Only include system parameter if provided
            if system_prompt:
                api_kwargs["system"] = system_prompt
            
            # Make the API call
            response = self._client.messages.create(**api_kwargs)
            
            # Extract and return text
            if hasattr(response, 'content') and isinstance(response.content, list) and len(response.content) > 0:
                return self._extract_text_from_content(response.content)
            
            return ""
            
        except Exception as e:
            logger.error(f"Error querying Anthropic: {str(e)}")
            raise RuntimeError(f"Anthropic query failed: {str(e)}")
    
    def stream_query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        """
        Query the Anthropic API with streaming.
        
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
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        try:
            # Check if messages are provided in kwargs
            if "messages" in kwargs:
                messages = kwargs.pop("messages")
            else:
                # Create a simple message
                messages = [{"role": "user", "content": prompt}]
            
            # Create API call arguments
            api_kwargs = {
                "model": self._model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                **kwargs,
            }
            
            # Only include system parameter if provided
            if system_prompt:
                api_kwargs["system"] = system_prompt
                
            # Make the streaming API call
            with self._client.messages.stream(**api_kwargs) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Error streaming from Anthropic: {str(e)}")
            raise RuntimeError(f"Anthropic streaming query failed: {str(e)}")
    
    def query_with_conversation(
        self,
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """
        Query Anthropic with a conversation history.
        
        Args:
            messages: List of message dictionaries in the format 
                     [{"role": "user"|"assistant"|"system", "content": str}, ...]
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional arguments for the provider
            
        Returns:
            The generated response as a string
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        try:
            # Convert messages to Anthropic format if needed
            anthropic_messages = self._format_messages_for_anthropic(messages)
            
            # Ensure system is properly passed (system parameter should be a string, not a list)
            system = None
            if system_prompt:
                if isinstance(system_prompt, list):
                    # Convert list of strings to single string
                    if all(isinstance(item, str) for item in system_prompt):
                        system = "\n".join(system_prompt)
                    else:
                        # Convert any non-string items to string
                        system = "\n".join(str(item) for item in system_prompt)
                elif isinstance(system_prompt, dict):
                    # Convert dict to JSON string
                    import json
                    system = json.dumps(system_prompt)
                else:
                    # Ensure it's a string
                    system = str(system_prompt)
            
            # Make the API call
            response = self._client.messages.create(
                model=self._model,
                messages=anthropic_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                **kwargs,
            )
            
            # Return the content
            if hasattr(response, "content") and response.content:
                result = ""
                for block in response.content:
                    if hasattr(block, "type") and block.type == "text" and hasattr(block, "text"):
                        result += block.text
                    elif hasattr(block, "text"):
                        result += block.text
                    elif isinstance(block, dict) and block.get("type") == "text" and "text" in block:
                        result += block["text"]
                return result
            return ""
        except Exception as e:
            logger.error(f"Error querying Anthropic with conversation: {str(e)}")
            raise RuntimeError(f"Anthropic conversation query failed: {str(e)}")
    
    def stream_with_conversation(
        self,
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        """
        Stream a response from Anthropic with a conversation history.
        
        Args:
            messages: List of message dictionaries in the format 
                     [{"role": "user"|"assistant"|"system", "content": str}, ...]
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional arguments for the provider
            
        Yields:
            Chunks of the generated response as they become available
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        try:
            # Convert messages to Anthropic format if needed
            anthropic_messages = self._format_messages_for_anthropic(messages)
            
            # Ensure system is properly passed (system parameter should be a string, not a list)
            system = None
            if system_prompt:
                if isinstance(system_prompt, list):
                    # Convert list of strings to single string
                    if all(isinstance(item, str) for item in system_prompt):
                        system = "\n".join(system_prompt)
                    else:
                        # Convert any non-string items to string
                        system = "\n".join(str(item) for item in system_prompt)
                elif isinstance(system_prompt, dict):
                    # Convert dict to JSON string
                    import json
                    system = json.dumps(system_prompt)
                else:
                    # Ensure it's a string
                    system = str(system_prompt)
                
            # Make the streaming API call
            with self._client.messages.stream(
                model=self._model,
                messages=anthropic_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                **kwargs,
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Error streaming from Anthropic with conversation: {str(e)}")
            raise RuntimeError(f"Anthropic streaming conversation query failed: {str(e)}")
    
    def _format_messages_for_anthropic(
        self, 
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]]
    ) -> List[Dict[str, Any]]:
        """
        Format messages for the Anthropic API.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Properly formatted messages for Anthropic
        """
        result = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            # Convert string content to content blocks if needed (for assistant messages)
            if role == "assistant" and isinstance(content, str):
                content = [{"type": "text", "text": content}]
                
            # Skip system messages (handled separately)
            if role == "system":
                continue
                
            # Add the message
            result.append({
                "role": role,
                "content": content,
            })
            
        return result
    
    def query_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        tool_handler: Optional[Callable[[Dict[str, Any]], str]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Query the Anthropic API with tool support.
        
        Args:
            prompt: The user prompt to send
            tools: List of tool definitions in the Anthropic format
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            tool_handler: Optional callback function to handle tool calls
            **kwargs: Additional arguments for the provider
            
        Returns:
            The generated response as a string
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        if not self.tool_calls_supported():
            raise RuntimeError(f"Tool calls not supported by the model: {self._model}")
        
        try:
            # Check if messages are provided in kwargs
            if "messages" in kwargs:
                messages = kwargs.pop("messages")
            else:
                # Create a simple message
                messages = [{"role": "user", "content": prompt}]
            
            response = self._client.messages.create(
                model=self._model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                tools=tools,
                **kwargs,
            )
            
            # Handle tool calls if present
            if tool_handler and response.content:
                # Check for tool calls in content
                tool_calls = []
                for block in response.content:
                    # Handle both object and dictionary cases
                    block_type = None
                    tool_use_data = None
                    
                    # Check if it's an object with attributes
                    if hasattr(block, "type"):
                        block_type = block.type
                        if block_type == "tool_use" and hasattr(block, "tool_use"):
                            tool_use_data = block.tool_use
                    # Check if it's a dictionary
                    elif isinstance(block, dict) and "type" in block:
                        block_type = block["type"]
                        if block_type == "tool_use" and "tool_use" in block:
                            tool_use_data = block["tool_use"]
                    
                    if block_type == "tool_use" and tool_use_data:
                        tool_calls.append((block, tool_use_data))
                
                # Process tool calls if found
                if tool_calls:
                    # Process each tool call
                    tool_results = []
                    for _, tool_use_data in tool_calls:
                        try:
                            # For objects with attributes
                            if hasattr(tool_use_data, "id") and hasattr(tool_use_data, "name"):
                                tool_use_id = tool_use_data.id
                                tool_use_input = {
                                    "id": tool_use_data.id,
                                    "name": tool_use_data.name,
                                    "input": tool_use_data.input
                                }
                            # For dictionaries
                            else:
                                tool_use_id = tool_use_data["id"]
                                tool_use_input = tool_use_data
                            
                            # Call the tool handler with the tool call data
                            result = tool_handler(tool_use_input)
                            
                            # Add the tool result to the messages
                            tool_results.append({
                                "role": "tool",
                                "tool_use_id": tool_use_id,
                                "content": result,
                            })
                        except Exception as e:
                            logger.error(f"Error handling tool call: {str(e)}")
                            # Add error message as tool result
                            tool_results.append({
                                "role": "tool",
                                "tool_use_id": tool_use_id if 'tool_use_id' in locals() else "unknown",
                                "content": f"Error executing tool: {str(e)}",
                            })
                    
                    # Add tool results to messages and continue the conversation
                    all_messages = messages + [{
                        "role": "assistant",
                        "content": response.content,
                    }] + tool_results
                    
                    # Continue the conversation with tool results
                    final_response = self._client.messages.create(
                        model=self._model,
                        messages=all_messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        system=system_prompt,
                        tools=tools,
                        **kwargs,
                    )
                    
                    # Return the final content
                    result = self._extract_text_from_content(final_response.content)
                    return result
            
            # Return text content if no tool calls or handler
            return self._extract_text_from_content(response.content)
            
        except Exception as e:
            logger.error(f"Error querying Anthropic with tools: {str(e)}")
            raise RuntimeError(f"Anthropic tool query failed: {str(e)}")
    
    def stream_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        tool_handler: Optional[Callable[[Dict[str, Any]], str]] = None,
        **kwargs: Any,
    ) -> Generator[Union[str, Dict[str, Any]], None, None]:
        """
        Stream a response from Anthropic with tool support.
        
        Args:
            prompt: The user prompt to send
            tools: List of tool definitions in the Anthropic format
            system_prompt: Optional system prompt to guide the model's behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            tool_handler: Optional callback function to handle tool calls
            **kwargs: Additional arguments for the provider
            
        Yields:
            Either text chunks or tool call objects
            
        Raises:
            RuntimeError: If the provider is not initialized or the query fails
        """
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        if not self.tool_calls_supported():
            raise RuntimeError(f"Tool calls not supported by the model: {self._model}")
        
        try:
            # Check if messages are provided in kwargs
            if "messages" in kwargs:
                messages = kwargs.pop("messages")
            else:
                # Create a simple message
                messages = [{"role": "user", "content": prompt}]
            
            # Make the streaming API call
            with self._client.messages.stream(
                model=self._model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                tools=tools,
                **kwargs,
            ) as stream:
                tool_calls = []
                
                # Stream the response
                for chunk in stream:
                    # Handle content deltas
                    if hasattr(chunk, "delta") and hasattr(chunk.delta, "content") and chunk.delta.content:
                        for content_block in chunk.delta.content:
                            # Handle object with attributes
                            if hasattr(content_block, "type"):
                                if content_block.type == "text" and hasattr(content_block, "text"):
                                    yield content_block.text
                                elif content_block.type == "tool_use" and hasattr(content_block, "tool_use"):
                                    tool_use = content_block.tool_use
                                    # Collect tool call
                                    tool_calls.append(tool_use)
                                    # Create a dictionary representation of the tool call
                                    tool_call_dict = {
                                        "id": tool_use.id,
                                        "name": tool_use.name,
                                        "input": tool_use.input
                                    }
                                    # Yield the tool call as a special object
                                    yield {
                                        "type": "tool_call",
                                        "tool": tool_use.name,
                                        "id": tool_use.id,
                                        "args": tool_use.input,
                                    }
                            # Handle dictionary
                            elif isinstance(content_block, dict) and "type" in content_block:
                                if content_block["type"] == "text" and "text" in content_block:
                                    yield content_block["text"]
                                elif content_block["type"] == "tool_use" and "tool_use" in content_block:
                                    tool_use = content_block["tool_use"]
                                    # Collect tool call
                                    tool_calls.append(tool_use)
                                    # Yield the tool call as a special object
                                    yield {
                                        "type": "tool_call",
                                        "tool": tool_use["name"],
                                        "id": tool_use["id"],
                                        "args": tool_use["input"],
                                    }
                
                # Handle tool calls with the handler if provided
                if tool_handler and tool_calls:
                    # Process each tool call
                    tool_results = []
                    for tool_use in tool_calls:
                        try:
                            # Create a dictionary representation for the handler
                            if hasattr(tool_use, "id") and hasattr(tool_use, "name"):
                                tool_use_id = tool_use.id
                                tool_use_name = tool_use.name
                                tool_use_dict = {
                                    "id": tool_use.id,
                                    "name": tool_use.name,
                                    "input": tool_use.input
                                }
                            else:
                                tool_use_id = tool_use["id"]
                                tool_use_name = tool_use["name"]
                                tool_use_dict = tool_use
                            
                            # Call the tool handler
                            result = tool_handler(tool_use_dict)
                            
                            # Add the tool result
                            tool_results.append({
                                "role": "tool",
                                "tool_use_id": tool_use_id,
                                "content": result,
                            })
                            
                            # Yield the tool result
                            yield {
                                "type": "tool_result",
                                "tool": tool_use_name,
                                "id": tool_use_id,
                                "result": result,
                            }
                        except Exception as e:
                            logger.error(f"Error handling tool call: {str(e)}")
                            error_msg = f"Error executing tool: {str(e)}"
                            
                            # Add error message as tool result
                            tool_results.append({
                                "role": "tool",
                                "tool_use_id": tool_use_id if 'tool_use_id' in locals() else "unknown",
                                "content": error_msg,
                            })
                            
                            # Yield the error
                            yield {
                                "type": "tool_error",
                                "tool": tool_use_name if 'tool_use_name' in locals() else "unknown",
                                "id": tool_use_id if 'tool_use_id' in locals() else "unknown",
                                "error": error_msg,
                            }
                    
                    # Continue the conversation with tool results
                    all_messages = messages + [{
                        "role": "assistant",
                        "content": [
                            {"type": "text", "text": "I'll help with that."}
                        ],
                    }] + tool_results
                    
                    # Stream the continuation response
                    with self._client.messages.stream(
                        model=self._model,
                        messages=all_messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        system=system_prompt,
                        tools=tools,
                        **kwargs,
                    ) as continuation_stream:
                        # Yield a separator to indicate the continuation
                        yield {"type": "continuation", "message": "Continuing with tool results"}
                        
                        # Stream the continuation
                        for chunk in continuation_stream:
                            if hasattr(chunk, "delta") and hasattr(chunk.delta, "content") and chunk.delta.content:
                                for content_block in chunk.delta.content:
                                    if hasattr(content_block, "type") and content_block.type == "text":
                                        yield content_block.text
                                    elif isinstance(content_block, dict) and content_block.get("type") == "text":
                                        yield content_block["text"]
                    
        except Exception as e:
            logger.error(f"Error streaming from Anthropic with tools: {str(e)}")
            raise RuntimeError(f"Anthropic streaming with tools failed: {str(e)}")
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the provided text.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            The number of tokens in the text
            
        Raises:
            RuntimeError: If token counting fails
        """
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        try:
            from anthropic.tokenizer import count_tokens
            return count_tokens(text)
        except ImportError:
            # Fallback for older versions
            try:
                if hasattr(self._client, "count_tokens"):
                    return self._client.count_tokens(text)
                
                logger.warning("Token counting not available in this version of the Anthropic library")
                # Fallback to a rough estimate
                return len(text.split()) * 1.3
            except Exception as e:
                logger.error(f"Error counting tokens: {str(e)}")
                # Fallback to a rough estimate
                return len(text.split()) * 1.3
    
    def count_message_tokens(
        self, 
        messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
        model: Optional[str] = None
    ) -> int:
        """
        Count the number of tokens in a message sequence.
        
        Args:
            messages: The messages to count tokens for
            model: Optional model to use for counting
            
        Returns:
            The number of tokens in the messages
            
        Raises:
            RuntimeError: If token counting fails
        """
        if not self._client or not self._available:
            raise RuntimeError("Anthropic provider not initialized or unavailable")
            
        try:
            # Try to use the official tokenizer
            from anthropic.tokenizer import count_tokens
            
            # Format the messages as a conversation string
            conversation = ""
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                # Handle complex content types
                if isinstance(content, list):
                    # This is a content blocks format, extract the text parts
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            text_parts.append(block)
                    content = " ".join(text_parts)
                
                if role == "user":
                    conversation += f"\n\nHuman: {content}"
                elif role == "assistant":
                    conversation += f"\n\nAssistant: {content}"
                elif role == "system":
                    # System prompts are handled differently in token counting
                    conversation = f"System: {content}\n\n" + conversation
                else:
                    conversation += f"\n\n{role.capitalize()}: {content}"
            
            return count_tokens(conversation)
        except ImportError:
            # Fallback to counting each message separately
            total = 0
            for msg in messages:
                content = msg.get("content", "")
                
                # Handle complex content types
                if isinstance(content, list):
                    # This is a content blocks format, extract the text parts
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                    content = " ".join(text_parts)
                
                total += self.count_tokens(content)
            # Add overhead for message formatting
            return int(total * 1.1)
    
    def get_supported_models(self) -> List[str]:
        """Get a list of supported models."""
        return [
            "claude-3-5-sonnet-latest",
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
        ]
        
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the provider."""
        tool_support = self.tool_calls_supported()
        
        return {
            "name": self.name,
            "version": self._api_version or "unknown",
            "default_model": self._model,
            "available_models": self.get_supported_models(),
            "capabilities": [c.value for c in self.capabilities],
            "tool_support": tool_support,
            "streaming_support": True,
            "chat_history_support": True,
        }
        
    def tool_calls_supported(self) -> bool:
        """Check if the current model supports tool calls."""
        # Claude 3 models support tool calls
        return self._model.startswith("claude-3") 