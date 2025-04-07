"""
MCP module exports for AMAUTA.

This module registers the MCP components with the export manager.
"""

from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)

# Import but don't export the Typer app
from amauta_ai.mcp.command import run, version
from amauta_ai.mcp.server import McpServer, run_mcp_server

# Get the export manager instance
export_manager = ExportManager()

# Register classes
export_class(McpServer)

# Register functions
export_function(run_mcp_server)
# Don't register Typer app as it doesn't have __name__ attribute
# export_function(mcp_app)
export_function(run)
export_function(version)

# Register methods from McpServer as standalone functions
export_function(McpServer.run)
export_function(McpServer.handle_request)
export_function(McpServer._handle_ping)
export_function(McpServer._handle_get_tasks)
export_function(McpServer._handle_get_task)
export_function(McpServer._handle_get_next_task)
export_function(McpServer._handle_set_task_status)
export_function(McpServer._handle_expand_task)
export_function(McpServer._handle_analyze)
export_function(McpServer._handle_get_task_context)
export_function(McpServer._handle_generate_code)
