"""
Task Manager module exports for AMAUTA.

This module registers the task manager components with the export manager.
"""

from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)

# Import but don't export the task_app
from amauta_ai.task_manager.models import (
    ItemType,
    TaskItem,
    TaskPriority,
    TasksModel,
    TaskStatus,
)
from amauta_ai.task_manager.service import TaskManagerService

# Get the export manager instance
export_manager = ExportManager()

# Register classes
export_class(TaskManagerService)
export_class(TaskItem)
export_class(ItemType)
export_class(TaskStatus)
export_class(TaskPriority)
export_class(TasksModel)

# Don't register the task_app as it's a Typer app without a __name__ attribute
# export_function(task_app)

# Register methods from TaskManagerService as standalone functions
export_function(TaskManagerService.get_all_items)
export_function(TaskManagerService.get_item_by_id)
export_function(TaskManagerService.get_next_task)
export_function(TaskManagerService.add_item)
export_function(TaskManagerService.update_item)
export_function(TaskManagerService.delete_item)
export_function(TaskManagerService.set_item_status)
export_function(TaskManagerService.add_dependency)
export_function(TaskManagerService.remove_dependency)
export_function(TaskManagerService.validate_dependencies)
export_function(TaskManagerService.get_metadata)
export_function(TaskManagerService.set_metadata)
export_function(TaskManagerService.get_tasks_model)
export_function(TaskManagerService.save_tasks_model)
export_function(TaskManagerService.get_item)
export_function(TaskManagerService.update_item_status)
export_function(TaskManagerService.get_task_context)

# New hierarchy-related methods
export_function(TaskManagerService.get_children)
export_function(TaskManagerService.get_parent)
export_function(TaskManagerService.get_descendants)
export_function(TaskManagerService.get_ancestors)
