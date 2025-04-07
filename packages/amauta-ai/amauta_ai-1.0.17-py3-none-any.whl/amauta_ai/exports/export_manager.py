"""
Export Manager for AMAUTA

This module provides the ExportManager class, which is responsible for
registering and retrieving exported components from all modules in the project.
"""

import inspect
import logging
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
)

# Type variable for generic type annotations
T = TypeVar("T")

logger = logging.getLogger(__name__)


class ExportManager:
    """
    Singleton class that manages exports from all modules.

    This class provides a central registry for all exported components
    (classes, functions, constants) and handles their retrieval.
    """

    _instance = None

    def __new__(cls) -> "ExportManager":
        """Ensure only one instance of ExportManager exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(ExportManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialize the export manager registry."""
        # Registry structure:
        # {
        #   'classes': {'ClassName': ClassObj, ...},
        #   'functions': {'function_name': function_obj, ...},
        #   'constants': {'CONSTANT_NAME': value, ...}
        # }
        self._registry: Dict[str, Dict[str, Any]] = {"classes": {}, "functions": {}, "constants": {}}

        # Module registry to track which components come from which modules
        # {
        #   'module.name': {
        #     'classes': ['ClassName1', 'ClassName2', ...],
        #     'functions': ['function_name1', 'function_name2', ...],
        #     'constants': ['CONSTANT_NAME1', 'CONSTANT_NAME2', ...]
        #   }
        # }
        self._module_registry: Dict[str, Dict[str, List[str]]] = {}

        # Import hooks to execute when components are registered
        self._import_hooks: List[Callable[[str, str, Any], None]] = []

    def register_class(
        self, cls: Type[T], module_name: Optional[str] = None
    ) -> Type[T]:
        """
        Register a class with the export manager.

        Args:
            cls: The class to register
            module_name: The name of the module registering the class

        Returns:
            The registered class (unchanged)
        """
        if not inspect.isclass(cls):
            raise TypeError(f"Expected a class, got {type(cls)}")

        class_name = cls.__name__
        self._registry["classes"][class_name] = cls

        # Track in module registry
        if module_name:
            self._track_in_module_registry(module_name, "classes", class_name)

        logger.debug(f"Registered class '{class_name}' from module '{module_name}'")

        # Execute any import hooks
        for hook in self._import_hooks:
            hook("class", class_name, cls)

        return cls

    def register_function(
        self, func: Callable, module_name: Optional[str] = None
    ) -> Callable:
        """
        Register a function with the export manager.

        Args:
            func: The function to register
            module_name: The name of the module registering the function

        Returns:
            The registered function (unchanged)
        """
        if not callable(func) or inspect.isclass(func):
            raise TypeError(f"Expected a function, got {type(func)}")

        func_name = func.__name__
        self._registry["functions"][func_name] = func

        # Track in module registry
        if module_name:
            self._track_in_module_registry(module_name, "functions", func_name)

        logger.debug(f"Registered function '{func_name}' from module '{module_name}'")

        # Execute any import hooks
        for hook in self._import_hooks:
            hook("function", func_name, func)

        return func

    def register_constant(
        self, name: str, value: Any, module_name: Optional[str] = None
    ) -> None:
        """
        Register a constant with the export manager.

        Args:
            name: The name of the constant
            value: The value of the constant
            module_name: The name of the module registering the constant
        """
        self._registry["constants"][name] = value

        # Track in module registry
        if module_name:
            self._track_in_module_registry(module_name, "constants", name)

        logger.debug(f"Registered constant '{name}' from module '{module_name}'")

        # Execute any import hooks
        for hook in self._import_hooks:
            hook("constant", name, value)

    def get_class(self, name: str) -> Optional[Type[Any]]:
        """
        Get a registered class by name.

        Args:
            name: The name of the class to retrieve

        Returns:
            The class if found, None otherwise
        """
        return self._registry["classes"].get(name)

    def get_function(self, name: str) -> Optional[Callable[..., Any]]:
        """
        Get a registered function by name.

        Args:
            name: The name of the function to retrieve

        Returns:
            The function if found, None otherwise
        """
        return self._registry["functions"].get(name)

    def get_constant(self, name: str) -> Optional[Any]:
        """
        Get a registered constant by name.

        Args:
            name: The name of the constant to retrieve

        Returns:
            The constant value if found, None otherwise
        """
        return self._registry["constants"].get(name)

    def get_component(self, name: str) -> Optional[Any]:
        """
        Get a registered component (class, function, or constant) by name.

        Args:
            name: The name of the component to retrieve

        Returns:
            The component if found, None otherwise
        """
        # Try classes first
        component: Optional[Any] = self.get_class(name)
        if component is not None:
            return component

        # Then functions
        component = self.get_function(name)
        if component is not None:
            return component

        # Finally constants
        return self.get_constant(name)

    def list_components(self, component_type: Optional[str] = None) -> List[str]:
        """
        List all registered component names, optionally filtered by type.

        Args:
            component_type: Optional type filter ('classes', 'functions', 'constants')

        Returns:
            List of component names
        """
        if component_type:
            if component_type not in self._registry:
                raise ValueError(f"Invalid component type: {component_type}")
            return list(self._registry[component_type].keys())

        # Return all components if no specific type is requested
        all_components: List[str] = []
        for components in self._registry.values():
            all_components.extend(components.keys())
        return all_components

    def list_modules(self) -> List[str]:
        """
        List all modules that have registered components.

        Returns:
            List of module names
        """
        return list(self._module_registry.keys())

    def get_module_components(self, module_name: str) -> Dict[str, List[str]]:
        """
        Get all components registered by a specific module.

        Args:
            module_name: The name of the module

        Returns:
            Dictionary of component types to lists of component names
        """
        return self._module_registry.get(
            module_name, {"classes": [], "functions": [], "constants": []}
        )

    def register_import_hook(self, hook: Callable[[str, str, Any], None]) -> None:
        """
        Register a hook function to be called when components are registered.

        The hook will be called with (component_type, name, value) arguments.

        Args:
            hook: Function to call when a component is registered
        """
        self._import_hooks.append(hook)

    def _track_in_module_registry(
        self, module_name: str, component_type: str, component_name: str
    ) -> None:
        """
        Track a component in the module registry.

        Args:
            module_name: The name of the module
            component_type: The type of component ('classes', 'functions', 'constants')
            component_name: The name of the component
        """
        if module_name not in self._module_registry:
            self._module_registry[module_name] = {
                "classes": [],
                "functions": [],
                "constants": [],
            }

        if component_name not in self._module_registry[module_name][component_type]:
            self._module_registry[module_name][component_type].append(component_name)

    @classmethod
    def get_instance(cls) -> "ExportManager":
        """Get or create the singleton instance of ExportManager."""
        if cls._instance is None:
            cls._instance = ExportManager()
        return cls._instance

    def register(self, name: str, obj: Any) -> None:
        """
        Register an object with the export manager.
        
        Args:
            name: The name to register the object under
            obj: The object to register
        """
        if name in self._registry:
            logger.warning(f"Overwriting existing export: {name}")
        self._registry[name] = obj
        logger.debug(f"Registered export: {name}")


