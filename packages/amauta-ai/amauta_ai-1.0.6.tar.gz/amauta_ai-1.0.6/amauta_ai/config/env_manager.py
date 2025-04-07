"""Environment variable management for AMAUTA."""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class EnvManager:
    """
    Environment variable management for AMAUTA.

    This class provides advanced environment variable handling capabilities,
    including loading from multiple .env files, variable substitution,
    and environment-specific configuration.
    """

    def __init__(
        self,
        base_env_path: str = ".env",
        environment: Optional[str] = None,
        override_env: bool = True,
    ):
        """
        Initialize the environment manager.

        Args:
            base_env_path: Path to the base .env file
            environment: Optional environment name (e.g., 'development', 'production')
                If provided, will also load .env.<environment> file
            override_env: Whether to override existing environment variables
        """
        self.base_env_path = Path(base_env_path)
        self.environment = environment
        self.override_env = override_env
        self._loaded_vars: Dict[str, str] = {}

    def load(self) -> Dict[str, str]:
        """
        Load environment variables from .env files.

        Loads variables in this order (later files override earlier ones):
        1. .env (base file)
        2. .env.<environment> (if environment is specified)
        3. Existing environment variables (if override_env is False)

        Returns:
            Dictionary of loaded environment variables
        """
        # Start with empty dict
        env_vars: Dict[str, str] = {}

        # Load base .env file
        if self.base_env_path.exists():
            base_vars = self._parse_env_file(self.base_env_path)
            env_vars.update(base_vars)

        # Load environment-specific .env file if specified
        if self.environment:
            # Find the env-specific file in the same directory as base file
            base_dir = self.base_env_path.parent
            env_file_name = f".env.{self.environment}"
            env_specific_path = base_dir / env_file_name

            if env_specific_path.exists():
                env_specific_vars = self._parse_env_file(env_specific_path)
                env_vars.update(env_specific_vars)

        # Store loaded variables
        self._loaded_vars = env_vars.copy()

        # Apply variable substitution
        env_vars = self._substitute_variables(env_vars)

        # Set environment variables
        for key, value in env_vars.items():
            # Skip if variable exists and override is False
            if key in os.environ and not self.override_env:
                continue
            os.environ[key] = value

        return env_vars

    def _parse_env_file(self, file_path: Path) -> Dict[str, str]:
        """
        Parse a .env file and return variables as a dictionary.

        Args:
            file_path: Path to the .env file

        Returns:
            Dictionary of environment variables
        """
        env_vars: Dict[str, str] = {}

        try:
            # Ensure the path is a file, not a directory
            if not file_path.is_file():
                return env_vars
                
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Parse key-value pairs
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or (
                            value.startswith("'") and value.endswith("'")
                        ):
                            value = value[1:-1]

                        env_vars[key] = value
                    else:
                        print(
                            f"Warning: Invalid format in {file_path} at line {line_num}: {line}"
                        )
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")

        return env_vars

    def _substitute_variables(self, env_vars: Dict[str, str]) -> Dict[str, str]:
        """
        Substitute variables in values, e.g., ${VAR} or $VAR.

        Args:
            env_vars: Dictionary of environment variables

        Returns:
            Dictionary with substituted values
        """
        result: Dict[str, str] = {}
        var_pattern = re.compile(r"\$\{([^}]+)\}|\$([a-zA-Z0-9_]+)")

        # First pass: simple variables that don't depend on other variables
        for key, value in env_vars.items():
            result[key] = value

        # Multiple passes for nested variables
        # We need to handle cases where variables reference other variables
        for _ in range(3):  # Limit to 3 passes to avoid infinite recursion
            for key, value in result.items():
                # Find all variable references
                matches = var_pattern.findall(value)
                if matches:
                    new_value = value
                    for match in matches:
                        var_name = match[0] or match[1]  # Either ${VAR} or $VAR form
                        var_value = result.get(var_name, os.environ.get(var_name, ""))
                        # Replace both ${VAR} and $VAR forms
                        if match[0]:  # ${VAR} form
                            new_value = new_value.replace(f"${{{var_name}}}", var_value)
                        else:  # $VAR form
                            # Make sure we're replacing the exact variable name
                            new_value = re.sub(
                                r"\$" + var_name + r"\b", var_value, new_value
                            )
                    result[key] = new_value

        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get an environment variable value.

        Args:
            key: The environment variable name
            default: Default value if the variable is not set

        Returns:
            The environment variable value or the default
        """
        return os.environ.get(key, default)

    def set(self, key: str, value: str, override: Optional[bool] = None) -> None:
        """
        Set an environment variable.

        Args:
            key: The environment variable name
            value: The value to set
            override: Whether to override existing value.
                If None, uses the instance's override_env setting.
        """
        should_override = self.override_env if override is None else override

        if key in os.environ and not should_override:
            return

        os.environ[key] = value
        self._loaded_vars[key] = value

    def get_int(self, key: str, default: Optional[int] = None) -> Optional[int]:
        """
        Get an environment variable as an integer.

        Args:
            key: The environment variable name
            default: Default value if the variable is not set or invalid

        Returns:
            The environment variable as an integer, or the default
        """
        value = self.get(key)
        if value is None:
            return default

        try:
            return int(value)
        except ValueError:
            return default

    def get_bool(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        """
        Get an environment variable as a boolean.

        Args:
            key: The environment variable name
            default: Default value if the variable is not set

        Returns:
            The environment variable as a boolean, or the default
        """
        value = self.get(key)
        if value is None:
            return default

        return value.lower() in ("true", "yes", "1", "y", "t")

    def get_float(self, key: str, default: Optional[float] = None) -> Optional[float]:
        """
        Get an environment variable as a float.

        Args:
            key: The environment variable name
            default: Default value if the variable is not set or invalid

        Returns:
            The environment variable as a float, or the default
        """
        value = self.get(key)
        if value is None:
            return default

        try:
            return float(value)
        except ValueError:
            return default

    def validate_sensitive_vars(self, vars_to_check: List[str]) -> Dict[str, str]:
        """
        Validate that required sensitive environment variables are set and appear valid.
        
        This is particularly useful for checking API keys and other credentials.
        
        Args:
            vars_to_check: List of environment variable names to validate
            
        Returns:
            Dictionary of validation issues found (variable name: issue description)
        """
        issues = {}
        
        for var_name in vars_to_check:
            value = self.get(var_name)
            
            # Check if variable exists
            if value is None:
                issues[var_name] = "missing"
                continue
                
            # Check if variable has a value
            if not value or value.strip() == "":
                issues[var_name] = "empty"
                continue
                
            # Check if API key variables have minimum length (most API keys are longer)
            if "_API_KEY" in var_name and len(value) < 8:
                issues[var_name] = "too short (likely invalid)"
                continue
                
            # Check if value contains template placeholders
            if "${" in value or "your_" in value.lower() or "xxx" in value.lower():
                issues[var_name] = "contains template placeholder"
                continue
        
        return issues

    def validate_required_vars(self, required_vars: List[str]) -> Dict[str, bool]:
        """
        Validate that all required environment variables are set.
        
        Args:
            required_vars: List of required environment variable names
            
        Returns:
            Dictionary mapping variable names to boolean (True if present, False if missing)
        """
        results = {}
        
        for var_name in required_vars:
            value = self.get(var_name)
            results[var_name] = value is not None and value.strip() != ""
        
        return results

    def get_list(
        self, key: str, separator: str = ",", default: Optional[List[str]] = None
    ) -> List[str]:
        """
        Get an environment variable as a list.

        Args:
            key: The environment variable name
            separator: The separator to split the string
            default: Default value if the variable is not set

        Returns:
            The environment variable as a list, or the default
        """
        value = self.get(key)
        if value is None or value == "":
            # Important: Return the exact default list object if provided
            if default is not None:
                return default
            return []

        return [item.strip() for item in value.split(separator)]

    def save(self, file_path: Optional[str] = None) -> None:
        """
        Save current environment variables to a .env file.

        Args:
            file_path: Path to save the .env file (defaults to base_env_path)
        """
        target_path = Path(file_path) if file_path else self.base_env_path

        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write("# AMAUTA Environment Variables\n\n")

                # Group variables by common prefixes
                categorized_vars: Dict[str, Dict[str, str]] = {
                    "API Keys": {},
                    "Logging": {},
                    "Other": {},
                }

                for key, value in sorted(self._loaded_vars.items()):
                    if key.endswith("_API_KEY") or "API_KEY" in key:
                        categorized_vars["API Keys"][key] = value
                    elif "LOG" in key:
                        categorized_vars["Logging"][key] = value
                    else:
                        categorized_vars["Other"][key] = value

                # Write variables by category
                for category, vars_dict in categorized_vars.items():
                    if vars_dict:
                        f.write(f"# {category}\n")
                        for key, value in sorted(vars_dict.items()):
                            f.write(f"{key}={value}\n")
                        f.write("\n")

        except Exception as e:
            print(f"Error saving environment variables to {target_path}: {str(e)}")

    def generate_example(self, output_path: str = ".env.example") -> None:
        """
        Generate a .env.example file with all variable names from the loaded env.

        Args:
            output_path: Path to save the .env.example file
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# AMAUTA Environment Variables Example\n\n")

                # Group variables by common prefixes
                categorized_vars: Dict[str, List[str]] = {
                    "API Keys": [],
                    "Logging": [],
                    "Other": [],
                }

                for key in sorted(self._loaded_vars.keys()):
                    if key.endswith("_API_KEY") or "API_KEY" in key:
                        categorized_vars["API Keys"].append(key)
                    elif "LOG" in key:
                        categorized_vars["Logging"].append(key)
                    else:
                        categorized_vars["Other"].append(key)

                # Write variables by category
                for category, keys in categorized_vars.items():
                    if keys:
                        f.write(f"# {category}\n")
                        for key in sorted(keys):
                            f.write(f"{key}=\n")
                        f.write("\n")

        except Exception as e:
            print(f"Error generating example file at {output_path}: {str(e)}")
