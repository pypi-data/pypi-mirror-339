"""
Imports initialization module for AMAUTA.

This module is responsible for setting up the import hook system
and making exported components available to other modules.
"""

import importlib
import logging
import sys
import traceback
from types import ModuleType
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import os

# Import custom exceptions
from amauta_ai.imports.exceptions import (
    AmautaImportError,
    CircularDependencyError,
    ComponentRegistrationError,
    ImportSystemNotInitializedError,
)
from amauta_ai.imports.exceptions import (
    ModuleNotFoundError as AmautaModuleNotFoundError,
)

# Import lazy import system
from amauta_ai.imports.lazy_import import (
    LazyImporter,
    LazyModule,
    lazy_import,
    register_dependency,
    get_lazy_import_status,
)

# Set up logging
logger = logging.getLogger(__name__)


# Import the ExportManager on-demand to avoid circular imports
def get_export_manager() -> Any:
    """Get the ExportManager instance on-demand."""
    try:
        from amauta_ai.exports.export_manager import ExportManager

        return ExportManager()
    except ImportError as e:
        logger.error(f"Failed to import ExportManager: {str(e)}")
        raise AmautaImportError(
            message="Failed to import ExportManager. This is critical for the import system.",
            details={"original_error": str(e), "traceback": traceback.format_exc()},
        )


# Initialize imports if not already initialized
_initialized = False
_initializing = False
_failed_modules: Set[str] = set()
_import_order: List[str] = []
_import_errors: Dict[str, Dict[str, Any]] = {}
_module_dependencies: Dict[str, List[str]] = {}


