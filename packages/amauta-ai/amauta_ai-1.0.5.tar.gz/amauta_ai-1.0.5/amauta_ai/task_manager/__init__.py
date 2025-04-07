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

# Import models
from amauta_ai.task_manager.models import (
    Epic,
    Issue,
    Item,
    ItemType,
    Story,
    Task,
    TaskStatus,
    TaskWithChildren
)

# Expose the service
from amauta_ai.task_manager.service import TaskManagerService

# Expose commands
from amauta_ai.task_manager.commands import (
    add_dependency,
    add_task,
    analyze_complexity,
    clear_subtasks,
    complexity_report,
    create_item_from_template,
    display_item,
    expand_task,
    filter_tasks,
    fix_dependencies,
    list_tasks,
    next_task,
    remove_dependency,
    set_status,
    status_report,
    update_task,
    validate_dependencies,
)

# Import template service with fallback
try:
    from amauta_ai.task_manager.template_service import TemplateService
except ImportError:
    try:
        from amauta_ai.task_manager.template_service_fallback import TemplateService
        import logging
        logging.getLogger(__name__).warning("Using fallback TemplateService")
    except ImportError:
        import logging
        logging.getLogger(__name__).error("Failed to import TemplateService and fallback")
        
        class TemplateService:
            """Minimal stub for TemplateService when not available"""
            def __init__(self, *args, **kwargs):
                self.templates = {}

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
