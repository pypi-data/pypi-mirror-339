"""
Exceptions for the AMAUTA import system.

This module contains custom exception classes for handling
specific import-related errors in the AMAUTA system.
"""

from typing import Any, Dict, List, Optional


class AmautaImportError(Exception):
    """Base exception class for all AMAUTA import errors."""

    def __init__(
        self,
        message: str,
        module_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the exception.

        Args:
            message: The error message
            module_name: The name of the module that failed to import
            details: Additional details about the error
        """
        self.module_name = module_name
        self.details = details or {}

        if module_name:
            message = f"{message} (module: {module_name})"

        super().__init__(message)


class CircularDependencyError(AmautaImportError):
    """Exception raised when a circular dependency is detected."""

    def __init__(self, module_name: str, dependency_chain: List[str]):
        """
        Initialize the exception.

        Args:
            module_name: The name of the module with circular dependency
            dependency_chain: The chain of dependencies that form the circle
        """
        self.dependency_chain = dependency_chain

        # Create a readable representation of the dependency chain
        chain_str = " -> ".join(dependency_chain + [module_name])
        message = f"Circular dependency detected: {chain_str}"

        super().__init__(
            message=message,
            module_name=module_name,
            details={"dependency_chain": dependency_chain},
        )


class ModuleNotFoundError(AmautaImportError):
    """Exception raised when a module cannot be found."""

    def __init__(self, module_name: str, tried_paths: Optional[List[str]] = None):
        """
        Initialize the exception.

        Args:
            module_name: The name of the module that couldn't be found
            tried_paths: List of paths that were searched
        """
        # Filter out None values and ensure all items are strings
        self.tried_paths = []
        if tried_paths:
            self.tried_paths = [str(path) for path in tried_paths if path is not None]

        message = f"Module not found: {module_name}"
        if self.tried_paths:
            paths_str = "\n  - ".join([""] + self.tried_paths)
            message = f"{message}\nSearched in:{paths_str}"

        super().__init__(
            message=message,
            module_name=module_name,
            details={"tried_paths": self.tried_paths},
        )


class ComponentRegistrationError(AmautaImportError):
    """Exception raised when a component fails to register."""

    def __init__(
        self,
        component_name: str,
        component_type: str,
        module_name: Optional[str] = None,
        reason: str = "",
    ):
        """
        Initialize the exception.

        Args:
            component_name: The name of the component that failed to register
            component_type: The type of component (class, function, constant)
            module_name: The name of the module containing the component
            reason: The reason for the registration failure
        """
        self.component_name = component_name
        self.component_type = component_type

        message = f"Failed to register {component_type} '{component_name}'"
        if reason:
            message = f"{message}: {reason}"

        super().__init__(
            message=message,
            module_name=module_name,
            details={
                "component_name": component_name,
                "component_type": component_type,
                "reason": reason,
            },
        )


class ImportSystemNotInitializedError(AmautaImportError):
    """Exception raised when the import system is used before initialization."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__(
            message="Import system has not been initialized. Call initialize_imports() first.",
            details={
                "suggestion": "Call initialize_imports() before using other import functions"
            },
        )


class ImportErrorWithContext(ImportError):
    """Custom ImportError that includes context."""

    def __init__(
        self,
        message: str,
        module_name: str,
        importing_file: Optional[str] = None,
        dependency_chain: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the exception.

        Args:
            message: The error message
            module_name: The name of the module that failed to import
            importing_file: The file that is importing the module
            dependency_chain: The chain of dependencies that form the circle
            details: Additional details about the error
        """
        self.module_name = module_name
