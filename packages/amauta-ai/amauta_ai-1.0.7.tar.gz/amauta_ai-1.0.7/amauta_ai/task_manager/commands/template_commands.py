"""
Template management commands for the task manager.

This module provides commands for creating, managing, and applying task templates.
"""

from typing import List, Optional, Dict, Any
from typing_extensions import Annotated
import json
import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich import box

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
    template_app,
    
    # Utilities
    console,
    friendly_error,
    get_type_icon,
    get_priority_icon,
    get_status_icon,
    format_id,
    confirm_action,
    create_spinner,
)


@template_app.command("create")
@friendly_error("Failed to create template")
def create_template(
    name: Annotated[
        str, typer.Argument(help="Name of the template to create")
    ],
    description: Annotated[
        str, typer.Option(help="Description of the template")
    ] = "",
    from_item: Annotated[
        Optional[str], typer.Option(help="Create template from existing item ID")
    ] = None,
    type: Annotated[
        Optional[str],
        typer.Option(help="Type of the template (task, story, epic, issue)"),
    ] = "task",
    priority: Annotated[
        Optional[str],
        typer.Option(help="Priority of the template (low, medium, high, critical)"),
    ] = "medium",
    interactive: Annotated[
        bool, typer.Option(help="Create template interactively")
    ] = False,
) -> None:
    """
    Create a new task template.

    A template can be created from an existing item or by specifying details.
    Templates are stored in the templates directory and can be applied to create new items.

    Examples:
      - Create from scratch: amauta template create my-template
      - Create from item: amauta template create release-template --from-item EPIC-001
      - Create interactively: amauta template create my-template --interactive
    """
    task_service = TaskManagerService()
    
    # Initialize template data
    template_data = {
        "name": name,
        "description": description or f"Template for {name}",
        "item_type": type.lower(),
        "priority": priority.lower(),
        "status": "pending",  # Templates always start with pending status
        "children": [],
        "dependencies": []
    }
    
    # If creating from existing item, load its data
    if from_item:
        item = task_service.get_item_by_id(from_item)
        if not item:
            typer.secho(f"Error: Item '{from_item}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        # Copy relevant fields from the item
        template_data.update({
            "description": description or item.description or f"Template based on {from_item}",
            "item_type": item.type.value,
            "priority": item.priority.value,
            # Don't copy the status, templates should start as pending
            "children": [],  # Will be populated with child templates if needed
            "dependencies": []  # Will be populated with dependency templates if needed
        })
        
        # Option to include children
        if item.children and confirm_action(
            f"Include {len(item.children)} children in the template?",
            default=True
        ):
            # Process children recursively
            for child_id in item.children:
                child = task_service.get_item_by_id(child_id)
                if child:
                    child_template = {
                        "title": child.title,
                        "description": child.description,
                        "item_type": child.type.value,
                        "priority": child.priority.value,
                        "status": "pending",  # Templates always start with pending status
                    }
                    template_data["children"].append(child_template)
        
        # For dependencies, we'll just store the titles since IDs won't be meaningful in templates
        if item.dependencies and confirm_action(
            f"Include {len(item.dependencies)} dependencies in the template?",
            default=True
        ):
            for dep_id in item.dependencies:
                dep = task_service.get_item_by_id(dep_id)
                if dep:
                    template_data["dependencies"].append(dep.title)
    
    # Interactive creation
    if interactive:
        template_data["title"] = typer.prompt("Title", default=template_data.get("title", name))
        template_data["description"] = typer.prompt(
            "Description", default=template_data["description"]
        )
        
        # Type selection
        valid_types = [t.value for t in ItemType]
        type_input = typer.prompt(
            "Type (task, story, epic, issue)",
            default=template_data["item_type"],
            show_choices=False,
        ).lower()
        while type_input not in valid_types:
            typer.secho(f"Invalid type. Valid values: {', '.join(valid_types)}", fg=typer.colors.RED)
            type_input = typer.prompt(
                "Type", default=template_data["item_type"], show_choices=False
            ).lower()
        template_data["item_type"] = type_input
        
        # Priority selection
        valid_priorities = [p.value for p in TaskPriority]
        priority_input = typer.prompt(
            "Priority (low, medium, high, critical)",
            default=template_data["priority"],
            show_choices=False,
        ).lower()
        while priority_input not in valid_priorities:
            typer.secho(
                f"Invalid priority. Valid values: {', '.join(valid_priorities)}",
                fg=typer.colors.RED,
            )
            priority_input = typer.prompt(
                "Priority", default=template_data["priority"], show_choices=False
            ).lower()
        template_data["priority"] = priority_input
    else:
        # Set default title if not interactive
        template_data["title"] = template_data.get("title", name)
    
    # Validate type and priority 
    try:
        # Convert lowercase type to proper case to match enum values
        proper_type = template_data["item_type"].capitalize()
        ItemType(proper_type)
        template_data["item_type"] = proper_type  # Store with proper case
    except ValueError:
        valid_types = ", ".join([t.value for t in ItemType])
        typer.secho(
            f"Error: Invalid type '{template_data['item_type']}'. Valid values are: {valid_types}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    try:
        TaskPriority(template_data["priority"].lower())
    except ValueError:
        valid_priorities = ", ".join([p.value for p in TaskPriority])
        typer.secho(
            f"Error: Invalid priority '{template_data['priority']}'. Valid values are: {valid_priorities}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Save the template
    templates_dir = task_service.get_templates_directory()
    template_path = os.path.join(templates_dir, f"{name}.json")
    
    # Check if template already exists
    if os.path.exists(template_path):
        if not confirm_action(
            f"Template '{name}' already exists. Overwrite?", default=False
        ):
            typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
            return
    
    # Create templates directory if it doesn't exist
    os.makedirs(templates_dir, exist_ok=True)
    
    # Save the template
    with open(template_path, "w") as f:
        json.dump(template_data, f, indent=2)
    
    typer.secho(f"✅ Template '{name}' created successfully.", fg=typer.colors.GREEN)
    typer.secho(f"Template saved to: {template_path}", fg=typer.colors.BLUE)


@template_app.command("list")
@friendly_error("Failed to list templates")
def list_templates() -> None:
    """
    List all available task templates.

    This command shows all templates that can be applied to create new tasks.

    Examples:
      - List all templates: amauta template list
    """
    task_service = TaskManagerService()
    templates_dir = task_service.get_templates_directory()
    
    # Ensure templates directory exists
    os.makedirs(templates_dir, exist_ok=True)
    
    # List template files
    template_files = list(Path(templates_dir).glob("*.json"))
    
    if not template_files:
        typer.secho("No templates found.", fg=typer.colors.YELLOW)
        typer.secho(
            f"Create a template with: amauta template create <name>",
            fg=typer.colors.BLUE,
        )
        return
    
    # Create table
    table = Table(title="Available Templates", box=box.ROUNDED)
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Priority", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Children", style="green")
    table.add_column("Dependencies", style="red")
    
    # Load and display each template
    for template_file in sorted(template_files):
        try:
            with open(template_file, "r") as f:
                template_data = json.load(f)
            
            # Get template type icon
            try:
                type_enum = ItemType(template_data.get("item_type", "task"))
                type_display = f"{get_type_icon(type_enum)} {type_enum.value}"
            except ValueError:
                type_display = template_data.get("item_type", "task")
            
            # Get template priority icon
            try:
                priority_enum = TaskPriority(template_data.get("priority", "medium"))
                priority_display = f"{get_priority_icon(priority_enum)} {priority_enum.value}"
            except ValueError:
                priority_display = template_data.get("priority", "medium")
            
            # Add to table
            table.add_row(
                template_file.stem,  # Name without extension
                type_display,
                priority_display,
                template_data.get("description", ""),
                str(len(template_data.get("children", []))),
                str(len(template_data.get("dependencies", []))),
            )
        except Exception as e:
            typer.secho(
                f"Error reading template {template_file.name}: {str(e)}", 
                fg=typer.colors.RED
            )
    
    console.print(table)


@template_app.command("show")
@friendly_error("Failed to show template")
def show_template(
    name: Annotated[
        str, typer.Argument(help="Name of the template to show")
    ],
) -> None:
    """
    Show details of a specific template.

    This command displays the full details of a template, including its children and dependencies.

    Examples:
      - Show template details: amauta template show my-template
    """
    task_service = TaskManagerService()
    templates_dir = task_service.get_templates_directory()
    
    # Check if template exists
    template_path = os.path.join(templates_dir, f"{name}.json")
    if not os.path.exists(template_path):
        typer.secho(f"Error: Template '{name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Load template
    try:
        with open(template_path, "r") as f:
            template_data = json.load(f)
    except Exception as e:
        typer.secho(f"Error reading template: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Display template details
    console.print(f"[bold cyan]Template:[/bold cyan] {name}")
    console.print(f"[bold]Title:[/bold] {template_data.get('title', name)}")
    console.print(f"[bold]Description:[/bold] {template_data.get('description', '')}")
    
    # Type and priority with icons
    try:
        type_enum = ItemType(template_data.get("item_type", "task"))
        console.print(f"[bold]Type:[/bold] {get_type_icon(type_enum)} {type_enum.value}")
    except ValueError:
        console.print(f"[bold]Type:[/bold] {template_data.get('item_type', 'task')}")
    
    try:
        priority_enum = TaskPriority(template_data.get("priority", "medium"))
        console.print(f"[bold]Priority:[/bold] {get_priority_icon(priority_enum)} {priority_enum.value}")
    except ValueError:
        console.print(f"[bold]Priority:[/bold] {template_data.get('priority', 'medium')}")
    
    # Show children if any
    children = template_data.get("children", [])
    if children:
        console.print("\n[bold]Children:[/bold]")
        child_table = Table(box=box.ROUNDED)
        child_table.add_column("Title", style="cyan")
        child_table.add_column("Type", style="blue")
        child_table.add_column("Priority", style="yellow")
        child_table.add_column("Description", style="white")
        
        for child in children:
            # Get child type icon
            try:
                child_type_enum = ItemType(child.get("item_type", "task"))
                child_type_display = f"{get_type_icon(child_type_enum)} {child_type_enum.value}"
            except ValueError:
                child_type_display = child.get("item_type", "task")
            
            # Get child priority icon
            try:
                child_priority_enum = TaskPriority(child.get("priority", "medium"))
                child_priority_display = f"{get_priority_icon(child_priority_enum)} {child_priority_enum.value}"
            except ValueError:
                child_priority_display = child.get("priority", "medium")
            
            child_table.add_row(
                child.get("title", "Untitled"),
                child_type_display,
                child_priority_display,
                child.get("description", "")[:50] + ("..." if len(child.get("description", "")) > 50 else ""),
            )
        
        console.print(child_table)
    
    # Show dependencies if any
    dependencies = template_data.get("dependencies", [])
    if dependencies:
        console.print("\n[bold]Dependencies:[/bold]")
        for dep in dependencies:
            console.print(f"  - {dep}")
    
    # Template path
    console.print(f"\n[dim]Template path: {template_path}[/dim]")


@template_app.command("apply")
@friendly_error("Failed to apply template")
def apply_template(
    name: Annotated[
        str, typer.Argument(help="Name of the template to apply")
    ],
    parent: Annotated[
        Optional[str], typer.Option(help="Parent item ID to attach this item to")
    ] = None,
    prefix: Annotated[
        Optional[str], typer.Option(help="ID prefix for generated items (e.g., RELEASE)")
    ] = None,
    interactive: Annotated[
        bool, typer.Option(help="Apply template interactively, allowing customization")
    ] = False,
) -> None:
    """
    Apply a template to create new task items.

    This command creates new tasks based on the specified template.
    It can create complex hierarchies with parent-child relationships.

    Examples:
      - Apply template: amauta template apply release-template
      - Apply with parent: amauta template apply feature-template --parent EPIC-002
      - Apply with custom prefix: amauta template apply release-template --prefix RELEASE
      - Apply interactively: amauta template apply release-template --interactive
    """
    task_service = TaskManagerService()
    templates_dir = task_service.get_templates_directory()
    
    # Check if template exists
    template_path = os.path.join(templates_dir, f"{name}.json")
    if not os.path.exists(template_path):
        typer.secho(f"Error: Template '{name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Load template
    try:
        with open(template_path, "r") as f:
            template_data = json.load(f)
    except Exception as e:
        typer.secho(f"Error reading template: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Validate parent if specified
    parent_item = None
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if not parent_item:
            typer.secho(f"Error: Parent item '{parent}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
    
    # Interactive mode allows customization
    title = template_data.get("title", name)
    description = template_data.get("description", "")
    item_type = template_data.get("item_type", "task")
    priority = template_data.get("priority", "medium")
    
    if interactive:
        title = typer.prompt("Title", default=title)
        description = typer.prompt("Description", default=description)
        
        # Type selection
        valid_types = [t.value for t in ItemType]
        type_input = typer.prompt(
            "Type (task, story, epic, issue)",
            default=item_type,
            show_choices=False,
        ).lower()
        while type_input not in valid_types:
            typer.secho(f"Invalid type. Valid values: {', '.join(valid_types)}", fg=typer.colors.RED)
            type_input = typer.prompt(
                "Type", default=item_type, show_choices=False
            ).lower()
        item_type = type_input
        
        # Priority selection
        valid_priorities = [p.value for p in TaskPriority]
        priority_input = typer.prompt(
            "Priority (low, medium, high, critical)",
            default=priority,
            show_choices=False,
        ).lower()
        while priority_input not in valid_priorities:
            typer.secho(
                f"Invalid priority. Valid values: {', '.join(valid_priorities)}",
                fg=typer.colors.RED,
            )
            priority_input = typer.prompt(
                "Priority", default=priority, show_choices=False
            ).lower()
        priority = priority_input
    
    # Create the main item
    with create_spinner("Creating items from template..."):
        # Determine prefix for new items
        if not prefix:
            # Use the item type as the prefix if not specified
            prefix = item_type.upper()
        
        # Create the main item
        main_item = TaskItem(
            id="",  # Will be generated by the service
            title=title,
            description=description,
            type=ItemType(item_type),
            priority=TaskPriority(priority),
            status=TaskStatus.PENDING,  # Template items start as pending
            parent=parent,
            children=[],
            dependencies=[],
        )
        
        # Add the item
        main_item = task_service.add_item(main_item, id_prefix=prefix)
        
        # Create children if any
        children_map = {}  # Maps child index to created ID for dependency reference
        for i, child_data in enumerate(template_data.get("children", [])):
            child_type = child_data.get("item_type", "task")
            child_prefix = child_type.upper()
            
            child_item = TaskItem(
                id="",  # Will be generated by the service
                title=child_data.get("title", f"Child {i+1}"),
                description=child_data.get("description", ""),
                type=ItemType(child_type),
                priority=TaskPriority(child_data.get("priority", "medium")),
                status=TaskStatus.PENDING,  # Template items start as pending
                parent=main_item.id,
                children=[],
                dependencies=[],
            )
            
            # Add the child item
            child_item = task_service.add_item(child_item, id_prefix=child_prefix)
            children_map[i] = child_item.id
            
            # Add to parent's children
            main_item.children.append(child_item.id)
        
        # Update the main item with its children
        if main_item.children:
            task_service.update_item(main_item)
    
    # Show result
    typer.secho(f"✅ Template '{name}' applied successfully.", fg=typer.colors.GREEN)
    typer.secho(f"Created item: {main_item.id} - {main_item.title}", fg=typer.colors.BLUE)
    
    if main_item.children:
        typer.secho(f"Created {len(main_item.children)} child items:", fg=typer.colors.BLUE)
        for child_id in main_item.children:
            child = task_service.get_item_by_id(child_id)
            if child:
                typer.secho(f"  - {child.id} - {child.title}", fg=typer.colors.BLUE)


@template_app.command("delete")
@friendly_error("Failed to delete template")
def delete_template(
    name: Annotated[
        str, typer.Argument(help="Name of the template to delete")
    ],
    force: Annotated[
        bool, typer.Option(help="Delete without confirmation")
    ] = False,
) -> None:
    """
    Delete a task template.

    This command removes a template from the system.

    Examples:
      - Delete template: amauta template delete my-template
      - Force delete: amauta template delete my-template --force
    """
    task_service = TaskManagerService()
    templates_dir = task_service.get_templates_directory()
    
    # Check if template exists
    template_path = os.path.join(templates_dir, f"{name}.json")
    if not os.path.exists(template_path):
        typer.secho(f"Error: Template '{name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Confirm deletion
    if not force and not confirm_action(
        f"Are you sure you want to delete template '{name}'?", default=False
    ):
        typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
        return
    
    # Delete the template
    try:
        os.remove(template_path)
        typer.secho(f"✅ Template '{name}' deleted successfully.", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error deleting template: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)


# Export the commands
__all__ = [
    "create_template",
    "list_templates",
    "show_template",
    "apply_template",
    "delete_template",
] 