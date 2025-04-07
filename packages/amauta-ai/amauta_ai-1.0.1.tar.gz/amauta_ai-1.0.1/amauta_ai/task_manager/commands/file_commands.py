import os
import typer
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Annotated
from rich.console import Console

from amauta_ai.task_manager.service import TaskManagerService
from amauta_ai.task_manager.models import TaskItem, ItemType, TaskStatus
from amauta_ai.utils.error_handler import friendly_error

# Create a console for rich output
console = Console()

# Create a Typer application for task file commands
file_commands_app = typer.Typer(help="Task file-related commands")


@file_commands_app.command("generate-files")
@friendly_error("Failed to generate task files")
def generate_files(
    output_dir: Annotated[
        Optional[str],
        typer.Option(help="Directory to store generated task files"),
    ] = "tasks",
    format: Annotated[
        str,
        typer.Option(help="File format (md, txt, json)"),
    ] = "md",
    include_done: Annotated[
        bool,
        typer.Option(help="Include completed tasks"),
    ] = False,
    include_description: Annotated[
        bool,
        typer.Option(help="Include task description"),
    ] = True,
    include_dependencies: Annotated[
        bool,
        typer.Option(help="Include task dependencies"),
    ] = True,
    include_children: Annotated[
        bool,
        typer.Option(help="Include task children"),
    ] = True,
) -> None:
    """
    Generate individual files for each task.
    
    This command creates a separate file for each task in the tasks.json file.
    The files are stored in the specified output directory.
    
    Examples:
      - Generate markdown files: amauta task generate-files
      - Generate JSON files: amauta task generate-files --format json
      - Exclude completed tasks: amauta task generate-files --no-include-done
    """
    task_service = TaskManagerService()
    items = task_service.get_all_items()
    
    # Filter out completed tasks if requested
    if not include_done:
        items = [i for i in items if i.status != TaskStatus.DONE]
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    typer.secho(f"Generating task files in {output_path}...", fg=typer.colors.BLUE)
    
    # Track the number of files generated
    files_generated = 0
    
    # Process each item
    for item in items:
        # Create a filename based on the item ID and format
        filename = f"{item.id}.{format}"
        file_path = output_path / filename
        
        # Generate the file content based on the format
        if format == "md":
            content = _generate_markdown_content(item, task_service, include_description, include_dependencies, include_children)
        elif format == "json":
            content = _generate_json_content(item, task_service, include_description, include_dependencies, include_children)
        else:  # txt format
            content = _generate_text_content(item, task_service, include_description, include_dependencies, include_children)
        
        # Write the content to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        files_generated += 1
    
    typer.secho(f"✅ Generated {files_generated} task files.", fg=typer.colors.GREEN)


def _generate_markdown_content(
    item: TaskItem, 
    task_service: TaskManagerService, 
    include_description: bool, 
    include_dependencies: bool, 
    include_children: bool
) -> str:
    """Generate markdown content for a task."""
    content = f"# {item.id}: {item.title}\n\n"
    content += f"**Type:** {item.type.value}\n"
    content += f"**Status:** {item.status.value}\n"
    content += f"**Priority:** {item.priority.value}\n"
    
    if item.parent:
        parent_item = task_service.get_item_by_id(item.parent)
        parent_title = parent_item.title if parent_item else "Unknown"
        content += f"**Parent:** [{item.parent}] {parent_title}\n"
    
    if include_description and item.description:
        content += f"\n## Description\n\n{item.description}\n"
    
    if include_dependencies and item.dependencies:
        content += "\n## Dependencies\n\n"
        for dep_id in item.dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            dep_title = dep_item.title if dep_item else "Unknown"
            content += f"- [{dep_id}] {dep_title}\n"
    
    if include_children and item.children:
        content += "\n## Children\n\n"
        for child_id in item.children:
            child_item = task_service.get_item_by_id(child_id)
            child_title = child_item.title if child_item else "Unknown"
            content += f"- [{child_id}] {child_title}\n"
    
    return content


def _generate_json_content(
    item: TaskItem, 
    task_service: TaskManagerService, 
    include_description: bool, 
    include_dependencies: bool, 
    include_children: bool
) -> str:
    """Generate JSON content for a task."""
    data = {
        "id": item.id,
        "title": item.title,
        "type": item.type.value,
        "status": item.status.value,
        "priority": item.priority.value,
    }
    
    if item.parent:
        data["parent"] = item.parent
    
    if include_description and item.description:
        data["description"] = item.description
    
    if include_dependencies and item.dependencies:
        dep_data = []
        for dep_id in item.dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            dep_data.append({
                "id": dep_id,
                "title": dep_item.title if dep_item else "Unknown"
            })
        data["dependencies"] = dep_data
    
    if include_children and item.children:
        child_data = []
        for child_id in item.children:
            child_item = task_service.get_item_by_id(child_id)
            child_data.append({
                "id": child_id,
                "title": child_item.title if child_item else "Unknown"
            })
        data["children"] = child_data
    
    return json.dumps(data, indent=2)


def _generate_text_content(
    item: TaskItem, 
    task_service: TaskManagerService, 
    include_description: bool, 
    include_dependencies: bool, 
    include_children: bool
) -> str:
    """Generate plain text content for a task."""
    content = f"{item.id}: {item.title}\n"
    content += f"Type: {item.type.value}\n"
    content += f"Status: {item.status.value}\n"
    content += f"Priority: {item.priority.value}\n"
    
    if item.parent:
        parent_item = task_service.get_item_by_id(item.parent)
        parent_title = parent_item.title if parent_item else "Unknown"
        content += f"Parent: {item.parent} - {parent_title}\n"
    
    if include_description and item.description:
        content += f"\nDescription:\n{item.description}\n"
    
    if include_dependencies and item.dependencies:
        content += "\nDependencies:\n"
        for dep_id in item.dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            dep_title = dep_item.title if dep_item else "Unknown"
            content += f"- {dep_id} - {dep_title}\n"
    
    if include_children and item.children:
        content += "\nChildren:\n"
        for child_id in item.children:
            child_item = task_service.get_item_by_id(child_id)
            child_title = child_item.title if child_item else "Unknown"
            content += f"- {child_id} - {child_title}\n"
    
    return content 