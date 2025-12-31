"""Integration tests for basic CLI workflow."""

import unittest
import io
import sys
from unittest.mock import patch

from src.models.task import Task
from src.models.enums import Status, Priority
from src.services.task_store import TaskStore
from src.services.task_operations import TaskOperations
from src.cli.formatter import CLIFormatter


class TestCLIBasicWorkflow(unittest.TestCase):
    """Test full task lifecycle: create -> view -> update -> complete -> delete."""

    def setUp(self):
        """Set up fresh TaskStore, TaskOperations, and Formatter for each test."""
        self.store = TaskStore()
        self.operations = TaskOperations(self.store)
        self.formatter = CLIFormatter()
        self.captured_output = io.StringIO()

    def test_full_task_lifecycle(self):
        """Test create, view, update, complete, and delete workflow."""
        # Create task
        task = self.operations.create_task(title="Buy groceries")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.status, Status.INCOMPLETE)

        # View task
        tasks = self.operations.get_all_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")

        # Update task
        updated_task = self.operations.update_task(
            task.id,
            title="Buy groceries weekly",
            description="Weekly grocery shopping"
        )

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Buy groceries weekly")
        self.assertEqual(updated_task.description, "Weekly grocery shopping")

        # Mark as complete
        completed_task = self.operations.toggle_complete(task.id)

        self.assertIsNotNone(completed_task)
        self.assertEqual(completed_task.status, Status.COMPLETE)

        # Delete task
        result = self.operations.delete_task(task.id)

        self.assertTrue(result)

        # Verify deletion
        tasks = self.operations.get_all_tasks()

        self.assertEqual(len(tasks), 0)

    def test_create_multiple_tasks_and_view(self):
        """Test creating multiple tasks and viewing all."""
        task1 = self.operations.create_task(title="Task 1", priority=Priority.HIGH)
        task2 = self.operations.create_task(title="Task 2", priority=Priority.MEDIUM)
        task3 = self.operations.create_task(title="Task 3", priority=Priority.LOW)

        tasks = self.operations.get_all_tasks()

        self.assertEqual(len(tasks), 3)
        task_titles = [t.title for t in tasks]

        self.assertIn("Task 1", task_titles)
        self.assertIn("Task 2", task_titles)
        self.assertIn("Task 3", task_titles)

    def test_invalid_task_id_error_handling(self):
        """Test error handling for invalid task ID."""
        # Try to delete nonexistent task
        result = self.operations.delete_task(999)

        self.assertFalse(result)

        # Try to update nonexistent task
        updated_task = self.operations.update_task(999, title="Updated")

        self.assertIsNone(updated_task)

        # Try to complete nonexistent task
        completed_task = self.operations.toggle_complete(999)

        self.assertIsNone(completed_task)

    def test_formatter_display_task(self):
        """Test formatter displays task correctly."""
        task = self.operations.create_task(
            title="Test task",
            priority=Priority.HIGH
        )

        formatted = self.formatter.format_task(task)

        self.assertIn("Test task", formatted)
        self.assertIn("HIGH", formatted)
        self.assertIn(str(task.id), formatted)

    def test_formatter_display_list(self):
        """Test formatter displays task list correctly."""
        self.operations.create_task(title="Task 1", priority=Priority.HIGH)
        self.operations.create_task(title="Task 2", priority=Priority.MEDIUM)

        tasks = self.operations.get_all_tasks()
        formatted = self.formatter.format_list(tasks)

        self.assertIn("Task 1", formatted)
        self.assertIn("Task 2", formatted)
        self.assertIn("Tasks (2)", formatted)

    def test_formatter_empty_list(self):
        """Test formatter handles empty task list."""
        formatted = self.formatter.format_list([])

        self.assertIn("No tasks found", formatted)


if __name__ == "__main__":
    unittest.main()