def initialize_imports() -> None:
    """
    Initialize the AMAUTA import system.
    
    This function sets up the import system by registering all available
    modules and components. It can now use lazy loading to defer actual
    imports until the modules are needed, improving startup time.

    Raises:
        CircularDependencyError: If a circular dependency is detected
        AmautaImportError: For other import-related errors
    """
    global _initialized, _initializing, _failed_modules, _import_order, _import_errors

    # Prevent circular initialization
    if _initializing:
        logger.debug("Circular initialization detected, skipping")
        return

    # Skip if already initialized
    if _initialized:
        logger.debug("Imports already initialized")
        return

    # Set initializing flag to prevent circular calls
    _initializing = True

    try:
        # List of export modules to register for lazy import or directly import
        export_modules = [
            "amauta_ai.exports.config",
            "amauta_ai.exports.mcp",
            "amauta_ai.exports.rules",
            "amauta_ai.exports.summarizer",
            "amauta_ai.exports.task_manager",
            "amauta_ai.exports.ai",
        ]
        
        # Modules that should not use lazy imports
        direct_import_modules = [
            "amauta_ai.exports.analyzer",  # The analyzer module has issues with lazy imports
            "amauta_ai.task_manager.template_service",  # The template service has issues with lazy imports
        ]

        # Clear previous errors if reinitializing
        _import_errors = {}

        # Check if we should use lazy imports or fall back to traditional imports
        use_lazy_imports = os.environ.get("AMAUTA_USE_LAZY_IMPORTS", "").lower() in ("true", "1", "yes")
        
        # Always directly import modules that should not use lazy imports
        for module_name in direct_import_modules:
            try:
                logger.debug(f"Directly importing module: {module_name}")
                module = importlib.import_module(module_name)
                
                # Record successful import
                if module_name not in _import_order:
                    _import_order.append(module_name)
                    
                # Remove from failed modules if it was previously failed
                if module_name in _failed_modules:
                    _failed_modules.remove(module_name)
                    if module_name in _import_errors:
                        del _import_errors[module_name]
            except Exception as e:
                # Handle errors during import
                logger.error(f"Failed to directly import {module_name}: {str(e)}")
                _failed_modules.add(module_name)
                _import_errors[module_name] = {
                    "error_type": "direct_import_failed",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                }
        
        if use_lazy_imports:
            # Use the new lazy import system
            logger.debug("Using lazy import system")
            
            # Register modules for lazy import instead of importing immediately
            lazy_importer = LazyImporter()
            for module_name in export_modules:
                try:
                    logger.debug(f"Registering lazy import for module: {module_name}")
                    lazy_importer.register_lazy_module(module_name)
                    
                    # Record as successfully registered
                    if module_name not in _import_order:
                        _import_order.append(module_name)
                        
                    # Remove from failed modules if previously failed
                    if module_name in _failed_modules:
                        _failed_modules.remove(module_name)
                        if module_name in _import_errors:
                            del _import_errors[module_name]
                except Exception as e:
                    # Handle errors during registration
                    logger.error(f"Failed to register lazy import for {module_name}: {str(e)}")
                    _failed_modules.add(module_name)
                    _import_errors[module_name] = {
                        "error_type": "lazy_import_registration_failed",
                        "message": str(e),
                        "traceback": traceback.format_exc(),
                    }

            # Register inter-module dependencies for proper lazy loading
            try:
                # task_manager -> config
                register_dependency("amauta_ai.exports.task_manager", "amauta_ai.exports.config")
                
                # ai -> config
                register_dependency("amauta_ai.exports.ai", "amauta_ai.exports.config")
                
                # mcp -> ai, task_manager
                register_dependency("amauta_ai.exports.mcp", "amauta_ai.exports.ai")
                register_dependency("amauta_ai.exports.mcp", "amauta_ai.exports.task_manager")
                
                # reporter -> task_manager (analyzer is directly imported)
                register_dependency("amauta_ai.exports.reporter", "amauta_ai.exports.task_manager")
            except CircularDependencyError as e:
                logger.error(f"Circular dependency detected during dependency registration: {str(e)}")
                # Record the error but don't fail initialization
                _import_errors["dependency_registration"] = {
                    "error_type": "circular_dependency",
                    "message": str(e),
                    "details": {"dependency_chain": getattr(e, "dependency_chain", [])},
                }

            # Log initialization status
            logger.debug(f"Lazy import registration order: {', '.join(_import_order)}")
        else:
            # Use the original import method for stability
            logger.debug("Using traditional import system (set AMAUTA_USE_LAZY_IMPORTS=1 to enable lazy imports)")
            
            # Import modules one by one with error handling
            for module_name in export_modules:
                try:
                    logger.debug(f"Importing module: {module_name}")
                    module = importlib.import_module(module_name)
                    
                    # Record successful import
                    if module_name not in _import_order:
                        _import_order.append(module_name)
                        
                    # Remove from failed modules if it was previously failed
                    if module_name in _failed_modules:
                        _failed_modules.remove(module_name)
                        if module_name in _import_errors:
                            del _import_errors[module_name]
                except CircularDependencyError as e:
                    # Handle circular dependency specifically
                    logger.error(f"Circular dependency detected: {str(e)}")
                    _failed_modules.add(module_name)
                    _import_errors[module_name] = {
                        "error_type": "circular_dependency",
                        "message": str(e),
                        "details": e.details,
                        "dependency_chain": getattr(e, "dependency_chain", []),
                    }
                except AmautaModuleNotFoundError as e:
                    # Handle module not found error
                    logger.error(f"Module not found: {str(e)}")
                    _failed_modules.add(module_name)
                    _import_errors[module_name] = {
                        "error_type": "module_not_found",
                        "message": str(e),
                        "details": e.details,
                        "tried_paths": getattr(e, "tried_paths", []),
                    }
                except Exception as e:
                    # Handle other errors
                    logger.error(f"Failed to import module {module_name}: {str(e)}")
                    _failed_modules.add(module_name)
                    _import_errors[module_name] = {
                        "error_type": "generic_error",
                        "message": str(e),
                        "traceback": traceback.format_exc(),
                    }
                    
            # Log import order for debugging
            logger.debug(f"Import order: {', '.join(_import_order)}")

        # Log any failed registrations/imports
        if _failed_modules:
            logger.warning(f"Failed to {'register' if use_lazy_imports else 'import'} modules: {', '.join(_failed_modules)}")
            for module_name in _failed_modules:
                error_info = _import_errors.get(module_name, {})
                error_type = error_info.get("error_type", "unknown")
                message = error_info.get("message", "Unknown error")
                logger.warning(f"  - {module_name}: [{error_type}] {message}")

        # Set initialized flag
        _initialized = True
        logger.debug(f"Imports initialization completed successfully with {'lazy loading enabled' if use_lazy_imports else 'traditional imports'}")
    finally:
        # Clear initializing flag
        _initializing = False


