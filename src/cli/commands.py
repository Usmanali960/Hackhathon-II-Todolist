"""CLI command handlers."""

from typing import Optional
from ..models.enums import Priority
from ..services.task_operations import TaskOperations
from .formatter import CLIFormatter


class CommandHandler:
    """Handle CLI commands."""

    def __init__(self, operations: TaskOperations, formatter: CLIFormatter) -> None:
        """Initialize with operations and formatter."""
        self._operations = operations
        self._formatter = formatter

    def handle_add(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[str] = None,
    ):
        """
        Handle add task command.

        Args:
            title: Task title
            description: Optional description
            priority: Optional priority (high/medium/low)
            tags: Optional comma-separated tags

        Returns:
            Created Task or None if failed
        """
        try:
            # Parse priority
            parsed_priority = Priority.MEDIUM
            if priority:
                from ..utils.validators import validate_priority
                parsed_priority = validate_priority(priority)

            # Parse tags
            parsed_tags = None
            if tags:
                from ..utils.validators import validate_tags
                parsed_tags = validate_tags(tags)

            # Create task
            task = self._operations.create_task(
                title=title,
                description=description,
                priority=parsed_priority,
                tags=parsed_tags,
            )

            return task
        except Exception as e:
            return None

    def handle_delete(self, task_id: int):
        """
        Handle delete task command.

        Args:
            task_id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            return self._operations.delete_task(task_id)
        except Exception as e:
            return False

    def handle_update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[str] = None,
    ):
        """
        Handle update task command.

        Args:
            task_id: Task ID to update
            title: Optional new title
            description: Optional new description
            priority: Optional new priority (high/medium/low)
            tags: Optional comma-separated tags

        Returns:
            Updated Task or None if failed
        """
        try:
            # Build update fields
            fields = {}

            if title:
                fields["title"] = title

            if description is not None:
                fields["description"] = description

            if priority:
                from ..utils.validators import validate_priority
                fields["priority"] = validate_priority(priority)

            if tags is not None:
                from ..utils.validators import validate_tags
                fields["tags"] = validate_tags(tags)

            if fields:
                return self._operations.update_task(task_id, **fields)
            else:
                return None
        except Exception as e:
            return None

    def handle_list(self):
        """
        Handle list tasks command.

        Returns:
            List of all tasks
        """
        return self._operations.get_all_tasks()

    def handle_complete(self, task_id: int):
        """
        Handle mark task as complete command.

        Args:
            task_id: Task ID to mark complete

        Returns:
            Updated Task or None if not found
        """
        try:
            return self._operations.toggle_complete(task_id)
        except Exception as e:
            return None

    def handle_search(self, keyword: str):
        """
        Handle search tasks command.

        Args:
            keyword: Search keyword

        Returns:
            List of matching tasks
        """
        return self._operations.search_tasks(keyword)

    def handle_filter(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        has_due_date: Optional[bool] = None,
    ):
        """
        Handle filter tasks command.

        Args:
            status: Filter by status (complete/incomplete)
            priority: Filter by priority (high/medium/low)
            has_due_date: Filter by due date presence

        Returns:
            List of filtered tasks
        """
        tasks = self._operations.get_all_tasks()

        # Filter by status
        if status:
            from ..models.enums import Status
            status_map = {
                "complete": Status.COMPLETE,
                "incomplete": Status.INCOMPLETE,
            }
            if status in status_map:
                tasks = self._operations.filter_by_status(status_map[status])

        # Filter by priority
        if priority:
            priority_map = {
                "high": Priority.HIGH,
                "medium": Priority.MEDIUM,
                "low": Priority.LOW,
            }
            if priority in priority_map:
                tasks = self._operations.filter_by_priority(priority_map[priority])

        # Filter by due date
        if has_due_date is not None:
            tasks = self._operations.filter_by_due_date(has_due_date)

        return tasks

    def handle_sort(self, by: str, order: str = "asc"):
        """
        Handle sort tasks command.

        Args:
            by: Sort by (due_date, priority, title)
            order: Sort order (asc/desc)

        Returns:
            Sorted list of tasks
        """
        tasks = self._operations.get_all_tasks()
        ascending = order.lower() == "asc"

        if by == "due_date":
            tasks = self._operations.sort_by_due_date(ascending)
        elif by == "priority":
            tasks = self._operations.sort_by_priority(not ascending)  # Default descending
        elif by == "title":
            tasks = self._operations.sort_by_title(ascending)

        return tasks
