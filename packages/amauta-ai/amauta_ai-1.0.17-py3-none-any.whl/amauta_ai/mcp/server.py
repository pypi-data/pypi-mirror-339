"""
MCP (Model Control Protocol) server implementation for Cursor integration.

This module implements the server component that allows Cursor to interact with 
AMAUTA via the Model Control Protocol. It receives JSON requests via stdin and
responds via stdout, handling various operations like task management and code analysis.
"""

import json
import logging
import os
import select
import sys
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from amauta_ai.ai.service import AiProvider, AiService
from amauta_ai.analyzer.service import AnalyzerService
from amauta_ai.config.service import ConfigService
from amauta_ai.task_manager.models import ItemType, TaskStatus
from amauta_ai.task_manager.service import TaskManagerService
from amauta_ai.utils.logger import get_logger

logger = get_logger(__name__)


def _get_required_param(params: Dict[str, Any], param_name: str) -> Any:
    """
    Get a required parameter from the params dictionary or raise an error.

    Args:
        params: The parameters dictionary.
        param_name: The name of the required parameter.

    Returns:
        The parameter value.

    Raises:
        ValueError: If the parameter is missing.
    """
    if param_name not in params:
        raise ValueError(f"Missing required parameter '{param_name}'")
    return params[param_name]


def _get_language_from_extension(extension: str) -> str:
    """
    Infer programming language from file extension.
    
    Args:
        extension: The file extension (including the dot)
        
    Returns:
        The inferred language name, defaults to "python" if unknown
    """
    language_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript", 
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".go": "go",
        ".rs": "rust",
    }
    return language_map.get(extension, "python")  # Default to python


class ServerError(Exception):
    """Error raised by the server when processing a request."""

    pass


class AmautaJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for AMAUTA objects."""

    def default(self, obj):
        """Convert custom objects to JSON serializable types."""
        # Handle Pydantic models (TaskItem, etc.)
        if hasattr(obj, "model_dump"):
            return obj.model_dump()

        # Handle Path objects
        if isinstance(obj, Path):
            return str(obj)

        # Handle Enum values
        if hasattr(obj, "value") and not isinstance(obj, type):
            return obj.value

        # Let the base class handle other types or raise TypeError
        return super().default(obj)


class McpServer:
    """
    Model Control Protocol server for Cursor integration.

    This class handles JSON-RPC style requests from Cursor over stdin/stdout,
    providing a programmatic interface to AMAUTA's functionality.
    """

    def __init__(
        self,
        amautarc_path: Optional[Path] = None,
        tasks_json_path: Optional[Path] = None,
    ):
        """
        Initialize the MCP server.

        Args:
            amautarc_path: Path to the .amautarc.yaml configuration file.
            tasks_json_path: Path to the tasks.json file.
        """
        # Convert paths to strings or use None
        amautarc_path_str = str(amautarc_path) if amautarc_path else None
        tasks_json_path_str = str(tasks_json_path) if tasks_json_path else None

        # Initialize services
        self.config_service = ConfigService(config_path=amautarc_path_str)
        self.config = self.config_service.get_config()
        self.ai_service = AiService(self.config_service)
        self.task_service = TaskManagerService(tasks_file=tasks_json_path_str)

        # Initialize logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # Map request types to their handler methods
        self.handlers: Dict[str, Callable] = {
            "ping": self._handle_ping,
            "get_tasks": self._handle_get_tasks,
            "get_task": self._handle_get_task,
            "get_next_task": self._handle_get_next_task,
            "set_task_status": self._handle_set_task_status,
            "expand_task": self._handle_expand_task,
            "analyze": self._handle_analyze,
            "get_task_context": self._handle_get_task_context,
            "generate_code": self._handle_generate_code,
        }

    def run(self) -> None:
        """
        Run the MCP server, processing input from stdin and producing output to stdout.
        """
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)

                # Print response as JSON using our custom encoder
                print(json.dumps(response, cls=AmautaJSONEncoder), flush=True)

            except json.JSONDecodeError:
                error_response = {
                    "error": {
                        "code": -32700,
                        "message": "Parse error: Invalid JSON was received",
                    }
                }
                print(json.dumps(error_response), flush=True)

            except Exception as e:
                error_response = {
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}",
                        "data": traceback.format_exc(),
                    }
                }
                print(json.dumps(error_response), flush=True)

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming request and return a response.

        Args:
            request: The parsed JSON request dictionary

        Returns:
            A response dictionary to be serialized as JSON
        """
        # Extract request components
        request_type = request.get("type")
        request_id = request.get("id")
        params = request.get("params", {})

        # Validate request
        if not request_type:
            return {
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "Invalid request: Missing 'type' field",
                },
            }

        # Find appropriate handler
        handler = self.handlers.get(request_type)
        if not handler:
            return {
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: Unknown request type '{request_type}'",
                },
            }

        # Execute handler
        try:
            result = handler(params)
            return {
                "id": request_id,
                "result": result,
            }
        except Exception as e:
            # Log error to stderr (won't interfere with protocol)
            print(f"Error handling request: {str(e)}", file=sys.stderr)

            # Make sure we return an error response that has the "error" key
            error_response = {
                "id": request_id,
                "error": {
                    "code": -32000,
                    "message": f"Server error: {str(e)}",
                    "data": traceback.format_exc(),
                },
            }
            return error_response

    def _handle_ping(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a ping request to check server is alive."""
        return {"status": "ok", "version": "1.0.0"}

    def _handle_get_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to get all tasks, optionally filtered by status.

        Args:
            params: Request parameters including optional 'status' filter

        Returns:
            Dictionary with list of tasks
        """
        status_filter = params.get("status")
        items = self.task_service.get_all_items()

        if status_filter:
            # Convert string to enum value if needed
            try:
                status_enum = TaskStatus(status_filter)
                items = [i for i in items if i.status == status_enum]
            except ValueError:
                # Invalid status, just use string comparison as fallback
                items = [i for i in items if i.status.value == status_filter]

        return {"tasks": items}  # Keep key as 'tasks' for API compatibility

    def _handle_get_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to get a specific task by ID.

        Args:
            params: Request parameters including 'task_id'

        Returns:
            Dictionary with task details or error
        """
        task_id = params.get("task_id")
        if not task_id:
            raise ValueError("Missing required parameter 'task_id'")

        item = self.task_service.get_item_by_id(task_id)
        if not item:
            raise ValueError(f"Item with ID '{task_id}' not found")

        return {"task": item}  # Keep key as 'task' for API compatibility

    def _handle_get_next_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to get the next task to work on.

        Returns:
            Dictionary with the next task or null if no tasks are available
        """
        # Use the service's built-in method
        next_item = self.task_service.get_next_task()

        if not next_item:
            return {"task": None}

        return {"task": next_item}  # Keep key as 'task' for API compatibility

    def _handle_set_task_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to update a task's status.

        Args:
            params: Request parameters including 'task_id' and 'status'

        Returns:
            Dictionary with success status
        """
        task_id = params.get("task_id")
        status_str = params.get("status")

        if not task_id:
            raise ValueError("Missing required parameter 'task_id'")
        if not status_str:
            raise ValueError("Missing required parameter 'status'")

        # Validate and convert status value to enum
        try:
            status_enum = TaskStatus(status_str)
        except ValueError:
            valid_statuses = [s.value for s in TaskStatus]
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )

        # Use service method to update status
        success = self.task_service.set_item_status(task_id, status_enum)
        if not success:
            raise ValueError(
                f"Item with ID '{task_id}' not found or status update failed"
            )

        return {"success": True}

    def _handle_expand_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to expand an item into child items.

        Note: This is a simplified implementation that will need to be enhanced
        to support proper hierarchical expansion based on item type.

        Args:
            params: Request parameters including 'task_id' and optional 'num_subtasks'

        Returns:
            Dictionary with success status and new child items or error
        """
        item_id = params.get(
            "task_id"
        )  # Keep param name as 'task_id' for API compatibility
        num_children = params.get("num_subtasks", 3)  # Default to 3 if not provided

        if not item_id:
            raise ValueError("Missing required parameter 'task_id'")

        parent_item = self.task_service.get_item_by_id(item_id)
        if not parent_item:
            raise ValueError(f"Item '{item_id}' not found")

        # Simple validation - check if it already has children
        if parent_item.children:
            raise ValueError(f"Item '{item_id}' already has children")

        # Determine appropriate child type based on parent type
        child_type_map = {
            ItemType.EPIC: ItemType.TASK,
            ItemType.TASK: ItemType.STORY,
            ItemType.STORY: ItemType.ISSUE,
            ItemType.ISSUE: None,  # Issues can't have children
        }

        child_type = child_type_map.get(parent_item.type)
        if not child_type:
            raise ValueError(
                f"Items of type {parent_item.type.value} cannot have children"
            )

        # Create placeholder children
        new_children = []
        base_title = (
            parent_item.title[:30] + "..."
            if len(parent_item.title) > 30
            else parent_item.title
        )

        # Default titles based on child type
        if child_type == ItemType.TASK:
            default_titles = [
                f"Backend for {base_title}",
                f"Frontend for {base_title}",
                f"Infrastructure for {base_title}",
            ]
        elif child_type == ItemType.STORY:
            default_titles = [
                f"User can view {base_title}",
                f"User can create {base_title}",
                f"User can edit {base_title}",
            ]
        else:  # ISSUE
            default_titles = [
                f"Implement {base_title}",
                f"Write tests for {base_title}",
                f"Document {base_title}",
            ]

        # Create child items
        for i in range(num_children):
            # Use default titles or generate generic ones if num_children > len(default_titles)
            child_title = default_titles[i % len(default_titles)]

            # Add the item using the service (automatically handles ID generation and parent-child relationship)
            child_item = self.task_service.add_item(
                item_type=child_type,
                title=child_title,
                description=f"Auto-generated child for {parent_item.id}",
                parent_id=item_id,
            )
            new_children.append(child_item)

        # Return success with the new children
        return {
            "success": True,
            "subtasks": new_children,  # Keep key as 'subtasks' for API compatibility
        }

    def _handle_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to analyze the codebase.

        Args:
            params: Request parameters including optional 'path'

        Returns:
            Dictionary with analysis results or error
        """
        # Extract path, default to current directory ('.') if not provided
        path_to_analyze = params.get("path", ".")

        try:
            # The AnalyzerService.analyze() method doesn't accept a path parameter
            # Instead, the path is set during analyzer initialization
            # We need to create a new analyzer instance with the specified path
            analyzer = AnalyzerService(self.config_service, base_path=path_to_analyze)
            analysis_results = analyzer.analyze()
            return {"analysis": analysis_results}
        except Exception as e:
            # Re-raise as a standard exception for the main handler to catch
            raise Exception(f"Analysis failed: {str(e)}")

    def _handle_get_task_context(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to get detailed context for a task.

        Args:
            params: Request parameters including 'task_id' and optional 'include_code_analysis'

        Returns:
            Dictionary with task context information
        """
        item_id = params.get(
            "task_id"
        )  # Keep param name as 'task_id' for API compatibility
        if not item_id:
            raise ValueError("Missing required parameter 'task_id'")

        include_code_analysis = params.get("include_code_analysis", True)

        # Get task context
        context = self.task_service.get_task_context(
            item_id, include_code_analysis=include_code_analysis
        )

        return {"context": context}

    def _log_error(self, message: str) -> None:
        """
        Log an error message to stderr.
        
        Args:
            message: The error message to log.
        """
        logger.error(message)
        print(message, file=sys.stderr)

    def _handle_generate_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a 'generate_code' request.

        Args:
            params: The request parameters.
                - task_id: The ID of the task to generate code for.
                - file_path: The target file path to generate code for.
                - language: (Optional) The language to use. If not provided, inferred from file extension.
                - provider: (Optional) AI provider to use (anthropic, openai, perplexity). Default is anthropic.

        Returns:
            A dictionary containing the generated code.
        """
        # Validate parameters
        task_id = _get_required_param(params, "task_id")
        file_path = _get_required_param(params, "file_path")
        language = params.get("language")
        provider_name = params.get("provider")

        # Infer language from file extension if not provided
        if language is None:
            extension = os.path.splitext(file_path)[1].lower()
            language = _get_language_from_extension(extension)

        # Normalize provider name and map to enum
        ai_provider = None
        if provider_name:
            provider_name = provider_name.lower()
            for provider in AiProvider:
                if provider.value == provider_name:
                    ai_provider = provider
                    break
        
        # Default to Anthropic if provider not recognized
        if ai_provider is None:
            ai_provider = AiProvider.ANTHROPIC

        try:
            # Create AI service
            ai_service = AiService(self.config_service)
            
            # Get task details from task_id if it exists
            task_details = {}
            if task_id:
                try:
                    task = self.task_service.get_item_by_id(task_id)
                    if task:
                        task_details = {
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "details": task.details or ""
                        }
                except Exception as e:
                    self._log_error(f"Error getting task details: {str(e)}")
                    # Create minimal task details from task_id
                    task_details = {
                        "id": task_id,
                        "title": f"Task {task_id}",
                        "description": f"Generate code for {file_path}",
                        "details": ""
                    }
            
            # Generate code
            code = ai_service.generate_code(
                task_details=task_details,
                language=language,
                provider=ai_provider
            )

            return {
                "code": code,
                "language": language,
                "file_path": file_path,
            }
        except Exception as e:
            # Handle errors
            error_message = str(e)
            self._log_error(f"Code generation error: {error_message}")
            raise ServerError(f"Code generation failed: {error_message}")


def run_mcp_server(
    amautarc_path: Optional[Path] = None, tasks_json_path: Optional[Path] = None
):
    """Run the MCP server for Cursor integration."""
    try:
        print("Starting AMAUTA MCP server...")
        server = McpServer(
            amautarc_path=amautarc_path, 
            tasks_json_path=tasks_json_path
        )
        server.run()
    except Exception as e:
        print(f"Error in MCP server: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_mcp_server()
