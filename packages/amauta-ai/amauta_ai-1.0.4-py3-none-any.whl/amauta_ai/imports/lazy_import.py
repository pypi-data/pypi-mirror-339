"""
Lazy import system for AMAUTA.

This module provides functionality for lazily importing modules
only when they are actually needed. This can significantly improve
startup time and reduce memory usage.
"""

import importlib
import logging
import sys
import traceback
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from amauta_ai.imports.exceptions import (
    AmautaImportError,
    CircularDependencyError,
)
from amauta_ai.imports.exceptions import (
    ModuleNotFoundError as AmautaModuleNotFoundError,
)

logger = logging.getLogger(__name__)


class LazyModule:
    """
    A proxy class that wraps a module and defers its import until attributes are accessed.
    
    This is used to implement lazy loading of modules, which can improve startup time
    and reduce memory usage by only importing modules when they are actually needed.
    """

    def __init__(self, module_name: str) -> None:
        """
        Initialize a lazy module proxy.
        
        Args:
            module_name: The fully qualified name of the module to lazily import
        """
        self._module_name = module_name
        self._module: Optional[ModuleType] = None
        self._initialized = False
        self._initializing = False
        self._error: Optional[Exception] = None
        
        # For introspection/debugging
        self.__file__ = f"<lazy_import {module_name}>"
        self.__name__ = module_name
        self.__package__ = module_name.split('.')[0] if '.' in module_name else None

    def _initialize(self) -> None:
        """
        Import the actual module when needed.
        
        This method is called the first time an attribute is accessed.
        """
        if self._initialized or self._initializing:
            return
            
        self._initializing = True
        
        try:
            # Import the module using the standard Python import system
            logger.debug(f"Lazy importing module: {self._module_name}")
            self._module = importlib.import_module(self._module_name)
            self._initialized = True
            logger.debug(f"Successfully lazy imported module: {self._module_name}")
        except ModuleNotFoundError as e:
            # Convert to our custom exception type
            self._error = AmautaModuleNotFoundError(
                module_name=self._module_name,
                tried_paths=[getattr(e, 'path', [])]
            )
            logger.error(f"Failed to lazy import module {self._module_name}: {e}")
            raise self._error from e
        except Exception as e:
            # Store any other errors for future reference
            self._error = AmautaImportError(
                message=f"Error during lazy import: {str(e)}",
                module_name=self._module_name,
                details={"original_error": str(e), "traceback": traceback.format_exc()}
            )
            logger.error(f"Error lazy importing {self._module_name}: {e}")
            raise self._error from e
        finally:
            self._initializing = False

    def __getattr__(self, name: str) -> Any:
        """
        Intercept attribute access to lazily import the module when needed.
        
        Args:
            name: The attribute name being accessed
            
        Returns:
            The requested attribute from the actual module
            
        Raises:
            AmautaImportError: If the module cannot be imported or has errors
            AttributeError: If the module doesn't have the requested attribute
        """
        # Import the module if not already done
        if not self._initialized:
            self._initialize()
            
        if self._module is None:
            raise self._error or AmautaImportError(
                message=f"Failed to lazy import module: {self._module_name}",
                module_name=self._module_name
            )
            
        # Access the attribute from the actual module
        try:
            return getattr(self._module, name)
        except AttributeError:
            raise AttributeError(f"Module '{self._module_name}' has no attribute '{name}'")

    def __dir__(self) -> List[str]:
        """
        Support dir() calls on the lazy module.
        
        Returns:
            List of attribute names available in the module
        """
        if not self._initialized:
            try:
                self._initialize()
            except Exception:
                # Return minimal information if the module can't be loaded
                return ['__file__', '__name__', '__package__']
                
        if self._module is not None:
            return dir(self._module)
        return ['__file__', '__name__', '__package__']


