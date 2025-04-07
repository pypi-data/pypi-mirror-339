"""Helper utility functions for AMAUTA.

This module provides various utility functions used throughout the AMAUTA project.
"""

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from amauta_ai.utils.logger import get_logger

# Setup logger
logger = get_logger(__name__)

# Type variables for generic functions
T = TypeVar("T")


def is_offline_mode() -> bool:
    """Check if application is running in offline mode.
    
    Offline mode is activated by setting the AMAUTA_OFFLINE environment variable
    or using the --offline flag in CLI commands.
    
    Returns:
        bool: True if offline mode is active, False otherwise
    """
    return os.environ.get("AMAUTA_OFFLINE", "0").lower() in ("1", "true", "yes")


def is_debug_mode() -> bool:
    """Check if application is running in debug mode.
    
    Debug mode is activated by setting the AMAUTA_DEBUG environment variable.
    
    Returns:
        bool: True if debug mode is active, False otherwise
    """
    return os.environ.get("AMAUTA_DEBUG", "0").lower() in ("1", "true", "yes")


def create_spinner(text: str) -> Progress:
    """Create a spinner for displaying progress during long-running operations.
    
    Args:
        text (str): The text to display next to the spinner
        
    Returns:
        Progress: A rich Progress object with a spinner configuration
    """
    return Progress(
        SpinnerColumn(),
        TextColumn(f"[bold blue]{text}[/bold blue]"),
        transient=True,
    )


def run_with_spinner(func: Callable[..., T], text: str, *args: Any, **kwargs: Any) -> T:
    """Run a function with a spinner indicating progress.
    
    Args:
        func: The function to run
        text: The text to display next to the spinner
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The return value of the function
    """
    spinner = create_spinner(text)
    with spinner:
        spinner.start()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            spinner.stop()


def create_table(title: str, columns: List[str]) -> Table:
    """Create a rich formatted table.
    
    Args:
        title (str): The title of the table
        columns (List[str]): The column names
        
    Returns:
        Table: A rich Table object
    """
    table = Table(title=title)
    for column in columns:
        table.add_column(column, style="cyan", no_wrap=True)
    return table


def print_info(message: str) -> None:
    """Print an informational message.
    
    Args:
        message (str): The message to print
    """
    console = Console()
    console.print(f"[bold blue]Info:[/bold blue] {message}")


def print_success(message: str) -> None:
    """Print a success message.
    
    Args:
        message (str): The message to print
    """
    console = Console()
    console.print(f"[bold green]Success:[/bold green] {message}")


def print_warning(message: str) -> None:
    """Print a warning message.
    
    Args:
        message (str): The message to print
    """
    console = Console()
    console.print(f"[bold yellow]Warning:[/bold yellow] {message}")


def print_error(message: str) -> None:
    """Print an error message.
    
    Args:
        message (str): The message to print
    """
    console = Console()
    console.print(f"[bold red]Error:[/bold red] {message}")


def execute_in_parallel(func: Callable[[Any], T], items: List[Any], max_workers: int = None) -> List[T]:
    """Execute a function in parallel for multiple items.
    
    Args:
        func (callable): The function to execute
        items (list): The items to process
        max_workers (int, optional): Maximum number of worker threads
        
    Returns:
        List[T]: The list of results
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(func, items))


def confirm_action(message: str, default: bool = False) -> bool:
    """Ask for user confirmation before proceeding with an action.
    
    Args:
        message (str): The confirmation message
        default (bool): Default response if user just presses Enter
        
    Returns:
        bool: True if confirmed, False otherwise
    """
    return typer.confirm(message, default=default)


def select_option(message: str, options: List[str], default: Optional[str] = None) -> str:
    """Ask user to select an option from a list.
    
    Args:
        message (str): The prompt message
        options (List[str]): Available options
        default (str, optional): Default option
        
    Returns:
        str: Selected option
    """
    return typer.prompt(
        message,
        type=typer.Choice(options),
        default=default or options[0],
        show_choices=True,
    )


def get_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with an optional default value.
    
    Args:
        prompt (str): The prompt message
        default (str, optional): Default value if user just presses Enter
        
    Returns:
        str: User input
    """
    return typer.prompt(prompt, default=default or "") 