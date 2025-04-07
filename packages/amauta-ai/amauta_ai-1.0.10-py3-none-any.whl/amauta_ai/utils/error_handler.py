"""
Error handling utilities for AMAUTA.

This module provides decorators and context managers for handling errors
in a user-friendly way, with appropriate logging and rich formatting.
"""

import functools
import logging
import sys
import traceback
from contextlib import contextmanager
from typing import Any, Callable, Optional, TypeVar, cast

import typer
from rich.console import Console
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console(stderr=True)

# Type variable for function decorators
F = TypeVar("F", bound=Callable[..., Any])


def friendly_error(
    message: Optional[str] = None,
    exit_code: int = 1,
    log_traceback: bool = True,
    show_traceback: bool = False,
) -> Callable[[F], F]:
    """
    Decorator for handling exceptions in a user-friendly way.

    Args:
        message: Custom error message prefix (defaults to the exception message)
        exit_code: Exit code to use when errors occur
        log_traceback: Whether to log the traceback
        show_traceback: Whether to show the traceback to the user

    Returns:
        Decorated function that handles exceptions gracefully
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except typer.Exit:
                # Let typer handle this normally
                raise
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                console.print("\n[yellow]Operation interrupted by user[/]")
                sys.exit(130)  # Standard exit code for SIGINT
            except Exception as e:
                # Get the exception details
                exc_type, exc_value, exc_traceback = sys.exc_info()

                # Log the error
                if log_traceback:
                    logger.error(
                        f"Error in {func.__name__}: {str(e)}",
                        exc_info=(exc_type, exc_value, exc_traceback),
                    )

                # Display user-friendly error
                error_title = message or f"[red bold]Error:[/] {str(e)}"

                if show_traceback or _debug_mode():
                    # Show traceback in debug mode or if explicitly requested
                    tb_str = "".join(
                        traceback.format_exception(exc_type, exc_value, exc_traceback)
                    )
                    console.print(
                        Panel(
                            f"{error_title}\n\n[dim]{tb_str}[/]",
                            title="[red]Error Details[/]",
                            border_style="red",
                        )
                    )
                else:
                    console.print(f"[red bold]Error:[/] {str(e)}")
                    console.print(
                        "[dim]Run with AMAUTA_DEBUG=1 to see the full traceback.[/]"
                    )

                # Exit with the specified code
                sys.exit(exit_code)

        return cast(F, wrapper)

    return decorator


@contextmanager
def error_context(
    message: str = "An error occurred",
    exit_code: int = 1,
    log_traceback: bool = True,
    show_traceback: bool = False,
):
    """
    Context manager for handling exceptions in a user-friendly way.

    Args:
        message: Custom error message prefix
        exit_code: Exit code to use when errors occur
        log_traceback: Whether to log the traceback
        show_traceback: Whether to show the traceback to the user
    """
    try:
        yield
    except typer.Exit:
        # Let typer handle this normally
        raise
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.print("\n[yellow]Operation interrupted by user[/]")
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        # Get the exception details
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # Log the error
        if log_traceback:
            logger.error(
                f"{message}: {str(e)}",
                exc_info=(exc_type, exc_value, exc_traceback),
            )

        # Display user-friendly error
        if show_traceback or _debug_mode():
            # Show traceback in debug mode or if explicitly requested
            tb_str = "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )
            console.print(
                Panel(
                    f"{message}: {str(e)}\n\n[dim]{tb_str}[/]",
                    title="[red]Error Details[/]",
                    border_style="red",
                )
            )
        else:
            console.print(f"[red bold]Error:[/] {str(e)}")
            console.print("[dim]Run with AMAUTA_DEBUG=1 to see the full traceback.[/]")

        # Exit with the specified code
        sys.exit(exit_code)


def _debug_mode() -> bool:
    """Check if debug mode is enabled via environment variable."""
    import os

    return os.environ.get("AMAUTA_DEBUG", "").lower() in ("true", "1", "yes")
