"""MCP module for Cursor integration."""

from amauta_ai.mcp.command import mcp_app
from amauta_ai.mcp.server import McpServer, run_mcp_server

__all__ = ["McpServer", "run_mcp_server", "mcp_app"]
