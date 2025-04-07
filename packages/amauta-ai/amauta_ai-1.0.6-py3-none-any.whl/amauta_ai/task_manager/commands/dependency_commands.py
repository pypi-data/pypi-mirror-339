"""
Dependency management commands for the task manager.

This module provides commands for managing task dependencies.
"""

from typing import List, Optional, Set, Dict, Any
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


@task_app.command("add-dependency")
@friendly_error("Failed to add dependency")
def add_dependency(
    item_id: Annotated[
        str, typer.Argument(help="ID of the item that depends on another item")
    ],
    depends_on_id: Annotated[
        str, typer.Argument(help="ID of the item that is depended upon")
    ],
    force: Annotated[
        bool, typer.Option(help="Force adding even if it creates a circular dependency")
    ] = False,
) -> None:
    """
    Add a dependency between two items.

    This command marks that one item depends on another, meaning the first item
    should not be started until the second one is completed.

    Examples:
      - Add dependency: amauta task add-dependency TASK-002 TASK-001
        (TASK-002 depends on TASK-001 being completed first)
    """
    task_service = TaskManagerService()

    # Verify items exist
    item = task_service.get_item_by_id(item_id)
    depends_on = task_service.get_item_by_id(depends_on_id)

    if not item:
        typer.secho(f"Error: Item '{item_id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    if not depends_on:
        typer.secho(f"Error: Item '{depends_on_id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Check for self-dependency
    if item_id == depends_on_id:
        typer.secho(
            f"Error: Cannot add dependency to itself ('{item_id}').",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Check if dependency already exists
    if depends_on_id in item.dependencies:
        typer.secho(
            f"Dependency from '{item_id}' to '{depends_on_id}' already exists.",
            fg=typer.colors.YELLOW,
        )
        return

    # Add dependency
    try:
        if force:
            # Skip circular dependency check
            if depends_on_id not in item.dependencies:
                item.dependencies.append(depends_on_id)
                task_service.update_item(item)
                typer.secho(
                    f"Dependency added: {item_id} → {depends_on_id} (forced)",
                    fg=typer.colors.GREEN,
                )
        else:
            # Use the service method which includes circular dependency checks
            task_service.add_dependency(item_id, depends_on_id)
            typer.secho(
                f"Dependency added: {item_id} → {depends_on_id}",
                fg=typer.colors.GREEN,
            )
    except Exception as e:
        typer.secho(f"Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(1)


@task_app.command("remove-dependency")
@friendly_error("Failed to remove dependency")
def remove_dependency(
    item_id: Annotated[
        str, typer.Argument(help="ID of the item that depends on another item")
    ],
    depends_on_id: Annotated[
        str, typer.Argument(help="ID of the item that is depended upon")
    ],
) -> None:
    """
    Remove a dependency between two items.

    Examples:
      - Remove dependency: amauta task remove-dependency TASK-002 TASK-001
        (TASK-002 no longer depends on TASK-001)
    """
    task_service = TaskManagerService()

    # Verify items exist
    item = task_service.get_item_by_id(item_id)

    if not item:
        typer.secho(f"Error: Item '{item_id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Check if dependency exists
    if depends_on_id not in item.dependencies:
        typer.secho(
            f"No dependency from '{item_id}' to '{depends_on_id}' exists.",
            fg=typer.colors.YELLOW,
        )
        return

    # Remove dependency
    item.dependencies.remove(depends_on_id)
    task_service.update_item(item)
    typer.secho(
        f"Dependency removed: {item_id} → {depends_on_id}",
        fg=typer.colors.GREEN,
    )


@task_app.command("batch-remove-dependencies")
@friendly_error("Failed to batch remove dependencies")
def batch_remove_dependencies(
    item_id: Annotated[
        str, typer.Argument(help="ID of the item to modify dependencies for")
    ],
    remove_all: Annotated[
        bool,
        typer.Option(
            help="Remove all dependencies (item will no longer depend on anything)"
        ),
    ] = False,
    remove_completed: Annotated[
        bool,
        typer.Option(help="Remove dependencies on items that are already completed"),
    ] = False,
    dry_run: Annotated[
        bool, typer.Option(help="Show what would be done without making changes")
    ] = False,
) -> None:
    """
    Remove multiple dependencies from an item in batch.

    This command can remove all dependencies or just those to completed items.

    Examples:
      - Remove all dependencies: amauta task batch-remove-dependencies TASK-002 --remove-all
      - Remove completed dependencies: amauta task batch-remove-dependencies TASK-002 --remove-completed
      - Show what would be removed: amauta task batch-remove-dependencies TASK-002 --remove-all --dry-run
    """
    task_service = TaskManagerService()

    # Verify item exists
    item = task_service.get_item_by_id(item_id)

    if not item:
        typer.secho(f"Error: Item '{item_id}' not found.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Get the item's dependencies
    dependencies = item.dependencies

    if not dependencies:
        typer.secho(f"Item '{item_id}' has no dependencies.", fg=typer.colors.YELLOW)
        return

    # Determine which dependencies to remove
    deps_to_remove = []

    if remove_all:
        deps_to_remove = dependencies.copy()
    elif remove_completed:
        for dep_id in dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            if dep_item and dep_item.status == TaskStatus.DONE:
                deps_to_remove.append(dep_id)

    # Show what will be removed
    if not deps_to_remove:
        typer.secho("No dependencies will be removed.", fg=typer.colors.YELLOW)
        return

    # Create a table to show dependencies that will be removed
    table = Table(title=f"Dependencies for {item_id}")
    table.add_column("Dependency ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Title", style="white")
    table.add_column("Action", style="yellow")

    for dep_id in dependencies:
        dep_item = task_service.get_item_by_id(dep_id)
        status = "Unknown"
        title = "Unknown"
        action = "Keep"

        if dep_item:
            status = f"{get_status_icon(dep_item.status)} {dep_item.status.value}"
            title = dep_item.title

        if dep_id in deps_to_remove:
            action = "Remove"

        table.add_row(dep_id, status, title, action)

    console.print(table)

    # If dry run, exit here
    if dry_run:
        typer.secho(
            f"Dry run: {len(deps_to_remove)} dependencies would be removed.",
            fg=typer.colors.BLUE,
        )
        return

    # Confirm action
    if not confirm_action(
        f"Remove {len(deps_to_remove)} dependencies from {item_id}?", default=False
    ):
        typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
        return

    # Remove dependencies
    modified_deps = [dep for dep in dependencies if dep not in deps_to_remove]
    item.dependencies = modified_deps
    task_service.update_item(item)

    typer.secho(
        f"Removed {len(deps_to_remove)} dependencies from {item_id}.",
        fg=typer.colors.GREEN,
    )


@task_app.command("validate-dependencies")
@friendly_error("Failed to validate dependencies")
def validate_dependencies(
    fix: Annotated[
        bool, typer.Option(help="Automatically fix invalid dependencies")
    ] = False,
    dry_run: Annotated[
        bool, typer.Option(help="Show validation issues without fixing them")
    ] = False,
) -> None:
    """
    Validate all task dependencies in the system.

    This checks for:
    - Invalid dependencies (references to non-existent items)
    - Circular dependencies
    - Self-dependencies

    Examples:
      - Validate only: amauta task validate-dependencies
      - Validate and fix: amauta task validate-dependencies --fix
      - Show what would be fixed: amauta task validate-dependencies --fix --dry-run
    """
    task_service = TaskManagerService()
    items = task_service.get_all_items()

    # Create sets to store items with issues
    invalid_deps = {}  # item_id -> list of invalid dep_ids
    circular_deps = {}  # item_id -> list of circular dep_ids

    # Check for invalid and circular dependencies
    for item in items:
        # Check for invalid dependencies
        item_invalid_deps = []
        for dep_id in item.dependencies:
            if not task_service.get_item_by_id(dep_id):
                item_invalid_deps.append(dep_id)
            elif dep_id == item.id:  # Self-dependency
                item_invalid_deps.append(dep_id)

        if item_invalid_deps:
            invalid_deps[item.id] = item_invalid_deps

        # Check for circular dependencies
        item_circular_deps = []
        for dep_id in item.dependencies:
            if dep_id != item.id:  # Skip self-dependencies
                try:
                    if task_service.has_circular_dependency(item.id, dep_id):
                        item_circular_deps.append(dep_id)
                except (AttributeError, NotImplementedError):
                    # If has_circular_dependency is not implemented, use a simple check
                    # This is not as thorough but better than nothing
                    dep_item = task_service.get_item_by_id(dep_id)
                    if dep_item and item.id in dep_item.dependencies:
                        item_circular_deps.append(dep_id)

        if item_circular_deps:
            circular_deps[item.id] = item_circular_deps

    # Display results
    if not invalid_deps and not circular_deps:
        typer.secho("All dependencies are valid!", fg=typer.colors.GREEN)
        return

    # Display invalid dependencies
    if invalid_deps:
        invalid_table = Table(title="Invalid Dependencies", box=box.ROUNDED)
        invalid_table.add_column("Item ID", style="cyan")
        invalid_table.add_column("Invalid Dependency", style="red")
        invalid_table.add_column("Issue", style="yellow")
        invalid_table.add_column("Action", style="green")

        for item_id, deps in invalid_deps.items():
            for dep_id in deps:
                issue = "Self-dependency" if dep_id == item_id else "Does not exist"
                action = "Remove" if fix else "None"
                invalid_table.add_row(item_id, dep_id, issue, action)

        console.print(invalid_table)

    # Display circular dependencies
    if circular_deps:
        circular_table = Table(title="Circular Dependencies", box=box.ROUNDED)
        circular_table.add_column("Item ID", style="cyan")
        circular_table.add_column("Depends On", style="cyan")
        circular_table.add_column("Issue", style="yellow")
        circular_table.add_column("Action", style="green")

        for item_id, deps in circular_deps.items():
            for dep_id in deps:
                issue = "Creates circular dependency"
                action = "Remove" if fix else "None"
                circular_table.add_row(item_id, dep_id, issue, action)

        console.print(circular_table)

    # If dry run or not fixing, exit here
    if dry_run:
        total_issues = len([d for deps in invalid_deps.values() for d in deps]) + len(
            [d for deps in circular_deps.values() for d in deps]
        )
        typer.secho(
            f"Dry run: {total_issues} dependency issues would be fixed.",
            fg=typer.colors.BLUE,
        )
        return
    elif not fix:
        typer.secho(
            "Run with --fix to automatically remove invalid dependencies.",
            fg=typer.colors.YELLOW,
        )
        return

    # Fix issues
    fixed_count = 0

    # Fix invalid dependencies
    for item_id, deps in invalid_deps.items():
        item = task_service.get_item_by_id(item_id)
        if item:
            for dep_id in deps:
                if dep_id in item.dependencies:
                    item.dependencies.remove(dep_id)
                    fixed_count += 1
            task_service.update_item(item)

    # Fix circular dependencies
    for item_id, deps in circular_deps.items():
        item = task_service.get_item_by_id(item_id)
        if item:
            for dep_id in deps:
                if dep_id in item.dependencies:
                    item.dependencies.remove(dep_id)
                    fixed_count += 1
            task_service.update_item(item)

    typer.secho(f"Fixed {fixed_count} dependency issues.", fg=typer.colors.GREEN)


@task_app.command("analyze-dependencies")
@friendly_error("Failed to analyze dependencies")
def analyze_dependencies(
    item_id: Annotated[
        Optional[str],
        typer.Argument(help="ID of the item to analyze (or all if not specified)"),
    ] = None,
    show_blocked: Annotated[
        bool, typer.Option(help="Show which items are blocked and by what")
    ] = False,
    depth: Annotated[
        int, typer.Option(help="Maximum depth for dependency tree display")
    ] = 3,
) -> None:
    """
    Analyze dependencies between tasks.

    This command provides a detailed view of how items depend on each other.
    It can show a dependency tree, blocked items, and more.

    Examples:
      - Analyze all dependencies: amauta task analyze-dependencies
      - Analyze for specific item: amauta task analyze-dependencies EPIC-001
      - Show blocked items: amauta task analyze-dependencies --show-blocked
    """
    task_service = TaskManagerService()

    # Single item analysis
    if item_id:
        item = task_service.get_item_by_id(item_id)
        if not item:
            typer.secho(f"Error: Item '{item_id}' not found.", fg=typer.colors.RED)
            raise typer.Exit(1)

        # Show item details
        console.print(f"\n[bold]Dependencies for {format_id(item_id)}:[/bold] {item.title}")

        # Show direct dependencies
        if item.dependencies:
            console.print("\n[bold]Depends On:[/bold]")
            deps_table = Table(show_header=True, box=box.SIMPLE)
            deps_table.add_column("ID", style="cyan")
            deps_table.add_column("Status", style="green")
            deps_table.add_column("Title", style="white")

            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item:
                    status = f"{get_status_icon(dep_item.status)} {dep_item.status.value}"
                    deps_table.add_row(dep_id, status, dep_item.title)
                else:
                    deps_table.add_row(dep_id, "❓ Unknown", "Item not found")

            console.print(deps_table)
        else:
            console.print("[green]This item has no dependencies.[/green]")

        # Show what depends on this item
        dependants = []
        for other_item in task_service.get_all_items():
            if item_id in other_item.dependencies:
                dependants.append(other_item)

        if dependants:
            console.print("\n[bold]Items that depend on this:[/bold]")
            deps_table = Table(show_header=True, box=box.SIMPLE)
            deps_table.add_column("ID", style="cyan")
            deps_table.add_column("Status", style="green")
            deps_table.add_column("Title", style="white")

            for dep_item in dependants:
                status = f"{get_status_icon(dep_item.status)} {dep_item.status.value}"
                deps_table.add_row(dep_item.id, status, dep_item.title)

            console.print(deps_table)
        else:
            console.print("[green]No items depend on this.[/green]")

        # Show dependency tree
        console.print("\n[bold]Dependency Tree:[/bold]")
        try:
            dependency_tree = _build_dependency_tree(task_service, item_id, depth)
            console.print(dependency_tree)
        except Exception as e:
            console.print(f"[yellow]Could not build dependency tree: {str(e)}[/yellow]")

    # Global analysis
    else:
        items = task_service.get_all_items()
        items_with_deps = [i for i in items if i.dependencies]

        # Summary
        console.print(f"\n[bold]Dependency Analysis for All Items[/bold]")
        console.print(f"Total items: {len(items)}")
        console.print(f"Items with dependencies: {len(items_with_deps)}")

        # Dependency stats table
        stats_table = Table(title="Dependency Statistics", box=box.ROUNDED)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Count", style="green")

        # Count items by dependency count
        no_deps = len([i for i in items if not i.dependencies])
        one_dep = len([i for i in items if len(i.dependencies) == 1])
        two_to_five = len([i for i in items if 2 <= len(i.dependencies) <= 5])
        more_than_five = len([i for i in items if len(i.dependencies) > 5])

        stats_table.add_row("Items with no dependencies", str(no_deps))
        stats_table.add_row("Items with 1 dependency", str(one_dep))
        stats_table.add_row("Items with 2-5 dependencies", str(two_to_five))
        stats_table.add_row("Items with >5 dependencies", str(more_than_five))

        # Count blocking vs non-blocking items
        blocking_items = set()
        for item in items:
            for dep_id in item.dependencies:
                blocking_items.add(dep_id)

        stats_table.add_row(
            "Items that block other items", str(len(blocking_items))
        )

        console.print(stats_table)

        # Show blocked items
        if show_blocked:
            blocked_items = [
                i
                for i in items
                if i.status != TaskStatus.DONE and i.dependencies
            ]

            if blocked_items:
                console.print("\n[bold]Blocked Items:[/bold]")
                blocked_table = Table(box=box.ROUNDED)
                blocked_table.add_column("ID", style="cyan")
                blocked_table.add_column("Title", style="white")
                blocked_table.add_column("Status", style="yellow")
                blocked_table.add_column("Blocked By", style="red")

                for item in blocked_items:
                    blocking_deps = []
                    for dep_id in item.dependencies:
                        dep_item = task_service.get_item_by_id(dep_id)
                        if dep_item and dep_item.status != TaskStatus.DONE:
                            blocking_deps.append(
                                f"{dep_id} ({get_status_icon(dep_item.status)})"
                            )

                    if blocking_deps:
                        blocked_table.add_row(
                            item.id,
                            item.title,
                            f"{get_status_icon(item.status)} {item.status.value}",
                            ", ".join(blocking_deps),
                        )

                console.print(blocked_table)
            else:
                console.print("[green]No blocked items found.[/green]")


@task_app.command("fix-dependencies")
@friendly_error("Failed to fix dependencies")
def fix_dependencies(
    suggest_only: Annotated[
        bool, typer.Option(help="Only suggest fixes without applying them")
    ] = False,
) -> None:
    """
    Suggest and apply fixes for dependency issues.

    This command analyzes task dependencies and suggests improvements, such as
    adding missing dependencies, removing unnecessary ones, etc.

    Examples:
      - Suggest and apply fixes: amauta task fix-dependencies
      - Only suggest fixes: amauta task fix-dependencies --suggest-only
    """
    task_service = TaskManagerService()
    items = task_service.get_all_items()

    # Create sets to track different types of issues
    missing_deps = {}  # item_id -> list of suggested deps
    unnecessary_deps = {}  # item_id -> list of unnecessary deps
    transitive_deps = {}  # item_id -> list of transitive deps

    # TODO: Implement logic to identify missing dependencies

    # Find unnecessary dependencies (to completed items with no dependents)
    for item in items:
        if item.status != TaskStatus.DONE:  # Only check non-completed items
            unnecessary = []
            for dep_id in item.dependencies:
                dep_item = task_service.get_item_by_id(dep_id)
                if dep_item and dep_item.status == TaskStatus.DONE:
                    # Check if this completed dependency has any other active dependents
                    has_active_dependents = False
                    for other in items:
                        if (
                            other.id != item.id
                            and dep_id in other.dependencies
                            and other.status != TaskStatus.DONE
                        ):
                            has_active_dependents = True
                            break
                    
                    if not has_active_dependents:
                        unnecessary.append(dep_id)
            
            if unnecessary:
                unnecessary_deps[item.id] = unnecessary

    # Find transitive dependencies
    # A->B->C, where A also directly depends on C
    for item in items:
        transitive = []
        for dep_id in item.dependencies:
            dep_item = task_service.get_item_by_id(dep_id)
            if dep_item:
                # Check if any of the dependencies of this dependency are also
                # direct dependencies of the item
                for transitive_dep_id in dep_item.dependencies:
                    if transitive_dep_id in item.dependencies:
                        transitive.append(transitive_dep_id)
        
        if transitive:
            transitive_deps[item.id] = transitive

    # Show results
    if not missing_deps and not unnecessary_deps and not transitive_deps:
        typer.secho(
            "No dependency issues found that need fixing.", fg=typer.colors.GREEN
        )
        return

    # Show suggestions for missing dependencies
    if missing_deps:
        missing_table = Table(title="Suggested Missing Dependencies", box=box.ROUNDED)
        missing_table.add_column("Item ID", style="cyan")
        missing_table.add_column("Suggested Dependency", style="green")
        missing_table.add_column("Reason", style="yellow")
        missing_table.add_column("Action", style="blue")

        for item_id, deps in missing_deps.items():
            for dep_id in deps:
                reason = "Related tasks"  # Placeholder, would be more specific
                action = "Add" if not suggest_only else "Suggest"
                missing_table.add_row(item_id, dep_id, reason, action)

        console.print(missing_table)

    # Show suggestions for unnecessary dependencies
    if unnecessary_deps:
        unnecessary_table = Table(
            title="Unnecessary Dependencies", box=box.ROUNDED
        )
        unnecessary_table.add_column("Item ID", style="cyan")
        unnecessary_table.add_column("Unnecessary Dependency", style="red")
        unnecessary_table.add_column("Reason", style="yellow")
        unnecessary_table.add_column("Action", style="blue")

        for item_id, deps in unnecessary_deps.items():
            for dep_id in deps:
                reason = "Depends on completed task"
                action = "Remove" if not suggest_only else "Suggest"
                unnecessary_table.add_row(item_id, dep_id, reason, action)

        console.print(unnecessary_table)

    # Show suggestions for transitive dependencies
    if transitive_deps:
        transitive_table = Table(
            title="Transitive Dependencies (Redundant)", box=box.ROUNDED
        )
        transitive_table.add_column("Item ID", style="cyan")
        transitive_table.add_column("Transitive Dependency", style="yellow")
        transitive_table.add_column("Through", style="green")
        transitive_table.add_column("Action", style="blue")

        for item_id, deps in transitive_deps.items():
            item = task_service.get_item_by_id(item_id)
            if not item:
                continue
                
            for dep_id in deps:
                # Find the intermediate dependency
                through = []
                for direct_dep_id in item.dependencies:
                    direct_dep = task_service.get_item_by_id(direct_dep_id)
                    if direct_dep and dep_id in direct_dep.dependencies:
                        through.append(direct_dep_id)
                
                through_str = ", ".join(through)
                action = "Remove" if not suggest_only else "Suggest"
                transitive_table.add_row(item_id, dep_id, through_str, action)

        console.print(transitive_table)

    # If only suggesting, exit here
    if suggest_only:
        typer.secho(
            "\nRun without --suggest-only to apply these fixes.",
            fg=typer.colors.YELLOW,
        )
        return

    # Confirm action
    total_fixes = sum(len(deps) for deps in missing_deps.values()) + sum(
        len(deps) for deps in unnecessary_deps.values()
    ) + sum(len(deps) for deps in transitive_deps.values())
    
    if not confirm_action(
        f"Apply {total_fixes} suggested dependency fixes?", default=False
    ):
        typer.secho("Operation cancelled.", fg=typer.colors.YELLOW)
        return

    # Apply fixes
    fix_count = 0

    # Add missing dependencies
    for item_id, deps in missing_deps.items():
        item = task_service.get_item_by_id(item_id)
        if item:
            for dep_id in deps:
                if dep_id not in item.dependencies:
                    try:
                        task_service.add_dependency(item_id, dep_id)
                        fix_count += 1
                    except Exception as e:
                        typer.secho(
                            f"Failed to add dependency {item_id} → {dep_id}: {str(e)}",
                            fg=typer.colors.RED,
                        )

    # Remove unnecessary dependencies
    for item_id, deps in unnecessary_deps.items():
        item = task_service.get_item_by_id(item_id)
        if item:
            for dep_id in deps:
                if dep_id in item.dependencies:
                    item.dependencies.remove(dep_id)
                    fix_count += 1
            task_service.update_item(item)

    # Remove transitive dependencies
    for item_id, deps in transitive_deps.items():
        item = task_service.get_item_by_id(item_id)
        if item:
            for dep_id in deps:
                if dep_id in item.dependencies:
                    item.dependencies.remove(dep_id)
                    fix_count += 1
            task_service.update_item(item)

    typer.secho(f"Applied {fix_count} dependency fixes.", fg=typer.colors.GREEN)


# Helper functions for dependency analysis
def _build_dependency_tree(
    task_service: TaskManagerService, item_id: str, max_depth: int = 3
) -> Tree:
    """Build a dependency tree for visualization."""
    item = task_service.get_item_by_id(item_id)
    if not item:
        return Tree(f"[red]Item {item_id} not found[/red]")

    visited = set()  # Track visited items to avoid cycles

    def build_tree(current_id: str, depth: int = 0) -> Tree:
        current_item = task_service.get_item_by_id(current_id)
        if not current_item:
            return Tree(f"[red]{current_id} (not found)[/red]")

        status_color = "green" if current_item.status == TaskStatus.DONE else "yellow"
        tree = Tree(
            f"[cyan]{current_id}[/cyan]: [{status_color}]{get_status_icon(current_item.status)} {current_item.title}[/{status_color}]"
        )

        # Stop at max depth or if we've visited this item before
        if depth >= max_depth or current_id in visited:
            if current_item.dependencies:
                tree.add(f"[dim]... ({len(current_item.dependencies)} more dependencies)[/dim]")
            return tree

        visited.add(current_id)

        # Add dependencies
        for dep_id in current_item.dependencies:
            # Skip if it would create a cycle
            if dep_id not in visited:
                dep_tree = build_tree(dep_id, depth + 1)
                tree.add(dep_tree)
            else:
                dep_item = task_service.get_item_by_id(dep_id)
                status = "Unknown"
                if dep_item:
                    status_color = "green" if dep_item.status == TaskStatus.DONE else "yellow"
                    status = f"[{status_color}]{get_status_icon(dep_item.status)} {dep_item.title}[/{status_color}]"
                tree.add(f"[cyan]{dep_id}[/cyan]: {status} [dim](cyclic reference)[/dim]")

        visited.remove(current_id)  # Remove from visited to allow showing in other branches
        return tree

    return build_tree(item_id)


# Export the commands
__all__ = [
    "add_dependency",
    "remove_dependency",
    "batch_remove_dependencies",
    "validate_dependencies",
    "analyze_dependencies",
    "fix_dependencies",
] 