# Decorator functions for easy registration


def export_class(
    cls: Optional[Type[T]] = None, *, module_name: Optional[str] = None
) -> Callable[[Type[T]], Type[T]] | Type[T]:
    """
    Decorator to register a class with the export manager.

    Can be used with or without arguments:
    @export_class
    class MyClass: ...

    @export_class(module_name='my_module')
    class MyClass: ...

    Args:
        cls: The class to register (when used without parentheses)
        module_name: The name of the module registering the class

    Returns:
        Decorator function or decorated class
    """
    export_manager = ExportManager()

    def decorator(inner_cls: Type[T]) -> Type[T]:
        nonlocal module_name
        if module_name is None:
            module_name = inner_cls.__module__

        return export_manager.register_class(inner_cls, module_name)

    # Handle both @export_class and @export_class(module_name=...)
    if cls is None:
        return decorator
    return decorator(cls)


def export_function(
    func: Optional[Callable] = None, *, module_name: Optional[str] = None
) -> Callable[[Callable], Callable] | Callable:
    """
    Decorator to register a function with the export manager.

    Can be used with or without arguments:
    @export_function
    def my_function(): ...

    @export_function(module_name='my_module')
    def my_function(): ...

    Args:
        func: The function to register (when used without parentheses)
        module_name: The name of the module registering the function

    Returns:
        Decorator function or decorated function
    """
    export_manager = ExportManager()

    def decorator(inner_func: Callable) -> Callable:
        nonlocal module_name
        if module_name is None:
            module_name = inner_func.__module__

        return export_manager.register_function(inner_func, module_name)

    # Handle both @export_function and @export_function(module_name=...)
    if func is None:
        return decorator
    return decorator(func)


def export_constant(name: str, value: Any, module_name: Optional[str] = None) -> None:
    """
    Register a constant with the export manager.

    Args:
        name: The name of the constant
        value: The value of the constant
        module_name: The name of the module registering the constant
    """
    export_manager = ExportManager()

    effective_module_name = module_name
    if effective_module_name is None:
        # Try to infer module name from caller's stack frame
        try:
            frame = inspect.currentframe()
            if frame is not None and frame.f_back is not None:
                module_name_from_globals = frame.f_back.f_globals.get("__name__")
                if module_name_from_globals is not None:
                    effective_module_name = module_name_from_globals
        except Exception as e:
            logger.warning(
                f"Could not automatically determine module name for constant '{name}': {e}"
            )

    export_manager.register_constant(name, value, effective_module_name)
