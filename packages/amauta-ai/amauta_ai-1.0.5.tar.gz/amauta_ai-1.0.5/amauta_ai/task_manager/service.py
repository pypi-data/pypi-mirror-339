"""Task manager service for AMAUTA."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Updated imports to use new models
from amauta_ai.task_manager.models import (
    ItemType,
    TaskItem,
    TaskPriority,
    TasksModel,
    TaskStatus,
)

# Import for lazy loading the DotNotationParser
import importlib


# Custom exceptions for dependency validation
class DependencyValidationError(Exception):
    """Base exception for dependency validation errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.details = details or {}
        super().__init__(message)


class CircularDependencyError(DependencyValidationError):
    """Exception raised when a circular dependency is detected."""

    def __init__(
        self, item_id: str, depends_on_id: str, cycle: Optional[List[str]] = None
    ):
        self.item_id = item_id
        self.depends_on_id = depends_on_id
        self.cycle = cycle or []

        if cycle:
            cycle_str = " -> ".join(cycle) + f" -> {cycle[0]}"
            message = f"Adding dependency from '{item_id}' to '{depends_on_id}' would create a circular dependency: {cycle_str}"
        else:
            message = f"Adding dependency from '{item_id}' to '{depends_on_id}' would create a circular dependency"

        super().__init__(
            message,
            {"item_id": item_id, "depends_on_id": depends_on_id, "cycle": cycle},
        )


class InvalidDependencyError(DependencyValidationError):
    """Exception raised when a dependency references a non-existent item."""

    def __init__(self, item_id: str, depends_on_id: str):
        self.item_id = item_id
        self.depends_on_id = depends_on_id
        message = f"Item '{depends_on_id}' referenced in dependency does not exist"

        super().__init__(message, {"item_id": item_id, "depends_on_id": depends_on_id})


class SelfDependencyError(CircularDependencyError):
    """Exception raised when an item depends on itself."""

    def __init__(self, item_id: str):
        super().__init__(item_id, item_id)
        self.message = f"Item '{item_id}' cannot depend on itself"


