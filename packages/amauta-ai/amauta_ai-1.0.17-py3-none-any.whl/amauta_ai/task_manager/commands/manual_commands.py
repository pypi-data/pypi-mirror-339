"""
Manual task management commands for creating detailed tasks without AI assistance.

This module provides commands for creating and managing tasks manually with extensive details.
"""

from typing import Optional, List, Dict, Any, Annotated
from typing_extensions import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
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


@task_app.command("create")
@friendly_error("Failed to create task manually")
def create_task_manually(
    title: Annotated[
        str, typer.Option("--title", "-t", help="Title of the task to create")
    ],
    description: Annotated[
        str, typer.Option("--description", "-d", help="Detailed description of the task")
    ],
    type: Annotated[
        str,
        typer.Option(help="Type of task to create (task, story, epic, issue)"),
    ] = "task",
    parent: Annotated[
        Optional[str], typer.Option(help="Parent item ID to attach this task to")
    ] = None,
    priority: Annotated[
        str,
        typer.Option(help="Priority of the task (low, medium, high, critical)"),
    ] = "medium",
    details: Annotated[
        Optional[str], typer.Option(help="Additional implementation details or context")
    ] = "",
    test_strategy: Annotated[
        Optional[str], typer.Option(help="Testing strategy for this task")
    ] = None,
    dependencies: Annotated[
        Optional[List[str]], typer.Option(help="Comma-separated list of task IDs this task depends on")
    ] = None,
    status: Annotated[
        str, typer.Option(help="Initial status of task (pending, in_progress, review, done)")
    ] = "pending",
    research_notes: Annotated[
        Optional[str], typer.Option(help="Research notes for the Research phase")
    ] = None,
    plan_notes: Annotated[
        Optional[str], typer.Option(help="Planning notes for the Plan phase")
    ] = None,
    execute_notes: Annotated[
        Optional[str], typer.Option(help="Implementation notes for the Execute phase")
    ] = None,
    test_notes: Annotated[
        Optional[str], typer.Option(help="Testing notes for the Test phase")
    ] = None,
    documentation_notes: Annotated[
        Optional[str], typer.Option(help="Documentation notes for the Document phase")
    ] = None,
    tags: Annotated[
        Optional[List[str]], typer.Option(help="Comma-separated list of tags for this task")
    ] = None,
    estimated_hours: Annotated[
        Optional[float], typer.Option(help="Estimated hours to complete this task")
    ] = None,
    due_date: Annotated[
        Optional[str], typer.Option(help="Due date for this task (YYYY-MM-DD)")
    ] = None,
) -> None:
    """
    Create a new task manually with detailed information.

    This command allows you to create a comprehensive task with all possible details
    without using AI assistance. It provides full control over all task properties.

    Examples:
      - Create basic task: amauta task create --title="Implement login form" --description="Create user login form with validation"
      - Create with full workflow notes: 
        amauta task create --title="Authentication system" --description="Main description" 
          --research-notes="Research notes here" --plan-notes="Planning approach" 
          --execute-notes="Implementation details" --test-notes="Testing strategy" 
          --documentation-notes="Documentation plans"
      - Create with dependencies: amauta task create --title="UI Implementation" --dependencies="TASK-001,TASK-002"
      - Create with estimated work: amauta task create --title="Database setup" --estimated-hours=4 --due-date="2025-05-15"
      - Create as epic: amauta task create --title="User Management" --type=epic --priority=high
    """
    task_service = TaskManagerService()
    
    # Validate parent if specified
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if not parent_item:
            typer.secho(f"Error: Parent item '{parent}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
    
    # Validate type
    try:
        item_type = ItemType(type.title())
    except ValueError:
        valid_types = ", ".join([t.value for t in ItemType])
        typer.secho(
            f"Error: Invalid type '{type}'. Valid values are: {valid_types}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Validate priority
    try:
        item_priority = TaskPriority(priority.lower())
    except ValueError:
        valid_priorities = ", ".join([p.value for p in TaskPriority])
        typer.secho(
            f"Error: Invalid priority '{priority}'. Valid values are: {valid_priorities}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Validate status
    try:
        item_status = TaskStatus(status.lower().replace("-", "_"))
    except ValueError:
        valid_statuses = ", ".join([s.value.replace("_", "-") for s in TaskStatus])
        typer.secho(
            f"Error: Invalid status '{status}'. Valid values are: {valid_statuses}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Process dependencies
    dependency_list = []
    if dependencies:
        for dep_id in dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            if not dep_item:
                typer.secho(f"Warning: Dependency item '{dep_id}' not found. Skipping.", fg=typer.colors.YELLOW)
            else:
                dependency_list.append(dep_id)
    
    # Build comprehensive workflow section in description if workflow notes are provided
    detailed_description = description if description else ""
    
    # If any workflow notes provided, build structured workflow section
    if any([research_notes, plan_notes, execute_notes, test_notes, documentation_notes]):
        workflow_notes = "\n\n## Workflow\n"
        
        if research_notes:
            workflow_notes += f"\n### Research Phase\n{research_notes}\n"
        
        if plan_notes:
            workflow_notes += f"\n### Plan Phase\n{plan_notes}\n"
            
        if execute_notes:
            workflow_notes += f"\n### Execute Phase\n{execute_notes}\n"
            
        if test_notes:
            workflow_notes += f"\n### Test Phase\n{test_notes}\n"
            
        if documentation_notes:
            workflow_notes += f"\n### Document Phase\n{documentation_notes}\n"
        
        detailed_description += workflow_notes
    
    # Construct the details field with additional metadata
    detailed_details = details if details else ""
    
    # Add metadata to details if provided
    metadata_section = ""
    if estimated_hours:
        metadata_section += f"\n## Estimated Hours\n{estimated_hours}\n"
        
    if due_date:
        metadata_section += f"\n## Due Date\n{due_date}\n"
        
    if tags:
        metadata_section += f"\n## Tags\n{', '.join(tags)}\n"
    
    if metadata_section:
        detailed_details += metadata_section
    
    # Create the task item
    metadata = {
        "manually_created": True,
        "estimated_hours": estimated_hours if estimated_hours else None,
        "due_date": due_date if due_date else None,
        "tags": tags if tags else []
    }
    
    # Add the task
    result_id = task_service.add_item(
        item_type=item_type,
        title=title,
        description=detailed_description,
        parent_id=parent,
        priority=item_priority,
        details=detailed_details,
        dependencies=dependency_list,
        test_strategy=test_strategy,
    ).id
    
    # Update status if not the default (pending)
    if item_status != TaskStatus.PENDING:
        item = task_service.get_item_by_id(result_id)
        if item:
            item.status = item_status
            task_service.update_item(item)
    
    # Update metadata
    item = task_service.get_item_by_id(result_id)
    if item:
        item.metadata.update(metadata)
        task_service.update_item(item)
    
    # Display the created task
    created_item = task_service.get_item_by_id(result_id)
    if created_item:
        console.print()
        console.print(Panel(
            f"[bold green]Task Created: {format_id(created_item.id)}[/bold green]\n\n"
            f"[bold]{created_item.title}[/bold]\n\n"
            f"{created_item.description}",
            title=f"{get_type_icon(created_item.type)} {created_item.type.value}",
            subtitle=f"{get_priority_icon(created_item.priority)} {created_item.priority.value.capitalize()} Priority",
            expand=False,
            width=100
        ))
        
        # Show additional details if present
        if created_item.details:
            console.print(Panel(
                f"{created_item.details}",
                title="Additional Details",
                expand=False,
                width=100
            ))
        
        # Show dependencies if any
        if created_item.dependencies:
            dependency_titles = []
            for dep_id in created_item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item:
                    dependency_titles.append(f"{format_id(dep_id)} - {dep_item.title}")
                else:
                    dependency_titles.append(f"{format_id(dep_id)} - [not found]")
            
            console.print("Dependencies:")
            for dep_title in dependency_titles:
                console.print(f"  - {dep_title}")
        
        # Show parent relationship if any
        if created_item.parent:
            parent_item = task_service.get_item_by_id(created_item.parent)
            if parent_item:
                console.print(f"[dim]Parent: {format_id(parent_item.id)} - {parent_item.title}[/dim]")
        
        # Show test strategy if any
        if created_item.test_strategy:
            console.print(Panel(
                f"{created_item.test_strategy}",
                title="Test Strategy",
                expand=False,
                width=100
            ))
        
        # Show metadata
        if created_item.metadata:
            metadata_str = ""
            if "estimated_hours" in created_item.metadata and created_item.metadata["estimated_hours"]:
                metadata_str += f"Estimated Hours: {created_item.metadata['estimated_hours']}\n"
            if "due_date" in created_item.metadata and created_item.metadata["due_date"]:
                metadata_str += f"Due Date: {created_item.metadata['due_date']}\n"
            if "tags" in created_item.metadata and created_item.metadata["tags"]:
                metadata_str += f"Tags: {', '.join(created_item.metadata['tags'])}\n"
            
            if metadata_str:
                console.print(Panel(
                    metadata_str,
                    title="Metadata",
                    expand=False,
                    width=100
                ))
        
        console.print()
        typer.secho(
            f"Task added successfully with ID: {created_item.id}",
            fg=typer.colors.GREEN,
        )
    else:
        typer.secho(
            f"Task was created with ID: {result_id}, but could not retrieve it for display.",
            fg=typer.colors.YELLOW,
        )


@task_app.command("edit-details")
@friendly_error("Failed to edit task details")
def edit_task_details(
    id: Annotated[
        str, typer.Argument(help="ID of the task to edit")
    ],
    title: Annotated[
        Optional[str], typer.Option("--title", "-t", help="New title for the task")
    ] = None,
    description: Annotated[
        Optional[str], typer.Option("--description", "-d", help="New description for the task")
    ] = None,
    priority: Annotated[
        Optional[str],
        typer.Option(help="New priority of the task (low, medium, high, critical)"),
    ] = None,
    status: Annotated[
        Optional[str], typer.Option(help="New status of task (pending, in_progress, review, done)")
    ] = None,
    details: Annotated[
        Optional[str], typer.Option(help="Additional implementation details or context")
    ] = None,
    test_strategy: Annotated[
        Optional[str], typer.Option(help="Testing strategy for this task")
    ] = None,
    add_dependencies: Annotated[
        Optional[List[str]], typer.Option(help="Comma-separated list of task IDs to add as dependencies")
    ] = None,
    remove_dependencies: Annotated[
        Optional[List[str]], typer.Option(help="Comma-separated list of task IDs to remove from dependencies")
    ] = None,
    research_notes: Annotated[
        Optional[str], typer.Option(help="Research notes for the Research phase")
    ] = None,
    plan_notes: Annotated[
        Optional[str], typer.Option(help="Planning notes for the Plan phase")
    ] = None,
    execute_notes: Annotated[
        Optional[str], typer.Option(help="Implementation notes for the Execute phase")
    ] = None,
    test_notes: Annotated[
        Optional[str], typer.Option(help="Testing notes for the Test phase")
    ] = None,
    documentation_notes: Annotated[
        Optional[str], typer.Option(help="Documentation notes for the Document phase")
    ] = None,
    estimated_hours: Annotated[
        Optional[float], typer.Option(help="Estimated hours to complete this task")
    ] = None,
    due_date: Annotated[
        Optional[str], typer.Option(help="Due date for this task (YYYY-MM-DD)")
    ] = None,
    add_tags: Annotated[
        Optional[List[str]], typer.Option(help="Comma-separated list of tags to add")
    ] = None,
    remove_tags: Annotated[
        Optional[List[str]], typer.Option(help="Comma-separated list of tags to remove")
    ] = None,
) -> None:
    """
    Edit an existing task with detailed information.

    This command allows you to modify any aspect of an existing task with detailed options.

    Examples:
      - Update title and description: amauta task edit-details TASK-001 --title="New title" --description="New description"
      - Update workflow notes: amauta task edit-details TASK-001 --research-notes="Updated research" --execute-notes="New implementation details"
      - Change status and priority: amauta task edit-details TASK-001 --status=in-progress --priority=high
      - Update dependencies: amauta task edit-details TASK-001 --add-dependencies=TASK-002,TASK-003 --remove-dependencies=TASK-004
      - Update metadata: amauta task edit-details TASK-001 --estimated-hours=6 --due-date="2025-06-01" --add-tags=frontend,urgent
    """
    task_service = TaskManagerService()
    
    # Get the task
    item = task_service.get_item_by_id(id)
    if not item:
        typer.secho(f"Error: Task with ID '{id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # Track if anything was updated
    updated = False
    
    # Update basic fields if provided
    if title is not None:
        item.title = title
        updated = True
    
    if description is not None:
        item.description = description
        updated = True
    
    # Update priority if provided
    if priority is not None:
        try:
            item.priority = TaskPriority(priority.lower())
            updated = True
        except ValueError:
            valid_priorities = ", ".join([p.value for p in TaskPriority])
            typer.secho(
                f"Error: Invalid priority '{priority}'. Valid values are: {valid_priorities}",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    
    # Update status if provided
    if status is not None:
        try:
            item.status = TaskStatus(status.lower().replace("-", "_"))
            updated = True
        except ValueError:
            valid_statuses = ", ".join([s.value.replace("_", "-") for s in TaskStatus])
            typer.secho(
                f"Error: Invalid status '{status}'. Valid values are: {valid_statuses}",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    
    # Update details if provided
    if details is not None:
        item.details = details
        updated = True
    
    # Update test strategy if provided
    if test_strategy is not None:
        item.test_strategy = test_strategy
        updated = True
    
    # Handle dependencies
    if add_dependencies:
        for dep_id in add_dependencies:
            if dep_id not in item.dependencies:
                # Validate dependency exists
                dep_item = task_service.get_item_by_id(dep_id)
                if not dep_item:
                    typer.secho(f"Warning: Dependency item '{dep_id}' not found. Skipping.", fg=typer.colors.YELLOW)
                    continue
                
                # Check for circular dependencies
                try:
                    task_service.add_dependency(id, dep_id)
                    updated = True
                except Exception as e:
                    typer.secho(f"Warning: Could not add dependency '{dep_id}': {str(e)}", fg=typer.colors.YELLOW)
    
    if remove_dependencies:
        for dep_id in remove_dependencies:
            if dep_id in item.dependencies:
                item.dependencies.remove(dep_id)
                updated = True
    
    # Update workflow notes by extracting and modifying the relevant sections
    if any([research_notes, plan_notes, execute_notes, test_notes, documentation_notes]):
        # Parse existing description to find workflow sections
        desc_lines = item.description.split("\n")
        workflow_found = False
        research_section = None
        plan_section = None
        execute_section = None
        test_section = None
        document_section = None
        
        # Find existing sections
        for i, line in enumerate(desc_lines):
            if "## Workflow" in line:
                workflow_found = True
                
            if workflow_found:
                if "### Research" in line and research_notes is not None:
                    research_section = i
                elif "### Plan" in line and plan_notes is not None:
                    plan_section = i
                elif "### Execute" in line and execute_notes is not None:
                    execute_section = i
                elif "### Test" in line and test_notes is not None:
                    test_section = i
                elif "### Document" in line and documentation_notes is not None:
                    document_section = i
        
        # If no workflow section found but notes provided, add a new one
        if not workflow_found and any([research_notes, plan_notes, execute_notes, test_notes, documentation_notes]):
            item.description += "\n\n## Workflow"
            desc_lines = item.description.split("\n")
            workflow_found = True
        
        # Update or add sections
        modified_lines = desc_lines.copy()
        
        # Helper function to update a section
        def update_section(section_name, section_idx, new_content):
            nonlocal modified_lines, updated
            
            if section_idx is not None:
                # Replace existing section
                section_end = section_idx + 1
                while section_end < len(modified_lines):
                    if modified_lines[section_end].startswith("###"):
                        break
                    section_end += 1
                
                modified_lines[section_idx+1:section_end] = [new_content]
            else:
                # Add new section at the end of workflow
                workflow_end = len(modified_lines)
                for i in range(len(modified_lines)-1, 0, -1):
                    if modified_lines[i].startswith("## ") and modified_lines[i] != "## Workflow":
                        workflow_end = i
                        break
                
                # Insert new section
                modified_lines.insert(workflow_end, f"\n### {section_name}\n{new_content}")
            
            updated = True
        
        # Update sections with new content
        if research_notes is not None:
            update_section("Research Phase", research_section, research_notes)
            
        if plan_notes is not None:
            update_section("Plan Phase", plan_section, plan_notes)
            
        if execute_notes is not None:
            update_section("Execute Phase", execute_section, execute_notes)
            
        if test_notes is not None:
            update_section("Test Phase", test_section, test_notes)
            
        if documentation_notes is not None:
            update_section("Document Phase", document_section, documentation_notes)
        
        # Update the description
        if modified_lines != desc_lines:
            item.description = "\n".join(modified_lines)
            updated = True
    
    # Update metadata
    if not item.metadata:
        item.metadata = {}
    
    if estimated_hours is not None:
        item.metadata["estimated_hours"] = estimated_hours
        updated = True
    
    if due_date is not None:
        item.metadata["due_date"] = due_date
        updated = True
    
    # Handle tags
    if "tags" not in item.metadata:
        item.metadata["tags"] = []
    
    if add_tags:
        for tag in add_tags:
            if tag not in item.metadata["tags"]:
                item.metadata["tags"].append(tag)
                updated = True
    
    if remove_tags:
        for tag in remove_tags:
            if tag in item.metadata["tags"]:
                item.metadata["tags"].remove(tag)
                updated = True
    
    # Save changes if anything was updated
    if updated:
        task_service.update_item(item)
        
        # Display the updated task
        updated_item = task_service.get_item_by_id(id)
        if updated_item:
            console.print()
            console.print(Panel(
                f"[bold green]Task Updated: {format_id(updated_item.id)}[/bold green]\n\n"
                f"[bold]{updated_item.title}[/bold]\n\n"
                f"{updated_item.description}",
                title=f"{get_type_icon(updated_item.type)} {updated_item.type.value}",
                subtitle=f"{get_priority_icon(updated_item.priority)} {updated_item.priority.value.capitalize()} Priority",
                expand=False,
                width=100
            ))
            
            typer.secho(
                f"Task updated successfully: {updated_item.id}",
                fg=typer.colors.GREEN,
            )
        else:
            typer.secho(
                f"Task was updated with ID: {id}, but could not retrieve it for display.",
                fg=typer.colors.YELLOW,
            )
    else:
        typer.secho(
            "No changes were made to the task.",
            fg=typer.colors.YELLOW,
        ) 