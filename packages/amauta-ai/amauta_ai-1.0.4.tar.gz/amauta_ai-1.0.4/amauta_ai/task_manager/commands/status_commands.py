"""
Status management commands for the task manager.

This module provides commands for managing task statuses.
"""

from typing import List, Optional, Dict, Any
from typing_extensions import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
import sys

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
    create_items_table,
)


@task_app.command("set-status")
@friendly_error("Failed to set status")
def set_item_status(
    id: Annotated[
        str, typer.Argument(help="ID of the item to update status")
    ],
    status: Annotated[
        str, typer.Argument(help="New status (pending, in-progress, done, deferred)")
    ],
    recursive: Annotated[
        bool, typer.Option(help="Apply status to child items recursively")
    ] = False,
    force: Annotated[
        bool, typer.Option(help="Force status change even if dependencies are not met")
    ] = False,
) -> None:
    """
    Set the status of an item.

    This command updates the status of a task, story, epic, or issue.
    It can also apply the status change recursively to all child items.

    Examples:
      - Set status of a task: amauta task set-status TASK-001 done
      - Set status recursively: amauta task set-status EPIC-001 in-progress --recursive
      - Force status change: amauta task set-status TASK-001 in-progress --force
    """
    task_service = TaskManagerService()

    # Verify item exists
    item = task_service.get_item_by_id(id)
    if not item:
        typer.secho(f"Error: Item '{id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Check if status contains underscores
    if '_' in status:
        valid_statuses = ", ".join([s.value for s in TaskStatus])
        error_msg = f"Error: Invalid status '{status}'. Status values must use hyphens, not underscores. Valid values are: {valid_statuses}"
        typer.secho(error_msg, fg=typer.colors.RED)
        # Also write to stderr for test detection
        sys.stderr.write(f"Invalid status '{status}'. Use hyphens instead of underscores.\n")
        raise typer.Exit(1)
    
    # Normalize status format
    normalized_status = status.lower()
    
    # Validate status
    try:
        new_status = TaskStatus(normalized_status)
    except ValueError:
        valid_statuses = ", ".join([s.value for s in TaskStatus])
        typer.secho(
            f"Error: Invalid status '{status}'. Valid values are: {valid_statuses}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # If status is not changing, do nothing
    if item.status == new_status:
        typer.secho(
            f"Item '{id}' already has status '{new_status.value}'.", fg=typer.colors.YELLOW
        )
        return

    # Check dependencies unless forcing
    if not force and new_status == TaskStatus.IN_PROGRESS:
        # Check if any dependencies are not completed
        incomplete_deps = []
        for dep_id in item.dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            if dep_item and dep_item.status != TaskStatus.DONE:
                incomplete_deps.append(dep_id)

        if incomplete_deps:
            # Show warning about incomplete dependencies
            typer.secho(
                f"Warning: Item '{id}' has {len(incomplete_deps)} incomplete dependencies:",
                fg=typer.colors.YELLOW,
            )
            for dep_id in incomplete_deps:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item:
                    typer.secho(
                        f"  - {dep_id} ({dep_item.status.value}): {dep_item.title}",
                        fg=typer.colors.YELLOW,
                    )
            
            # Ask for confirmation
            if not confirm_action(
                "Continue setting status to in-progress despite incomplete dependencies?",
                default=False,
            ):
                typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
                return
            
            typer.secho(
                "Setting status despite incomplete dependencies.",
                fg=typer.colors.YELLOW,
            )

    # Store old status for logging
    old_status = item.status

    # Update the item's status
    item.status = new_status
    task_service.update_item(item)

    typer.secho(
        f"✅ Item '{id}' status updated from '{old_status.value}' to '{new_status.value}'",
        fg=typer.colors.GREEN,
    )

    # Apply recursively to children if requested
    if recursive and item.children:
        updated_children = 0
        for child_id in item.children:
            child_item = task_service.get_item_by_id(child_id)
            if child_item and child_item.status != new_status:
                child_item.status = new_status
                task_service.update_item(child_item)
                updated_children += 1
                
                # Apply to grandchildren recursively
                if child_item.children:
                    for grandchild_id in child_item.children:
                        grandchild = task_service.get_item_by_id(grandchild_id)
                        if grandchild and grandchild.status != new_status:
                            grandchild.status = new_status
                            task_service.update_item(grandchild)
                            updated_children += 1

        if updated_children > 0:
            typer.secho(
                f"Updated {updated_children} child items recursively.",
                fg=typer.colors.GREEN,
            )

    # Print a summary
    console.print()
    panel = Panel(
        f"Status Update Summary:\n"
        f"  Item: {id} - {item.title}\n"
        f"  Type: {item.type.value}\n"
        f"  Status: {new_status.value}",
        title="Status Update",
        border_style="green",
    )
    console.print(panel)


@task_app.command("status-report")
@friendly_error("Failed to generate status report")
def status_report(
    group_by: Annotated[
        Optional[str],
        typer.Option(
            help="Group by field (type, status, priority, parent)"
        ),
    ] = "status",
    include_done: Annotated[
        bool, typer.Option(help="Include completed items in the report")
    ] = False,
    days: Annotated[
        Optional[int],
        typer.Option(help="Only include items updated in the last N days")
    ] = None,
    parent: Annotated[
        Optional[str],
        typer.Option(help="Filter by parent ID to show status of a specific Epic or Task")
    ] = None,
) -> None:
    """
    Generate a report of task statuses.

    This command provides an overview of all tasks in the system, categorized by status
    or other grouping criteria.

    Examples:
      - Basic report: amauta task status-report
      - Group by type: amauta task status-report --group-by type
      - Exclude completed: amauta task status-report --no-include-done
      - Show recent updates: amauta task status-report --days 7
      - Report for specific parent: amauta task status-report --parent EPIC-001
    """
    task_service = TaskManagerService()
    items = task_service.get_all_items()

    # Filter out completed items if requested
    if not include_done:
        items = [i for i in items if i.status != TaskStatus.DONE]

    # Filter by parent if specified
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if not parent_item:
            typer.secho(f"Error: Parent item '{parent}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)
        
        # Include the parent and all its descendants
        items = [i for i in items if i.id == parent or i.parent == parent]
        
        # Add grandchildren as well
        grandchildren = []
        for item in items:
            if item.children:
                for child_id in item.children:
                    child = task_service.get_item_by_id(child_id)
                    if child and child not in items:
                        grandchildren.append(child)
        
        items.extend(grandchildren)

    # Filter by last updated date if specified
    if days is not None:
        # Ideally, we would have a last_updated field in the TaskItem model
        # For now, we'll just show a message that this feature is not implemented
        typer.secho(
            f"Note: Filtering by update date is not implemented in the current version.",
            fg=typer.colors.YELLOW,
        )

    # If no items match criteria, show a message and exit
    if not items:
        typer.secho("No items match the specified criteria.", fg=typer.colors.YELLOW)
        return

    # Group items based on the specified criteria
    grouped_items = {}
    
    for item in items:
        if group_by == "type":
            key = item.type.value
        elif group_by == "status":
            key = item.status.value
        elif group_by == "priority":
            key = item.priority.value
        elif group_by == "parent":
            if item.parent:
                parent_item = task_service.get_item_by_id(item.parent)
                key = f"{item.parent} - {parent_item.title if parent_item else 'Unknown'}"
            else:
                key = "No Parent"
        else:
            # Default to status
            key = item.status.value
        
        if key not in grouped_items:
            grouped_items[key] = []
        
        grouped_items[key].append(item)

    # Generate report title
    title = "Status Report"
    if parent:
        parent_item = task_service.get_item_by_id(parent)
        if parent_item:
            title = f"Status Report for {parent} - {parent_item.title}"
    
    console.print(f"[bold]{title}[/bold]")
    console.print(f"Total items: {len(items)}")
    console.print(f"Grouped by: {group_by}")
    console.print()

    # Display each group
    for group_name, group_items in grouped_items.items():
        # Create a table for this group
        table = Table(title=f"{group_name} ({len(group_items)})", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Type", style="blue")
        
        # Skip status column if grouping by status
        if group_by != "status":
            table.add_column("Status", style="green")
        
        # Skip priority column if grouping by priority
        if group_by != "priority":
            table.add_column("Priority", style="yellow")
        
        table.add_column("Title", style="white")
        
        # Add parent column if not grouping by parent
        if group_by != "parent":
            table.add_column("Parent", style="magenta")
        
        # Add items to the table
        for item in group_items:
            row = [item.id, f"{get_type_icon(item.type)} {item.type.value}"]
            
            if group_by != "status":
                row.append(f"{get_status_icon(item.status)} {item.status.value}")
            
            if group_by != "priority":
                row.append(f"{get_priority_icon(item.priority)} {item.priority.value}")
            
            row.append(item.title)
            
            if group_by != "parent" and item.parent:
                parent_item = task_service.get_item_by_id(item.parent)
                if parent_item:
                    row.append(f"{item.parent} - {parent_item.title}")
                else:
                    row.append(f"{item.parent} (not found)")
            elif group_by != "parent":
                row.append("")
            
            table.add_row(*row)
        
        console.print(table)
        console.print()

    # Summary of status counts
    status_counts = {}
    for item in items:
        status = item.status.value
        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] += 1
    
    console.print("[bold]Status Summary:[/bold]")
    for status, count in status_counts.items():
        percentage = (count / len(items)) * 100
        console.print(f"{status}: {count} ({percentage:.1f}%)")


@task_app.command("status-validate")
@friendly_error("Failed to validate statuses")
def status_validate(
    fix: Annotated[
        bool, typer.Option(help="Automatically fix invalid statuses")
    ] = False,
    dry_run: Annotated[
        bool, typer.Option(help="Show validation issues without fixing them")
    ] = False,
) -> None:
    """
    Validate task statuses against rules.

    This command checks for status inconsistencies, such as:
    - Tasks with done status but with incomplete dependencies
    - Tasks with in-progress status but with incomplete parent tasks

    Examples:
      - Check status consistency: amauta task status-validate
      - Fix status issues: amauta task status-validate --fix
      - Show what would be fixed: amauta task status-validate --fix --dry-run
    """
    task_service = TaskManagerService()
    items = task_service.get_all_items()

    # Track items with issues
    done_with_incomplete_deps = []  # Items marked as done but with incomplete dependencies
    in_progress_with_incomplete_deps = []  # Items in progress but with incomplete dependencies
    done_with_incomplete_parent = []  # Items marked as done but parent isn't
    inconsistent_family_statuses = []  # Parent-child status inconsistencies

    # Check for status inconsistencies
    for item in items:
        # Check for done items with incomplete dependencies
        if item.status == TaskStatus.DONE and item.dependencies:
            has_incomplete_deps = False
            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item and dep_item.status != TaskStatus.DONE:
                    has_incomplete_deps = True
                    break
            
            if has_incomplete_deps:
                done_with_incomplete_deps.append(item)
        
        # Check for in-progress items with incomplete dependencies
        elif item.status == TaskStatus.IN_PROGRESS and item.dependencies:
            has_incomplete_deps = False
            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item and dep_item.status != TaskStatus.DONE:
                    has_incomplete_deps = True
                    break
            
            if has_incomplete_deps:
                in_progress_with_incomplete_deps.append(item)
        
        # Check for done items with incomplete parent
        if item.status == TaskStatus.DONE and item.parent:
            parent_item = task_service.get_item_by_id(item.parent)
            if parent_item and parent_item.status != TaskStatus.DONE:
                done_with_incomplete_parent.append(item)
        
        # Check for parent-child status inconsistencies
        if item.children:
            # If parent is done, all children should be done
            if item.status == TaskStatus.DONE:
                has_incomplete_children = False
                for child_id in item.children:
                    child_item = task_service.get_item_by_id(child_id)
                    if child_item and child_item.status != TaskStatus.DONE:
                        has_incomplete_children = True
                        break
                
                if has_incomplete_children:
                    inconsistent_family_statuses.append((item, "children_not_done"))
            
            # If parent is deferred, all children should be deferred
            elif item.status == TaskStatus.DEFERRED:
                has_active_children = False
                for child_id in item.children:
                    child_item = task_service.get_item_by_id(child_id)
                    if child_item and child_item.status != TaskStatus.DEFERRED:
                        has_active_children = True
                        break
                
                if has_active_children:
                    inconsistent_family_statuses.append((item, "children_not_deferred"))
    
    # If no issues found, show success message and exit
    if (
        not done_with_incomplete_deps
        and not in_progress_with_incomplete_deps
        and not done_with_incomplete_parent
        and not inconsistent_family_statuses
    ):
        typer.secho("All item statuses are valid!", fg=typer.colors.GREEN)
        return
    
    # Display results
    console.print("[bold]Status Validation Results[/bold]")
    
    if done_with_incomplete_deps:
        table = Table(title="Done Items with Incomplete Dependencies", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Incomplete Dependencies", style="red")
        table.add_column("Suggested Action", style="yellow")
        
        for item in done_with_incomplete_deps:
            incomplete_deps = []
            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item and dep_item.status != TaskStatus.DONE:
                    incomplete_deps.append(f"{dep_id} ({dep_item.status.value})")
            
            action = "Set to in-progress" if fix else "None"
            table.add_row(
                item.id,
                item.title,
                ", ".join(incomplete_deps),
                action,
            )
        
        console.print(table)
        console.print()
    
    if in_progress_with_incomplete_deps:
        table = Table(title="In-Progress Items with Incomplete Dependencies", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Incomplete Dependencies", style="red")
        table.add_column("Suggested Action", style="yellow")
        
        for item in in_progress_with_incomplete_deps:
            incomplete_deps = []
            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item and dep_item.status != TaskStatus.DONE:
                    incomplete_deps.append(f"{dep_id} ({dep_item.status.value})")
            
            action = "Set to pending" if fix else "None"
            table.add_row(
                item.id,
                item.title,
                ", ".join(incomplete_deps),
                action,
            )
        
        console.print(table)
        console.print()
    
    if done_with_incomplete_parent:
        table = Table(title="Done Items with Incomplete Parent", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Parent", style="red")
        table.add_column("Suggested Action", style="yellow")
        
        for item in done_with_incomplete_parent:
            parent_item = task_service.get_item_by_id(item.parent)
            parent_info = f"{item.parent} ({parent_item.status.value})" if parent_item else item.parent
            
            action = "None (informational only)"
            table.add_row(
                item.id,
                item.title,
                parent_info,
                action,
            )
        
        console.print(table)
        console.print()
    
    if inconsistent_family_statuses:
        table = Table(title="Inconsistent Parent-Child Statuses", box=box.ROUNDED)
        table.add_column("Parent ID", style="cyan")
        table.add_column("Parent Status", style="green")
        table.add_column("Issue", style="red")
        table.add_column("Suggested Action", style="yellow")
        
        for item, issue_type in inconsistent_family_statuses:
            if issue_type == "children_not_done":
                issue = "Parent is done but has incomplete children"
                action = "Mark children as done" if fix else "None"
            elif issue_type == "children_not_deferred":
                issue = "Parent is deferred but has active children"
                action = "Mark children as deferred" if fix else "None"
            else:
                issue = "Unknown inconsistency"
                action = "None"
            
            table.add_row(
                item.id,
                item.status.value,
                issue,
                action,
            )
        
        console.print(table)
        console.print()
    
    # If dry run, exit here
    if dry_run:
        total_issues = (
            len(done_with_incomplete_deps)
            + len(in_progress_with_incomplete_deps)
            + len(inconsistent_family_statuses)
        )
        typer.secho(
            f"Dry run: {total_issues} status issues would be fixed.",
            fg=typer.colors.BLUE,
        )
        return
    elif not fix:
        typer.secho(
            "Run with --fix to automatically resolve these status inconsistencies.",
            fg=typer.colors.YELLOW,
        )
        return
    
    # Fix the issues
    fixed_count = 0
    
    # Fix done items with incomplete dependencies
    for item in done_with_incomplete_deps:
        item.status = TaskStatus.IN_PROGRESS
        task_service.update_item(item)
        fixed_count += 1
    
    # Fix in-progress items with incomplete dependencies
    for item in in_progress_with_incomplete_deps:
        item.status = TaskStatus.PENDING
        task_service.update_item(item)
        fixed_count += 1
    
    # Fix inconsistent family statuses
    for item, issue_type in inconsistent_family_statuses:
        if issue_type == "children_not_done":
            # Mark all children as done
            for child_id in item.children:
                child_item = task_service.get_item_by_id(child_id)
                if child_item and child_item.status != TaskStatus.DONE:
                    child_item.status = TaskStatus.DONE
                    task_service.update_item(child_item)
                    fixed_count += 1
        
        elif issue_type == "children_not_deferred":
            # Mark all children as deferred
            for child_id in item.children:
                child_item = task_service.get_item_by_id(child_id)
                if child_item and child_item.status != TaskStatus.DEFERRED:
                    child_item.status = TaskStatus.DEFERRED
                    task_service.update_item(child_item)
                    fixed_count += 1
    
    typer.secho(f"Fixed {fixed_count} status issues.", fg=typer.colors.GREEN)


@task_app.command("next")
@friendly_error("Failed to determine next task")
def next_task(
    count: Annotated[
        int,
        typer.Option("--count", "-n", help="Number of tasks to suggest"),
    ] = 1,
    min_priority: Annotated[
        Optional[str],
        typer.Option(help="Minimum priority to consider (low, medium, high, critical)"),
    ] = None,
    include_dependencies: Annotated[
        bool,
        typer.Option(help="Show dependency information for suggested tasks"),
    ] = True,
    include_hierarchy: Annotated[
        bool,
        typer.Option(help="Show parent/child hierarchy for suggested tasks"),
    ] = True,
) -> None:
    """
    Suggest the next task(s) to work on.

    This command analyzes the task dependencies, priorities, and statuses to recommend
    the next tasks to work on. It prioritizes high-priority tasks that are ready to start
    (all dependencies are completed).

    Examples:
      - Get next task: amauta task next
      - Get top 3 tasks: amauta task next --count 3
      - Only high priority: amauta task next --min-priority high
    """
    # Validate priority if provided
    priority_enum = None
    if min_priority:
        try:
            priority_enum = TaskPriority(min_priority.lower())
        except ValueError:
            typer.secho(
                f"Invalid priority '{min_priority}'. Valid values are: {', '.join([p.value for p in TaskPriority])}",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    # Get task service
    task_service = TaskManagerService()

    # Use the service's get_next_task method
    next_tasks = task_service.get_next_task(count=count, min_priority=priority_enum)

    # Display results
    if not next_tasks:
        typer.secho(
            "No actionable tasks found. All tasks may be completed or blocked by dependencies.",
            fg=typer.colors.YELLOW,
        )
        return

    # Create a table to display the next tasks
    table = Table(title=f"Next {len(next_tasks)} Task(s) to Work On", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Title", style="white")

    for item in next_tasks:
        table.add_row(
            item.id,
            f"{get_type_icon(item.type)} {item.type.value}",
            f"{get_priority_icon(item.priority)} {item.priority.value}",
            f"{get_status_icon(item.status)} {item.status.value}",
            item.title,
        )

    console.print(table)

    # Show additional information for each task
    for i, item in enumerate(next_tasks):
        console.print(f"\n[bold]Task {i+1}: {format_id(item.id)}[/bold] - {item.title}")

        # Show parent hierarchy if requested
        if include_hierarchy and item.parent:
            hierarchy = []
            current_parent_id = item.parent
            
            while current_parent_id:
                parent_item = task_service.get_item_by_id(current_parent_id)
                if not parent_item:
                    hierarchy.append(f"{current_parent_id} (not found)")
                    break
                
                hierarchy.append(f"{format_id(parent_item.id)} - {parent_item.title}")
                current_parent_id = parent_item.parent
            
            if hierarchy:
                console.print("[bold]Part of:[/bold]")
                for j, parent_info in enumerate(reversed(hierarchy)):
                    console.print(f"{'  ' * j}└─ {parent_info}")

        # Show children if requested and available
        if include_hierarchy and item.children:
            console.print("[bold]Children:[/bold]")
            for child_id in item.children:
                child_item = task_service.get_item_by_id(child_id)
                if child_item:
                    status_color = "green" if child_item.status == TaskStatus.DONE else "yellow"
                    console.print(
                        f"  └─ {format_id(child_id)} - [{status_color}]{get_status_icon(child_item.status)} {child_item.title}[/{status_color}]"
                    )
                else:
                    console.print(f"  └─ {format_id(child_id)} - Not found")

        # Show dependencies if requested
        if include_dependencies and item.dependencies:
            console.print("[bold]Dependencies:[/bold]")
            all_dependencies_met = True
            
            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item:
                    is_done = dep_item.status == TaskStatus.DONE
                    status_color = "green" if is_done else "red"
                    status_prefix = "✓ " if is_done else "✗ "
                    console.print(
                        f"  {status_prefix}{format_id(dep_id)} - [{status_color}]{dep_item.title}[/{status_color}]"
                    )
                    
                    if not is_done:
                        all_dependencies_met = False
                else:
                    console.print(f"  ? {format_id(dep_id)} - Not found")
                    all_dependencies_met = False
            
            if all_dependencies_met:
                console.print("[green]All dependencies are satisfied.[/green]")
            else:
                console.print("[yellow]Some dependencies are not yet completed.[/yellow]")
        
        # Show a brief description if available
        if item.description:
            console.print("[bold]Description:[/bold]")
            console.print(f"  {item.description.split('\n')[0][:100]}...")
    
    # Show a brief summary
    console.print(f"\n[green]Found {len(next_tasks)} actionable task(s).[/green]")
    if min_priority:
        console.print(f"Filtered by minimum priority: {min_priority}")


@task_app.command("bulk-operations")
@friendly_error("Failed to perform bulk operations")
def bulk_operations(
    operation: Annotated[
        str,
        typer.Argument(help="Operation to perform (set-status, add-dependency, remove-dependency)"),
    ],
    value: Annotated[
        str,
        typer.Argument(help="Value for the operation (status value or dependency ID)"),
    ],
    ids: Annotated[
        List[str],
        typer.Argument(help="IDs of items to operate on"),
    ],
    dry_run: Annotated[
        bool, typer.Option(help="Show what would be done without making changes")
    ] = False,
) -> None:
    """
    Perform bulk operations on multiple items at once.

    This command allows you to perform the same operation on multiple items in one go,
    such as setting the status of multiple items or adding/removing dependencies.

    Examples:
      - Set status in bulk: amauta task bulk-operations set-status in-progress TASK-001 TASK-002 TASK-003
      - Add dependency in bulk: amauta task bulk-operations add-dependency EPIC-001 TASK-001 TASK-002 TASK-003
      - Remove dependency in bulk: amauta task bulk-operations remove-dependency TASK-001 TASK-002 TASK-003 TASK-004
      - Dry run: amauta task bulk-operations set-status done TASK-001 TASK-002 --dry-run
    """
    task_service = TaskManagerService()
    
    # Validate operation
    valid_operations = ["set-status", "add-dependency", "remove-dependency"]
    if operation not in valid_operations:
        typer.secho(
            f"Error: Invalid operation '{operation}'. Valid operations are: {', '.join(valid_operations)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Validate items exist
    items = []
    missing_ids = []
    for item_id in ids:
        item = task_service.get_item_by_id(item_id)
        if item:
            items.append(item)
        else:
            missing_ids.append(item_id)
    
    if missing_ids:
        typer.secho(
            f"Error: The following items were not found: {', '.join(missing_ids)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    
    # Validate value based on operation
    if operation == "set-status":
        try:
            status_value = TaskStatus(value.lower())
        except ValueError:
            valid_statuses = ", ".join([s.value for s in TaskStatus])
            typer.secho(
                f"Error: Invalid status '{value}'. Valid values are: {valid_statuses}",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    elif operation in ["add-dependency", "remove-dependency"]:
        dependency = task_service.get_item_by_id(value)
        if not dependency:
            typer.secho(
                f"Error: Dependency item '{value}' not found.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    
    # Create a table to preview the operations
    table = Table(title="Bulk Operations Preview", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Current", style="yellow")
    table.add_column("Operation", style="green")
    table.add_column("New Value", style="blue")
    table.add_column("Status", style="red")
    
    # Fill the table based on operation
    for item in items:
        if operation == "set-status":
            current = f"{get_status_icon(item.status)} {item.status.value}"
            new_value = f"{get_status_icon(status_value)} {status_value.value}"
            status = "No Change" if item.status == status_value else "Will Change"
        elif operation == "add-dependency":
            current = ", ".join(item.dependencies) if item.dependencies else "None"
            new_value = value
            status = "Already Exists" if value in item.dependencies else "Will Add"
        elif operation == "remove-dependency":
            current = ", ".join(item.dependencies) if item.dependencies else "None"
            new_value = value
            status = "Not Found" if value not in item.dependencies else "Will Remove"
        
        table.add_row(
            item.id,
            item.title,
            current,
            operation,
            new_value,
            status,
        )
    
    console.print(table)
    
    # Count the changes that will be made
    change_count = 0
    if operation == "set-status":
        change_count = sum(1 for item in items if item.status != status_value)
    elif operation == "add-dependency":
        change_count = sum(1 for item in items if value not in item.dependencies)
    elif operation == "remove-dependency":
        change_count = sum(1 for item in items if value in item.dependencies)
    
    # If no changes will be made, show a message and exit
    if change_count == 0:
        typer.secho(
            "No changes needed. All items already have the specified value.",
            fg=typer.colors.YELLOW,
        )
        return
    
    # If dry run, exit here
    if dry_run:
        typer.secho(
            f"Dry run: {change_count} changes would be made to {len(items)} items.",
            fg=typer.colors.BLUE,
        )
        return
    
    # Confirm the operation
    if not confirm_action(
        f"Perform {operation} with value '{value}' on {len(items)} items?",
        default=False,
    ):
        typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
        return
    
    # Perform the operations
    success_count = 0
    
    for item in items:
        try:
            if operation == "set-status":
                if item.status != status_value:
                    item.status = status_value
                    task_service.update_item(item)
                    success_count += 1
            
            elif operation == "add-dependency":
                if value not in item.dependencies:
                    # Use the service method to handle circular dependency checks
                    task_service.add_dependency(item.id, value)
                    success_count += 1
            
            elif operation == "remove-dependency":
                if value in item.dependencies:
                    item.dependencies.remove(value)
                    task_service.update_item(item)
                    success_count += 1
        
        except Exception as e:
            typer.secho(
                f"Error updating {item.id}: {str(e)}",
                fg=typer.colors.RED,
            )
    
    typer.secho(
        f"Successfully performed {operation} on {success_count} out of {len(items)} items.",
        fg=typer.colors.GREEN,
    )


# Export the commands
__all__ = [
    "set_item_status",
    "status_report",
    "status_validate",
    "next_task",
    "bulk_operations",
] 