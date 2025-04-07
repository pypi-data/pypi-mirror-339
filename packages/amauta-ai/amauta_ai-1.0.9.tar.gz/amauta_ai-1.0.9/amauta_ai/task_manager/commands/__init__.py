"""
Task management commands for AMAUTA CLI.

This is a new modular implementation of the commands that were previously in commands.py.
The modules are organized by command category for better maintainability.
"""

# Import the base module for shared functionality
from amauta_ai.task_manager.commands.base import (
    # Typer apps for CLI command groups
    task_app,
    template_app,
)

# Import commands from modules
from amauta_ai.task_manager.commands.list_commands import list_items, show_item
from amauta_ai.task_manager.commands.dependency_commands import (
    add_dependency,
    remove_dependency,
    batch_remove_dependencies,
    validate_dependencies,
    analyze_dependencies,
    fix_dependencies,
)
from amauta_ai.task_manager.commands.status_commands import (
    set_item_status,
    status_report,
    status_validate,
    next_task,
    bulk_operations,
)
from amauta_ai.task_manager.commands.template_commands import (
    create_template,
    list_templates,
    show_template,
    apply_template,
    delete_template,
)
from amauta_ai.task_manager.commands.import_export import (
    export_tasks,
    import_tasks,
    export_templates,
    import_templates,
)
from amauta_ai.task_manager.commands.ai_commands import (
    add_task_with_ai,
    update_task_with_ai,
    update_task_cascade_with_ai,
    expand_task_with_ai,
    analyze_complexity,
    generate_tasks_from_prompt,
)
from amauta_ai.task_manager.commands.file_commands import (
    file_commands_app,
    generate_files,
)

# Import dot notation commands
from amauta_ai.task_manager.commands.dot_notation import (
    dot_notation_app,
    resolve_reference,
    show_by_reference,
    suggest_completions,
    set_status_by_reference,
    init as init_dot_notation,
)

# Initialize dot notation commands
init_dot_notation()

# Add file commands to task_app
task_app.add_typer(file_commands_app, name="file")

# Also register generate-files command directly at the task_app level for backward compatibility
task_app.command("generate-files")(generate_files)

# Register list command directly at the task_app level
task_app.command("list")(list_items)

# Export all commands for backward compatibility
__all__ = [
    # Typer apps
    "task_app",
    "template_app",
    "dot_notation_app",
    "file_commands_app",
    
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
    "update_task_cascade_with_ai",
    "expand_task_with_ai",
    "analyze_complexity",
    "generate_tasks_from_prompt",
    
    # File commands
    "generate_files",
    
    # Dot notation commands
    "resolve_reference",
    "show_by_reference",
    "suggest_completions",
    "set_status_by_reference",
] 