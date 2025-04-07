"""
Task management commands for AMAUTA CLI.

This module provides commands for creating, organizing, and tracking development tasks.
THIS FILE IS FOR BACKWARD COMPATIBILITY ONLY.
All functionality has been moved to the amauta_ai.task_manager.commands subpackage.
"""

import sys
import warnings

# Issue a deprecation warning but only once per session
warnings.filterwarnings('once', 
    message='Direct imports from amauta_ai.task_manager.commands are deprecated. ' +
            'Import from amauta_ai.task_manager.commands submodules instead.',
    category=DeprecationWarning)

# Re-export everything from the new module structure
from amauta_ai.task_manager.commands import (
    # Typer apps
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
    
    # Status commands
    set_item_status,
    status_report,
    status_validate,
    next_task,
    bulk_operations,
    
    # Template commands
    create_template,
    list_templates,
    show_template,
    apply_template,
    delete_template,
    
    # Import/Export commands
    export_tasks,
    import_tasks,
    export_templates,
    import_templates,
    
    # AI-assisted commands
    add_task_with_ai,
    update_task_with_ai,
    expand_task_with_ai,
    analyze_complexity,
    generate_tasks_from_prompt,
)

# Include utilities from base.py that were in the original file
from amauta_ai.task_manager.commands.base import import_with_fallback

# Export everything
__all__ = [
    # Utility functions
    "import_with_fallback",
    
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
    
    # Status commands
    "set_item_status",
    "status_report",
    "status_validate",
    "next_task",
    "bulk_operations",
    
    # Template commands
    "create_template",
    "list_templates",
    "show_template",
    "apply_template",
    "delete_template",
    
    # Import/Export commands
    "export_tasks",
    "import_tasks",
    "export_templates",
    "import_templates",
    
    # AI-assisted commands
    "add_task_with_ai",
    "update_task_with_ai",
    "expand_task_with_ai",
    "analyze_complexity",
    "generate_tasks_from_prompt",
] 