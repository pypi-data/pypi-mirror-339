"""
AI service for AMAUTA.

This module provides the core functionality for interacting with AI providers,
handling both online and offline modes, and managing provider-specific interactions.
"""

import hashlib
import importlib.util
import json
import logging
import os
import re
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Set

import requests

# Remove circular imports
from amauta_ai.config.service import ConfigService
from amauta_ai.utils.logger import get_logger
from amauta_ai.config.models import ProviderCapability
from amauta_ai.ai.provider_selection import ProviderSelectionService, ProviderMode

# Configure logging
logger = logging.getLogger(__name__)

# Check for provider libraries
ANTHROPIC_AVAILABLE = importlib.util.find_spec("anthropic") is not None
PERPLEXIPY_AVAILABLE = importlib.util.find_spec("perplexipy") is not None

# Import providers if available
if ANTHROPIC_AVAILABLE:
    from anthropic import Anthropic, APIError as AnthropicAPIError
else:
    Anthropic = None
    AnthropicAPIError = None

# Import Perplexity if available
try:
    from perplexipy import PerplexityClient
except ImportError:
    logger.warning("PerplexiPy package not available or incompatible")
    PerplexityClient = None
    PERPLEXIPY_AVAILABLE = False

# Ensure the conditional import warnings are logged only if imports fail
if not ANTHROPIC_AVAILABLE:
    logger.warning(
        "Anthropic package not available. Install with: pip install anthropic>=0.49.0"
    )
if not PERPLEXIPY_AVAILABLE:
    logger.warning(
        "PerplexiPy package not available. Install with: pip install perplexipy>=1.2.0"
    )


class AiProvider(str, Enum):
    """AI provider types.

    This enum defines the available AI providers that can be used
    for generating responses.
    """

    ANTHROPIC = "anthropic"
    PERPLEXITY = "perplexipy"
    OFFLINE = "offline"