class LazyImporter:
    """
    Manages lazy imports throughout the application.
    
    This class provides a centralized way to register and access lazy module imports,
    as well as track dependencies and handle errors.
    """
    
    _instance = None
    
    def __new__(cls) -> 'LazyImporter':
        """
        Ensure only one LazyImporter instance exists (Singleton pattern).
        
        Returns:
            The single LazyImporter instance
        """
        if cls._instance is None:
            cls._instance = super(LazyImporter, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the LazyImporter internal state."""
        self._lazy_modules: Dict[str, LazyModule] = {}
        self._module_dependencies: Dict[str, List[str]] = {}
        self._import_errors: Dict[str, Exception] = {}

    def register_lazy_module(self, module_name: str) -> LazyModule:
        """
        Register a module for lazy importing.
        
        Args:
            module_name: The fully qualified name of the module to register
            
        Returns:
            A LazyModule proxy for the module
        """
        if module_name in self._lazy_modules:
            return self._lazy_modules[module_name]
            
        # Create a new lazy module proxy
        lazy_module = LazyModule(module_name)
        self._lazy_modules[module_name] = lazy_module
        
        # Replace the module in sys.modules with our lazy version if it's not already imported
        if module_name not in sys.modules:
            sys.modules[module_name] = lazy_module
            logger.debug(f"Registered lazy import for module: {module_name}")
        else:
            logger.debug(f"Module {module_name} already imported, not replacing with lazy version")
            
        return lazy_module
    
    def register_module_dependency(self, module_name: str, depends_on: str) -> None:
        """
        Register a dependency relationship between modules.
        
        Args:
            module_name: The module that depends on another
            depends_on: The module that is depended upon
            
        Raises:
            CircularDependencyError: If this would create a circular dependency
        """
        # Initialize the dependency list if this is the first dependency for this module
        if module_name not in self._module_dependencies:
            self._module_dependencies[module_name] = []
            
        # Check for circular dependencies
        if self._would_create_cycle(module_name, depends_on):
            cycle = self._find_dependency_cycle(module_name, depends_on)
            raise CircularDependencyError(module_name, cycle or [depends_on])
            
        if depends_on not in self._module_dependencies[module_name]:
            self._module_dependencies[module_name].append(depends_on)
            logger.debug(f"Registered dependency: {module_name} depends on {depends_on}")
    
    def _would_create_cycle(self, module_name: str, depends_on: str) -> bool:
        """
        Check if adding a dependency would create a cycle.
        
        Args:
            module_name: The module that would depend on another
            depends_on: The module that would be depended upon
            
        Returns:
            True if this would create a circular dependency, False otherwise
        """
        # Direct circular dependency
        if module_name == depends_on:
            return True
            
        # Check if depends_on directly or indirectly depends on module_name
        return self._is_dependent_on(depends_on, module_name, set())
    
    def _is_dependent_on(self, module: str, target: str, visited: Set[str]) -> bool:
        """
        Recursively check if a module depends on a target module.
        
        Args:
            module: The module to check dependencies for
            target: The target module to look for in the dependency chain
            visited: Set of already visited modules to avoid infinite recursion
            
        Returns:
            True if module depends on target, False otherwise
        """
        if module in visited:
            return False
            
        visited.add(module)
        
        # Check direct dependencies
        deps = self._module_dependencies.get(module, [])
        if target in deps:
            return True
            
        # Check indirect dependencies
        for dep in deps:
            if self._is_dependent_on(dep, target, visited):
                return True
                
        return False
    
    def _find_dependency_cycle(self, start: str, end: str) -> Optional[List[str]]:
        """
        Find a dependency cycle if one exists.
        
        Args:
            start: The starting module
            end: The ending module
            
        Returns:
            A list representing the cycle, or None if no cycle exists
        """
        def dfs(current: str, path: List[str], visited: Set[str]) -> Optional[List[str]]:
            if current == start and len(path) > 0:
                return path
                
            if current in visited:
                return None
                
            visited.add(current)
            path.append(current)
            
            for dep in self._module_dependencies.get(current, []):
                result = dfs(dep, path.copy(), visited)
                if result:
                    return result
                    
            return None
            
        return dfs(end, [], set())
    
    def get_module(self, module_name: str) -> Union[LazyModule, ModuleType]:
        """
        Get a module by name, either a real imported module or a lazy module.
        
        Args:
            module_name: The name of the module to get
            
        Returns:
            The module or lazy module
            
        Raises:
            KeyError: If the module is not registered and not in sys.modules
        """
        # Check if we have a lazy module
        if module_name in self._lazy_modules:
            return self._lazy_modules[module_name]
            
        # Check if it's already imported
        if module_name in sys.modules:
            return sys.modules[module_name]
            
        # If not found, try to register it as a new lazy module
        return self.register_lazy_module(module_name)
    
    def get_import_errors(self) -> Dict[str, Exception]:
        """
        Get a dictionary of import errors that occurred during lazy imports.
        
        Returns:
            Dictionary mapping module names to exceptions
        """
        return self._import_errors.copy()
    
    def get_module_dependencies(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of module dependencies.
        
        Returns:
            Dictionary mapping module names to lists of dependencies
        """
        return self._module_dependencies.copy()


# Helper functions for easier use

def lazy_import(module_name: str) -> Union[LazyModule, ModuleType]:
    """
    Lazily import a module.
    
    Args:
        module_name: The name of the module to import
        
    Returns:
        A proxy object that will load the module when accessed,
        or the actual module if it's already imported
    """
    importer = LazyImporter()
    return importer.get_module(module_name)


def register_dependency(module_name: str, depends_on: str) -> None:
    """
    Register a dependency between modules.
    
    Args:
        module_name: The module that depends on another
        depends_on: The module that is depended upon
    """
    importer = LazyImporter()
    importer.register_module_dependency(module_name, depends_on)


def get_lazy_import_status() -> Dict[str, Any]:
    """
    Get status information about the lazy import system.
    
    Returns:
        A dictionary with status information
    """
    importer = LazyImporter()
    return {
        "registered_modules": list(importer._lazy_modules.keys()),
        "module_dependencies": importer.get_module_dependencies(),
        "import_errors": {k: str(v) for k, v in importer.get_import_errors().items()}
    } 