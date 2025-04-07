"""
Console utilities for AMAUTA.

This module contains various utility functions for console operations,
including spinners, progress bars, and confirmations.
"""

import os
import typer
from typing import Optional, List, Any, Callable
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from contextlib import contextmanager
from amauta_ai.task_manager.models import TaskPriority, ItemType

# Create a shared console instance
console = Console()

@contextmanager
def create_spinner(message: str):
    """Create a spinner with the specified message."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task(description=message, total=None)
        try:
            yield progress
        finally:
            progress.stop_task(task)

def confirm_action(message: str, default: bool = False) -> bool:
    """Ask for user confirmation with a message."""
    return typer.confirm(message, default=default)

def format_id(id_str: str) -> str:
    """Format an ID with appropriate color."""
    if id_str.startswith("EPIC"):
        return f"[bold purple]{id_str}[/bold purple]"
    elif id_str.startswith("TASK"):
        return f"[bold blue]{id_str}[/bold blue]"
    elif id_str.startswith("STORY"):
        return f"[bold green]{id_str}[/bold green]"
    elif id_str.startswith("ISSUE"):
        return f"[bold red]{id_str}[/bold red]"
    else:
        return f"[bold]{id_str}[/bold]"

def get_priority_icon(priority: TaskPriority) -> str:
    """Get an icon representing a priority level."""
    if priority == TaskPriority.CRITICAL:
        return "🔴"
    elif priority == TaskPriority.HIGH:
        return "🟠"
    elif priority == TaskPriority.MEDIUM:
        return "🟡"
    elif priority == TaskPriority.LOW:
        return "🟢"
    else:
        return "⚪"

def get_type_icon(item_type: ItemType) -> str:
    """Get an icon representing an item type."""
    if item_type == ItemType.EPIC:
        return "🏆"
    elif item_type == ItemType.TASK:
        return "📋"
    elif item_type == ItemType.STORY:
        return "📖"
    elif item_type == ItemType.ISSUE:
        return "🐞"
    else:
        return "📄" 