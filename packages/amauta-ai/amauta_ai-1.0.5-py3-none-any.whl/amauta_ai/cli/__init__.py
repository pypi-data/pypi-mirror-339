"""Command line interface for AMAUTA."""

import logging
import os

# import sys  # Removed unused import
from typing import List, Optional

import typer

# Setup basic logging
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger("amauta")

from amauta_ai.cli.commands import *
from amauta_ai.cli.commands.config import *
from amauta_ai.cli.commands.config import config_group


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the AMAUTA CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Ensure imports are initialized
        from amauta_ai.imports import initialize_imports

        initialize_imports()

        # Import app only after imports are initialized
        from amauta_ai.main import app

        # Run the app
        return app(args)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        logger.warning("Operation interrupted by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        if os.environ.get("AMAUTA_DEBUG", "").lower() in ("true", "1", "yes"):
            # Show traceback in debug mode
            import traceback

            traceback.print_exc()
        return 1


__all__ = ["main", "config_group"]
