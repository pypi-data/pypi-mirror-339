"""
Dot notation access commands for task references.

These commands allow users to access tasks using a simplified dot notation
(e.g., EPIC1.TASK2.STORY3) directly within AMAUTA commands.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from typing import List, Optional

from amauta_ai.task_manager.service import TaskManagerService
from amauta_ai.task_manager.commands.utils import (
    DotNotationError,
    AmbiguousReferenceError,
    ReferenceNotFoundError,
    InvalidReferenceFormatError,
)
from amauta_ai.task_manager.commands.item_display import format_task_item

# Create a Typer app for dot notation commands
dot_notation_app = typer.Typer(
    help="Access tasks using simplified dot notation (e.g., EPIC1.TASK2.STORY3)",
    name="dot",
)

console = Console()


@dot_notation_app.command("resolve")
def resolve_reference(
    reference: str = typer.Argument(..., help="Dot notation reference to resolve (e.g., EPIC1.TASK2)"),
):
    """
    Resolve a dot notation reference to a task ID.
    
    Example: amauta task dot resolve EPIC1.TASK2
    """
    try:
        task_manager = TaskManagerService()
        resolved_id = task_manager.resolve_dot_notation(reference)
        console.print(f"Reference [bold cyan]{reference}[/] resolves to: [bold green]{resolved_id}[/]")
    except AmbiguousReferenceError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        console.print("\nPossible matches:")
        for match in e.matches:
            console.print(f"  - [cyan]{match}[/]")
    except ReferenceNotFoundError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
    except InvalidReferenceFormatError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


@dot_notation_app.command("show")
def show_by_reference(
    reference: str = typer.Argument(..., help="Dot notation reference to show (e.g., EPIC1.TASK2)"),
):
    """
    Show a task using dot notation reference.
    
    Example: amauta task dot show EPIC1.TASK2
    """
    try:
        task_manager = TaskManagerService()
        item_id = task_manager.resolve_dot_notation(reference)
        item = task_manager.get_item_by_id(item_id)
        
        if not item:
            console.print(f"[bold red]Error:[/] Task with ID '{item_id}' not found.")
            return
            
        # Format and display the task
        formatted_item = format_task_item(item, task_manager)
        console.print(formatted_item)
        
    except DotNotationError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


@dot_notation_app.command("complete")
def suggest_completions(
    partial_reference: str = typer.Argument(..., help="Partial dot notation reference to complete"),
    limit: int = typer.Option(10, help="Maximum number of suggestions to display"),
):
    """
    Suggest completions for a partial dot notation reference.
    
    Example: amauta task dot complete EPIC1.T
    """
    try:
        task_manager = TaskManagerService()
        suggestions = task_manager.suggest_dot_notation_completions(partial_reference)
        
        if suggestions:
            console.print(f"Completions for [bold cyan]{partial_reference}[/]:")
            for i, suggestion in enumerate(suggestions[:limit], 1):
                console.print(f"  {i}. [cyan]{suggestion}[/]")
                
            if len(suggestions) > limit:
                console.print(f"  ... and {len(suggestions) - limit} more")
        else:
            console.print(f"No completions found for [bold cyan]{partial_reference}[/]")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


@dot_notation_app.command("set-status")
def set_status_by_reference(
    reference: str = typer.Argument(..., help="Dot notation reference to the task"),
    status: str = typer.Argument(..., help="New status (pending, in-progress, done, deferred)"),
    cascade: bool = typer.Option(False, "--cascade", "-c", help="Update status of dependent items"),
):
    """
    Set the status of a task using dot notation reference.
    
    Example: amauta task dot set-status EPIC1.TASK2 done
    """
    try:
        task_manager = TaskManagerService()
        item_id = task_manager.resolve_dot_notation(reference)
        
        # Reuse the existing set_item_status logic
        from amauta_ai.task_manager.commands.status_commands import set_item_status
        set_item_status(item_id=item_id, status=status, cascade=cascade)
        
    except DotNotationError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


# Initialize function called by __init__.py
def init():
    """Initialize the dot notation commands module."""
    # This function will be called when the module is imported
    from amauta_ai.task_manager.commands.base import task_app
    task_app.add_typer(dot_notation_app) 