def import_module_with_dependencies(
    module_name: str, dependency_chain: Optional[List[str]] = None
) -> ModuleType:
    """
    Import a module and track its dependencies.
    
    This function now uses lazy importing for better performance, 
    only loading modules when they are actually needed.

    Args:
        module_name: The name of the module to import
        dependency_chain: The chain of dependencies leading to this import (for cycle detection)

    Returns:
        The imported module object or a lazy module proxy

    Raises:
        CircularDependencyError: If a circular dependency is detected
        AmautaModuleNotFoundError: If the module cannot be found
        AmautaImportError: For other import-related errors
    """
    # Initialize dependency chain if not provided
    if dependency_chain is None:
        dependency_chain = []

    # Check for circular dependencies
    if module_name in dependency_chain:
        cycle = dependency_chain[dependency_chain.index(module_name) :]
        raise CircularDependencyError(module_name, cycle)

    # Skip if the module is already imported
    if module_name in _import_order:
        module = sys.modules.get(module_name)
        if module is not None:
            return module
        # If somehow the module is in _import_order but not in sys.modules,
        # continue with the import

    # Track dependency chain
    current_chain = dependency_chain + [module_name]

    try:
        # Use lazy import instead of direct importlib
        logger.debug(f"Lazy importing module: {module_name}")
        module = lazy_import(module_name)

        # Record successful import/registration
        if module_name not in _import_order:
            _import_order.append(module_name)

        # Remove from failed modules if it was previously failed
        if module_name in _failed_modules:
            _failed_modules.remove(module_name)
            if module_name in _import_errors:
                del _import_errors[module_name]

        # Register dependencies in the current chain for future reference
        if len(current_chain) > 1:
            for i in range(len(current_chain) - 1):
                register_dependency(current_chain[i+1], current_chain[i])

        return module
    except AmautaModuleNotFoundError as e:
        # The exception handler already has the necessary details
        raise e
    except ModuleNotFoundError as e:
        # Get detailed information about the import failure
        name = getattr(e, "name", module_name)
        paths = getattr(e, "path", [])

        if name != module_name:
            # The failure was in a dependency
            _module_dependencies.setdefault(module_name, []).append(name)

            # Add more helpful information
            tried_paths = []
            for path in sys.path:
                tried_paths.append(f"{path}/{name.replace('.', '/')}.py")

            raise AmautaModuleNotFoundError(
                module_name=name, tried_paths=tried_paths
            ) from e
        else:
            # The failure was in the requested module itself
            tried_paths = []
            for path in sys.path:
                tried_paths.append(f"{path}/{module_name.replace('.', '/')}.py")

            raise AmautaModuleNotFoundError(
                module_name=module_name, tried_paths=tried_paths
            ) from e
    except Exception as e:
        # Handle unexpected errors
        raise AmautaImportError(
            message=f"Unexpected error during import: {str(e)}",
            module_name=module_name,
            details={
                "original_error": str(e),
                "traceback": traceback.format_exc(),
                "dependency_chain": current_chain,
            },
        ) from e


# Define all exported symbols
__all__: List[str] = [
    "initialize_imports",
    "import_module_with_dependencies",
    "get_import_status",
    "get_detailed_error",
    "fix_import_errors",
    "lazy_import",
    "register_dependency",
    "get_lazy_import_status",
    "LazyModule",
]


def _import_hook(
    component_type: str,
    name: str,
    value: Any,
    dependency_chain: Optional[List[str]] = None,
) -> None:
    """
    Hook function called when components are registered with the ExportManager.

    Args:
        component_type: The type of component ('class', 'function', 'constant')
        name: The name of the component
        value: The component value
        dependency_chain: The chain of dependencies leading to this import (for cycle detection)

    Raises:
        ComponentRegistrationError: If the component cannot be registered
    """
    try:
        globals()[name] = value
        if name not in __all__:
            __all__.append(name)
        logger.debug(f"Imported {component_type} '{name}' via hook")
    except Exception as e:
        logger.error(f"Error in import hook for {component_type} '{name}': {str(e)}")
        raise ComponentRegistrationError(
            component_name=name, component_type=component_type, reason=str(e)
        ) from e


# Register the import hook when this module is imported
try:
    export_manager = get_export_manager()
    export_manager.register_import_hook(_import_hook)
    logger.debug("Import hook registered successfully")
except Exception as e:
    logger.error(f"Failed to register import hook: {str(e)}")


def get_import_status() -> Dict[str, Any]:
    """
    Get the current status of the import system.

    Returns:
        Dict with import status information
    """
    return {
        "initialized": _initialized,
        "initializing": _initializing,
        "failed_modules": list(_failed_modules),
        "import_order": _import_order,
        "registered_components": __all__,
        "import_errors": _import_errors,
        "module_dependencies": _module_dependencies,
    }


def get_detailed_error(module_name: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed error information for a specific module.

    Args:
        module_name: The name of the module

    Returns:
        Dict with error details if the module has an error, None otherwise
    """
    if not _initialized and not _initializing:
        raise ImportSystemNotInitializedError()

    return _import_errors.get(module_name)


def fix_import_errors() -> Tuple[List[str], List[str]]:
    """
    Attempt to fix import errors by reimporting failed modules.

    Returns:
        Tuple of (fixed_modules, remaining_failed_modules)
    """
    if not _initialized and not _initializing:
        raise ImportSystemNotInitializedError()

    fixed_modules = []

    # Try to reimport each failed module
    current_failed_modules = list(
        _failed_modules
    )  # Make a copy to avoid modification during iteration
    for module_name in current_failed_modules:
        try:
            # Attempt to import the module
            importlib.import_module(module_name)

            # Record successful import
            if module_name not in _import_order:
                _import_order.append(module_name)

            # Remove from failed modules
            _failed_modules.remove(module_name)
            if module_name in _import_errors:
                del _import_errors[module_name]

            fixed_modules.append(module_name)
        except Exception as e:
            # Update error information
            logger.error(f"Failed to fix import for {module_name}: {str(e)}")
            _import_errors[module_name] = {
                "error_type": "fix_attempt_failed",
                "message": str(e),
                "traceback": traceback.format_exc(),
            }

    return fixed_modules, list(_failed_modules)


# Ensure initialization doesn't run automatically on import
# Instead, rely on explicit initialize_imports() calls
