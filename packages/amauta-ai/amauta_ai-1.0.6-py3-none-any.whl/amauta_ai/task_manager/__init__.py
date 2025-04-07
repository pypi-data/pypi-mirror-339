"""
The Task Manager module handles all task-related operations and commands.
"""
from typing import Any, Dict, List, Optional, Union

# Import models safely
try:
    from amauta_ai.task_manager.models import (
        ItemType,
        TaskStatus,
        TaskItem,
        TasksModel,
        TaskPriority,
        TaskTemplate,
        TemplatesModel
    )
except ImportError as e:
    import logging
    logging.getLogger(__name__).warning(f"Failed to import task models: {e}")

# Expose the service safely
try:
    from amauta_ai.task_manager.service import TaskManagerService
except ImportError as e:
    import logging
    logging.getLogger(__name__).warning(f"Failed to import TaskManagerService: {e}")

# Import template service (with fallback)
try:
    try:
        # First try the original module
        from amauta_ai.task_manager.template_service import TemplateService
    except ImportError:
        # Try the fallback module
        try:
            import os
            import sys
            
            # Create the template_service.py from fallback if needed
            current_dir = os.path.dirname(__file__)
            template_service_path = os.path.join(current_dir, 'template_service.py')
            fallback_path = os.path.join(current_dir, 'template_service_fallback.py')
            
            if not os.path.exists(template_service_path) and os.path.exists(fallback_path):
                print(f"Creating {template_service_path} from {fallback_path}")
                with open(fallback_path, 'r') as src:
                    with open(template_service_path, 'w') as dst:
                        dst.write(src.read())
                
            # Now try to import again
            from amauta_ai.task_manager.template_service import TemplateService
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Failed to create template_service.py: {e}")
            
            # Provide a minimal fallback
            class TemplateService:
                """Minimal fallback for TemplateService"""
                def __init__(self, *args, **kwargs):
                    self.templates = {}
except Exception as e:
    import logging
    logging.getLogger(__name__).error(f"Failed to import or create TemplateService: {e}")
    
    # Provide a minimal fallback
    class TemplateService:
        """Minimal fallback for TemplateService"""
        def __init__(self, *args, **kwargs):
            self.templates = {}

# Re-export from commands/ directory
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
    
    # AI commands
    add_task_with_ai,
    update_task_with_ai,
    update_task_cascade_with_ai,
    expand_task_with_ai,
    analyze_complexity,
    generate_tasks_from_prompt,
    
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
    
    # File commands
    generate_files
)

__all__ = [
    # Typer apps
    "task_app",
    "template_app",
    
    # Models
    "ItemType",
    "TaskStatus",
    "TaskItem",
    "TasksModel",
    "TaskPriority",
    "TaskTemplate",
    "TemplatesModel",
    
    # Services
    "TaskManagerService",
    "TemplateService",
    
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
    
    # AI commands
    "add_task_with_ai",
    "update_task_with_ai",
    "update_task_cascade_with_ai",
    "expand_task_with_ai",
    "analyze_complexity",
    "generate_tasks_from_prompt",
    
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
    
    # File commands
    "generate_files"
]
