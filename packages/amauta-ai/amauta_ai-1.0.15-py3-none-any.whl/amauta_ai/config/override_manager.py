"""Configuration override system for AMAUTA.

This module provides a system for managing configuration overrides from multiple
sources with a clear precedence order.
"""

from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

from amauta_ai.config.models import AmautarcConfig


class ConfigSource(Enum):
    """Configuration source types with precedence order (higher value = higher precedence)."""

    DEFAULT = auto()  # Default values provided by the application
    CONFIG_FILE = auto()  # Values from .amautarc.yaml
    ENV_VARIABLES = auto()  # Values from environment variables
    CLI_ARGS = auto()  # Values from command-line arguments
    RUNTIME = auto()  # Values set programmatically at runtime


class OverrideManager:
    """
    Configuration override management system.

    This class manages configuration values from multiple sources
    and resolves them according to a defined precedence order.
    """

    def __init__(self) -> None:
        """Initialize the override manager."""
        # Store values by source type
        self._values: Dict[ConfigSource, Dict[str, Any]] = {
            source: {} for source in ConfigSource
        }

        # Cache of resolved values (cleared when values are updated)
        self._resolved_cache: Dict[str, Any] = {}

        # Initialize default source with empty dict
        self._values[ConfigSource.DEFAULT] = {}

    def set_defaults(self, config: AmautarcConfig) -> None:
        """
        Set default configuration values.

        Args:
            config: The default configuration
        """
        self._values[ConfigSource.DEFAULT] = self._flatten_config(config.model_dump())
        self._clear_cache()

    def set_config_file_values(self, config: AmautarcConfig) -> None:
        """
        Set configuration values from config file.

        Args:
            config: Configuration from .amautarc.yaml
        """
        self._values[ConfigSource.CONFIG_FILE] = self._flatten_config(
            config.model_dump()
        )
        self._clear_cache()

    def set_env_values(self, env_values: Dict[str, str]) -> None:
        """
        Set values from environment variables.

        Args:
            env_values: Mapped environment variable values
        """
        self._values[ConfigSource.ENV_VARIABLES] = env_values
        self._clear_cache()

    def set_cli_values(self, cli_values: Dict[str, Any]) -> None:
        """
        Set values from command line arguments.

        Args:
            cli_values: Command line argument values
        """
        self._values[ConfigSource.CLI_ARGS] = cli_values
        self._clear_cache()

    def set_runtime_value(self, key: str, value: Any) -> None:
        """
        Set a runtime configuration value.

        Args:
            key: Configuration key (can be dot-notation path)
            value: Value to set
        """
        self._values[ConfigSource.RUNTIME][key] = value
        self._clear_cache()

    def remove_runtime_value(self, key: str) -> bool:
        """
        Remove a runtime configuration value.

        Args:
            key: Configuration key to remove

        Returns:
            True if value was removed, False if it didn't exist
        """
        if key in self._values[ConfigSource.RUNTIME]:
            del self._values[ConfigSource.RUNTIME][key]
            self._clear_cache()
            return True
        return False

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value with override precedence applied.

        Args:
            key: Configuration key (can be dot-notation path)
            default: Default value if not found in any source

        Returns:
            The resolved configuration value
        """
        # Check cache first
        if key in self._resolved_cache:
            return self._resolved_cache[key]

        # Check sources in precedence order (highest to lowest)
        for source in reversed(list(ConfigSource)):
            if key in self._values[source]:
                value = self._values[source][key]
                self._resolved_cache[key] = value
                return value

        # Return default if not found
        return default

    def get_all_values(self) -> Dict[str, Any]:
        """
        Get all configuration values with overrides applied.

        Returns:
            Dictionary of all resolved configuration values
        """
        # Start with empty result
        result: Dict[str, Any] = {}

        # Get all unique keys from all sources
        all_keys: set[str] = set()
        for source in ConfigSource:
            all_keys.update(self._values[source].keys())

        # Resolve each key
        for key in all_keys:
            result[key] = self.get_value(key)

        return result

    def to_config(self) -> AmautarcConfig:
        """
        Convert the resolved values back to an AmautarcConfig.

        Returns:
            AmautarcConfig with all resolved values
        """
        # Get all resolved values
        flat_values = self.get_all_values()

        # Convert flat dictionary back to nested structure
        nested_dict = self._unflatten_config(flat_values)

        # Create AmautarcConfig from the nested dictionary
        return AmautarcConfig.model_validate(nested_dict)

    def reset(self) -> None:
        """Reset all override values."""
        for source in ConfigSource:
            self._values[source] = {}
        self._clear_cache()

    def get_value_source(self, key: str) -> Optional[ConfigSource]:
        """
        Get the source of a configuration value.

        Args:
            key: Configuration key

        Returns:
            The source of the value, or None if not found
        """
        # Check sources in precedence order (highest to lowest)
        for source in reversed(list(ConfigSource)):
            if key in self._values[source]:
                return source

        return None

    def _clear_cache(self) -> None:
        """Clear the resolved values cache."""
        self._resolved_cache = {}

    def _flatten_config(
        self, config: Dict[str, Any], prefix: str = ""
    ) -> Dict[str, Any]:
        """
        Flatten a nested configuration dictionary to dot notation.

        Args:
            config: Nested configuration dictionary
            prefix: Prefix for keys (used in recursion)

        Returns:
            Flattened dictionary with dot notation keys
        """
        result: Dict[str, Union[str, int, float, bool, None, List, Dict]] = {}

        for key, value in config.items():
            new_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                # Recursively flatten nested dictionaries
                result.update(self._flatten_config(value, new_key))
            else:
                # Add leaf values directly
                result[new_key] = value

        return result

    def _unflatten_config(self, flat_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a flattened configuration dictionary back to nested structure.

        Args:
            flat_config: Flattened dictionary with dot notation keys

        Returns:
            Nested dictionary structure
        """
        result: Dict[str, Union[str, int, float, bool, None, List, Dict[str, Any]]] = {}

        for key, value in flat_config.items():
            parts = key.split(".")
            current = result

            # Navigate/create the nested dictionary structure
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}

                # If this part exists but is not a dict, we have a conflict
                if not isinstance(current[part], dict):
                    # Handle the conflict by creating a nested object
                    # Store the original value with an empty key
                    orig_value = current[part]
                    current[part] = {"": orig_value}

                current = current[part]

            # Set the value at the leaf
            current[parts[-1]] = value

        return result

    def get_source_values(self, source: ConfigSource) -> Dict[str, Any]:
        """
        Get all configuration values from a specific source.

        Args:
            source: The configuration source

        Returns:
            Dictionary of values from the specified source
        """
        return self._values[source].copy()

    def clear_source(self, source: ConfigSource) -> None:
        """
        Clear all values from a specific source.

        Args:
            source: The configuration source to clear
        """
        self._values[source] = {}
        self._clear_cache()

    def get_precedence_report(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate a report showing the precedence of values for each key.

        Returns:
            Dictionary mapping each key to a list of sources and values
        """
        # Get all unique keys from all sources
        all_keys = set()
        for source in ConfigSource:
            all_keys.update(self._values[source].keys())

        # Build the report
        report: Dict[str, List[Dict[str, Any]]] = {}

        for key in all_keys:
            key_report = []
            for source in ConfigSource:
                if key in self._values[source]:
                    key_report.append(
                        {
                            "source": source.name,
                            "value": self._values[source][key],
                            "active": source == self.get_value_source(key),
                        }
                    )

            report[key] = key_report

        return report