class AiService:
    """Service for interacting with AI providers."""
    
    def __init__(self, config_service: ConfigService, offline_mode: bool = False) -> None:
        """Initialize the AI service."""
        self.config_service = config_service
        self.offline_mode = offline_mode
        
        # Initialize provider clients as None
        self._anthropic_client = None
        self._perplexity_client = None
        
        # Initialize the provider selection service
        self.provider_selection = ProviderSelectionService(config_service)

        # Initialize response cache for offline mode
        self._response_cache: Dict[str, str] = {}
        self._cache_file = os.path.expanduser("~/.amauta/response_cache.json")

        # Try to load cached responses
        self._load_response_cache()

        # Check for forced offline mode
        if os.environ.get("AMAUTA_OFFLINE", "").lower() in ("true", "1", "yes"):
            self.offline_mode = True
            logger.info(
                "AMAUTA is running in offline mode due to environment variable."
            )

        # Auto-detect missing API keys and set offline mode if needed
        if not offline_mode and not self._has_any_api_keys():
            logger.warning("No API keys found. Automatically enabling offline mode.")
            self.offline_mode = True

    def is_offline(self) -> bool:
        """Check if the service is running in offline mode."""
        return self.offline_mode

    def set_offline_mode(self, offline: bool) -> None:
        """Set the offline mode."""
        self.offline_mode = offline
        logger.info(f"Offline mode set to: {offline}")

    def has_valid_credentials(self) -> bool:
        """Check if valid API credentials are configured and usable.
        
        This method not only checks if API keys exist but also attempts to validate
        that they are correct and usable.
        
        Returns:
            bool: True if at least one valid API credential is available, False otherwise
        """
        # First, check if any API keys are configured
        if not self._has_any_api_keys():
            return False
            
        # Then try to initialize at least one provider client
        anthropic_client = self._get_anthropic_client()
        if anthropic_client:
            return True
            
        perplexity_client = self._get_perplexity_client()
        if perplexity_client:
            return True
            
        # If we get here, we have keys but they may not be valid
        return False

    def _get_anthropic_client(self) -> Optional[Any]:
        """Get the Anthropic API client."""
        if self.offline_mode or not ANTHROPIC_AVAILABLE or not Anthropic:
            return None

        if self._anthropic_client is None:
            try:
                api_key = self.config_service.get_api_key("anthropic")
                if not api_key:
                    logger.warning("Anthropic API key not found. Will try other providers.")
                    return None

                self._anthropic_client = Anthropic(api_key=api_key)
                logger.info("Successfully initialized Anthropic client")

            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {str(e)}")
                return None

        return self._anthropic_client

    def _get_perplexity_client(self) -> Optional[Any]:
        """Get the Perplexity API client."""
        if self.offline_mode or not PERPLEXIPY_AVAILABLE or not PerplexityClient:
            return None

        if self._perplexity_client is None:
            try:
                api_key = self.config_service.get_api_key("perplexipy")
                if not api_key:
                    logger.warning("Perplexity API key not found. Will try other providers.")
                    return None
                
                self._perplexity_client = PerplexityClient(key=api_key)
                logger.info("Successfully initialized PerplexiPy client")
                
            except Exception as e:
                logger.warning(f"Failed to initialize PerplexiPy client: {str(e)}")
                return None

        return self._perplexity_client

    def _generate_offline_prd_tasks(self, prd_content: str) -> str:
        """Generate offline tasks from a PRD.

        Args:
            prd_content (str): The PRD content to analyze

        Returns:
            str: A JSON string containing mock tasks
        """
        # Generate a mock task list in JSON format
        mock_tasks = [
            {
                "id": "TASK-1",
                "title": "Design System Architecture",
                "description": "Create the high-level system architecture design",
                "details": "1. Define system components\n2. Create architecture diagrams\n3. Document API specifications",
                "priority": "high",
                "dependencies": [],
            },
            {
                "id": "TASK-2",
                "title": "Setup Development Environment",
                "description": "Set up the initial development environment and tools",
                "details": "1. Configure version control\n2. Set up development tools\n3. Create development guidelines",
                "priority": "medium",
            }
        ]
        return json.dumps(mock_tasks)

    def _generate_offline_response(self, prompt: str, mode: str) -> str:
        """Generate an offline response."""
        return f"[OFFLINE MODE] Unable to process request: {prompt}\n\nPlease ensure you have the required API keys configured and are connected to the internet."

    def _offline_response(self, prompt: str, system_prompt: Optional[str], mode: str) -> str:
        """Generate a detailed offline response."""
        response = "[OFFLINE MODE]\n\n"
        if system_prompt:
            response += f"System Context: {system_prompt}\n\n"
        response += f"Unable to process {mode} request: {prompt}\n\n"
        response += "To enable AI features:\n"
        response += "1. Ensure you have the required API keys configured\n"
        response += "2. Check your internet connection\n"
        response += "3. Verify the AI provider services are available"
        return response

    def query_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        allow_tool_calls: bool = False,
        **kwargs: Any,
    ) -> str:
        """Query the Anthropic API."""
        client = self._get_anthropic_client()
        if not client:
            return self._offline_response(prompt, system_prompt, "general")

        try:
            # Get the model from config or use default
            provider_config = self.config_service.get_provider_config("anthropic")
            model = provider_config.default_model if provider_config else "claude-3-5-sonnet-latest"

            # Create the message - using updated Anthropic API format
            messages = [{"role": "user", "content": prompt}]

            # Make the API call with proper system parameter handling
            api_kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            
            # Only include system parameter if it's provided
            if system_prompt:
                api_kwargs["system"] = system_prompt
                
            # Add any additional kwargs
            api_kwargs.update(kwargs)
            
            # Make the API call
            response = client.messages.create(**api_kwargs)

            # Return the content - ensure we handle the response format correctly
            if hasattr(response, 'content') and isinstance(response.content, list) and len(response.content) > 0:
                # New Claude response format
                if hasattr(response.content[0], 'text'):
                    return response.content[0].text
                elif isinstance(response.content[0], dict) and 'text' in response.content[0]:
                    return response.content[0]['text']
            
            # Fallback for potential format changes
            return str(response.content)

        except Exception as e:
            logger.error(f"Error querying Anthropic: {str(e)}")
            return self._offline_response(prompt, system_prompt, "general")

    def query_perplexity(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        stream: bool = False,
        **kwargs: Any,
    ) -> str:
        """Query the Perplexity API."""
        client = self._get_perplexity_client()
        if not client:
            return self._offline_response(prompt, system_prompt, "research")

        try:
            # Combine system prompt and user prompt if both provided
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Use the client to query using updated PerplexiPy API
            if stream:
                # For streaming responses (different handling for PerplexiPy)
                try:
                    response_parts = []
                    for part in client.queryStreamable(full_prompt):
                        response_parts.append(part)
                    return "".join(response_parts)
                except AttributeError:
                    # Fallback if queryStreamable isn't available
                    logger.warning("Falling back to non-streaming query for PerplexiPy")
                    return client.query(full_prompt)
            else:
                # Regular query
                return client.query(full_prompt)

        except Exception as e:
            logger.error(f"Error querying Perplexity: {str(e)}")
            return self._offline_response(prompt, system_prompt, "research")

    def expand_task(
        self,
        task: str,
        num_subtasks: int = 3,
        provider: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Dict[str, str]]:
        """
        Expand a task into subtasks using AI.

        Args:
            task: The task to expand (title and description)
            num_subtasks: Number of subtasks to generate
            provider: Explicitly select AI provider to use
            **kwargs: Additional arguments for the AI provider

        Returns:
            List of subtask dictionaries with 'title' and 'description' keys
        """
        # Check if we're in offline mode
        if self.offline_mode:
            return self._generate_offline_task_expansion(task)

        # Construct prompt for task expansion
        prompt = f"""
        Expand the following task into {num_subtasks} distinct subtasks that need to be completed to fulfill the parent task.
        
        TASK:
        {task}
        
        For each subtask, provide:
        1. A clear, concise title
        2. A detailed description including:
           - Specific work that needs to be done
           - Any technical requirements
           - Definition of done
           
        Format your response as a JSON array of objects, each with 'title' and 'description' fields:
        [
          {{
            "title": "Subtask 1 Title",
            "description": "Detailed description of subtask 1"
          }},
          ...
        ]
        
        Ensure that together, these subtasks fully address all requirements of the parent task.
        """
        
        system_prompt = "You are an expert software development project manager, skilled at breaking down complex tasks into well-defined subtasks."
        
        # Query the LLM with the selected provider if specified
        try:
            response = self.query_llm(
                prompt=prompt,
                system_prompt=system_prompt,
                mode="task",
                required_capabilities={ProviderCapability.TASK},
                provider=provider,
                **kwargs
            )
            
            # Parse the response
            try:
                subtasks = json.loads(response)
                
                # Validate the response format
                if not isinstance(subtasks, list):
                    raise ValueError("Response is not a list")
                
                # Validate and format each subtask
                formatted_subtasks = []
                for subtask in subtasks:
                    if not isinstance(subtask, dict):
                        continue
                    
                    title = subtask.get("title", "").strip()
                    description = subtask.get("description", "").strip()
                    
                    if title and description:
                        formatted_subtasks.append({
                            "title": title,
                            "description": description
                        })
                
                return formatted_subtasks[:num_subtasks]  # Limit to requested number
                
            except json.JSONDecodeError:
                # Try to extract JSON from the response
                match = re.search(r'(\[.*?\])', response, re.DOTALL)
                if match:
                    try:
                        subtasks = json.loads(match.group(1))
                        
                        # Validate and format each subtask
                        formatted_subtasks = []
                        for subtask in subtasks:
                            if not isinstance(subtask, dict):
                                continue
                            
                            title = subtask.get("title", "").strip()
                            description = subtask.get("description", "").strip()
                            
                            if title and description:
                                formatted_subtasks.append({
                                    "title": title,
                                    "description": description
                                })
                        
                        return formatted_subtasks[:num_subtasks]  # Limit to requested number
                    except (json.JSONDecodeError, AttributeError):
                        pass
                
                raise ValueError("Failed to parse AI response into valid JSON")
                
        except Exception as e:
            logger.error(f"Error in task expansion: {str(e)}")
            # Fall back to offline mode if AI fails
            return self._generate_offline_task_expansion(task)

    def query_anthropic_with_thinking(
        self, task_details: Dict[str, Any], provider: str = "anthropic"
    ) -> Dict[str, Any]:
        """Analyze the complexity of a task.

        This method uses AI to analyze various aspects of task complexity,
        including technical difficulty, risk factors, and resource requirements.

        Args:
            task_details (Dict[str, Any]): The task to analyze, containing:
                - id (str): The task ID
                - title (str): The task title
                - description (str): The task description
                - details (str): Additional implementation details
            provider (str): The AI provider to use (default: "anthropic")

        Returns:
            Dict[str, Any]: A dictionary containing the analysis results:
                - complexityScore (int): A score from 1-10
                - timeEstimate (str): Estimated time to complete
                - riskLevel (str): Risk level (low, medium, high)
                - technicalDifficulty (str): Description of technical challenges
                - resourceRequirements (List[str]): Required resources
                - riskFactors (List[str]): Potential risks
                - mitigationStrategies (List[str]): Risk mitigation strategies

        Raises:
            ValueError: If the task details are invalid
            Exception: For other unexpected errors
        """
        if not task_details or not isinstance(task_details, dict):
            raise ValueError("Task details must be a non-empty dictionary")

        required_fields = ["id", "title", "description"]
        for field in required_fields:
            if field not in task_details:
                raise ValueError(f"Task details missing required field: {field}")

        # Prepare the prompt for complexity analysis
        prompt = f"""
        Please analyze the complexity of this task:

        Task ID: {task_details.get('id', 'unknown')}
        Title: {task_details.get('title', '')}
        Description: {task_details.get('description', '')}
        Details: {task_details.get('details', '')}

        Provide a detailed analysis including:
        1. Complexity score (1-10)
        2. Time estimate
        3. Risk level (low, medium, high)
        4. Technical difficulty
        5. Resource requirements
        6. Risk factors
        7. Mitigation strategies

        Format your response as a JSON object with this structure:
        ```json
        {{
          "complexityScore": 5,
          "timeEstimate": "2-3 days",
          "riskLevel": "medium",
          "technicalDifficulty": "Description of technical challenges",
          "resourceRequirements": ["Requirement 1", "Requirement 2"],
          "riskFactors": ["Risk 1", "Risk 2"],
          "mitigationStrategies": ["Strategy 1", "Strategy 2"]
        }}
        ```

        Provide JSON only, no explanatory text.
        """

        try:
            # Query the AI with the prompt
            response = self.query_llm(
                prompt=prompt,
                system_prompt="You are an expert at analyzing software task complexity.",
                max_tokens=2000,
                temperature=0.7,
                provider=provider,
            )

            try:
                # Extract JSON from the response
                import json
                import re

                # Try to find JSON within the response
                json_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", response)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = response

                analysis: Dict[str, Any] = json.loads(json_str)

                # Validate and clean up analysis
                required_fields = [
                    "complexityScore",
                    "timeEstimate",
                    "riskLevel",
                    "technicalDifficulty",
                    "resourceRequirements",
                    "riskFactors",
                    "mitigationStrategies",
                ]
                for field in required_fields:
                    if field not in analysis:
                        if field in [
                            "resourceRequirements",
                            "riskFactors",
                            "mitigationStrategies",
                        ]:
                            analysis[field] = []  # Empty list for array fields
                        else:
                            # Empty string for string fields
                            analysis[field] = ""

                # Validate complexity score
                try:
                    score = int(analysis["complexityScore"])
                    if score < 1 or score > 10:
                        # Default to medium if invalid
                        analysis["complexityScore"] = 5
                except (ValueError, TypeError):
                    analysis["complexityScore"] = 5

                # Validate risk level
                if analysis["riskLevel"].lower() not in ["low", "medium", "high"]:
                    # Default to medium if invalid
                    analysis["riskLevel"] = "medium"

                return analysis

            except Exception as e:
                logger.error(f"Error parsing complexity analysis JSON: {str(e)}")
                raise ValueError(f"Failed to parse complexity analysis: {str(e)}")

        except Exception as e:
            logger.error(f"Error analyzing task complexity: {str(e)}")
            raise Exception(f"Failed to analyze task complexity: {str(e)}")

    def generate_code(
        self,
        task_details: Dict[str, Any],
        language: str = "python",
        provider: str = "anthropic",
    ) -> str:
        """Generate code for a task.

        This method uses AI to generate code based on the task description and requirements.
        It can generate code in various programming languages and follows best practices
        for the specified language.

        Args:
            task_details (Dict[str, Any]): The task to generate code for, containing:
                - id (str): The task ID
                - title (str): The task title
                - description (str): The task description
                - details (str): Additional implementation details
            language (str): The programming language to use (default: "python")
            provider (str): The AI provider to use (default: "anthropic")

        Returns:
            str: The generated code with appropriate documentation

        Raises:
            ValueError: If the task details are invalid
            Exception: For other unexpected errors
        """
        if not task_details or not isinstance(task_details, dict):
            raise ValueError("Task details must be a non-empty dictionary")

        required_fields = ["id", "title", "description"]
        for field in required_fields:
            if field not in task_details:
                raise ValueError(f"Task details missing required field: {field}")

        # Prepare the prompt for code generation
        prompt = f"""
        Please generate code for this task:

        Task ID: {task_details.get('id', 'unknown')}
        Title: {task_details.get('title', '')}
        Description: {task_details.get('description', '')}
        Details: {task_details.get('details', '')}

        Requirements:
        1. Use {language} programming language
        2. Follow best practices and conventions
        3. Include proper documentation
        4. Handle errors appropriately
        5. Add unit tests if applicable

        Generate complete, production-ready code that can be used immediately.
        Include necessary imports and dependencies.
        Add comments explaining complex logic.
        """

        try:
            # Query the AI with the prompt
            response = self.query_llm(
                prompt=prompt,
                system_prompt=f"You are an expert {language} developer.",
                max_tokens=8000,  # Large context for complex code
                temperature=0.7,
                provider=provider,
            )

            try:
                import re

                # Extract code blocks if present
                code_blocks = re.findall(r"```(?:\w+)?\n([\s\S]*?)```", response)
                if code_blocks:
                    # Combine all code blocks
                    return "\n\n".join(block.strip() for block in code_blocks)
                else:
                    # Return the entire response if no code blocks found
                    return response.strip()

            except Exception as e:
                logger.error(f"Error extracting code from response: {str(e)}")
                return response.strip()

        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            raise Exception(f"Failed to generate code: {str(e)}")

    def query_llm(
        self,
        prompt: str,
        mode: str = "general",
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        required_capabilities: Optional[Set[ProviderCapability]] = None,
        provider: Optional[str] = None,
        research: bool = False,
        **kwargs: Any,
    ) -> str:
        """
        Query a language model provider based on mode and requirements.
        
        Args:
            prompt: The prompt to send to the model
            mode: The operating mode (general, research, code, analysis, task)
            system_prompt: Optional system instructions
            max_tokens: Maximum response tokens
            temperature: Temperature for generation
            required_capabilities: Required provider capabilities
            provider: Optional explicit provider override
            research: Whether this is a research-focused query
            **kwargs: Additional kwargs to pass to the provider
            
        Returns:
            Generated response
            
        Raises:
            RuntimeError: If no provider is available or query fails
        """
        if self.offline_mode:
            return self._offline_response(prompt, system_prompt, mode)

        logger.debug(f"Querying LLM (mode={mode}, research={research})")
        
        try:
            # Select provider based on mode, research flag and required capabilities
            try:
                # Map string capabilities to enum values if needed
                if required_capabilities and isinstance(next(iter(required_capabilities), None), str):
                    required_capabilities = {ProviderCapability(cap) for cap in required_capabilities}
                    
                # Use provider selection service to get the appropriate provider
                selected_provider = self.provider_selection.get_provider_for_operation(
                    operation_type=mode,
                    research=research,
                    provider=provider,
                    required_capabilities=required_capabilities,
                )
                logger.info(f"Selected provider for {mode} mode: {selected_provider}")
                
            except Exception as e:
                logger.error(f"Provider selection failed: {str(e)}")
                if provider:  # If explicit provider was specified, try to use it
                    selected_provider = provider
                    logger.info(f"Falling back to explicitly requested provider: {provider}")
                else:
                    # Default fallbacks
                    selected_provider = "anthropic" if ANTHROPIC_AVAILABLE else "perplexipy"
                    logger.info(f"Using default provider: {selected_provider}")

            # Query the selected provider
            if selected_provider == "anthropic":
                if not ANTHROPIC_AVAILABLE:
                    raise RuntimeError("Anthropic provider is not available")
                response = self.query_anthropic(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs,
                )
            elif selected_provider == "perplexipy":
                if not PERPLEXIPY_AVAILABLE:
                    raise RuntimeError("Perplexity provider is not available")
                response = self.query_perplexity(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs,
                )
            else:
                raise RuntimeError(f"Unsupported provider: {selected_provider}")

            return response

        except Exception as e:
            logger.error(f"LLM query failed: {str(e)}")
            
            # Try to fall back to other providers if available
            if provider and (provider == "anthropic" or provider == "perplexipy"):
                fallback = "perplexipy" if provider == "anthropic" else "anthropic"
                try:
                    logger.info(f"Attempting fallback to {fallback} provider")
                    return self.query_llm(
                        prompt=prompt,
                        mode=mode,
                        system_prompt=system_prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        provider=fallback,
                        research=research,
                        **kwargs,
                    )
                except Exception as fallback_error:
                    logger.error(f"Fallback to {fallback} failed: {str(fallback_error)}")
            
            # If all else fails, use offline mode
            logger.warning("All providers failed. Using offline mode response.")
            return self._offline_response(prompt, system_prompt, mode)

    def _has_any_api_keys(self) -> bool:
        """Check if any API keys are configured.

        Returns:
            bool: True if at least one API key is configured, False otherwise
        """
        return bool(
            self.config_service.get_api_key("anthropic")
            or self.config_service.get_api_key("perplexipy")
        )

    def _load_response_cache(self) -> None:
        """Load cached responses from disk.

        This method loads previously cached responses from the cache file.
        If the file doesn't exist or is invalid, it initializes an empty cache.
        """
        try:
            if os.path.exists(self._cache_file):
                with open(self._cache_file, "r") as f:
                    self._response_cache = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load response cache: {str(e)}")
            self._response_cache = {}

    def _generate_cache_key(
        self, prompt: str, system_prompt: Optional[str] = None, mode: str = "general"
    ) -> str:
        """
        Generate a cache key for storing and retrieving offline responses.

        Args:
            prompt: The main prompt text
            system_prompt: Optional system prompt text
            mode: The type of response being generated (e.g., "general", "task", "research")

        Returns:
            A unique string key for caching
        """
        # Create a string combining all inputs that affect the response
        key_parts = [
            prompt.strip(),
            system_prompt.strip() if system_prompt else "",
            mode.strip(),
        ]

        # Join parts and create a hash
        combined = "||".join(key_parts)
        return hashlib.sha256(combined.encode()).hexdigest()

    def query(
        self,
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
        # If a specific provider was requested, try to use it
        if provider_name:
            if provider_name.lower() == AiProvider.ANTHROPIC.value:
                return self.query_anthropic(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens or 2000,
                    temperature=temperature or 0.7,
                    **kwargs,
                )
            elif provider_name.lower() == AiProvider.PERPLEXITY.value:
                return self.query_perplexity(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens or 2000,
                    temperature=temperature or 0.7,
                    stream=stream,
                    **kwargs,
                )
                
        # Default behavior - use query_llm which handles provider selection
        return self.query_llm(
            prompt=prompt, 
            system_prompt=system_prompt,
            max_tokens=max_tokens or 2000,
            temperature=temperature or 0.7,
            provider=provider_name,
            **kwargs
        )
        
    def query_with_tools(
        self,
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
        # For now, only Anthropic supports tool calls
        if self.offline_mode:
            return {"text": self._offline_response(prompt, system_prompt, "tools"), "tool_calls": []}
            
        try:
            # Get Anthropic client
            client = self._get_anthropic_client()
            if not client:
                return {"text": self._offline_response(prompt, system_prompt, "tools"), "tool_calls": []}
                
            # Get model
            provider_config = self.config_service.get_provider_config("anthropic")
            use_model = model or (provider_config.default_model if provider_config else "claude-3-5-sonnet-latest")
            
            # Create the message
            messages = [{"role": "user", "content": prompt}]
            
            # Format tools for Anthropic
            formatted_tools = []
            for tool in tools:
                formatted_tools.append({
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "input_schema": tool.get("parameters", {})
                })
            
            # Make the API call
            response = client.messages.create(
                model=use_model,
                messages=messages,
                max_tokens=max_tokens or 2000,
                temperature=temperature or 0.7,
                system=system_prompt,
                tools=formatted_tools
            )
            
            # Extract tool calls
            tool_calls = []
            for content in response.content:
                if content.type == "tool_use":
                    tool_calls.append({
                        "name": content.tool_use.name,
                        "parameters": content.tool_use.input
                    })
            
            # Extract text
            text_content = ""
            for content in response.content:
                if content.type == "text":
                    text_content += content.text
            
            return {"text": text_content, "tool_calls": tool_calls}
            
        except Exception as e:
            logger.error(f"Error querying with tools: {str(e)}")
            return {"text": f"Error: {str(e)}", "tool_calls": []}
            
    def query_task(
        self,
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
        # Task-specific system prompt if none provided
        if system_prompt is None:
            if task_type == "create":
                system_prompt = "You are an expert at breaking down technical requirements into well-defined tasks."
            elif task_type == "expand":
                system_prompt = "You are an expert at breaking down tasks into smaller, manageable subtasks."
            elif task_type == "analyze":
                system_prompt = "You are an expert at analyzing task complexity and requirements."
            else:
                system_prompt = "You are an expert at software project management and task organization."
        
        # Query the AI
        response = self.query_llm(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens or 4000,
            temperature=temperature or 0.7,
            provider=provider_name,
            **kwargs
        )
        
        # Try to parse the response as JSON if appropriate
        try:
            if task_type in ["create", "expand", "analyze"]:
                import json
                import re
                
                # Try to find JSON in the response
                json_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\}|\[[\s\S]*?\])\s*```", response)
                if json_match:
                    parsed_data = json.loads(json_match.group(1))
                    return {"success": True, "data": parsed_data, "raw_response": response}
        except Exception as e:
            logger.warning(f"Could not parse JSON from response: {str(e)}")
        
        # Return raw response if parsing failed
        return {"success": True, "data": None, "raw_response": response}


class ReporterService:
    """
    Service for generating reports.
    
    This service is responsible for generating reports based on analysis results.
    """
    
    def __init__(
        self,
        config_service: Optional[ConfigService] = None,
        base_path: str = ".",
    ):
        """
        Initialize the reporter service.
        
        Args:
            config_service: The configuration service to use. If None, a new one is created.
            base_path: The base path to use for generating reports.
        """
        self.config_service = config_service or ConfigService()
        self.base_path = Path(base_path).resolve()
        self.config = self.config_service.get_config()
        
        # Initialize services lazily to avoid circular imports
        self._analyzer_service = None
        self._task_manager_service = None
    
    @property
    def analyzer_service(self):
        """Lazily initialize the analyzer service."""
        if self._analyzer_service is None:
            from amauta_ai.analyzer.service import AnalyzerService
            self._analyzer_service = AnalyzerService(
                config_service=self.config_service, 
                base_path=str(self.base_path)
            )
        return self._analyzer_service
    
    @property
    def task_manager_service(self):
        """Lazily initialize the task manager service."""
        if self._task_manager_service is None:
            from amauta_ai.task_manager.service import TaskManagerService
            self._task_manager_service = TaskManagerService()
        return self._task_manager_service

    def generate_report(
        self,
        format: str = "md",
        analysis_result: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate a comprehensive project report.

        This method generates a report in the specified format, including:
        - Project overview
        - Technical analysis
        - Task statistics
        - Code quality metrics
        - Recommendations

        Args:
            format (str): The output format (md, html, json)
            analysis_result (Optional[Dict[str, Any]]): Pre-computed analysis result

        Returns:
            str: The generated report in the specified format

        Raises:
            ValueError: If the format is not supported
            Exception: For other unexpected errors
        """
        # Get analysis result if not provided
        if analysis_result is None:
            try:
                analysis_result = self.analyzer_service.analyze_project()
            except Exception as e:
                logger.error(f"Error running project analysis: {str(e)}")
                analysis_result = self._get_fallback_analysis()

        # Get task information
        try:
            tasks = self.task_manager_service.get_all_tasks()
            task_stats = self.task_manager_service.get_task_statistics()
        except Exception as e:
            logger.error(f"Error getting task information: {str(e)}")
            tasks = []
            task_stats = {}

        # Generate report in requested format
        if format == "md":
            return self._generate_markdown_report(analysis_result, tasks, task_stats)
        elif format == "html":
            return self._generate_html_report(analysis_result, tasks, task_stats)
        elif format == "json":
            return self._generate_json_report(analysis_result, tasks, task_stats)
        else:
            raise ValueError(f"Unknown format: {format}")

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Get a fallback minimal analysis result when analyzer fails.

        Returns:
            A dictionary with minimal structure required for report generation
        """
        return {
            "file_summary": {"total_files": 0, "files_by_type": {}},
            "tech_stack": {
                "languages": [],
                "frameworks": [],
                "libraries": [],
                "tools": [],
            },
        }

    def _run_with_timeout(self, func, timeout=60, *args, **kwargs):
        """Run a function with a timeout.

        Args:
            func: The function to run
            timeout: Timeout in seconds
            *args: Arguments to pass to func
            **kwargs: Keyword arguments to pass to func

        Returns:
            The result of the function

        Raises:
            TimeoutError: If the function times out
        """
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                # Create a custom timeout error with more context
                raise TimeoutError(
                    f"Function {func.__name__} timed out after {timeout} seconds"
                )
