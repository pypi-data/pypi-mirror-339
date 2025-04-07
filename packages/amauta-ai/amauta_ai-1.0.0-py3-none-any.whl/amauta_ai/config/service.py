"""Configuration service for AMAUTA."""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set
import os
import logging

import yaml

from amauta_ai.config.env_manager import EnvManager
from amauta_ai.config.models import (
    AiProviderConfig,
    AiProviderType,
    AmautarcConfig,
    ProviderCapability,
    ProviderPreferences,
    ModelMetadata,
    ResearchModeConfig,
)
from amauta_ai.config.override_manager import ConfigSource, OverrideManager


# Custom YAML representer for Pydantic models
def _represent_enum(dumper, data):
    """Custom representer for Enum values."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data.value))


class ConfigService:
    """
    Configuration service for AMAUTA.

    This service is responsible for loading and validating configuration from
    .env and .amautarc.yaml files.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration service.

        Args:
            config_path: Optional path to the configuration file
        """
        # Check for local .amautarc.yaml first (in current directory)
        local_config_path = os.path.join(os.getcwd(), ".amautarc.yaml")
        
        if config_path:
            self.config_path = config_path
        elif os.path.exists(local_config_path):
            self.config_path = local_config_path
            print(f"Using local config file: {local_config_path}")
        else:
            self.config_path = os.path.expanduser("~/.amautarc.yaml")
        
        print(f"ConfigService initialized with config path: {self.config_path}")
        
        self._config: Optional[AmautarcConfig] = None
        self._config_cache: Dict[str, Any] = {}
        self._change_listeners: Dict[str, List[Callable]] = {}

        # Initialize the override manager
        self.override_manager = OverrideManager()

        # Load environment variables from both home directory and current directory
        self.env_manager = EnvManager(base_env_path=".env")
        self.env_manager.load()
        
        # Also load from current directory .env if it exists
        if os.path.exists(".env"):
            local_env_manager = EnvManager(base_env_path=".env")
            local_env_manager.load()
            print("Loaded environment variables from local .env file")

        # Register YAML representers for custom types
        yaml.add_representer(AiProviderType, _represent_enum)

        # Initialize configuration from sources
        self._init_config()

    def _init_config(self) -> None:
        """Initialize configuration from all sources."""
        # Set default configuration in the override manager
        default_config = self.get_default_config()
        self.override_manager.set_defaults(default_config)

        # Load and set configuration from file
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    # Only try to validate if yaml.safe_load returned a dict
                    if isinstance(data, dict):
                        try:
                            file_config = AmautarcConfig.model_validate(data)
                            self.override_manager.set_config_file_values(file_config)
                        except Exception as validation_err:
                            print(f"Error validating .amautarc.yaml: {str(validation_err)}")
                    else:
                        print(f"Error loading .amautarc.yaml: Not a valid YAML dictionary")
            except yaml.YAMLError as yaml_err:
                print(f"Error parsing .amautarc.yaml: {str(yaml_err)}")
            except Exception as e:
                print(f"Error loading .amautarc.yaml: {str(e)}")

        # Set environment variable overrides
        env_overrides = self._get_env_overrides()
        self.override_manager.set_env_values(env_overrides)

        # Update internal config with overridden values
        self._refresh_config()
        
        # Validate sensitive environment variables
        self._validate_sensitive_env_vars()

    def _validate_sensitive_env_vars(self) -> None:
        """
        Validate sensitive environment variables (like API keys) at startup.
        
        This helps catch configuration issues early and provides helpful warnings.
        """
        logger = logging.getLogger(__name__)
        
        # Get all required API key environment variables from provider configs
        sensitive_vars = []
        for provider_name, provider_config in self.get_config().ai.items():
            if provider_config.api_key_env_var:
                sensitive_vars.append(provider_config.api_key_env_var)
        
        # Validate the sensitive variables
        issues = self.env_manager.validate_sensitive_vars(sensitive_vars)
        
        if issues:
            logger.warning("===== SENSITIVE ENVIRONMENT VARIABLE ISSUES =====")
            for var_name, issue in issues.items():
                logger.warning(f"  • {var_name}: {issue}")
            logger.warning("You may experience authentication failures until these issues are fixed.")
            logger.warning("================================================")
        else:
            logger.debug("All sensitive environment variables validated successfully.")

    def _refresh_config(self) -> None:
        """Refresh the internal configuration from the override manager."""
        self._config = self.override_manager.to_config()
        self._clear_cache()

    def _get_env_overrides(self) -> Dict[str, str]:
        """
        Extract configuration overrides from environment variables.

        Returns:
            Dictionary of configuration keys to environment values
        """
        overrides: Dict[str, str] = {}

        # Map known environment variables to config paths
        env_mappings = {
            "AMAUTA_LOG_LEVEL": "log_level",
            "AMAUTA_PROJECT_NAME": "project.name",
            "AMAUTA_PROJECT_DESCRIPTION": "project.description",
        }

        # Map environment variables to configuration keys
        for env_var, config_key in env_mappings.items():
            value = self.env_manager.get(env_var)
            if value is not None:
                overrides[config_key] = value

        # Handle API keys for providers
        for provider_name, provider_config in self.get_default_config().ai.items():
            env_var = provider_config.api_key_env_var
            if env_var and self.env_manager.get(env_var) is not None:
                # We don't store API keys in the config, but we can override the env var name
                # if a different env var exists with the value
                pass

        return overrides

    def _load_amautarc(self) -> AmautarcConfig:
        """
        Load the .amautarc.yaml file.

        Returns:
            The loaded AmautarcConfig
        """
        # This method is maintained for compatibility, but we use the override manager now
        return self._config or self.get_default_config()

    def get_config(self) -> AmautarcConfig:
        """
        Get the configuration.

        Returns:
            The AmautarcConfig
        """
        if self._config is None:
            self._refresh_config()

        return self._config

    def get_api_key(self, provider_name: str) -> Optional[str]:
        """
        Get an API key for a specific provider.

        Args:
            provider_name: Name of the provider in the config

        Returns:
            The API key if found, None otherwise
        """
        config = self.get_config()

        if provider_name not in config.ai:
            logger = logging.getLogger(__name__)
            logger.warning(f"Provider '{provider_name}' not found in config")
            return None

        provider_config = config.ai[provider_name]
        env_var_name = provider_config.api_key_env_var
        
        # Get the API key from environment variables
        api_key = self.env_manager.get(env_var_name)
        
        # Try directly from os.environ as a fallback
        if api_key is None:
            logger = logging.getLogger(__name__)
            logger.debug(f"API key for provider '{provider_name}' not found in environment variable '{env_var_name}'")
            api_key = os.environ.get(env_var_name)
        
        # Validate the API key if it exists
        if api_key:
            # Basic validation - reject obviously invalid keys
            if len(api_key) < 8:  # Most API keys are much longer
                logger = logging.getLogger(__name__)
                logger.error(f"API key for '{provider_name}' appears invalid (too short)")
                return None
                
            # Log only first and last few characters of the key for debugging
            # This helps with troubleshooting without exposing the full key
            if api_key and len(api_key) > 10:
                logger = logging.getLogger(__name__)
                masked_key = f"{api_key[:4]}...{api_key[-4:]}"
                logger.debug(f"Using API key for '{provider_name}': {masked_key}")
        else:
            logger = logging.getLogger(__name__)
            logger.warning(f"No API key found for provider '{provider_name}'")
        
        return api_key

    def save_config(
        self, config: AmautarcConfig, file_path: Optional[str] = None
    ) -> None:
        """
        Save the configuration to .amautarc.yaml.

        Args:
            config: The configuration to save
            file_path: Optional path to save the config to (defaults to self.config_path)
        """
        target_path = Path(file_path) if file_path else Path(self.config_path)

        # Convert Pydantic model to dict with proper handling of enums
        config_dict = config.model_dump()
        self._convert_enums_to_strings(config_dict)

        with open(target_path, "w", encoding="utf-8") as f:
            yaml.dump(config_dict, f, default_flow_style=False)

        # Update the config file values in the override manager
        self.override_manager.set_config_file_values(config)

        # Refresh internal config
        self._refresh_config()

        # Notify listeners of config change
        self._notify_change("config", config)

    def _convert_enums_to_strings(self, config_dict: Dict[str, Any]) -> None:
        """
        Convert Enum values to strings in the config dictionary.

        Args:
            config_dict: The configuration dictionary to process
        """
        # Process AI provider configurations
        if "ai" in config_dict and isinstance(config_dict["ai"], dict):
            for provider_key, provider_config in config_dict["ai"].items():
                if isinstance(provider_config, dict) and "provider" in provider_config:
                    if hasattr(provider_config["provider"], "value"):
                        provider_config["provider"] = provider_config["provider"].value

        # Process other potential enum values
        # Add additional enum conversions here if needed

    def generate_env_example(self, output_path: str = ".env.example") -> None:
        """
        Generate a .env.example file based on the configuration.

        Args:
            output_path: Path to the output .env.example file
        """
        config = self.get_config()
        env_vars = set()

        # Collect all API key environment variables
        for provider_config in config.ai.values():
            env_vars.add(provider_config.api_key_env_var)

        # Add other environment variables
        env_vars.add("AMAUTA_LOG_LEVEL")
        env_vars.add("AMAUTA_PROJECT_NAME")
        env_vars.add("AMAUTA_PROJECT_DESCRIPTION")

        # Create EnvManager for generating example
        env_manager = EnvManager()

        # Set all variables with empty values
        for var in sorted(env_vars):
            env_manager.set(var, "")

        # Generate example file
        env_manager.generate_example(output_path)

    def generate_amautarc_example(
        self, output_path: str = ".amautarc.example.yaml"
    ) -> None:
        """
        Generate a .amautarc.example.yaml file based on the default configuration.

        Args:
            output_path: Path to the output .amautarc.example.yaml file
        """
        config = self.get_default_config()

        # Convert to dict with proper handling of enums
        config_dict = config.model_dump()
        self._convert_enums_to_strings(config_dict)

        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(config_dict, f, default_flow_style=False)

    def get_default_config(self) -> AmautarcConfig:
        """
        Get the default configuration.

        Returns:
            The default AmautarcConfig
        """
        anthropic_models = {
            "claude-3-5-sonnet-latest": ModelMetadata(
                name="claude-3-5-sonnet-latest",
                context_window=200000,
                max_tokens_out=4096,
                supports_vision=True,
                supports_tools=True,
                recommended_for=["general", "code", "task", "analysis"],
            ),
            "claude-3-opus-20240229": ModelMetadata(
                name="claude-3-opus-20240229",
                context_window=180000,
                max_tokens_out=4096,
                supports_vision=True,
                supports_tools=True,
                recommended_for=["analysis", "research"],
            ),
            "claude-3-sonnet-20240229": ModelMetadata(
                name="claude-3-sonnet-20240229",
                context_window=160000,
                max_tokens_out=4096,
                supports_vision=True,
                supports_tools=True,
                recommended_for=["general", "code", "task"],
            ),
            "claude-3-haiku-20240307": ModelMetadata(
                name="claude-3-haiku-20240307",
                context_window=48000,
                max_tokens_out=4096,
                supports_vision=True,
                supports_tools=True,
                recommended_for=["general"],
            ),
        }

        perplexity_models = {
            "sonar-medium-online": ModelMetadata(
                name="sonar-medium-online",
                context_window=32000,
                max_tokens_out=4096,
                supports_vision=False,
                supports_tools=False,
                recommended_for=["research", "general"],
            ),
            "sonar-small-online": ModelMetadata(
                name="sonar-small-online",
                context_window=12000,
                max_tokens_out=4096,
                supports_vision=False,
                supports_tools=False,
                recommended_for=["research"],
            ),
            "llama-3-sonar-large-32k-online": ModelMetadata(
                name="llama-3-sonar-large-32k-online",
                context_window=32000,
                max_tokens_out=4096,
                supports_vision=False,
                supports_tools=False,
                recommended_for=["research", "general"],
            ),
        }
        
        return AmautarcConfig(
            project={
                "name": "AMAUTA",
                "description": "AMAUTA Unified AI Development Command Center",
            },
            analyzer={
                "ignored_paths": [
                    "node_modules",
                    "venv",
                    ".venv",
                    "dist",
                    "build",
                    "__pycache__",
                    ".git",
                ],
                "languages": ["javascript", "typescript", "python"],
                "max_file_size_kb": 1024,
            },
            ai={
                "anthropic": AiProviderConfig(
                    provider=AiProviderType.ANTHROPIC,
                    default_model="claude-3-5-sonnet-latest",
                    api_key_env_var="ANTHROPIC_API_KEY",
                    capabilities={
                        ProviderCapability.GENERAL,
                        ProviderCapability.CODE,
                        ProviderCapability.TASK,
                        ProviderCapability.ANALYSIS,
                        ProviderCapability.RESEARCH,
                        ProviderCapability.STREAMING,
                        ProviderCapability.TOOL_CALLS,
                        ProviderCapability.FUNCTION_CALLING,
                        ProviderCapability.VISION,
                        ProviderCapability.LONG_CONTEXT,
                    },
                    models=anthropic_models,
                    version="0.49.0+",
                    timeout_seconds=60,
                    retry_attempts=2,
                ),
                "perplexipy": AiProviderConfig(
                    provider=AiProviderType.PERPLEXITY,
                    default_model="sonar-medium-online",
                    api_key_env_var="PERPLEXITY_API_KEY",
                    capabilities={
                        ProviderCapability.GENERAL,
                        ProviderCapability.RESEARCH,
                        ProviderCapability.CODE,
                        ProviderCapability.TASK,
                        ProviderCapability.ANALYSIS,
                        ProviderCapability.LONG_CONTEXT,
                        ProviderCapability.RAG,
                    },
                    models=perplexity_models,
                    version="1.2.0+",
                    timeout_seconds=60,
                    retry_attempts=2,
                ),
            },
            provider_preferences=ProviderPreferences(
                general=["anthropic", "perplexipy"],
                research=["perplexipy", "anthropic"],
                code=["anthropic", "perplexipy"],
                analysis=["anthropic", "perplexipy"],
                task=["anthropic", "perplexipy"],
            ),
            research_mode=ResearchModeConfig(
                enabled_by_default=False,
                preferred_providers=["perplexipy", "anthropic"],
                context_boost=True,
                required_capabilities=[
                    ProviderCapability.RESEARCH,
                    ProviderCapability.LONG_CONTEXT,
                ],
                prompt_templates={
                    "code_analysis": "Analyze the following code with research focus, considering best practices, patterns, and potential improvements: {code}",
                    "architecture": "Research the most appropriate architecture for this project, considering {requirements}",
                }
            ),
            log_level="INFO",
        )

    def get_anthropic_config(self) -> Optional[AiProviderConfig]:
        """
        Get the Anthropic provider configuration.

        Returns:
            The Anthropic provider configuration if configured, None otherwise
        """
        config = self.get_config()
        return config.ai.get("anthropic")

    def get_perplexity_config(self) -> Optional[AiProviderConfig]:
        """
        Get the Perplexity provider configuration.

        Returns:
            The Perplexity provider configuration if configured, None otherwise
        """
        config = self.get_config()
        return config.ai.get("perplexipy")

    def get_research_mode_config(self) -> ResearchModeConfig:
        """
        Get the research mode configuration.
        
        Returns:
            The research mode configuration
        """
        config = self.get_config()
        return config.research_mode

    def is_research_mode_enabled_by_default(self) -> bool:
        """
        Check if research mode is enabled by default.
        
        Returns:
            True if research mode is enabled by default, False otherwise
        """
        return self.get_research_mode_config().enabled_by_default

    def get_research_required_capabilities(self) -> Set[ProviderCapability]:
        """
        Get the capabilities required for research mode.
        
        Returns:
            Set of capabilities required for research mode
        """
        config = self.get_research_mode_config()
        return set(config.required_capabilities)

    def get_recommended_model(self, provider_name: str, operation_type: str) -> Optional[str]:
        """
        Get the recommended model for a specific provider and operation type.
        
        Args:
            provider_name: The provider name
            operation_type: The operation type (general, research, code, analysis, task)
            
        Returns:
            The recommended model name or None if no recommendation
        """
        provider_config = self.get_provider_config(provider_name)
        if not provider_config or not provider_config.models:
            return None
        
        # Filter models recommended for this operation type
        recommended_models = {
            name: metadata 
            for name, metadata in provider_config.models.items() 
            if operation_type in metadata.recommended_for
        }
        
        if not recommended_models:
            return provider_config.default_model
        
        # Sort by context window size (larger is better)
        sorted_models = sorted(
            recommended_models.items(),
            key=lambda x: x[1].context_window,
            reverse=True
        )
        
        # Return the top recommendation
        return sorted_models[0][0] if sorted_models else provider_config.default_model

    def get_model_metadata(self, provider_name: str, model_name: Optional[str] = None) -> Optional[ModelMetadata]:
        """
        Get metadata for a specific model from a provider.
        
        Args:
            provider_name: The provider name
            model_name: The model name (or None for default model)
            
        Returns:
            The model metadata or None if not found
        """
        provider_config = self.get_provider_config(provider_name)
        if not provider_config or not provider_config.models:
            return None
        
        if not model_name:
            model_name = provider_config.default_model
        
        return provider_config.models.get(model_name)

    def get_provider_timeout(self, provider_name: str) -> int:
        """
        Get timeout setting for a provider.
        
        Args:
            provider_name: The provider name
            
        Returns:
            Timeout in seconds (defaults to 60)
        """
        provider_config = self.get_provider_config(provider_name)
        if not provider_config:
            return 60
        return provider_config.timeout_seconds

    def get_provider_retry_attempts(self, provider_name: str) -> int:
        """
        Get retry attempts for a provider.
        
        Args:
            provider_name: The provider name
            
        Returns:
            Number of retry attempts (defaults to 2)
        """
        provider_config = self.get_provider_config(provider_name)
        if not provider_config:
            return 2
        return provider_config.retry_attempts

    def get_base_url(self, provider_name: str) -> Optional[str]:
        """
        Get the base URL for a provider.
        
        Args:
            provider_name: The provider name
            
        Returns:
            The base URL or None if not set
        """
        provider_config = self.get_provider_config(provider_name)
        if not provider_config:
            return None
        return provider_config.base_url

    def get_prompt_template(self, template_name: str) -> Optional[str]:
        """
        Get a prompt template from the research_mode configuration.
        
        Args:
            template_name: The name of the template
            
        Returns:
            The template string or None if not found
        """
        research_config = self.get_research_mode_config()
        return research_config.prompt_templates.get(template_name)

    def get_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using a dot-notation path.

        Args:
            key_path: Dot-notation path to the value (e.g., "project.name")
            default: Default value to return if the key doesn't exist

        Returns:
            The configuration value at the specified path
        """
        # First try from the override manager
        value = self.override_manager.get_value(key_path)
        if value is not None:
            return value

        # Fall back to cached method
        return self._legacy_get_value(key_path, default)

    def _legacy_get_value(self, key_path: str, default: Any = None) -> Any:
        """Legacy method for getting config values, used as fallback."""
        # Check cache first
        if key_path in self._config_cache:
            return self._config_cache[key_path]

        config = self.get_config()

        # Handle root-level attributes directly
        if "." not in key_path:
            if hasattr(config, key_path):
                value = getattr(config, key_path)
                self._config_cache[key_path] = value
                return value
            return default

        # Navigate the path for nested attributes
        parts = key_path.split(".")
        current = config.model_dump()

        try:
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default

            # Cache the result
            self._config_cache[key_path] = current
            return current
        except (KeyError, TypeError, AttributeError):
            return default

    def set_value(self, key_path: str, value: Any, save: bool = True) -> bool:
        """
        Set a configuration value using a dot-notation path.

        Args:
            key_path: Dot-notation path to the value (e.g., "project.name")
            value: The value to set
            save: Whether to save the configuration to disk

        Returns:
            True if successful, False otherwise
        """
        # Set the value as a runtime override
        self.override_manager.set_runtime_value(key_path, value)

        # Refresh config
        self._refresh_config()

        # Save to disk if requested
        if save:
            try:
                self.save_config(self._config)
            except Exception as e:
                print(f"Error saving config: {str(e)}")
                return False

        # Notify listeners
        self._notify_change(key_path, value)

        return True

    def _clear_cache(self) -> None:
        """Clear the configuration value cache."""
        self._config_cache = {}

    def add_change_listener(self, key_path: str, callback: Callable) -> None:
        """
        Add a listener for configuration changes.

        Args:
            key_path: The path to monitor for changes
            callback: The function to call when the value changes
        """
        if key_path not in self._change_listeners:
            self._change_listeners[key_path] = []

        self._change_listeners[key_path].append(callback)

    def remove_change_listener(self, key_path: str, callback: Callable) -> bool:
        """
        Remove a configuration change listener.

        Args:
            key_path: The path being monitored
            callback: The callback function to remove

        Returns:
            True if the listener was removed, False otherwise
        """
        if key_path in self._change_listeners:
            try:
                self._change_listeners[key_path].remove(callback)
                return True
            except ValueError:
                return False
        return False

    def _notify_change(self, key_path: str, value: Any) -> None:
        """
        Notify listeners of a configuration change.

        Args:
            key_path: The path that changed
            value: The new value
        """
        # Notify listeners for the specific path
        if key_path in self._change_listeners:
            for callback in self._change_listeners[key_path]:
                try:
                    callback(key_path, value)
                except Exception as e:
                    print(f"Error in config change listener: {str(e)}")

        # Notify listeners for parent paths
        parts = key_path.split(".")
        for i in range(len(parts)):
            parent_path = ".".join(parts[:i])
            if parent_path and parent_path in self._change_listeners:
                parent_value = self.get_value(parent_path)
                for callback in self._change_listeners[parent_path]:
                    try:
                        callback(parent_path, parent_value)
                    except Exception as e:
                        print(f"Error in config change listener: {str(e)}")

        # Notify global listeners
        if "*" in self._change_listeners:
            for callback in self._change_listeners["*"]:
                try:
                    callback(key_path, value)
                except Exception as e:
                    print(f"Error in config change listener: {str(e)}")

    def reset_to_defaults(self, save: bool = True) -> None:
        """
        Reset configuration to default values.

        Args:
            save: Whether to save the configuration to disk
        """
        # Reset the override manager
        self.override_manager.reset()

        # Set default values
        default_config = self.get_default_config()
        self.override_manager.set_defaults(default_config)

        # Refresh config
        self._refresh_config()

        if save:
            self.save_config(self._config)

        self._notify_change("config", self._config)

    def merge_config(self, config_data: Dict[str, Any], save: bool = True) -> bool:
        """
        Merge configuration data with the current configuration.

        Args:
            config_data: Configuration data to merge
            save: Whether to save the configuration to disk

        Returns:
            True if successful, False otherwise
        """
        # Convert to flat dictionary
        flat_data = self.override_manager._flatten_config(config_data)

        # Set each value as a runtime override
        for key, value in flat_data.items():
            self.override_manager.set_runtime_value(key, value)

        # Refresh config
        self._refresh_config()

        # Save to disk if requested
        if save:
            try:
                self.save_config(self._config)
                return True
            except Exception as e:
                print(f"Error saving merged config: {str(e)}")
                return False

        return True

    def _deep_merge(self, d1: Dict[str, Any], d2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.

        Args:
            d1: First dictionary
            d2: Second dictionary (values override d1)

        Returns:
            Merged dictionary
        """
        result = d1.copy()

        for key, value in d2.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                # Recursively merge nested dictionaries
                result[key] = self._deep_merge(result[key], value)
            else:
                # Override or add value
                result[key] = value

        return result

    def get_override_source(self, key_path: str) -> Optional[ConfigSource]:
        """
        Get the source of a configuration value.

        This indicates which configuration source (default, config file, environment, etc.)
        is providing the effective value for the given key.

        Args:
            key_path: The configuration key path in dot notation

        Returns:
            The source of the configuration value, or None if not found
        """
        return self.override_manager.get_value_source(key_path)

    def get_precedence_report(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate a report showing all sources for each configuration key.

        Returns:
            Dictionary mapping keys to lists of source information
        """
        return self.override_manager.get_precedence_report()

    def set_cli_args(self, args: Dict[str, Any]) -> None:
        """
        Set configuration values from command line arguments.

        Args:
            args: Dictionary of command line arguments
        """
        # Set CLI args in the override manager
        self.override_manager.set_cli_values(args)

        # Refresh config
        self._refresh_config()

    def get_provider_capabilities(self, provider_name: str) -> Set[ProviderCapability]:
        """
        Get the capabilities of a specific provider.

        Args:
            provider_name: Name of the provider in the config

        Returns:
            Set of capabilities supported by the provider
        """
        config = self.get_config()
        if provider_name not in config.ai:
            return set()

        provider_config = config.ai[provider_name]
        return provider_config.capabilities or set()

    def get_preferred_providers(self, mode: str) -> List[str]:
        """
        Get the ordered list of preferred providers for a specific mode.

        Args:
            mode: Operation mode (general, research, code, analysis, task)

        Returns:
            List of provider names in order of preference
        """
        config = self.get_config()
        preferences = getattr(config.provider_preferences, mode, None)
        if preferences is None:
            return config.provider_preferences.general

        return preferences

    def get_provider_by_capabilities(
        self, required_capabilities: Set[ProviderCapability]
    ) -> Optional[str]:
        """
        Get the first available provider that supports all required capabilities.

        Args:
            required_capabilities: Set of capabilities that must be supported

        Returns:
            Name of the first provider that supports all capabilities, or None if none found
        """
        config = self.get_config()
        
        for provider_name, provider_config in config.ai.items():
            if not provider_config.capabilities:
                continue
                
            if required_capabilities.issubset(provider_config.capabilities):
                # Check if API key is available
                if self.get_api_key(provider_name):
                    return provider_name
                    
        return None

    def select_provider(
        self,
        mode: str,
        required_capabilities: Optional[Set[ProviderCapability]] = None,
        provider_override: Optional[str] = None,
    ) -> Optional[str]:
        """
        Select the most appropriate provider based on mode, capabilities, and preferences.

        Args:
            mode: Operation mode (general, research, code, analysis, task)
            required_capabilities: Optional set of capabilities that must be supported
            provider_override: Optional provider name to use regardless of other factors

        Returns:
            Name of the selected provider, or None if no suitable provider found
        """
        if provider_override:
            config = self.get_config()
            if provider_override in config.ai:
                if required_capabilities:
                    provider_caps = self.get_provider_capabilities(provider_override)
                    if not required_capabilities.issubset(provider_caps):
                        return None
                return provider_override
            return None

        # Get preferred providers for the mode
        preferred_providers = self.get_preferred_providers(mode)

        # If no specific capabilities required, return first available preferred provider
        if not required_capabilities:
            for provider_name in preferred_providers:
                if self.get_api_key(provider_name):
                    return provider_name
            return None

        # Check preferred providers in order for required capabilities
        for provider_name in preferred_providers:
            provider_caps = self.get_provider_capabilities(provider_name)
            if required_capabilities.issubset(provider_caps):
                if self.get_api_key(provider_name):
                    return provider_name

        # If no preferred provider found, try any provider with required capabilities
        return self.get_provider_by_capabilities(required_capabilities)

    def get_provider_preferences(self) -> ProviderPreferences:
        """Get provider preferences.

        Returns:
            ProviderPreferences: The provider preferences from the config
        """
        config = self.get_config()
        return config.provider_preferences

    def get_provider_config(self, provider_name: str) -> Optional[AiProviderConfig]:
        """
        Get the configuration for a specific provider.

        Args:
            provider_name: Name of the provider.

        Returns:
            The provider configuration if found, None otherwise.
        """
        config = self.get_config()
        return config.ai.get(provider_name)
