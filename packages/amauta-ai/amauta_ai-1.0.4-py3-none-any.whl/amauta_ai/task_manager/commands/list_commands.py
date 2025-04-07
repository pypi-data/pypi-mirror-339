"""
List and show commands for the task manager.

This module provides commands for listing and viewing tasks.
"""

from typing import Optional, List, Dict, Any, Annotated
from typing_extensions import Annotated
import sys
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.tree import Tree
from rich import box
from datetime import datetime
import json
import shutil

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
    create_items_table,
)

# Create a console for rich output
console = Console()

# Create a Typer application for task commands
task_app = typer.Typer(help="Task management commands")

@task_app.command("list")  # Keep command name 'list' for user simplicity
@friendly_error("Failed to list items")
def list_items(
    status: Annotated[
        Optional[str],
        typer.Option(
            help="Filter items by status (pending, in-progress, done, deferred)"
        ),
    ] = None,
    priority: Annotated[
        Optional[str],
        typer.Option(help="Filter items by priority (low, medium, high, critical)"),
    ] = None,
    type: Annotated[
        Optional[str],
        typer.Option(help="Filter items by type (Epic, Task, Story, Issue)"),
    ] = None,
    parent: Annotated[
        Optional[str],
        typer.Option(help="Filter items by parent ID"),
    ] = None,
    has_dependencies: Annotated[
        Optional[bool],
        typer.Option(help="Filter items that have dependencies"),
    ] = None,
    has_children: Annotated[
        Optional[bool],
        typer.Option(help="Filter items that have children"),
    ] = None,
    query: Annotated[
        Optional[str],
        typer.Option("--query", "-q", help="Search in title and description"),
    ] = None,
    sort_by: Annotated[
        Optional[str],
        typer.Option(help="Sort items by field (id, type, status, priority, title)"),
    ] = None,
    reverse: Annotated[
        bool,
        typer.Option("--reverse", "-r", help="Reverse the sort order"),
    ] = False,
    group_by: Annotated[
        Optional[str],
        typer.Option(help="Group items by field (type, status, priority, parent)"),
    ] = None,
    compact: Annotated[
        bool,
        typer.Option(help="Display in compact format with less detail"),
    ] = False,
    show_details: Annotated[
        bool,
        typer.Option(help="Include a column with the beginning of item details"),
    ] = False,
    show_counts: Annotated[
        bool,
        typer.Option(help="Include columns with dependency and children counts"),
    ] = False,
    view_as_tree: Annotated[
        bool,
        typer.Option(help="Display items in a hierarchy tree view"),
    ] = False,
    timeline_view: Annotated[
        bool,
        typer.Option(help="Display items in a visual timeline by status"),
    ] = False,
    tree_depth: Annotated[
        int,
        typer.Option(help="Maximum depth to display in tree view"),
    ] = 3,
    output: Annotated[
        Optional[str],
        typer.Option(help="Output format (table, json)"),
    ] = "table",
) -> None:
    """
    List items (Epics, Tasks, Stories, Issues) with filtering, sorting, and grouping.

    Examples:
      - List all pending items: amauta task list --status pending
      - List high priority tasks: amauta task list --type Task --priority high
      - Group by status: amauta task list --group-by status
      - Sort by priority (highest first): amauta task list --sort-by priority
      - Search for specific items: amauta task list --query "authentication"
      - List children of an item: amauta task list --parent EPIC-001
      - List items with dependencies: amauta task list --has-dependencies
      - Show items in tree view: amauta task list --view-as-tree
      - Show detailed tree with depth: amauta task list --view-as-tree --tree-depth 4
      - Show visual timeline: amauta task list --timeline-view
    """
    # Use the TaskManagerService to get items
    task_service = TaskManagerService()
    items = task_service.get_all_items()

    # FILTERING SECTION
    # Filter by status if provided
    if status:
        try:
            status_enum = TaskStatus(status.lower())
            items = [i for i in items if i.status == status_enum]
        except ValueError:
            typer.secho(
                f"Warning: Invalid status '{status}'. Valid values are: {', '.join([s.value for s in TaskStatus])}",
                fg=typer.colors.YELLOW,
            )

    # Filter by priority if provided
    if priority:
        try:
            priority_enum = TaskPriority(priority.lower())
            items = [i for i in items if i.priority == priority_enum]
        except ValueError:
            typer.secho(
                f"Warning: Invalid priority '{priority}'. Valid values are: {', '.join([p.value for p in TaskPriority])}",
                fg=typer.colors.YELLOW,
            )

    # Filter by type if provided
    if type:
        try:
            type_enum = ItemType(type.capitalize())
            items = [i for i in items if i.type == type_enum]
        except ValueError:
            typer.secho(
                f"Warning: Invalid type '{type}'. Valid values are: {', '.join([t.value for t in ItemType])}",
                fg=typer.colors.YELLOW,
            )

    # Filter by parent if provided
    if parent:
        items = [i for i in items if i.parent == parent]

    # Filter by has_dependencies if provided
    if has_dependencies is not None:
        if has_dependencies:
            items = [i for i in items if i.dependencies]
        else:
            items = [i for i in items if not i.dependencies]

    # Filter by has_children if provided
    if has_children is not None:
        if has_children:
            items = [i for i in items if i.children]
        else:
            items = [i for i in items if not i.children]

    # Filter by query if provided
    if query:
        query = query.lower()
        items = [
            i
            for i in items
            if query in i.title.lower() or query in i.description.lower()
        ]

    # SORTING SECTION
    # Define a sort key function based on the sort_by parameter
    def get_sort_key(item):
        if sort_by == "id":
            return item.id
        elif sort_by == "type":
            return item.type.value
        elif sort_by == "status":
            # Use custom status order: in-progress, pending, done, deferred
            status_order = {
                TaskStatus.IN_PROGRESS: 0,
                TaskStatus.PENDING: 1,
                TaskStatus.DONE: 2,
                TaskStatus.DEFERRED: 3,
            }
            return status_order[item.status]
        elif sort_by == "priority":
            # Use custom priority order: critical, high, medium, low
            priority_order = {
                TaskPriority.CRITICAL: 0,
                TaskPriority.HIGH: 1,
                TaskPriority.MEDIUM: 2,
                TaskPriority.LOW: 3,
            }
            return priority_order[item.priority]
        else:  # Default to title
            return item.title.lower()

    # Sort the items
    if sort_by:
        items.sort(key=get_sort_key, reverse=reverse)
    elif reverse:  # If only reverse is specified, sort by ID
        items.sort(key=lambda i: i.id, reverse=True)

    # DISPLAY SECTION
    if output == "json":
        # Format items as JSON and print
        items_dict = [item.dict() for item in items]
        console.print_json(json.dumps(items_dict))
        return

    # Display as table
    if len(items) == 0:
        console.print("[yellow]No items found matching the criteria.[/yellow]")
        return

    # If tree view is requested, show hierarchical view instead of table
    if view_as_tree:
        show_tree_view(items, task_service, tree_depth)
        return
        
    # If timeline view is requested, show status timeline instead of table
    if timeline_view:
        show_timeline_view(items)
        return

    # Group by the specified field if requested
    if group_by:
        create_grouped_table()
    else:
        # Create a single table with all items
        table = create_items_table(title=f"Items ({len(items)})", 
                                  include_details=show_details,
                                  include_counts=show_counts)

        for item in items:
            row = [
                format_id(item.id),
                f"{get_type_icon(item.type)} {item.type.value}",
                f"{get_status_icon(item.status)} {item.status.value}",
                f"{get_priority_icon(item.priority)} {item.priority.value}",
                item.title[:50] + ("..." if len(item.title) > 50 else ""),
            ]
            
            # Add details column if requested
            if show_details:
                details = item.details or ""
                details_preview = details[:27] + "..." if len(details) > 30 else details
                row.append(details_preview)
                
            # Add count columns if requested
            if show_counts:
                row.append(str(len(item.dependencies)))
                row.append(str(len(item.children)))
            
            table.add_row(*row)

        console.print(table)

    # Display item count
    if len(items) == 0:
        console.print("[yellow]No items found matching the criteria.[/yellow]")
    else:
        console.print(f"[green]Showing {len(items)} items.[/green]")
        
        # Add summary section with statistics if there are items and not in compact mode
        if not compact and len(items) > 1:
            console.print("\n[bold]Summary:[/bold]")
            
            # Count by status
            status_counts = {}
            for item in items:
                status_val = item.status.value
                if status_val not in status_counts:
                    status_counts[status_val] = 0
                status_counts[status_val] += 1
            
            status_table = Table(title="Status Distribution", box=box.SIMPLE)
            status_table.add_column("Status", style="bold")
            status_table.add_column("Count", justify="right")
            status_table.add_column("Percentage", justify="right")
            
            for status_name, count in status_counts.items():
                percentage = (count / len(items)) * 100
                icon = get_status_icon(TaskStatus(status_name))
                status_table.add_row(
                    f"{icon} {status_name}",
                    str(count),
                    f"{percentage:.1f}%"
                )
            
            console.print(status_table)
            
            # Count by type if we have different types
            type_counts = {}
            for item in items:
                type_val = item.type.value
                if type_val not in type_counts:
                    type_counts[type_val] = 0
                type_counts[type_val] += 1
            
            if len(type_counts) > 1:  # Only show if we have more than one type
                type_table = Table(title="Type Distribution", box=box.SIMPLE)
                type_table.add_column("Type", style="bold")
                type_table.add_column("Count", justify="right")
                type_table.add_column("Percentage", justify="right")
                
                for type_name, count in type_counts.items():
                    percentage = (count / len(items)) * 100
                    icon = get_type_icon(ItemType(type_name))
                    type_table.add_row(
                        f"{icon} {type_name}",
                        str(count),
                        f"{percentage:.1f}%"
                    )
                
                console.print(type_table)


