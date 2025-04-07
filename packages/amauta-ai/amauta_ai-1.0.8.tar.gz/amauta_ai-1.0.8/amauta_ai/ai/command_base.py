"""
Base class for AI-powered commands in AMAUTA.

This module provides a standardized way for AMAUTA commands to interact with
AI providers through the AI Provider Selection Service.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Set, TypeVar, Union, cast

from amauta_ai.ai.prompts import PromptContext, PromptManager, PromptType
from amauta_ai.ai.provider_selection import ProviderMode, ProviderSelectionError, ProviderSelectionService
from amauta_ai.ai.service import AiService
from amauta_ai.config.models import ProviderCapability
from amauta_ai.config.service import ConfigService

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for generic result type
T = TypeVar('T')  # Generic type for command result

class AiCommandError(Exception):
    """Exception raised for errors in AI command execution."""
    pass

class AiCommandBase(Generic[T], ABC):
    """
    Base class for commands that use AI providers.
    
    This class handles common functionality like provider selection, 
    offline mode detection, prompt management, and structured interaction 
    with the AI service.
    
    Attributes:
        config_service: The configuration service instance
        provider_selection_service: Service for selecting AI providers
        ai_service: Service for interacting with AI providers
        prompt_manager: Service for generating provider-optimized prompts
    """
    
    def __init__(
        self, 
        offline: bool = False, 
        research: bool = False, 
        provider: Optional[str] = None,
        operation_type: str = "general"
    ):
        """
        Initialize an AI command.
        
        Args:
            offline: Whether to run in offline mode
            research: Whether to use research mode
            provider: Optional explicit provider selection
            operation_type: The type of operation (maps to ProviderMode)
        """
        self.config_service = ConfigService()
        self.provider_selection_service = ProviderSelectionService(self.config_service)
        
        # Check for global flags, but import here to avoid circular dependencies
        try:
            from amauta_ai.main import global_options
            
            # Check for global research flag if one wasn't explicitly provided
            global_research = False
            if hasattr(global_options, 'research'):
                global_research = global_options.research
            
            # Global flag takes precedence over local parameter
            self.research = global_research or research
            
            # Check for global offline flag
            global_offline = False
            if hasattr(global_options, 'offline'):
                global_offline = global_options.offline
                
            # Global offline flag takes precedence
            self.offline = global_offline or offline
            
            # Check for global provider override
            global_provider = None
            if hasattr(global_options, 'provider'):
                global_provider = global_options.provider
                
            # Global provider takes precedence
            self.provider = global_provider or provider
            
        except ImportError:
            # If we can't import global_options, use the provided parameters
            self.research = research
            self.offline = offline
            self.provider = provider
        
        # Initialize the AI service with the determined offline mode
        self.ai_service = AiService(config_service=self.config_service, offline_mode=self.offline)
        self.prompt_manager = PromptManager()
        
        self.operation_type = operation_type
        
        # Cache for selected provider
        self._selected_provider: Optional[str] = None
        self._selected_model: Optional[str] = None
        
        # Log configuration 
        if self.research:
            logger.info(f"Command initialized with research mode enabled")
        if self.provider:
            logger.info(f"Command initialized with explicit provider: {self.provider}")
    
    @abstractmethod
    def execute(self) -> T:
        """
        Execute the command using the appropriate AI provider.
        
        This method should be implemented by subclasses to perform
        the actual command functionality.
        
        Returns:
            The command result
        """
        pass
    
    def select_provider(
        self, 
        mode: Optional[ProviderMode] = None,
        required_capabilities: Optional[Set[ProviderCapability]] = None
    ) -> str:
        """
        Select the appropriate AI provider.
        
        Args:
            mode: The operation mode (defaults to the instance's operation_type)
            required_capabilities: Optional set of required capabilities
            
        Returns:
            The selected provider name
            
        Raises:
            AiCommandError: If no suitable provider is found or offline mode is enabled
        """
        if self.offline:
            return "offline"
        
        # Use the instance operation_type if mode is not explicitly provided
        if mode is None:
            try:
                mode = ProviderMode(self.operation_type)
            except ValueError:
                logger.warning(f"Unknown operation type: {self.operation_type}, using GENERAL mode")
                mode = ProviderMode.GENERAL
            
        try:
            provider = self.provider_selection_service.select_provider(
                mode=mode,
                research=self.research,
                provider=self.provider,
                required_capabilities=required_capabilities
            )
            self._selected_provider = provider
            logger.info(f"Selected provider: {provider} for operation type: {mode.value}")
            return provider
        except ProviderSelectionError as e:
            logger.warning(f"Provider selection failed: {str(e)}, falling back to offline mode")
            # Fall back to offline mode if provider selection fails
            self.ai_service.set_offline_mode(True)
            self.offline = True
            return "offline"
        except Exception as e:
            # For test cases or any unexpected error, also fall back to offline
            logger.error(f"Unexpected error during provider selection: {str(e)}")
            self.ai_service.set_offline_mode(True)
            self.offline = True
            return "offline"
    
    def select_model(self, context_size: Optional[int] = None) -> str:
        """
        Select the appropriate model for the selected provider.
        
        Args:
            context_size: Optional required context window size
            
        Returns:
            The selected model name
            
        Raises:
            AiCommandError: If no provider has been selected yet
        """
        if not self._selected_provider or self._selected_provider == "offline":
            raise AiCommandError("Cannot select model: No provider selected or in offline mode")
        
        try:
            mode = ProviderMode(self.operation_type)
        except ValueError:
            logger.warning(f"Unknown operation type: {self.operation_type}, using GENERAL mode")
            mode = ProviderMode.GENERAL
            
        model = self.provider_selection_service.select_model(
            provider=self._selected_provider,
            mode=mode,
            research=self.research,
            context_size=context_size
        )
        
        self._selected_model = model
        logger.info(f"Selected model: {model} for provider: {self._selected_provider}")
        return model
    
    def generate_prompt(
        self, 
        prompt_type: Union[PromptType, str],
        template_vars: Optional[Dict[str, Any]] = None,
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a provider-optimized prompt.
        
        Args:
            prompt_type: The type of prompt to generate
            template_vars: Variables to use in the template
            context_data: Additional context data for prompt generation
            
        Returns:
            The generated prompt
        """
        if not self._selected_provider:
            try:
                self.select_provider()
            except Exception as e:
                logger.warning(f"Failed to select provider for prompt generation: {str(e)}")
                # Fall back to a generic provider
                self._selected_provider = "offline"
        
        # Create the prompt context
        context = PromptContext(
            provider=self._selected_provider or "offline",
            operation_type=self.operation_type,
            research=self.research,
            **(context_data or {})
        )
        
        # Generate the prompt
        return self.prompt_manager.generate_prompt(
            prompt_type=prompt_type,
            context=context,
            template_vars=template_vars
        )
    
    def get_system_prompt(self) -> str:
        """
        Get a provider-specific system prompt.
        
        Returns:
            A system prompt optimized for the provider and operation
        """
        if not self._selected_provider:
            try:
                self.select_provider()
            except Exception as e:
                logger.warning(f"Failed to select provider for system prompt: {str(e)}")
                # Fall back to a generic provider
                self._selected_provider = "offline"
                
        return self.prompt_manager.get_system_prompt(
            provider=self._selected_provider or "offline",
            operation_type=self.operation_type,
            research=self.research
        )
    
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        required_capabilities: Optional[Set[ProviderCapability]] = None,
        stream: bool = False,
        json_mode: bool = False,
        **kwargs: Any
    ) -> Union[str, List[str]]:
        """
        Query the AI provider with the given prompt.
        
        Args:
            prompt: The prompt to send to the AI provider
            system_prompt: Optional system prompt to guide the AI response
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for response generation
            required_capabilities: Optional set of required provider capabilities
            stream: Whether to stream the response
            json_mode: Whether to request a JSON response
            **kwargs: Additional provider-specific parameters
            
        Returns:
            The AI response as a string, or a list of response chunks if streaming
            
        Raises:
            AiCommandError: If the query fails
        """
        if self.offline:
            offline_response = f"[OFFLINE MODE] Cannot process query: {prompt[:50]}..."
            return [offline_response] if stream else offline_response
        
        try:
            # Select provider if not already selected
            if not self._selected_provider:
                self.select_provider(required_capabilities=required_capabilities)
            
            # Select model if not already selected
            if not self._selected_model and self._selected_provider != "offline":
                self.select_model()
            
            # Use the system prompt if provided, otherwise generate one
            final_system_prompt = system_prompt if system_prompt else self.get_system_prompt()
            
            # Query the AI service - always pass stream parameter
            query_params = {
                "prompt": prompt,
                "system_prompt": final_system_prompt,
                "provider_name": self._selected_provider,
                "model": self._selected_model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": stream,
                "json_mode": json_mode
            }
            query_params.update(kwargs)
            
            # Call with the parameters
            response = self.ai_service.query(**query_params)
            
            if stream:
                # Convert generator to list for testing
                return list(response) if hasattr(response, '__iter__') else [str(response)]
            else:
                return cast(str, response)
                
        except Exception as e:
            logger.error(f"Error during AI query: {str(e)}")
            raise AiCommandError(f"Failed to query AI provider: {str(e)}")
    
    def query_with_template(
        self,
        prompt_type: Union[PromptType, str],
        template_vars: Dict[str, Any],
        system_prompt: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        stream: bool = False,
        json_mode: bool = False,
        **kwargs: Any
    ) -> Union[str, List[str]]:
        """
        Generate a prompt from a template and query the AI provider.
        
        This is a convenience method that combines generate_prompt() and query().
        
        Args:
            prompt_type: The type of prompt to generate
            template_vars: Variables to use in the template
            system_prompt: Optional system prompt to guide the AI response
            context_data: Additional context data for prompt generation
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for response generation
            stream: Whether to stream the response
            json_mode: Whether to request a JSON response
            **kwargs: Additional provider-specific parameters
            
        Returns:
            The AI response as a string, or a list of response chunks if streaming
            
        Raises:
            AiCommandError: If the prompt generation or query fails
        """
        try:
            prompt = self.generate_prompt(
                prompt_type=prompt_type,
                template_vars=template_vars,
                context_data=context_data
            )
            
            return self.query(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                json_mode=json_mode,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Error during templated query: {str(e)}")
            raise AiCommandError(f"Failed to query with template: {str(e)}")
    
    def parse_json_response(self, response: str) -> Any:
        """
        Parse a JSON response from the AI provider.
        
        Args:
            response: The response string
            
        Returns:
            The parsed JSON object
            
        Raises:
            AiCommandError: If the response is not valid JSON
        """
        try:
            # Try to extract JSON from the response if it's not already JSON
            import json
            import re
            
            # Try direct parsing first
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Look for JSON patterns in the response
                json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
                json_matches = re.findall(json_pattern, response)
                
                if json_matches:
                    for json_str in json_matches:
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            continue
                
                # Try to find any JSON-like structure surrounded by {} or []
                json_pattern = r"(\{[\s\S]*\}|\[[\s\S]*\])"
                json_matches = re.findall(json_pattern, response)
                
                if json_matches:
                    for json_str in json_matches:
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            continue
                
                # If we get here, we couldn't parse any JSON
                raise AiCommandError(f"Failed to parse JSON from response: {response[:100]}...")
                
        except Exception as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            raise AiCommandError(f"Failed to parse JSON response: {str(e)}") 