"""Business logic service for task operations."""

from typing import List, Optional, Set
from datetime import datetime

from ..models.task import Task
from ..models.enums import Status, Priority
from .task_store import TaskStore
from .recurrence_engine import RecurrenceEngine
from ..utils.validators import (
    validate_title,
    validate_description,
    validate_priority,
    validate_tags,
)


class TaskOperations:
    """Business logic for task operations."""

    def __init__(self, store: TaskStore) -> None:
        """Initialize with task store dependency."""
        self._store = store
        self._recurrence_engine = RecurrenceEngine()

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[Set[str]] = None,
        due_date: Optional[datetime] = None,
        reminder_time: Optional[datetime] = None,
        recurrence_rule=None,
    ) -> Task:
        """
        Create new task with validation.

        Args:
            title: Task title (required)
            description: Optional description
            priority: Task priority (default: MEDIUM)
            tags: Set of tags (default: empty)
            due_date: Optional due date
            reminder_time: Optional reminder time
            recurrence_rule: Optional recurrence rule

        Returns:
            Created Task with auto-generated ID

        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        validate_title(title)
        validate_description(description)

        # Create task with validated fields
        task = Task(
            id=0,  # Will be assigned by store
            title=title,
            description=description,
            priority=priority,
            tags=tags or set(),
            due_date=due_date,
            reminder_time=reminder_time,
            recurrence_rule=recurrence_rule,
        )

        return self._store.add(task)

    def delete_task(self, id: int) -> bool:
        """
        Delete task by ID.

        Args:
            id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        return self._store.delete(id)

    def update_task(self, id: int, **fields) -> Optional[Task]:
        """
        Update task fields by ID.

        Args:
            id: Task ID to update
            **fields: Fields to update (any Task attribute except id/created_at)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If validation fails or trying to update immutable fields
        """
        # Check for immutable fields
        if "id" in fields or "created_at" in fields:
            raise ValueError("Cannot update id or created_at fields.")

        # Validate fields if provided
        if "title" in fields:
            validate_title(fields["title"])
        if "description" in fields:
            validate_description(fields["description"])
        if "priority" in fields and isinstance(fields["priority"], str):
            fields["priority"] = validate_priority(fields["priority"])

        return self._store.update(id, **fields)

    def get_task(self, id: int) -> Optional[Task]:
        """
        Retrieve task by ID.

        Args:
            id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self._store.get(id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all Task entities
        """
        return self._store.list_all()

    def toggle_complete(self, id: int) -> Optional[Task]:
        """
        Toggle task completion status and generate recurring task if applicable.

        Args:
            id: Task ID to toggle

        Returns:
            Updated Task if found, None otherwise

        Note:
            If task has recurrence_rule, generates next occurrence task
            (RecurrenceEngine integration will be added in User Story 3)
        """
        task = self._store.get(id)
        if task is None:
            return None

        # Toggle status
        if task.status == Status.INCOMPLETE:
            task.status = Status.COMPLETE

            # Generate recurring task if applicable
            if task.has_recurrence():
                next_task = self._recurrence_engine.calculate_next_occurrence(task)
                self._store.add(next_task)
        else:
            task.status = Status.INCOMPLETE

        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title or description.

        Args:
            keyword: Search term (case-insensitive)

        Returns:
            List of matching Tasks (empty if none match)
        """
        keyword_lower = keyword.lower()
        all_tasks = self._store.list_all()

        return [
            task
            for task in all_tasks
            if keyword_lower in task.title.lower()
            or (task.description and keyword_lower in task.description.lower())
            or any(keyword_lower in tag.lower() for tag in task.tags)
        ]

    def filter_by_status(self, status: Status) -> List[Task]:
        """
        Filter tasks by completion status.

        Args:
            status: Status to filter by

        Returns:
            List of matching Tasks
        """
        return [task for task in self._store.list_all() if task.status == status]

    def filter_by_priority(self, priority: Priority) -> List[Task]:
        """
        Filter tasks by priority level.

        Args:
            priority: Priority to filter by

        Returns:
            List of matching Tasks
        """
        return [task for task in self._store.list_all() if task.priority == priority]

    def filter_by_due_date(self, has_due_date: bool) -> List[Task]:
        """
        Filter tasks by presence of due date.

        Args:
            has_due_date: True to include only tasks with due dates,
                        False to include only tasks without due dates

        Returns:
            List of matching Tasks
        """
        if has_due_date:
            return [task for task in self._store.list_all() if task.due_date is not None]
        else:
            return [task for task in self._store.list_all() if task.due_date is None]

    def sort_by_due_date(self, ascending: bool = True) -> List[Task]:
        """
        Sort tasks by due date.

        Args:
            ascending: Sort order (default: ascending)

        Returns:
            Sorted list of Tasks (tasks without due_date placed at end)
        """
        tasks = self._store.list_all()

        # Separate tasks with and without due dates
        with_due = [t for t in tasks if t.due_date is not None]
        without_due = [t for t in tasks if t.due_date is None]

        # Sort tasks with due dates
        with_due.sort(key=lambda t: t.due_date, reverse=not ascending)

        return with_due + without_due

    def sort_by_priority(self, ascending: bool = False) -> List[Task]:
        """
        Sort tasks by priority (HIGH > MEDIUM > LOW).

        Args:
            ascending: Sort order (default: descending)

        Returns:
            Sorted list of Tasks
        """
        tasks = self._store.list_all()

        priority_order = {Priority.HIGH: 2, Priority.MEDIUM: 1, Priority.LOW: 0}

        tasks.sort(key=lambda t: priority_order[t.priority], reverse=not ascending)

        return tasks

    def sort_by_title(self, ascending: bool = True) -> List[Task]:
        """
        Sort tasks alphabetically by title.

        Args:
            ascending: Sort order (default: ascending)

        Returns:
            Sorted list of Tasks (case-insensitive)
        """
        tasks = self._store.list_all()

        tasks.sort(key=lambda t: t.title.lower(), reverse=not ascending)

        return tasks

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks.

        Returns:
            List of Tasks that are overdue (due_date < now AND status INCOMPLETE)
        """
        return [task for task in self._store.list_all() if task.is_overdue()]

    def get_due_reminders(self) -> List[Task]:
        """
        Get tasks with due reminders.

        Returns:
            List of Tasks with reminder_time <= now AND reminder_notified == False
        """
        return [task for task in self._store.list_all() if task.should_remind()]

    def mark_reminder_notified(self, task: Task) -> None:
        """
        Mark task reminder as notified.

        Args:
            task: Task to update

        Note:
            Updates task in storage with reminder_notified = True
        """
        task.reminder_notified = True
