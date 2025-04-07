"""
Base module for task management commands.

This module provides common imports, utilities, and configuration for all command modules.
"""

import datetime
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union, cast
from typing_extensions import Annotated

import typer
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

# Shared console instance
console = Console()

# Safe imports with fallback mechanism
def import_with_fallback(module_name: str, fallback_direct_import: bool = True) -> Any:
    """
    Import a module with fallback to direct import if lazy import fails.
    
    Args:
        module_name: The name of the module to import
        fallback_direct_import: Whether to fall back to direct import if lazy import fails
        
    Returns:
        The imported module
    """
    try:
        # Check if we should use lazy imports
        use_lazy_imports = os.environ.get("AMAUTA_USE_LAZY_IMPORTS", "").lower() in ("true", "1", "yes")
        
        # Special case for modules that have issues with lazy imports
        if (module_name == "amauta_ai.exports.analyzer" or 
            module_name.startswith("amauta_ai.analyzer.") or
            module_name == "amauta_ai.task_manager.template_service"):
            # Always use direct imports for these modules
            return importlib.import_module(module_name)
        
        if use_lazy_imports:
            # Try lazy import first
            try:
                from amauta_ai.imports.lazy_import import lazy_import
                return lazy_import(module_name)
            except Exception as e:
                if not fallback_direct_import:
                    raise e
                # If lazy import fails, fall back to direct import
                print(f"Warning: Lazy import failed for {module_name}, falling back to direct import.")
        
        # Direct import
        return importlib.import_module(module_name)
    except Exception as e:
        print(f"Error importing {module_name}: {e}")
        raise

# Import common services using the fallback mechanism
TaskManagerService = import_with_fallback("amauta_ai.task_manager.service").TaskManagerService
ConfigService = import_with_fallback("amauta_ai.config.service").ConfigService
AiService = import_with_fallback("amauta_ai.ai.service").AiService
AiProvider = import_with_fallback("amauta_ai.ai.service").AiProvider
ProviderCapability = import_with_fallback("amauta_ai.config.models").ProviderCapability
TemplateService = import_with_fallback("amauta_ai.task_manager.template_service").TemplateService
TemplateValidationError = import_with_fallback("amauta_ai.task_manager.template_service").TemplateValidationError

# Import models
from amauta_ai.task_manager.models import (
    ItemType,
    TaskItem,
    TaskPriority,
    TaskStatus,
    TaskTemplate,
)

from amauta_ai.utils.error_handler import friendly_error

# Create Typer app instances for different command groups
task_app = typer.Typer(
    help="Task management commands for tracking and organizing work items",
    no_args_is_help=True,
)

template_app = typer.Typer(
    help="Task template commands for creating and applying task templates",
    no_args_is_help=True,
)

# Add template app as a subcommand to task app
task_app.add_typer(template_app, name="template")

# Common utility functions that are shared across multiple command modules

def get_global_research_flag() -> bool:
    """
    Get the global research flag value set by the --research flag in the main command.
    
    Returns:
        bool: True if the global research flag is enabled, False otherwise
    """
    try:
        # Import here to avoid circular imports
        from amauta_ai.main import global_options
        return global_options.research
    except (AttributeError, ImportError):
        # If global_options is not available or doesn't have the research attribute
        return False

def get_status_icon(status: TaskStatus) -> str:
    """
    Get a status icon for display in tables and trees.
    
    Args:
        status: The task status
        
    Returns:
        A string icon representing the status
    """
    if status == TaskStatus.PENDING:
        return "⏱️"
    elif status == TaskStatus.IN_PROGRESS:
        return "🔄"
    elif status == TaskStatus.DONE:
        return "✅"
    elif status == TaskStatus.DEFERRED:
        return "⏸️"
    return "❓"

def get_priority_icon(priority: TaskPriority) -> str:
    """
    Get a priority icon for display in tables and trees.
    
    Args:
        priority: The task priority
        
    Returns:
        A string icon representing the priority
    """
    if priority == TaskPriority.CRITICAL:
        return "🔴"
    elif priority == TaskPriority.HIGH:
        return "🟠"
    elif priority == TaskPriority.MEDIUM:
        return "🟡"
    elif priority == TaskPriority.LOW:
        return "🟢"
    return "❓"

def get_type_icon(item_type: ItemType) -> str:
    """
    Get an item type icon for display in tables and trees.
    
    Args:
        item_type: The item type
        
    Returns:
        A string icon representing the item type
    """
    if item_type == ItemType.EPIC:
        return "📚"
    elif item_type == ItemType.STORY:
        return "📝"
    elif item_type == ItemType.TASK:
        return "📋"
    elif item_type == ItemType.ISSUE:
        return "🐛"
    return "❓"

def format_id(item_id: str) -> str:
    """
    Format an item ID for display with consistent styling.
    
    Args:
        item_id: The item ID
        
    Returns:
        A formatted item ID string
    """
    return f"[cyan]{item_id}[/cyan]"

def confirm_action(message: str, default: bool = False) -> bool:
    """
    Prompt the user to confirm an action.
    
    Args:
        message: The confirmation message
        default: The default value if the user just presses Enter
        
    Returns:
        True if confirmed, False otherwise
    """
    return Confirm.ask(message, default=default)

def create_spinner(message: str) -> Progress:
    """
    Create a spinner progress indicator with the given message.
    
    Args:
        message: The message to display with the spinner
        
    Returns:
        A Progress object with a spinner
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        console=console,
    )

def create_items_table(title: str = "Items", include_details: bool = False, include_counts: bool = False) -> Table:
    """
    Create a consistent table for displaying items.
    
    Args:
        title: The table title
        include_details: Whether to include a column showing the beginning of item details
        include_counts: Whether to include columns with dependency and children counts
        
    Returns:
        A configured Table object
    """
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Title", style="white")
    
    # Add the additional columns if requested
    if include_details:
        table.add_column("Details", style="dim", max_width=30)
    
    if include_counts:
        table.add_column("Deps", justify="right", style="magenta")
        table.add_column("Children", justify="right", style="magenta")
    
    return table

def resolve_task_reference(reference: str) -> str:
    """
    Resolve a task reference that could be either a direct ID or dot notation.
    
    This function acts as an extension point that allows commands to accept
    both direct task IDs and dot notation references.
    
    Args:
        reference: The task reference (either a task ID or dot notation)
        
    Returns:
        The resolved task ID
        
    Raises:
        ValueError: If the reference is invalid or cannot be resolved
    """
    task_manager = TaskManagerService()
    
    # First check if it's a direct ID
    item = task_manager.get_item_by_id(reference)
    if item:
        return reference
        
    # Try to resolve as dot notation
    try:
        return task_manager.resolve_dot_notation(reference)
    except Exception as e:
        # Convert to a friendlier error message
        raise ValueError(f"Invalid task reference '{reference}': {str(e)}")

# Export these for use in other modules
__all__ = [
    # Imported services
    "TaskManagerService",
    "ConfigService",
    "AiService",
    "AiProvider",
    "ProviderCapability",
    "TemplateService",
    "TemplateValidationError",
    
    # Imported models
    "ItemType",
    "TaskItem",
    "TaskPriority",
    "TaskStatus",
    "TaskTemplate",
    
    # Typer apps
    "task_app",
    "template_app",
    
    # Utilities
    "console",
    "friendly_error",
    "import_with_fallback",
    "get_status_icon",
    "get_priority_icon",
    "get_type_icon",
    "format_id",
    "confirm_action",
    "create_spinner",
    "create_items_table",
    "resolve_task_reference",
] 