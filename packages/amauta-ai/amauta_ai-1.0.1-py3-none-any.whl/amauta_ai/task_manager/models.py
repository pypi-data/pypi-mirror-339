"""Models for the task manager module."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status of a task."""

    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    DEFERRED = "deferred"


class TaskPriority(str, Enum):
    """Priority of a task."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# New Enum for Hierarchy Levels
class ItemType(str, Enum):
    """Type of item in the hierarchy."""

    EPIC = "Epic"
    TASK = "Task"
    STORY = "Story"
    ISSUE = "Issue"


# Unified Model for all hierarchy levels
class TaskItem(BaseModel):
    """A single item (Epic, Task, Story, or Issue) in the hierarchy."""

    id: str = Field(
        ...,
        description="Unique identifier for the item (e.g., EPIC-001, TASK-001, ISSUE-001.1).",
    )
    type: ItemType = Field(..., description="The type of the item in the hierarchy.")
    title: str = Field(..., description="A short, descriptive title for the item.")
    description: str = Field(
        default="",
        description="Detailed description, including acceptance criteria for Stories.",
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Current status of the item."
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="Priority level of the item."
    )
    dependencies: List[str] = Field(
        default_factory=list,
        description="List of IDs of items that this item depends on.",
    )
    parent: Optional[str] = Field(
        default=None,
        description="ID of the parent item in the hierarchy (None for Epics).",
    )
    children: List[str] = Field(
        default_factory=list, description="List of IDs of direct child items."
    )
    details: str = Field(default="", description="Additional details or context.")
    test_strategy: Optional[str] = Field(
        default=None, description="Suggested testing strategy, if applicable."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the item, such as complexity scores."
    )
    # Add other common fields as needed, e.g., assignee, estimate


# Updated Root Model
class TasksModel(BaseModel):
    """The root model for tasks.json, containing a flat list of all items."""

    items: List[TaskItem] = Field(
        default_factory=list,
        description="Flat list of all TaskItems (Epics, Tasks, Stories, Issues).",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata associated with the task list."
    )


class TaskTemplate(BaseModel):
    """
    Template for creating common task types.

    Represents a reusable template with predefined:
    - Name (unique identifier for the template)
    - Type (Epic, Task, Story, or Issue)
    - Title pattern (with placeholders)
    - Description pattern (with placeholders)
    - Default status
    - Default priority
    - Predefined dependencies pattern (with placeholders)
    - Details pattern (with placeholders)
    - Test strategy pattern (with placeholders)
    """

    name: str
    type: ItemType
    title_pattern: str
    description_pattern: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    parent_pattern: Optional[str] = None
    dependency_patterns: List[str] = Field(default_factory=list)
    details_pattern: str = ""
    test_strategy_pattern: Optional[str] = None


class TemplatesModel(BaseModel):
    """
    Root model for the templates.json file.

    Contains:
    - List of all task templates
    """

    templates: List[TaskTemplate] = Field(default_factory=list)


# --- Old Models Removed ---
# class Subtask(BaseModel): ...
# class Task(BaseModel): ...
