"""In-memory task storage service."""

from typing import List, Optional
from datetime import datetime

from ..models.task import Task


class TaskStore:
    """In-memory storage for Task entities."""

    def __init__(self) -> None:
        """Initialize empty task store with auto-incrementing ID counter."""
        self._tasks = {}
        self._next_id = 1

    def add(self, task: Task) -> Task:
        """
        Add task to storage and assign auto-incrementing ID.

        Args:
            task: Task entity without ID (id will be assigned)

        Returns:
            Task with assigned ID

        Raises:
            ValueError: If task validation fails
        """
        # Assign auto-incrementing ID
        task.id = self._next_id
        self._next_id += 1

        # Store task
        self._tasks[task.id] = task

        return task

    def get(self, id: int) -> Optional[Task]:
        """
        Retrieve task by ID.

        Args:
            id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(id)

    def delete(self, id: int) -> bool:
        """
        Delete task by ID.

        Args:
            id: Task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        if id in self._tasks:
            del self._tasks[id]
            return True
        return False

    def update(self, id: int, **fields) -> Optional[Task]:
        """
        Update task fields by ID.

        Args:
            id: Task ID to update
            **fields: Fields to update (title, description, priority, tags, etc.)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If validation fails for any field
        """
        task = self.get(id)
        if task is None:
            return None

        # Update mutable fields (id and created_at are immutable)
        for field, value in fields.items():
            if field not in ["id", "created_at"]:
                setattr(task, field, value)

        # Set updated_at to current time
        task.updated_at = datetime.now()

        return task

    def list_all(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all Task entities (empty list if none exist)
        """
        return list(self._tasks.values())

    def exists(self, id: int) -> bool:
        """
        Check if task exists.

        Args:
            id: Task ID to check

        Returns:
            True if task exists, False otherwise
        """
        return id in self._tasks

    def count(self) -> int:
        """
        Get total task count.

        Returns:
            Number of tasks in storage
        """
        return len(self._tasks)
