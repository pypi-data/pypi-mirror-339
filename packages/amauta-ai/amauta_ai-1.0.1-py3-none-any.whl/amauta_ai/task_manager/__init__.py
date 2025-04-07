"""
Task manager package for AMAUTA.

This package provides functionality for managing project tasks, including creating,
organizing, and tracking development tasks.
"""

# Re-export from commands.py for backward compatibility
# This will be updated to import from commands/ directory after full refactoring
from amauta_ai.task_manager.commands import (
    task_app,
    template_app,
    
    # List and show commands
    list_items,
    show_item,
    
    # Dependency commands
    add_dependency,
    remove_dependency,
    batch_remove_dependencies,
    validate_dependencies,
    analyze_dependencies,
    fix_dependencies,
)

# Import template_service
from amauta_ai.task_manager.template_service import *

__all__ = [
    # Typer apps
    "task_app",
    "template_app",
    
    # List and show commands
    "list_items",
    "show_item",
    
    # Dependency commands
    "add_dependency",
    "remove_dependency",
    "batch_remove_dependencies",
    "validate_dependencies",
    "analyze_dependencies",
    "fix_dependencies",
]
