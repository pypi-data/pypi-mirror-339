"""Command-line interface for the MCP module."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from typing_extensions import Annotated

# Import the run_mcp_server function at the module level
from amauta_ai.mcp.server import run_mcp_server
from amauta_ai.utils.error_handler import friendly_error

mcp_app = typer.Typer(
    name="mcp",
    help="Model Control Protocol (MCP) for Cursor integration",
    no_args_is_help=True,
)

console = Console(stderr=True)  # Initialize console to output to stderr by default


@mcp_app.callback()
def callback() -> None:
    """Model Control Protocol (MCP) for Cursor integration."""
    pass


@mcp_app.command("run")
@friendly_error("Failed to start MCP server")
def run(
    config_file: Annotated[
        Optional[Path],
        typer.Option(
            help="Path to the .amautarc.yaml configuration file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ] = None,
    tasks_file: Annotated[
        Optional[Path],
        typer.Option(
            help="Path to the tasks.json file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ] = None,
) -> None:
    """
    Run the MCP server for Cursor integration.

    This command starts a server that communicates with Cursor IDE
    using stdin/stdout according to the Model Control Protocol.
    """
    # We don't use typer.echo here because all stdout is reserved for MCP
    console.print("Starting AMAUTA MCP server...")
    # Call the imported function directly, passing the paths
    run_mcp_server(amautarc_path=config_file, tasks_json_path=tasks_file)


@mcp_app.command("version")
@friendly_error("Failed to show MCP version")
def version() -> None:
    """Show the MCP protocol version supported by AMAUTA."""
    console.print("AMAUTA MCP Protocol version: 1.0.0")
    console.print("Compatible with Cursor MCP version: 1.0")
