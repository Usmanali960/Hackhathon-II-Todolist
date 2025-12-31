"""CLI output formatting utilities."""

from typing import List
from ..models.task import Task
from ..models.enums import Status, Priority
from ..utils.datetime_parser import format_datetime


class CLIFormatter:
    """Format output for CLI display."""

    def __init__(self) -> None:
        """Initialize formatter."""
        pass

    def format_task(self, task: Task, show_details: bool = False) -> str:
        """
        Format single task for display.

        Args:
            task: Task to format
            show_details: If True, include all attributes; if False, summary only

        Returns:
            Formatted string for CLI display

        Example (summary):
            [✗] #1: Buy groceries (MEDIUM)

        Example (detailed):
            [✗] #1: Buy groceries (MEDIUM)
                Due: 2025-01-15 | Tags: shopping, urgent
                Description: Buy milk, eggs, and bread
        """
        # Status indicator
        if task.is_overdue():
            status_indicator = "⚠"
        elif task.status == Status.COMPLETE:
            status_indicator = "✓"
        else:
            status_indicator = "✗"

        # Priority abbreviation
        priority_abbrev = {
            Priority.HIGH: "HIGH",
            Priority.MEDIUM: "MED",
            Priority.LOW: "LOW"
        }

        if show_details:
            # Detailed format
            lines = [
                f"[{status_indicator}] #{task.id}: {task.title} ({priority_abbrev[task.priority]})"
            ]

            if task.description:
                lines.append(f"    Description: {task.description}")

            if task.due_date:
                lines.append(f"    Due: {format_datetime(task.due_date)}")

            if task.reminder_time:
                lines.append(f"    Reminder: {format_datetime(task.reminder_time)}")

            if task.tags:
                tags_str = ", ".join(sorted(task.tags))
                lines.append(f"    Tags: {tags_str}")

            return "\n".join(lines)
        else:
            # Summary format
            return f"[{status_indicator}] #{task.id}: {task.title} ({priority_abbrev[task.priority]})"

    def format_list(self, tasks: List[Task]) -> str:
        """
        Format list of tasks for display.

        Args:
            tasks: List of Tasks to format

        Returns:
            Formatted string with task list header and table

        Example:
            Tasks (3):
            ┌────┬─────────────────────────────┬────────┬──────┐
            │ ID │ Title                       │ Status │ Prio │
            ├────┼─────────────────────────────┼────────┼──────┤
            │  1 │ Buy groceries               │  ✗    │ MED  │
            │  2 │ Complete project docs       │  ✓    │ HIGH │
            │  3 │ Pay bills                  │  ✗    │ LOW  │
            └────┴─────────────────────────────┴────────┴──────┘
        """
        if not tasks:
            return self.format_empty_list()

        # Table header
        lines = [
            f"Tasks ({len(tasks)}):",
            "┌────┬─────────────────────────────┬────────┬──────┐",
            "│ ID │ Title                       │ Status │ Prio │",
            "├────┼─────────────────────────────┼────────┼──────┤",
        ]

        # Table rows
        priority_abbrev = {
            Priority.HIGH: "HIGH",
            Priority.MEDIUM: "MED",
            Priority.LOW: "LOW"
        }

        for task in tasks:
            # Status indicator
            if task.is_overdue():
                status_indicator = "⚠"
            elif task.status == Status.COMPLETE:
                status_indicator = "✓"
            else:
                status_indicator = "✗"

            # Truncate title if too long (max 27 chars)
            title = task.title[:27]
            if len(task.title) > 27:
                title += "..."

            lines.append(
                f"│ {task.id:3} │ {title:27} │  {status_indicator:2}    │ {priority_abbrev[task.priority]:4} │"
            )

        # Table footer
        lines.append("└────┴─────────────────────────────┴────────┴──────┘")

        return "\n".join(lines)

    def format_error(self, message: str) -> str:
        """
        Format error message for display.

        Args:
            message: Error message

        Returns:
            Formatted error string with consistent prefix

        Example:
            ERROR: Task #999 not found.
        """
        return f"ERROR: {message}"

    def format_reminder(self, task: Task) -> str:
        """
        Format reminder notification for display.

        Args:
            task: Task with due reminder

        Returns:
            Formatted reminder string for CLI notification

        Example:
            🔔 REMINDER: Task #1 "Buy groceries" is due now!
        """
        return f"🔔 REMINDER: Task #{task.id} \"{task.title}\" is due now!"

    def format_success(self, message: str) -> str:
        """
        Format success message for display.

        Args:
            message: Success message

        Returns:
            Formatted success string

        Example:
            ✓ Task created successfully.
        """
        return f"✓ {message}"

    def format_empty_list(self) -> str:
        """
        Format message for empty task list.

        Returns:
            Formatted message for no tasks

        Example:
            No tasks found. Use 'Add Task' to create your first task.
        """
        return "No tasks found. Use 'Add Task' to create your first task."

    def format_filter_result(self, tasks: List[Task], criteria: str) -> str:
        """
        Format filter result message.

        Args:
            tasks: Filtered task list
            criteria: Description of filter criteria

        Returns:
            Formatted result message with count

        Example:
            Found 2 tasks matching "high" priority:
            ...
        """
        return f"Found {len(tasks)} tasks matching \"{criteria}\":"
