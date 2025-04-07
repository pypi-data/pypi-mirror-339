"""
Import and export commands for the task manager.

This module provides commands for importing and exporting tasks in various formats.
"""

from typing import List, Optional, Dict, Any
from typing_extensions import Annotated
import json
import csv
import os
from pathlib import Path
import yaml
import typer
from rich.console import Console
from rich import box
from rich.table import Table

# Import from the base module
from amauta_ai.task_manager.commands.base import (
    # Imported services
    TaskManagerService,
    
    # Imported models
    ItemType,
    TaskItem,
    TaskPriority,
    TaskStatus,
    
    # Typer apps
    task_app,
    
    # Utilities
    console,
    friendly_error,
    get_status_icon,
    get_priority_icon,
    get_type_icon,
    format_id,
    confirm_action,
    create_spinner,
)


@task_app.command("export")
@friendly_error("Failed to export tasks")
def export_tasks(
    output: Annotated[
        str, typer.Argument(help="Output file path (e.g., tasks.json, tasks.csv)")
    ],
    format: Annotated[
        Optional[str],
        typer.Option(
            help="Export format (json, csv, yaml). If not specified, will be inferred from output file extension."
        ),
    ] = None,
    include_done: Annotated[
        bool, typer.Option(help="Include completed tasks in export")
    ] = True,
    parent: Annotated[
        Optional[str], typer.Option(help="Export only tasks under specified parent ID")
    ] = None,
) -> None:
    """
    Export tasks to a file in different formats.

    This command exports tasks to JSON, CSV, or YAML formats.
    The export format can be specified or inferred from the file extension.

    Examples:
      - Export all tasks to JSON: amauta task export tasks.json
      - Export active tasks only: amauta task export tasks.csv --no-include-done
      - Export specific parent: amauta task export epic-tasks.yaml --parent EPIC-001
      - Explicitly specify format: amauta task export tasks.dat --format json
    """
    task_service = TaskManagerService()
    
    # Determine format from file extension if not specified
    if not format:
        _, ext = os.path.splitext(output)
        if ext.lower() == '.json':
            format = 'json'
        elif ext.lower() == '.csv':
            format = 'csv'
        elif ext.lower() in ['.yaml', '.yml']:
            format = 'yaml'
        else:
            typer.secho(
                f"Error: Cannot determine export format from extension '{ext}'. "
                "Please specify --format.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    
    # Validate format
    format = format.lower()
    if format not in ['json', 'csv', 'yaml']:
        typer.secho(
            f"Error: Unsupported format '{format}'. Supported formats: json, csv, yaml.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Get all items
    items = task_service.get_all_items()
    
    # Filter by completion status if requested
    if not include_done:
        items = [item for item in items if item.status != TaskStatus.DONE]
    
    # Filter by parent if specified
    if parent:
        # Validate parent exists
        parent_item = task_service.get_item_by_id(parent)
        if not parent_item:
            typer.secho(f"Error: Parent item '{parent}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        # Include the parent and its descendants
        parent_and_descendants = [parent_item]
        
        # Find direct children
        for item in items:
            if item.parent == parent:
                parent_and_descendants.append(item)
                
                # Find grandchildren
                for grandchild in items:
                    if grandchild.parent == item.id:
                        parent_and_descendants.append(grandchild)
        
        items = parent_and_descendants
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Export based on format
    with create_spinner(f"Exporting {len(items)} tasks to {format.upper()} format..."):
        if format == 'json':
            export_tasks_to_json(items, output)
        elif format == 'csv':
            export_tasks_to_csv(items, output)
        elif format == 'yaml':
            export_tasks_to_yaml(items, output)
    
    typer.secho(
        f"✅ Exported {len(items)} tasks to {output} in {format.upper()} format.",
        fg=typer.colors.GREEN,
    )


@task_app.command("import")
@friendly_error("Failed to import tasks")
def import_tasks(
    input_file: Annotated[
        str, typer.Argument(help="Input file path (e.g., tasks.json, tasks.csv)")
    ],
    format: Annotated[
        Optional[str],
        typer.Option(
            help="Import format (json, csv, yaml). If not specified, will be inferred from input file extension."
        ),
    ] = None,
    merge_strategy: Annotated[
        str,
        typer.Option(
            help="Strategy for handling duplicates (skip, update, replace)"
        ),
    ] = "skip",
    dry_run: Annotated[
        bool, typer.Option(help="Preview changes without importing")
    ] = False,
) -> None:
    """
    Import tasks from a file.

    This command imports tasks from JSON, CSV, or YAML formats.
    The import format can be specified or inferred from the file extension.

    Examples:
      - Import tasks from JSON: amauta task import tasks.json
      - Import and update duplicates: amauta task import tasks.csv --merge-strategy update
      - Preview import: amauta task import tasks.yaml --dry-run
      - Explicitly specify format: amauta task import tasks.dat --format json
    """
    task_service = TaskManagerService()
    
    # Validate the file exists
    if not os.path.exists(input_file):
        typer.secho(f"Error: Input file '{input_file}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Determine format from file extension if not specified
    if not format:
        _, ext = os.path.splitext(input_file)
        if ext.lower() == '.json':
            format = 'json'
        elif ext.lower() == '.csv':
            format = 'csv'
        elif ext.lower() in ['.yaml', '.yml']:
            format = 'yaml'
        else:
            typer.secho(
                f"Error: Cannot determine import format from extension '{ext}'. "
                "Please specify --format.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    
    # Validate format
    format = format.lower()
    if format not in ['json', 'csv', 'yaml']:
        typer.secho(
            f"Error: Unsupported format '{format}'. Supported formats: json, csv, yaml.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Validate merge strategy
    merge_strategy = merge_strategy.lower()
    if merge_strategy not in ['skip', 'update', 'replace']:
        typer.secho(
            f"Error: Invalid merge strategy '{merge_strategy}'. "
            "Valid strategies: skip, update, replace.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Import based on format
    try:
        if format == 'json':
            items = import_tasks_from_json(input_file)
        elif format == 'csv':
            items = import_tasks_from_csv(input_file)
        elif format == 'yaml':
            items = import_tasks_from_yaml(input_file)
        else:
            # Should never reach here due to validation above
            raise ValueError(f"Unsupported format: {format}")
    except Exception as e:
        typer.secho(f"Error parsing {format.upper()} file: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Preview imported items
    if not items:
        typer.secho(f"No tasks found in {input_file}.", fg=typer.colors.YELLOW)
        return
    
    # Display a preview of items to be imported
    console.print(f"[bold]Found {len(items)} tasks in {input_file}[/bold]")
    
    # Create a table to preview the first few tasks
    preview_count = min(5, len(items))
    table = Table(title=f"Preview ({preview_count} of {len(items)} tasks)", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Title", style="white")
    
    for i in range(preview_count):
        item = items[i]
        table.add_row(
            item.id or "(new)",
            item.type.value,
            item.status.value,
            item.title,
        )
    
    console.print(table)
    
    if len(items) > preview_count:
        console.print(f"... and {len(items) - preview_count} more tasks")
    
    # Check for duplicates
    existing_items = task_service.get_all_items()
    existing_ids = {item.id for item in existing_items}
    duplicate_count = sum(1 for item in items if item.id and item.id in existing_ids)
    
    if duplicate_count > 0:
        console.print(f"\n[yellow]Found {duplicate_count} potential duplicates[/yellow]")
        console.print(f"Using merge strategy: [bold]{merge_strategy}[/bold]")
    
    # If dry run, exit here
    if dry_run:
        typer.secho(
            f"Dry run completed. {len(items)} tasks would be imported.",
            fg=typer.colors.BLUE,
        )
        return
    
    # Confirm import
    if not confirm_action(
        f"Import {len(items)} tasks with '{merge_strategy}' merge strategy?",
        default=True,
    ):
        typer.secho("Import cancelled.", fg=typer.colors.YELLOW)
        return
    
    # Process the import with spinner
    with create_spinner(f"Importing {len(items)} tasks..."):
        # Track import statistics
        added_count = 0
        updated_count = 0
        skipped_count = 0
        
        for item in items:
            # If item has an ID, check if it exists
            if item.id and item.id in existing_ids:
                if merge_strategy == 'skip':
                    skipped_count += 1
                    continue
                elif merge_strategy == 'update':
                    # Get the existing item to merge with
                    existing_item = task_service.get_item_by_id(item.id)
                    # Preserve certain fields from existing item
                    item.children = existing_item.children
                    # Update the item
                    task_service.update_item(item)
                    updated_count += 1
                elif merge_strategy == 'replace':
                    # Completely replace the existing item
                    task_service.update_item(item)
                    updated_count += 1
            else:
                # For items without ID or that don't exist, add as new
                new_item = task_service.add_item(item)
                added_count += 1
    
    # Display import results
    typer.secho(
        f"✅ Import completed from {input_file}.", fg=typer.colors.GREEN
    )
    typer.secho(f"  - Added: {added_count}", fg=typer.colors.GREEN)
    typer.secho(f"  - Updated: {updated_count}", fg=typer.colors.GREEN)
    typer.secho(f"  - Skipped: {skipped_count}", fg=typer.colors.YELLOW)


@task_app.command("export-templates")
@friendly_error("Failed to export templates")
def export_templates(
    output: Annotated[
        str, typer.Argument(help="Output directory path")
    ],
    format: Annotated[
        str,
        typer.Option(help="Export format (json, yaml)"),
    ] = "json",
) -> None:
    """
    Export all templates to a directory.

    This command exports all task templates to a specified directory.

    Examples:
      - Export templates to directory: amauta task export-templates ./templates
      - Export as YAML: amauta task export-templates ./templates --format yaml
    """
    task_service = TaskManagerService()
    templates_dir = task_service.get_templates_directory()
    
    # Ensure templates directory exists
    os.makedirs(templates_dir, exist_ok=True)
    
    # Ensure output directory exists
    os.makedirs(output, exist_ok=True)
    
    # List template files
    template_files = list(Path(templates_dir).glob("*.json"))
    
    if not template_files:
        typer.secho("No templates found to export.", fg=typer.colors.YELLOW)
        return
    
    # Validate format
    format = format.lower()
    if format not in ['json', 'yaml']:
        typer.secho(
            f"Error: Unsupported format '{format}'. Supported formats: json, yaml.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Export each template
    exported_count = 0
    with create_spinner(f"Exporting {len(template_files)} templates..."):
        for template_file in template_files:
            try:
                # Load the template
                with open(template_file, "r") as f:
                    template_data = json.load(f)
                
                # Determine output filename
                template_name = template_file.stem
                if format == 'json':
                    output_file = os.path.join(output, f"{template_name}.json")
                else:  # yaml
                    output_file = os.path.join(output, f"{template_name}.yaml")
                
                # Save in the specified format
                if format == 'json':
                    with open(output_file, "w") as f:
                        json.dump(template_data, f, indent=2)
                else:  # yaml
                    with open(output_file, "w") as f:
                        yaml.dump(template_data, f, sort_keys=False)
                
                exported_count += 1
            except Exception as e:
                typer.secho(
                    f"Error exporting template {template_file.name}: {str(e)}",
                    fg=typer.colors.RED,
                )
    
    typer.secho(
        f"✅ Exported {exported_count} of {len(template_files)} templates to {output}.",
        fg=typer.colors.GREEN,
    )


@task_app.command("import-templates")
@friendly_error("Failed to import templates")
def import_templates(
    input_directory: Annotated[
        str, typer.Argument(help="Input directory containing template files")
    ],
    format: Annotated[
        Optional[str],
        typer.Option(help="Import format (json, yaml). If not specified, will process both."),
    ] = None,
    merge_strategy: Annotated[
        str,
        typer.Option(help="Strategy for handling duplicates (skip, replace)"),
    ] = "skip",
) -> None:
    """
    Import templates from a directory.

    This command imports task templates from a specified directory.

    Examples:
      - Import templates from directory: amauta task import-templates ./templates
      - Import only JSON templates: amauta task import-templates ./templates --format json
      - Replace existing templates: amauta task import-templates ./templates --merge-strategy replace
    """
    task_service = TaskManagerService()
    templates_dir = task_service.get_templates_directory()
    
    # Ensure input directory exists
    if not os.path.exists(input_directory):
        typer.secho(
            f"Error: Input directory '{input_directory}' not found.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Ensure templates directory exists
    os.makedirs(templates_dir, exist_ok=True)
    
    # Validate merge strategy
    merge_strategy = merge_strategy.lower()
    if merge_strategy not in ['skip', 'replace']:
        typer.secho(
            f"Error: Invalid merge strategy '{merge_strategy}'. "
            "Valid strategies: skip, replace.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Determine file patterns to search for
    patterns = []
    if format:
        format = format.lower()
        if format == 'json':
            patterns = ['*.json']
        elif format == 'yaml':
            patterns = ['*.yaml', '*.yml']
        else:
            typer.secho(
                f"Error: Unsupported format '{format}'. Supported formats: json, yaml.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    else:
        # Process both formats
        patterns = ['*.json', '*.yaml', '*.yml']
    
    # Find template files
    template_files = []
    for pattern in patterns:
        template_files.extend(list(Path(input_directory).glob(pattern)))
    
    if not template_files:
        typer.secho("No template files found in the specified directory.", fg=typer.colors.YELLOW)
        return
    
    # Import each template
    imported_count = 0
    skipped_count = 0
    with create_spinner(f"Importing {len(template_files)} templates..."):
        for template_file in template_files:
            try:
                # Determine template name from filename
                template_name = template_file.stem
                
                # Determine output path
                output_path = os.path.join(templates_dir, f"{template_name}.json")
                
                # Check if template already exists
                if os.path.exists(output_path) and merge_strategy == 'skip':
                    skipped_count += 1
                    continue
                
                # Load template data based on file extension
                template_data = None
                if template_file.suffix.lower() in ['.yaml', '.yml']:
                    with open(template_file, "r") as f:
                        template_data = yaml.safe_load(f)
                else:  # json
                    with open(template_file, "r") as f:
                        template_data = json.load(f)
                
                # Ensure required fields exist
                if not isinstance(template_data, dict):
                    typer.secho(
                        f"Error: Template {template_file.name} has invalid format.",
                        fg=typer.colors.RED,
                    )
                    continue
                
                # Save as JSON in templates directory
                with open(output_path, "w") as f:
                    json.dump(template_data, f, indent=2)
                
                imported_count += 1
            except Exception as e:
                typer.secho(
                    f"Error importing template {template_file.name}: {str(e)}",
                    fg=typer.colors.RED,
                )
    
    typer.secho(
        f"✅ Imported {imported_count} templates to {templates_dir}.",
        fg=typer.colors.GREEN,
    )
    if skipped_count > 0:
        typer.secho(f"Skipped {skipped_count} existing templates.", fg=typer.colors.YELLOW)


# Helper functions for export/import

def export_tasks_to_json(items: List[TaskItem], output_path: str) -> None:
    """Export tasks to a JSON file."""
    # Convert items to dictionaries
    items_data = []
    for item in items:
        # Convert enum values to strings
        item_dict = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "type": item.type.value,
            "priority": item.priority.value,
            "status": item.status.value,
            "parent": item.parent,
            "children": item.children,
            "dependencies": item.dependencies,
        }
        items_data.append(item_dict)
    
    # Write to file
    with open(output_path, "w") as f:
        json.dump(items_data, f, indent=2)


def export_tasks_to_csv(items: List[TaskItem], output_path: str) -> None:
    """Export tasks to a CSV file."""
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write header row
        writer.writerow([
            "id", "title", "description", "type", "priority", "status",
            "parent", "children", "dependencies"
        ])
        
        # Write data rows
        for item in items:
            writer.writerow([
                item.id,
                item.title,
                item.description,
                item.type.value,
                item.priority.value,
                item.status.value,
                item.parent or "",
                ",".join(item.children) if item.children else "",
                ",".join(item.dependencies) if item.dependencies else "",
            ])


def export_tasks_to_yaml(items: List[TaskItem], output_path: str) -> None:
    """Export tasks to a YAML file."""
    # Convert items to dictionaries
    items_data = []
    for item in items:
        # Convert enum values to strings
        item_dict = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "type": item.type.value,
            "priority": item.priority.value,
            "status": item.status.value,
            "parent": item.parent,
            "children": item.children,
            "dependencies": item.dependencies,
        }
        items_data.append(item_dict)
    
    # Write to file
    with open(output_path, "w") as f:
        yaml.dump(items_data, f, sort_keys=False)


def import_tasks_from_json(input_path: str) -> List[TaskItem]:
    """Import tasks from a JSON file."""
    with open(input_path, "r") as f:
        items_data = json.load(f)
    
    # Convert dictionaries to TaskItem objects
    items = []
    for item_data in items_data:
        try:
            item = TaskItem(
                id=item_data.get("id"),
                title=item_data.get("title", "Untitled"),
                description=item_data.get("description", ""),
                type=ItemType(item_data.get("type", "task")),
                priority=TaskPriority(item_data.get("priority", "medium")),
                status=TaskStatus(item_data.get("status", "pending")),
                parent=item_data.get("parent"),
                children=item_data.get("children", []),
                dependencies=item_data.get("dependencies", []),
            )
            items.append(item)
        except (ValueError, KeyError) as e:
            typer.secho(
                f"Warning: Skipping invalid item: {str(e)}",
                fg=typer.colors.YELLOW,
            )
    
    return items


def import_tasks_from_csv(input_path: str) -> List[TaskItem]:
    """Import tasks from a CSV file."""
    items = []
    with open(input_path, "r", newline="") as f:
        reader = csv.reader(f)
        
        # Read header row
        header = next(reader, None)
        if not header:
            return []
        
        # Create a mapping from header to index
        header_map = {column.lower(): i for i, column in enumerate(header)}
        
        # Required columns
        required_columns = ["title", "type", "priority", "status"]
        for column in required_columns:
            if column not in header_map:
                typer.secho(
                    f"Error: CSV file is missing required column '{column}'.",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
        
        # Process each row
        for row in reader:
            try:
                # Skip empty rows
                if not row or not any(row):
                    continue
                
                # Extract fields with proper indexing
                item_id = row[header_map.get("id", -1)] if "id" in header_map and header_map["id"] < len(row) else None
                title = row[header_map["title"]] if header_map["title"] < len(row) else "Untitled"
                description = row[header_map.get("description", -1)] if "description" in header_map and header_map["description"] < len(row) else ""
                type_str = row[header_map["type"]] if header_map["type"] < len(row) else "task"
                priority_str = row[header_map["priority"]] if header_map["priority"] < len(row) else "medium"
                status_str = row[header_map["status"]] if header_map["status"] < len(row) else "pending"
                parent = row[header_map.get("parent", -1)] if "parent" in header_map and header_map["parent"] < len(row) and row[header_map["parent"]] else None
                
                # Process children and dependencies (comma-separated lists)
                children_str = row[header_map.get("children", -1)] if "children" in header_map and header_map["children"] < len(row) else ""
                dependencies_str = row[header_map.get("dependencies", -1)] if "dependencies" in header_map and header_map["dependencies"] < len(row) else ""
                
                children = [child.strip() for child in children_str.split(",") if child.strip()] if children_str else []
                dependencies = [dep.strip() for dep in dependencies_str.split(",") if dep.strip()] if dependencies_str else []
                
                # Create TaskItem object
                item = TaskItem(
                    id=item_id,
                    title=title,
                    description=description,
                    type=ItemType(type_str.lower()),
                    priority=TaskPriority(priority_str.lower()),
                    status=TaskStatus(status_str.lower()),
                    parent=parent,
                    children=children,
                    dependencies=dependencies,
                )
                items.append(item)
            except (ValueError, KeyError, IndexError) as e:
                typer.secho(
                    f"Warning: Skipping invalid row: {str(e)}",
                    fg=typer.colors.YELLOW,
                )
    
    return items


def import_tasks_from_yaml(input_path: str) -> List[TaskItem]:
    """Import tasks from a YAML file."""
    with open(input_path, "r") as f:
        items_data = yaml.safe_load(f)
    
    if not isinstance(items_data, list):
        typer.secho(
            "Error: YAML file does not contain a list of items.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Convert dictionaries to TaskItem objects
    items = []
    for item_data in items_data:
        try:
            item = TaskItem(
                id=item_data.get("id"),
                title=item_data.get("title", "Untitled"),
                description=item_data.get("description", ""),
                type=ItemType(item_data.get("type", "task")),
                priority=TaskPriority(item_data.get("priority", "medium")),
                status=TaskStatus(item_data.get("status", "pending")),
                parent=item_data.get("parent"),
                children=item_data.get("children", []),
                dependencies=item_data.get("dependencies", []),
            )
            items.append(item)
        except (ValueError, KeyError) as e:
            typer.secho(
                f"Warning: Skipping invalid item: {str(e)}",
                fg=typer.colors.YELLOW,
            )
    
    return items


# Export the commands
__all__ = [
    "export_tasks",
    "import_tasks",
    "export_templates",
    "import_templates",
] 