class TaskManagerService:
    """
    Task manager service for AMAUTA.

    Manages a flat list of TaskItems (Epics, Tasks, Stories, Issues) stored in
    a JSON file, representing the project hierarchy.
    Ensures atomic writes to prevent data corruption.
    """

    def __init__(self, tasks_file: str = "tasks.json"):
        """
        Initialize the task manager service.

        Args:
            tasks_file: Path to the tasks JSON file (e.g., tasks.json).
        """
        self.tasks_file = tasks_file
        self.tasks_file_path = Path(tasks_file)
        self._items_cache: Optional[TasksModel] = None  # Cache for loaded items
        self._dot_notation_parser = None  # Lazy-loaded parser

    @property
    def dot_notation_parser(self):
        """
        Get the dot notation parser instance, lazy-loading it if necessary.
        
        Returns:
            An instance of DotNotationParser
        """
        if self._dot_notation_parser is None:
            # Lazy import to avoid circular dependencies
            dot_notation_module = importlib.import_module(
                "amauta_ai.task_manager.commands.utils.dot_notation"
            )
            parser_class = dot_notation_module.DotNotationParser
            self._dot_notation_parser = parser_class(self)
        return self._dot_notation_parser

    def resolve_dot_notation(self, reference: str) -> str:
        """
        Resolve a dot notation reference to a task ID.
        
        Args:
            reference: The dot notation reference (e.g., "EPIC1.TASK2.STORY3")
            
        Returns:
            The resolved task ID
            
        Raises:
            Various exceptions from DotNotationParser for parsing errors
        """
        return self.dot_notation_parser.parse(reference)
    
    def resolve_dot_notation_many(self, references: List[str]) -> Dict[str, str]:
        """
        Resolve multiple dot notation references at once.
        
        Args:
            references: List of dot notation references
            
        Returns:
            Dictionary mapping references to resolved IDs
            
        Raises:
            Various exceptions from DotNotationParser for parsing errors
        """
        return self.dot_notation_parser.resolve_many(references)
    
    def suggest_dot_notation_completions(self, partial_reference: str) -> List[str]:
        """
        Suggest possible completions for a partial dot notation reference.
        
        Args:
            partial_reference: The partial reference (e.g., "EPIC1." or "EPIC1.T")
            
        Returns:
            List of possible completions
        """
        return self.dot_notation_parser.suggest_completions(partial_reference)

    def get_item_by_dot_notation(self, reference: str) -> Optional[TaskItem]:
        """
        Get a task item using dot notation reference.
        
        Args:
            reference: The dot notation reference (e.g., "EPIC1.TASK2.STORY3")
            
        Returns:
            The task item, or None if not found
            
        Raises:
            Various exceptions from DotNotationParser for parsing errors
        """
        try:
            item_id = self.resolve_dot_notation(reference)
            return self.get_item_by_id(item_id)
        except Exception as e:
            # Convert to a friendlier error message
            raise ValueError(f"Invalid task reference '{reference}': {str(e)}")

    def _ensure_tasks_file_exists(self) -> None:
        """Ensure the tasks JSON file exists, creating it if necessary."""
        if not self.tasks_file_path.exists():
            self.tasks_file_path.parent.mkdir(parents=True, exist_ok=True)
            # Create with empty items list
            initial_model = TasksModel(items=[])
            self._items_cache = initial_model
            self._save()

    def _load(self) -> TasksModel:
        """Load items from the tasks JSON file."""
        self._ensure_tasks_file_exists()

        # Use cache if available
        if self._items_cache is not None:
            return self._items_cache

        try:
            with open(self.tasks_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Validate data against the TasksModel schema
                loaded_model = TasksModel.model_validate(data)
                self._items_cache = loaded_model
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            # Handle errors like corrupted file, missing file, or validation error
            print(
                f"Warning: Error loading {self.tasks_file_path}: {e}. Initializing with empty list."
            )
            self._items_cache = TasksModel(items=[])
            self._save()  # Save the empty structure to fix/create the file

        return self._items_cache

    def _save(self) -> None:
        """Save the current items model to the JSON file atomically."""
        if self._items_cache is None:
            # If cache is None, load first to avoid overwriting with nothing
            # Or handle as an error/warning, depending on desired behavior
            print("Warning: Attempting to save without loaded data. Loading first.")
            self._load()  # Load ensures _items_cache is populated
            if self._items_cache is None:  # If loading failed and cache is still None
                print("Error: Cannot save, failed to load or initialize task data.")
                return

        # Ensure the directory exists
        self.tasks_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Use tempfile for atomic write
        fd, temp_path_str = tempfile.mkstemp(
            dir=self.tasks_file_path.parent, suffix=".json.tmp"
        )
        temp_path = Path(temp_path_str)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                # Use model_dump for Pydantic v2
                json.dump(
                    self._items_cache.model_dump(mode="json"),
                    f,
                    indent=2,
                    ensure_ascii=False,
                )

            # Atomic rename (replace): Posix works directly, Windows needs unlink first
            if os.name == "nt" and self.tasks_file_path.exists():
                self.tasks_file_path.unlink()
            os.replace(temp_path, self.tasks_file_path)
        except Exception as e:
            print(f"Error saving tasks to {self.tasks_file_path}: {e}")
            # Clean up the temporary file if rename failed
            if temp_path.exists():
                temp_path.unlink()
            raise
        finally:
            # Ensure temp file is removed if it still exists (e.g., error before replace)
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError as unlink_err:
                    print(
                        f"Warning: Could not remove temporary file {temp_path}: {unlink_err}"
                    )

    def get_templates_directory(self) -> str:
        """
        Get the directory path for storing task templates.
        
        Returns:
            Path to the templates directory.
        """
        # Create a "templates" directory in the same location as the tasks file
        templates_dir = os.path.join(os.path.dirname(self.tasks_file_path), "templates")
        
        # If tasks file is in the current directory, use 'templates' subdirectory
        if os.path.dirname(self.tasks_file_path) == "":
            templates_dir = "templates"
            
        return templates_dir

    def invalidate_cache(self) -> None:  # Helper to force reload
        """Clear the internal cache to force a reload from disk."""
        self._items_cache = None

    def get_all_items(self) -> List[TaskItem]:
        """Get all task items (Epics, Tasks, Stories, Issues)."""
        return self._load().items

    def get_item_by_id(self, item_id: str) -> Optional[TaskItem]:
        """
        Get a specific item by its ID.

        Args:
            item_id: The ID of the item to retrieve.

        Returns:
            The TaskItem if found, None otherwise.
        """
        items_model = self._load()
        return next((item for item in items_model.items if item.id == item_id), None)

    # Placeholder for complex dependency/status based next task
    def get_next_task(
        self, count: int = 1, min_priority: Optional[TaskPriority] = None
    ) -> List[TaskItem]:
        """
        Get the next actionable task items based on dependencies, status, and priority.

        Args:
            count: Number of next tasks to return (default: 1)
            min_priority: Minimum priority threshold (only return tasks with this priority or higher)

        Returns:
            List of next actionable TaskItems, sorted by priority and status.
        """
        all_items = self.get_all_items()

        # Define priority order for sorting
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
        }

        # Filter by priority if specified
        if min_priority:
            min_priority_value = priority_order[min_priority]
            all_items = [
                item
                for item in all_items
                if priority_order[item.priority] <= min_priority_value
            ]

        # First, collect in-progress items (highest priority)
        in_progress_items = []
        pending_items = []

        for item in all_items:
            # Skip items that are done or deferred
            if item.status in [TaskStatus.DONE, TaskStatus.DEFERRED]:
                continue

            # Collect in-progress items
            if item.status == TaskStatus.IN_PROGRESS:
                in_progress_items.append(item)
            # Collect pending items
            elif item.status == TaskStatus.PENDING:
                pending_items.append(item)

        # Sort in-progress items by priority
        in_progress_items.sort(key=lambda x: priority_order[x.priority])

        # Filter pending items to those with all dependencies satisfied
        actionable_pending_items = []
        for item in pending_items:
            # Check if all dependencies are completed
            deps_complete = True
            for dep_id in item.dependencies:
                dep_item = self.get_item_by_id(dep_id)
                if dep_item and dep_item.status != TaskStatus.DONE:
                    deps_complete = False
                    break

            if deps_complete:
                actionable_pending_items.append(item)

        # Sort pending items by priority
        actionable_pending_items.sort(key=lambda x: priority_order[x.priority])

        # Combine the lists, with in-progress items first
        next_tasks = in_progress_items + actionable_pending_items

        # Limit to the requested count
        return next_tasks[:count] if next_tasks else []

    def add_item(
        self,
        item_type: ItemType,
        title: str,
        description: str,
        parent_id: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        details: str = "",
        test_strategy: Optional[str] = None,
        # Allow specifying dependencies at creation
        dependencies: Optional[List[str]] = None,
        # Allow specifying children at creation (less common)
        children: Optional[List[str]] = None,
        # Allow specifying ID (for imports/migrations, otherwise auto-generate)
        item_id: Optional[str] = None,
    ) -> TaskItem:
        """
        Add a new item (Epic, Task, Story, Issue) to the hierarchy.

        Handles ID generation and updating parent/child relationships.
        """
        items_model = self._load()

        if item_id is None:
            # Generate a new ID based on type and parent (needs more robust logic)
            # Placeholder ID generation:
            prefix = item_type.value.upper()
            count = sum(1 for i in items_model.items if i.id.startswith(prefix))
            generated_id = f"{prefix}-{count + 1:03d}"

            # Attempt issue ID generation based on parent
            if item_type == ItemType.ISSUE and parent_id:
                parent_item = self.get_item_by_id(parent_id)
                if parent_item:
                    # Corrected check for child item type
                    issue_count = 0
                    for child_id in parent_item.children:
                        child_item = self.get_item_by_id(child_id)
                        if child_item and child_item.type == ItemType.ISSUE:
                            issue_count += 1
                    issue_num = issue_count + 1
                    generated_id = f"{parent_id}.{issue_num}"  # e.g., STORY-001.1
                else:
                    print(
                        f"Warning: Parent {parent_id} not found for new Issue {title}. Using generic ID {generated_id}."
                    )
            item_id = generated_id
        elif self.get_item_by_id(item_id):
            raise ValueError(f"Cannot add item. ID '{item_id}' already exists.")

        # Validate parent exists if provided
        parent_item = None
        if parent_id:
            parent_item = self.get_item_by_id(parent_id)
            if not parent_item:
                raise ValueError(f"Parent item with ID {parent_id} not found.")
            # TODO: Add validation: Issues should have Story/Task parent, Stories Task/Epic, Tasks Epic.

        # Create the new item
        new_item = TaskItem(
            id=item_id,
            type=item_type,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            parent=parent_id,
            details=details,
            test_strategy=test_strategy,
            dependencies=dependencies or [],
            children=children or [],
        )

        items_model.items.append(new_item)

        # Update parent's children list if parent exists
        if parent_item:
            if item_id not in parent_item.children:
                parent_item.children.append(item_id)
                # We need to update the parent item in the list as well
                # Corrected indentation
                for i, item in enumerate(items_model.items):
                    if item.id == parent_id:
                        items_model.items[i] = parent_item
                        break

        self._save()
        self.invalidate_cache()  # Ensure next read gets the updated list
        return new_item

    def update_item(self, updated_item: TaskItem) -> TaskItem:
        """Update an existing item by replacing it in the list."""
        items_model = self._load()
        found = False
        for i, item in enumerate(items_model.items):
            if item.id == updated_item.id:
                # TODO: Handle potential changes in parent/children consistency?
                # For now, just replace the item.
                items_model.items[i] = updated_item
                found = True
                break

        if not found:
            raise ValueError(f"Item with ID {updated_item.id} not found for update.")

        self._save()
        self.invalidate_cache()
        return updated_item

    def delete_item(self, item_id: str) -> bool:
        """
        Delete an item by its ID.

        Also attempts to remove the item ID from its parent's children list.
        Does NOT currently handle cascading deletes or dependency updates.
        """
        items_model = self._load()
        item_to_delete = None
        item_index = -1

        for i, item in enumerate(items_model.items):
            if item.id == item_id:
                item_to_delete = item
                item_index = i
                break

        if item_to_delete is None:
            return False  # Item not found

        # Remove item from the list
        items_model.items.pop(item_index)

        # Remove from parent's children list
        if item_to_delete.parent:
            parent_item = self.get_item_by_id(item_to_delete.parent)
            if parent_item:
                if item_id in parent_item.children:
                    parent_item.children.remove(item_id)
                    # Update the parent item in the list
                    # Corrected indentation
                    for i, item in enumerate(items_model.items):
                        if item.id == parent_item.id:
                            items_model.items[i] = parent_item
                            break

        # TODO: Consider handling children (orphan them? delete them?)
        # TODO: Consider updating dependencies pointing to this item

        self._save()
        self.invalidate_cache()
        return True

    def set_item_status(
        self, item_id: str, status: TaskStatus, cascade: bool = False
    ) -> bool:
        """
        Set the status of an item.

        Args:
            item_id: The ID of the item to update.
            status: The new status.
            cascade: Whether to update child items recursively.

        Returns:
            True if the item was updated, False otherwise.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            return False

        item.status = status
        # Use update_item to handle saving and cache invalidation
        try:
            self.update_item(item)
        except ValueError:
            # Should not happen if get_item_by_id succeeded
            print(f"Error: Failed to update item {item_id} after status change.")
            return False

        # Implement cascading status updates down the hierarchy
        if cascade and item.children:
            for child_id in item.children:
                # Recursively update each child and their descendants
                self.set_item_status(child_id, status, cascade=True)

        return True

    def add_dependency(self, item_id: str, depends_on_id: str) -> bool:
        """
        Add a dependency from one item to another.

        Args:
            item_id: The ID of the item that will depend on another
            depends_on_id: The ID of the item that will be depended upon

        Returns:
            True if the dependency was added, False if it already existed

        Raises:
            InvalidDependencyError: If either item does not exist
            SelfDependencyError: If an item tries to depend on itself
            CircularDependencyError: If adding the dependency would create a circular dependency
        """
        item = self.get_item_by_id(item_id)
        depends_on_item = self.get_item_by_id(depends_on_id)

        if not item:
            raise InvalidDependencyError(item_id, depends_on_id)

        if not depends_on_item:
            raise InvalidDependencyError(item_id, depends_on_id)

        # Check for self-dependency
        if item_id == depends_on_id:
            raise SelfDependencyError(item_id)

        # Check for circular dependency
        if self.has_circular_dependency(item_id, depends_on_id):
            # Get the potential cycle for better error reporting
            cycle = None
            # First check for direct circular dependency
            if item_id in depends_on_item.dependencies:
                cycle = [item_id, depends_on_id]
            else:
                # Check for indirect circular dependency through ancestors
                ancestors = self.get_dependency_ancestors(depends_on_id)
                if item_id in ancestors:
                    # Try to construct a cycle path
                    cycle = self._find_dependency_path(depends_on_id, item_id)
                    if cycle:
                        cycle = [item_id] + cycle

            raise CircularDependencyError(item_id, depends_on_id, cycle)

        if depends_on_id not in item.dependencies:
            item.dependencies.append(depends_on_id)
            self.update_item(item)
            return True
        else:
            print(f"Dependency from {item_id} to {depends_on_id} already exists.")
            return False  # Indicate no change was made

    def _find_dependency_path(
        self, start_id: str, target_id: str
    ) -> Optional[List[str]]:
        """
        Find a path from start_id to target_id through dependencies.

        Args:
            start_id: The starting item ID
            target_id: The target item ID to find

        Returns:
            A list of item IDs forming a path from start_id to target_id,
            or None if no path exists
        """
        # Use breadth-first search to find the shortest path
        queue = [(start_id, [start_id])]
        visited = set()

        while queue:
            (current_id, path) = queue.pop(0)

            if current_id == target_id:
                return path

            if current_id in visited:
                continue

            visited.add(current_id)

            # Check all dependencies of the current item
            current_item = self.get_item_by_id(current_id)
            if current_item:
                for dep_id in current_item.dependencies:
                    if dep_id not in visited:
                        queue.append((dep_id, path + [dep_id]))

        return None

    def remove_dependency(self, item_id: str, depends_on_id: str) -> bool:
        """
        Remove a dependency from an item.

        Args:
            item_id: The ID of the item to remove dependency from
            depends_on_id: The ID of the item that was depended upon

        Returns:
            True if the dependency was removed, False if it didn't exist

        Raises:
            InvalidDependencyError: If the item does not exist
        """
        item = self.get_item_by_id(item_id)

        if not item:
            raise InvalidDependencyError(item_id, depends_on_id)

        if depends_on_id in item.dependencies:
            item.dependencies.remove(depends_on_id)
            self.update_item(item)
            return True
        else:
            return False

    # Placeholder for complex dependency validation
    def validate_dependencies(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Validate dependencies for cycles and missing items.

        Returns:
            Dict with two keys:
                - "circular": List of dictionaries containing information about circular dependencies
                - "missing": List of dictionaries containing information about missing dependencies
        """
        items_model = self._load()
        result = {"circular": [], "missing": []}
        item_ids = {item.id for item in items_model.items}

        # Check for missing dependencies
        for item in items_model.items:
            # Check for missing dependencies
            for dep_id in item.dependencies:
                if dep_id not in item_ids:
                    result["missing"].append(
                        {
                            "source_id": item.id,
                            "source_title": item.title,
                            "dependency_id": dep_id,
                            "message": f"{item.id} depends on missing item {dep_id}",
                        }
                    )
            # Check parent exists
            if item.parent and item.parent not in item_ids:
                result["missing"].append(
                    {
                        "source_id": item.id,
                        "source_title": item.title,
                        "dependency_id": item.parent,
                        "message": f"{item.id} has missing parent {item.parent}",
                    }
                )
            # Check children exist
            for child_id in item.children:
                if child_id not in item_ids:
                    result["missing"].append(
                        {
                            "source_id": item.id,
                            "source_title": item.title,
                            "dependency_id": child_id,
                            "message": f"{item.id} has missing child {child_id}",
                        }
                    )

        # Check for circular dependencies using DFS
        for item in items_model.items:
            # For each item, find all cycles that include this item
            cycles = self._find_dependency_cycles(item.id)
            for cycle in cycles:
                # Add to result if not already there
                cycle_dict = {
                    "cycle": cycle,
                    "message": f"Circular dependency detected: {' -> '.join(cycle)} -> {cycle[0]}",
                }
                if cycle_dict not in result["circular"]:
                    result["circular"].append(cycle_dict)

        return result

    def _find_dependency_cycles(self, start_id: str) -> List[List[str]]:
        """
        Find all dependency cycles that include the given item using DFS.

        Args:
            start_id: The ID of the starting item

        Returns:
            List of cycles where each cycle is a list of item IDs
        """
        cycles = []

        def dfs(current_id: str, path: List[str], visited: set):
            # If we've seen this item before in the current path, we found a cycle
            if current_id in path:
                # Get the cycle part (from the first occurrence to the end)
                cycle_start = path.index(current_id)
                cycle = path[cycle_start:]
                cycles.append(cycle)
                return

            # If we've already fully explored this node, no need to do it again
            if current_id in visited:
                return

            # Mark as visited
            visited.add(current_id)

            # Continue the search
            current_item = self.get_item_by_id(current_id)
            if current_item:
                # Add this item to the path
                path.append(current_id)

                # Check all dependencies
                for dep_id in current_item.dependencies:
                    dfs(dep_id, path.copy(), visited)

        # Start the DFS from the given item
        dfs(start_id, [], set())
        return cycles

    def has_circular_dependency(self, item_id: str, depends_on_id: str) -> bool:
        """
        Check if adding a dependency from item_id to depends_on_id would create a circular dependency.

        Args:
            item_id: The ID of the item that would depend on depends_on_id
            depends_on_id: The ID of the item that would be depended upon

        Returns:
            True if this would create a circular dependency, False otherwise
        """
        # If item_id == depends_on_id, this is a direct self-dependency (circular)
        if item_id == depends_on_id:
            return True

        # Check if depends_on_id depends directly on item_id (direct circle)
        dep_item = self.get_item_by_id(depends_on_id)
        if not dep_item:
            return False  # Item doesn't exist, so not a circular dependency

        if item_id in dep_item.dependencies:
            return True  # Direct circular dependency

        # Check for indirect circular dependency
        # Get all items that depends_on_id directly or indirectly depends on
        ancestors = self.get_dependency_ancestors(depends_on_id)

        # If item_id is among these, adding the new dependency would create a cycle
        return item_id in ancestors

    # Removed add_subtask, clear_subtasks as they are replaced by add_item/update_item

    def get_metadata(self) -> Dict[str, Any]:
        """Get the metadata from the tasks JSON file."""
        return self._load().metadata

    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        """Set the metadata in the tasks JSON file."""
        items_model = self._load()
        items_model.metadata = metadata
        self._save()

    # Kept get_tasks for potential backward compatibility / direct model access
    def get_tasks_model(self) -> TasksModel:
        """Get the raw TasksModel containing all items and metadata."""
        return self._load()

    # Kept save_tasks for potential backward compatibility / direct model access
    def save_tasks_model(self, tasks_model: TasksModel) -> None:
        """Save the provided TasksModel directly."""
        self._items_cache = tasks_model
        self._save()

    # Renamed get_task to get_item
    def get_item(self, item_id: str) -> TaskItem:
        """
        Get an item by its ID, raising ValueError if not found.
        """
        item = self.get_item_by_id(item_id)
        if item is None:
            raise ValueError(f"Item with ID {item_id} not found")
        return item

    # Renamed update_task_status to update_item_status
    def update_item_status(self, item_id: str, status: TaskStatus) -> TaskItem:
        """
        Update the status of an item, raising ValueError if not found.
        """
        # Use the existing set_item_status which handles saving
        if self.set_item_status(item_id, status):
            # Refetch the item to return the updated version
            updated_item = self.get_item_by_id(item_id)
            if updated_item:
                return updated_item
            else:
                # Should not happen if set_item_status returned True
                raise RuntimeError(
                    f"Failed to refetch item {item_id} after status update."
                )
        else:
            raise ValueError(f"Item with ID {item_id} not found for status update.")

    # Placeholder for context gathering
    def get_task_context(
        self, item_id: str, include_code_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Get detailed context for a task item (placeholder implementation).

        TODO: Implement context gathering using the new hierarchy.
        Needs to traverse parent/child relationships and dependencies.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item {item_id} not found")

        context = {
            "item": item.model_dump(mode="json"),
            "parent": None,
            "children": [],
            "dependencies": [],
            "blockers": [],  # Items that depend on this one
            "related_files": [],  # TODO: Integrate with analysis
        }

        # Add parent info
        if item.parent:
            parent_item = self.get_item_by_id(item.parent)
            if parent_item:
                context["parent"] = {
                    "id": parent_item.id,
                    "title": parent_item.title,
                    "type": parent_item.type.value,
                }

        # Add children info
        for child_id in item.children:
            child_item = self.get_item_by_id(child_id)
            if child_item:
                context["children"].append(
                    {
                        "id": child_item.id,
                        "title": child_item.title,
                        "type": child_item.type.value,
                        "status": child_item.status.value,
                    }
                )

        # Add dependency info
        for dep_id in item.dependencies:
            dep_item = self.get_item_by_id(dep_id)
            if dep_item:
                context["dependencies"].append(
                    {
                        "id": dep_item.id,
                        "title": dep_item.title,
                        "type": dep_item.type.value,
                        "status": dep_item.status.value,
                    }
                )

        # Find blockers (simple check)
        all_items = self.get_all_items()
        for potential_blocker in all_items:
            if item_id in potential_blocker.dependencies:
                context["blockers"].append(
                    {
                        "id": potential_blocker.id,
                        "title": potential_blocker.title,
                        "type": potential_blocker.type.value,
                        "status": potential_blocker.status.value,
                    }
                )

        # TODO: Add code analysis context based on keywords/analysis.json
        if include_code_analysis:
            print("Warning: Code analysis context integration not yet implemented.")

        return context

    # --- Helper methods for hierarchy traversal (can be expanded) ---

    def get_children(self, item_id: str) -> List[TaskItem]:
        """Get direct children of an item.

        Args:
            item_id: The ID of the item to get children for.

        Returns:
            A list of TaskItem objects for direct children.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            return []

        children = []
        for child_id in item.children:
            child = self.get_item_by_id(child_id)
            if child:
                children.append(child)

        return children

    def get_parent(self, item_id: str) -> Optional[TaskItem]:
        """Get the parent of an item."""
        item = self.get_item_by_id(item_id)
        if not item or not item.parent:
            return None
        return self.get_item_by_id(item.parent)

    def get_descendants(self, item_id: str) -> List[str]:
        """Get all descendants (children, grandchildren, etc.) of an item.

        Args:
            item_id: The ID of the item to get descendants for.

        Returns:
            A list of item IDs for all descendants.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            return []

        descendants = []
        # Add direct children
        descendants.extend(item.children)

        # Add children of children (recursively)
        for child_id in item.children:
            descendants.extend(self.get_descendants(child_id))

        return descendants

    def get_ancestors(self, item_id: str) -> List[TaskItem]:
        """Get all ancestors of an item up to the root Epic."""
        ancestors = []
        parent = self.get_parent(item_id)
        while parent:
            ancestors.append(parent)
            parent = self.get_parent(parent.id)
        return ancestors  # List is from immediate parent up to root

    def check_if_all_children_done(self, item_id: str) -> bool:
        """
        Check if all children of an item are marked as done.
        
        Args:
            item_id: The ID of the item to check
            
        Returns:
            True if all children are done, False otherwise
        """
        children = self.get_children(item_id)
        if not children:
            return True  # No children = all done
        
        return all(child.status == TaskStatus.DONE for child in children)
    
    def get_dependent_tasks(self, item_id: str, include_indirect: bool = True) -> List[TaskItem]:
        """
        Get all tasks that depend on the specified task.
        
        This method identifies all tasks that have a dependency on the specified task.
        If include_indirect is True, it will also find tasks that indirectly depend on
        the specified task through other dependencies.
        
        Args:
            item_id: The ID of the item to find dependents for
            include_indirect: Whether to include indirect dependencies
            
        Returns:
            A list of dependent TaskItems
        """
        all_items = self.get_all_items()
        dependent_tasks = []
        visited = set()
        
        def find_dependent_tasks(task_id: str):
            if task_id in visited:
                return
            
            visited.add(task_id)
            
            # Find direct dependencies
            direct_dependents = [item for item in all_items if task_id in item.dependencies]
            
            for dependent in direct_dependents:
                dependent_tasks.append(dependent)
                
                # Recurse to find indirect dependencies if requested
                if include_indirect:
                    find_dependent_tasks(dependent.id)
        
        # Start with the task we're looking for
        find_dependent_tasks(item_id)
        
        return dependent_tasks

    def get_dependency_ancestors(self, item_id: str) -> List[str]:
        """
        Get all items that this item directly or indirectly depends on.

        Args:
            item_id: The ID of the item to get ancestors for.

        Returns:
            A list of item IDs that are dependencies (direct or indirect) of this item.
        """
        return self._get_dependency_ancestors_helper(item_id, set())

    def _get_dependency_ancestors_helper(self, item_id: str, visited: set) -> List[str]:
        """Helper method for get_dependency_ancestors that handles cycle detection."""
        # If we've already visited this item, we have a cycle
        if item_id in visited:
            return []

        # Add this item to visited set
        visited.add(item_id)

        item = self.get_item_by_id(item_id)
        if not item:
            return []

        ancestors = []

        # Add direct dependencies
        ancestors.extend(item.dependencies)

        # Recursively add dependencies of dependencies
        for dep_id in item.dependencies:
            ancestors.extend(
                self._get_dependency_ancestors_helper(dep_id, visited.copy())
            )

        # Remove duplicates while preserving order
        seen = set()
        unique_ancestors = []
        for ancestor in ancestors:
            if ancestor not in seen:
                seen.add(ancestor)
                unique_ancestors.append(ancestor)

        return unique_ancestors

    def build_hierarchy_tree(self, item_id: str) -> Optional[str]:
        """
        Build a rich Tree representation of the hierarchy for an item.

        Args:
            item_id: The ID of the root item for the tree.

        Returns:
            A Rich Tree object or None if the item doesn't exist.
        """
        from rich.tree import Tree

        item = self.get_item_by_id(item_id)
        if not item:
            return None

        # Create the root node
        tree = Tree(f"{item_id} {item.title}")

        # Add all children recursively
        def add_children(parent_tree, parent_id):
            children = self.get_children(parent_id)
            for child in sorted(children, key=lambda x: x.id):
                status_icon = {
                    TaskStatus.PENDING: "⏱️",
                    TaskStatus.IN_PROGRESS: "🔄",
                    TaskStatus.DONE: "✅",
                    TaskStatus.DEFERRED: "⏸️",
                }.get(child.status, "⏱️")

                child_node = parent_tree.add(
                    f"{child.id} ({child.type.value}) {status_icon} - {child.title}"
                )

                # Recursively add this child's children
                add_children(child_node, child.id)

        add_children(tree, item_id)
        return tree

    def get_hierarchy_path(self, item_id: str) -> Optional[str]:
        """
        Get a formatted string representing the hierarchy path of an item.

        Args:
            item_id: ID of the item to get the hierarchy path for.

        Returns:
            A string in the format "Epic > Task > Story" or None if item not found.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            return None

        path = [item.title]
        current = item

        # Add all parents to the path
        while current.parent:
            parent = self.get_item_by_id(current.parent)
            if parent:
                path.insert(0, parent.title)
                current = parent
            else:
                break

        return " > ".join(path)

    def bulk_update(
        self,
        item_ids: List[str],
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        add_dependencies: Optional[List[str]] = None,
        remove_dependencies: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, Union[bool, str]]]:
        """
        Perform bulk updates on multiple items.

        Args:
            item_ids: List of item IDs to update.
            status: New status to set.
            priority: New priority to set.
            add_dependencies: List of dependency IDs to add.
            remove_dependencies: List of dependency IDs to remove.

        Returns:
            Dictionary mapping item IDs to results (success: bool, message: str).
        """
        results = {}
        items_model = self._load()  # Load once
        items_dict = {item.id: item for item in items_model.items}
        status_priority_changed_globally = False  # Flag for final save

        for item_id in item_ids:
            result_entry = {"success": True, "message": ""}
            messages = []
            overall_success = True
            changes_made_locally = False  # Track changes for *this specific item*

            if item_id not in items_dict:
                results[item_id] = {
                    "success": False,
                    "message": f"Item '{item_id}' not found",
                }
                continue

            item = items_dict[item_id]

            # --- Add Dependencies (Save happens inside add_dependency) ---
            if add_dependencies:
                for dep_id in add_dependencies:
                    try:
                        if dep_id not in items_dict:
                            raise InvalidDependencyError(
                                item_id,
                                dep_id,
                                message=f"Item '{dep_id}' referenced in dependency does not exist",
                            )

                        # add_dependency handles validation (circular, existence) and saving
                        # It returns True if added, False if already exists, raises error otherwise
                        added = self.add_dependency(item.id, dep_id)
                        if added:
                            messages.append(f"Added dependency '{dep_id}'.")
                            changes_made_locally = True
                        # else: # Dependency already existed - maybe add a message?
                        #    messages.append(f"Dependency '{dep_id}' already exists.")
                        #    pass # Not strictly a change, but an operation was attempted
                    except DependencyValidationError as e:
                        overall_success = False
                        messages.append(
                            f"Skipped adding dependency '{dep_id}': {str(e)}"
                        )
                    except Exception as e:  # Catch unexpected errors
                        overall_success = False
                        messages.append(f"Error adding dependency '{dep_id}': {str(e)}")

            # --- Remove Dependencies (Save happens inside remove_dependency) ---
            if remove_dependencies:
                for dep_id in remove_dependencies:
                    try:
                        # remove_dependency returns True if removed, False if not found
                        removed = self.remove_dependency(item.id, dep_id)
                        if removed:
                            changes_made_locally = True
                            messages.append(f"Removed dependency '{dep_id}'.")
                        else:
                            # Dependency not found - treat as warning/skip, not a hard failure for bulk op?
                            # Current test expects this to set overall_success = False
                            overall_success = False  # Align with test expectation
                            messages.append(
                                f"Skipped removing dependency '{dep_id}': Dependency not found on '{item_id}'."
                            )
                    except Exception as e:  # Catch unexpected errors
                        overall_success = False
                        messages.append(
                            f"Error removing dependency '{dep_id}': {str(e)}"
                        )

            # --- Update Status (Do NOT save here) ---
            if status is not None and item.status != status:
                item.status = status
                changes_made_locally = True
                status_priority_changed_globally = True  # Mark for final save
                messages.append(f"Status set to '{status.value}'.")

            # --- Update Priority (Do NOT save here) ---
            if priority is not None and item.priority != priority:
                item.priority = priority
                changes_made_locally = True
                status_priority_changed_globally = True  # Mark for final save
                messages.append(f"Priority set to '{priority.value}'.")

            # --- Finalize Result for this item ---
            if not messages and not changes_made_locally:
                # Only report 'No changes' if absolutely nothing happened for this item
                result_entry["message"] = "No changes required"
            else:
                result_entry["message"] = " ".join(messages).strip()

            result_entry["success"] = overall_success
            results[item_id] = result_entry

        # --- Final Save (only if status/priority changed directly in this method) ---
        if status_priority_changed_globally:
            self._items_cache = items_model  # Update cache before saving
            self._save()

        return results