def create_grouped_table():
    """Create tables grouped by the specified field."""
    # Check if group_by is valid
    valid_group_fields = ["type", "status", "priority", "parent"]
    if group_by not in valid_group_fields:
        typer.secho(
            f"Error: Invalid group field '{group_by}'. Valid values are: {', '.join(valid_group_fields)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
        
    # Group items by the specified field
    grouped_items = {}
    for item in items:
        if group_by == "status":
            key = item.status.value
        elif group_by == "priority":
            key = item.priority.value
        elif group_by == "type":
            key = item.type.value
        elif group_by == "parent":
            key = item.parent or "None"
        else:
            key = "All Items"  # Default group
        
        if key not in grouped_items:
            grouped_items[key] = []
        grouped_items[key].append(item)

    # Display each group
    for group_value, group_items in grouped_items.items():
        group_title = group_by.capitalize()
        table = create_items_table(title=f"{group_title}: {group_value} ({len(group_items)})",
                                   include_details=show_details,
                                   include_counts=show_counts)
        
        for item in group_items:
            row = [
                format_id(item.id),
                f"{get_type_icon(item.type)} {item.type.value}",
                f"{get_status_icon(item.status)} {item.status.value}",
                f"{get_priority_icon(item.priority)} {item.priority.value}",
                item.title[:50] + ("..." if len(item.title) > 50 else ""),
            ]
            
            # Add details column if requested
            if show_details:
                details = item.details or ""
                details_preview = details[:27] + "..." if len(details) > 30 else details
                row.append(details_preview)
                
            # Add count columns if requested
            if show_counts:
                row.append(str(len(item.dependencies)))
                row.append(str(len(item.children)))
            
            table.add_row(*row)
        
        console.print(table)
        console.print()  # Add a blank line between groups


def show_tree_view(items, task_service, max_depth=3):
    """
    Display items in a hierarchical tree view.
    
    Args:
        items: List of TaskItems to display
        task_service: TaskManagerService instance
        max_depth: Maximum depth to display in the tree
    """
    # Create a mapping of parent IDs to children
    parent_to_children = {}
    all_items = task_service.get_all_items()
    
    # Build a complete parent-child mapping
    for item in all_items:
        if item.parent:
            if item.parent not in parent_to_children:
                parent_to_children[item.parent] = []
            parent_to_children[item.parent].append(item)
    
    # Find top-level items (those in our filtered list with no parent or parent not in our items)
    top_level_ids = set()
    for item in items:
        if not item.parent:
            top_level_ids.add(item.id)
        else:
            # Check if parent is in our filtered list
            parent_in_list = False
            for potential_parent in items:
                if potential_parent.id == item.parent:
                    parent_in_list = True
                    break
            
            if not parent_in_list:
                top_level_ids.add(item.id)
    
    # Create the tree
    main_tree = Tree("[bold]Task Hierarchy[/bold]")
    
    # Track visited items to avoid circular references
    visited = set()
    
    def add_to_tree(parent_tree, item_id, current_depth=0):
        """Recursively add items to the tree."""
        if current_depth >= max_depth or item_id in visited:
            return
        
        visited.add(item_id)
        item = task_service.get_item_by_id(item_id)
        
        if not item:
            parent_tree.add(f"[dim]{item_id} (not found)[/dim]")
            return
        
        # Determine if this item is in our filtered list
        is_in_filtered_list = any(i.id == item_id for i in items)
        
        # Create node label
        type_icon = get_type_icon(item.type)
        status_icon = get_status_icon(item.status)
        status_color = "green" if item.status == TaskStatus.DONE else "yellow"
        priority_icon = get_priority_icon(item.priority)
        
        node_style = "" if is_in_filtered_list else "dim"
        node_label = f"[{node_style}]{format_id(item.id)} {type_icon} {item.title} [{status_color}]{status_icon}[/{status_color}] {priority_icon}[/{node_style}]"
        
        # Check for dependencies to show
        deps_text = ""
        if item.dependencies:
            deps_text = f" [magenta](deps: {len(item.dependencies)})[/magenta]"
        
        # Create the node
        node = parent_tree.add(f"{node_label}{deps_text}")
        
        # Add children if this item has any
        if item_id in parent_to_children:
            for child in parent_to_children[item_id]:
                add_to_tree(node, child.id, current_depth + 1)
        
        # Reset visited status for this node to allow other paths to reach it
        visited.remove(item_id)
    
    # Add all top-level items to the tree
    for item_id in sorted(top_level_ids):
        add_to_tree(main_tree, item_id)
    
    # Print the tree
    console.print(main_tree)
    console.print(f"[dim]Note: Showing hierarchy up to {max_depth} levels deep. Use --tree-depth to adjust.[/dim]")


def show_timeline_view(items):
    """
    Display items in a visual timeline/roadmap view grouped by status.
    
    Args:
        items: List of TaskItems to display
    """
    # Sort the statuses in a logical order: in-progress, pending, done, deferred
    status_order = [
        TaskStatus.IN_PROGRESS,
        TaskStatus.PENDING, 
        TaskStatus.DONE,
        TaskStatus.DEFERRED
    ]
    
    # Group items by status
    items_by_status = {}
    for status in status_order:
        items_by_status[status] = []
    
    for item in items:
        items_by_status[item.status].append(item)
    
    # Sort items in each status group by priority
    for status, status_items in items_by_status.items():
        status_items.sort(key=lambda x: {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3
        }[x.priority])
    
    # Create the timeline visualization
    console.print("\n[bold]Task Timeline View[/bold]\n")
    
    # Define column widths
    width = shutil.get_terminal_size().columns
    status_width = max(20, int(width * 0.2))
    item_width = width - status_width - 4  # Accounting for borders
    
    # Create table for the timeline
    timeline = Table(box=box.SIMPLE, expand=True)
    timeline.add_column("Status", style="bold", width=status_width)
    timeline.add_column("Items", width=item_width)
    
    # Add rows for each status
    for status in status_order:
        status_items = items_by_status[status]
        
        if not status_items:
            continue
            
        # Create a panel for each item
        items_display = []
        for item in status_items:
            type_icon = get_type_icon(item.type)
            priority_icon = get_priority_icon(item.priority)
            
            # Get priority color
            priority_color = "green"
            if item.priority == TaskPriority.HIGH:
                priority_color = "yellow"
            elif item.priority == TaskPriority.CRITICAL:
                priority_color = "red"
                
            # Format the item title with truncation if needed
            title = item.title
            if len(title) > 30:
                title = title[:27] + "..."
                
            # Create item representation
            item_text = f"[{priority_color}]{format_id(item.id)} {priority_icon}[/{priority_color}] {type_icon} {title}"
            
            # Add dependency indicator if present
            if item.dependencies:
                item_text += f" [magenta](↘{len(item.dependencies)})[/magenta]"
                
            # Add children indicator if present
            if item.children:
                item_text += f" [blue](↗{len(item.children)})[/blue]"
                
            items_display.append(item_text)
        
        # Join all items for this status
        status_display = "\n".join(items_display)
        
        # Get status icon and color
        status_icon = get_status_icon(status)
        status_name = status.value.capitalize()
        
        # Add status color
        if status == TaskStatus.DONE:
            status_color = "green"
        elif status == TaskStatus.IN_PROGRESS:
            status_color = "blue"
        elif status == TaskStatus.PENDING:
            status_color = "yellow"
        else:  # DEFERRED
            status_color = "dim"
            
        # Add the row to the timeline
        timeline.add_row(
            f"[{status_color}]{status_icon} {status_name}[/{status_color}]",
            status_display
        )
    
    console.print(timeline)
    console.print(f"[dim]Legend: ↘ Dependencies, ↗ Children[/dim]")


@task_app.command("show")
@friendly_error("Failed to show item")
def show_item(
    id: Annotated[
        str, typer.Argument(help="Item ID to show (Epic, Task, Story, or Issue)")
    ],
    show_graph: Annotated[
        bool, typer.Option(help="Show dependency graph for the item")
    ] = False,
    show_stats: Annotated[
        bool, typer.Option(help="Show dependency statistics for the item")
    ] = False,
    show_metadata: Annotated[
        bool, typer.Option(help="Show all metadata associated with the item")
    ] = False,
    show_related: Annotated[
        bool, typer.Option(help="Show all related items (parents, siblings, children)")
    ] = False,
) -> None:
    """
    Show detailed information about a specific item.

    Examples:
      - Show a task: amauta task show TASK-001
      - Show with dependency graph: amauta task show EPIC-001 --show-graph
      - Show with dependency statistics: amauta task show TASK-002 --show-stats
      - Show with metadata: amauta task show TASK-003 --show-metadata
      - Show with related items: amauta task show TASK-004 --show-related
    """
    task_service = TaskManagerService()
    item = task_service.get_item_by_id(id)

    if not item:
        typer.secho(f"Error: Item '{id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Create a panel for the item details
    title = f"{get_type_icon(item.type)} {item.type.value}: {item.id}"
    
    # Build the content
    content = [
        f"# {item.title}",
        "",
        f"**Status:** {get_status_icon(item.status)} {item.status.value}",
        f"**Priority:** {get_priority_icon(item.priority)} {item.priority.value}",
    ]

    # Add parent information if available
    if item.parent:
        parent = task_service.get_item_by_id(item.parent)
        if parent:
            content.append(
                f"**Parent:** {format_id(parent.id)} - {parent.title}"
            )
        else:
            content.append(f"**Parent:** {format_id(item.parent)} (not found)")
    
    # Add description
    if item.description:
        content.append("\n## Description\n")
        content.append(item.description)
    
    # Add details if available
    if item.details:
        content.append("\n## Details\n")
        content.append(item.details)
    
    # Add test strategy if available
    if item.test_strategy:
        content.append("\n## Test Strategy\n")
        content.append(item.test_strategy)
    
    # Add metadata if requested
    if show_metadata and item.metadata:
        content.append("\n## Metadata\n")
        for key, value in item.metadata.items():
            content.append(f"**{key}:** {value}")
    
    # Add dependencies if any
    if item.dependencies:
        content.append("\n## Dependencies\n")
        for dep_id in item.dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            if dep_item:
                status_icon = get_status_icon(dep_item.status)
                status_color = "green" if dep_item.status == TaskStatus.DONE else "yellow"
                content.append(
                    f"- {format_id(dep_id)} [{status_color}]{status_icon} {dep_item.status.value}[/{status_color}] - {dep_item.title}"
                )
            else:
                content.append(f"- {format_id(dep_id)} ❓ (not found)")
    
    # Add children if any
    if item.children:
        content.append("\n## Children\n")
        for child_id in item.children:
            child_item = task_service.get_item_by_id(child_id)
            if child_item:
                status_icon = get_status_icon(child_item.status)
                status_color = "green" if child_item.status == TaskStatus.DONE else "yellow"
                type_icon = get_type_icon(child_item.type)
                content.append(
                    f"- {format_id(child_id)} [{status_color}]{status_icon} {child_item.status.value}[/{status_color}] {type_icon} - {child_item.title}"
                )
            else:
                content.append(f"- {format_id(child_id)} ❓ (not found)")
    
    # Join the content sections
    markdown_content = "\n".join(content)
    
    # Create and display the panel
    panel = Panel(
        Markdown(markdown_content),
        title=title,
        expand=False,
    )
    console.print(panel)
    
    # Show dependency graph if requested
    if show_graph:
        # Enhanced dependency graph visualization
        try:
            console.print("\n[bold]Dependency Graph:[/bold]")
            
            # Create a tree for dependency visualization
            dep_tree = Tree(f"{format_id(item.id)} - {item.title}")
            
            # Track visited items to prevent cycles
            visited = set([id])
            
            # Recursively add dependencies to the tree
            def add_dependencies(tree_node, item_id, depth=0):
                if depth > 3 or item_id in visited:  # Limit depth to prevent excessive nesting
                    return
                
                visited.add(item_id)
                dep_item = task_service.get_item_by_id(item_id)
                
                if not dep_item or not dep_item.dependencies:
                    return
                
                for dep_id in dep_item.dependencies:
                    if dep_id in visited:
                        # Mark circular dependencies
                        tree_node.add(f"[red]{format_id(dep_id)} (circular reference)[/red]")
                        continue
                    
                    dep = task_service.get_item_by_id(dep_id)
                    if dep:
                        status_icon = get_status_icon(dep.status)
                        status_color = "green" if dep.status == TaskStatus.DONE else "yellow"
                        node_text = f"{format_id(dep_id)} [{status_color}]{status_icon}[/{status_color}] - {dep.title}"
                        child_node = tree_node.add(node_text)
                        
                        # Recursively add this dependency's dependencies
                        add_dependencies(child_node, dep_id, depth + 1)
                    else:
                        tree_node.add(f"[dim]{format_id(dep_id)} (not found)[/dim]")
            
            # Add dependencies starting from the current item
            add_dependencies(dep_tree, id)
            
            # Display the dependency tree
            console.print(dep_tree)
            console.print("[dim]Note: Limited to 3 levels of dependencies to prevent excessive nesting.[/dim]")
        except Exception as e:
            console.print(f"[yellow]Error building dependency graph: {str(e)}[/yellow]")
    
    # Show dependency statistics if requested
    if show_stats:
        # Check if additional functionality for dependency statistics is implemented
        try:
            # This would call a method like task_service.get_dependency_stats(id)
            # For now, just show a basic count
            direct_deps = len(item.dependencies)
            children = len(item.children)
            console.print("\n[bold]Dependency Statistics:[/bold]")
            console.print(f"Direct dependencies: {direct_deps}")
            console.print(f"Children: {children}")
            
            # Check for circular dependencies
            if direct_deps > 0:
                try:
                    has_circular = False
                    for dep_id in item.dependencies:
                        if task_service.has_circular_dependency(id, dep_id):
                            has_circular = True
                            break
                    
                    if has_circular:
                        console.print("[red]Warning: Circular dependencies detected![/red]")
                    else:
                        console.print("[green]No circular dependencies.[/green]")
                except (AttributeError, NotImplementedError):
                    # The has_circular_dependency method might not be available
                    pass
        except (AttributeError, NotImplementedError):
            console.print("[yellow]Dependency statistics functionality is not available.[/yellow]")

    # Show related items if requested
    if show_related:
        try:
            console.print("\n[bold]Related Items:[/bold]")
            
            # Show parent hierarchy
            if item.parent:
                console.print("\n[cyan]Parent Hierarchy:[/cyan]")
                parent_tree = Tree("[bold]Parents[/bold]")
                
                # Track current path up the hierarchy
                current_id = item.parent
                parent_path = []
                
                # Build the path up to the root
                while current_id:
                    parent_item = task_service.get_item_by_id(current_id)
                    if not parent_item:
                        break
                    
                    parent_path.insert(0, parent_item)
                    current_id = parent_item.parent
                
                # Create parent nodes
                current_node = parent_tree
                for parent in parent_path:
                    type_icon = get_type_icon(parent.type)
                    status_icon = get_status_icon(parent.status)
                    node_text = f"{format_id(parent.id)} {type_icon} {parent.title} {status_icon}"
                    current_node = current_node.add(node_text)
                
                console.print(parent_tree)
            
            # Show siblings (other children of the same parent)
            if item.parent:
                parent_item = task_service.get_item_by_id(item.parent)
                if parent_item and parent_item.children:
                    siblings = [
                        task_service.get_item_by_id(child_id)
                        for child_id in parent_item.children
                        if child_id != id and task_service.get_item_by_id(child_id)
                    ]
                    
                    if siblings:
                        console.print("\n[cyan]Siblings (from same parent):[/cyan]")
                        siblings_table = Table("ID", "Type", "Status", "Title", box=box.SIMPLE)
                        
                        for sibling in siblings:
                            siblings_table.add_row(
                                format_id(sibling.id),
                                f"{get_type_icon(sibling.type)} {sibling.type.value}",
                                f"{get_status_icon(sibling.status)} {sibling.status.value}",
                                sibling.title
                            )
                        
                        console.print(siblings_table)
            
            # Display child items in a compact format
            if item.children:
                console.print("\n[cyan]Children:[/cyan]")
                
                # Group children by type
                children_by_type = {}
                for child_id in item.children:
                    child = task_service.get_item_by_id(child_id)
                    if not child:
                        continue
                        
                    if child.type not in children_by_type:
                        children_by_type[child.type] = []
                    
                    children_by_type[child.type].append(child)
                
                # Display children by type
                for type_val, children in children_by_type.items():
                    type_icon = get_type_icon(type_val)
                    console.print(f"\n[bold]{type_icon} {type_val.value}s ({len(children)}):[/bold]")
                    
                    children_table = Table("ID", "Status", "Priority", "Title", box=box.SIMPLE)
                    
                    for child in sorted(children, key=lambda x: x.id):
                        children_table.add_row(
                            format_id(child.id),
                            f"{get_status_icon(child.status)} {child.status.value}",
                            f"{get_priority_icon(child.priority)} {child.priority.value}",
                            child.title
                        )
                    
                    console.print(children_table)
                    
                # Show completion status for children
                done_count = sum(1 for child_id in item.children if 
                                task_service.get_item_by_id(child_id) and 
                                task_service.get_item_by_id(child_id).status == TaskStatus.DONE)
                total_count = len(item.children)
                completion_pct = (done_count / total_count) * 100 if total_count > 0 else 0
                
                status_color = "green" if completion_pct == 100 else "yellow"
                console.print(f"[{status_color}]Completion: {done_count}/{total_count} ({completion_pct:.1f}%)[/{status_color}]")
        
        except Exception as e:
            console.print(f"[yellow]Error showing related items: {str(e)}[/yellow]")


# Export the commands
__all__ = ["list_items", "show_item"] 