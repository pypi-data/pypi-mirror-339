"""
Task item display utilities.

This module provides functions for formatting and displaying task items.
"""

from rich.panel import Panel
from typing import Optional

from amauta_ai.task_manager.models import TaskItem, ItemType, TaskStatus, TaskPriority
from amauta_ai.task_manager.service import TaskManagerService
from amauta_ai.task_manager.commands.base import (
    get_status_icon,
    get_priority_icon,
    get_type_icon,
    format_id,
)


def format_task_item(item: TaskItem, task_manager: TaskManagerService) -> Panel:
    """
    Format a task item for display.
    
    Args:
        item: The task item to format
        task_manager: The task manager service
        
    Returns:
        A rich Panel containing the formatted task item
    """
    # Get icons for status, priority, and type
    status_icon = get_status_icon(item.status)
    priority_icon = get_priority_icon(item.priority)
    type_icon = get_type_icon(item.type)
    
    # Create header with title and ID
    header = f"[bold]{type_icon} {item.type}: {format_id(item.id)}[/bold]"
    
    # Build lines of information
    lines = [
        f"┏{'━' * 100}┓",
        f"┃{item.title:^100}┃",
        f"┗{'━' * 100}┛",
        "",
        f"Status: {status_icon} {item.status} Priority: {priority_icon} {item.priority}",
    ]
    
    # Add parent information if available
    if item.parent:
        parent = task_manager.get_item_by_id(item.parent)
        parent_info = f"{parent.type} {format_id(parent.parent)}" if parent else item.parent
        lines.append(f"Parent: {parent_info}")
        
    # Add description
    if item.description:
        lines.extend(["", "Description", "", item.description])
        
    # Add details if available
    if item.details:
        lines.extend(["", "Details", "", item.details])
        
    # Add test strategy if available
    if item.test_strategy:
        lines.extend(["", "Test Strategy", "", item.test_strategy])
        
    # Add dependencies if available
    if item.dependencies:
        lines.extend(["", "Dependencies"])
        for dep_id in item.dependencies:
            dep = task_manager.get_item_by_id(dep_id)
            if dep:
                lines.append(f"  • {format_id(dep_id)} - {dep.title}")
            else:
                lines.append(f"  • {format_id(dep_id)} (not found)")
                
    # Add children if available
    if item.children:
        lines.extend(["", "Children"])
        for child_id in item.children:
            child = task_manager.get_item_by_id(child_id)
            if child:
                lines.append(f"  • {format_id(child_id)} {get_status_icon(child.status)} - {child.title}")
            else:
                lines.append(f"  • {format_id(child_id)} (not found)")
                
    # Join all lines
    content = "\n".join(lines)
    
    # Create and return panel
    return Panel(
        content,
        title=header,
        border_style="cyan",
        expand=False,
        padding=(1, 2),
    ) 