"""Integration test for organization workflow."""

import unittest
from datetime import datetime, timedelta
from src.models.task import Task
from src.models.enums import Status, Priority
from src.services.task_store import TaskStore
from src.services.task_operations import TaskOperations
from src.cli.formatter import CLIFormatter


class TestCLIOrganization(unittest.TestCase):
    """Test organization workflow: create multiple tasks -> filter -> sort -> search."""

    def setUp(self):
        """Set up fresh TaskStore, TaskOperations, and Formatter for each test."""
        self.store = TaskStore()
        self.operations = TaskOperations(self.store)
        self.formatter = CLIFormatter()

    def test_create_multiple_tasks_and_filter(self):
        """Test creating multiple tasks and filtering by priority."""
        # Create tasks with different priorities
        self.operations.create_task(title="High priority task", priority=Priority.HIGH)
        self.operations.create_task(title="Medium priority task", priority=Priority.MEDIUM)
        self.operations.create_task(title="Low priority task", priority=Priority.LOW)
        self.operations.create_task(title="Another medium task", priority=Priority.MEDIUM)

        # Filter by high priority
        high_tasks = self.operations.filter_by_priority(Priority.HIGH)

        self.assertEqual(len(high_tasks), 1)
        self.assertEqual(high_tasks[0].priority, Priority.HIGH)

        # Filter by medium priority
        medium_tasks = self.operations.filter_by_priority(Priority.MEDIUM)

        self.assertEqual(len(medium_tasks), 2)
        for task in medium_tasks:
            self.assertEqual(task.priority, Priority.MEDIUM)

    def test_filter_and_sort_combined(self):
        """Test filtering by status and then sorting by due date."""
        now = datetime.now()

        # Create tasks with different statuses and due dates
        task1 = self.operations.create_task(
            title="Incomplete with due date",
            due_date=now + timedelta(days=3),
        )
        task2 = self.operations.create_task(
            title="Complete with due date",
            due_date=now + timedelta(days=7),
        )
        task3 = self.operations.create_task(
            title="Another incomplete",
            due_date=now + timedelta(days=5),
        )

        # Mark one task as complete
        self.operations.toggle_complete(task2.id)

        # Filter by incomplete status
        incomplete_tasks = self.operations.filter_by_status(Status.INCOMPLETE)

        self.assertEqual(len(incomplete_tasks), 2)

        # Sort by due date ascending
        sorted_tasks = self.operations.sort_by_due_date(ascending=True)

        self.assertEqual(len(sorted_tasks), 4)
        # Verify tasks with due dates are sorted
        with_due = [t for t in sorted_tasks if t.due_date is not None]
        for i in range(len(with_due) - 1):
            self.assertLessEqual(with_due[i].due_date, with_due[i + 1].due_date)

    def test_search_across_multiple_tasks(self):
        """Test searching finds matching tasks across multiple tasks."""
        # Create tasks with specific keywords
        self.operations.create_task(
            title="Write documentation",
            description="Create comprehensive docs for project",
            tags={"work", "docs"},
        )
        self.operations.create_task(
            title="Review code",
            description="Review pull requests",
            tags={"work", "review"},
        )
        self.operations.create_task(
            title="Write unit tests",
            description="Add test coverage",
            tags={"work", "testing"},
        )

        # Search for "work" - should find 3 tasks
        work_tasks = self.operations.search_tasks("work")

        self.assertEqual(len(work_tasks), 3)

        # Search for "code" - should find 1 task
        code_tasks = self.operations.search_tasks("code")

        self.assertEqual(len(code_tasks), 1)
        self.assertEqual("Review", code_tasks[0].title)

    def test_filter_by_due_date_and_sort(self):
        """Test filtering by due date presence and sorting."""
        now = datetime.now()

        # Create tasks with and without due dates
        self.operations.create_task(title="No due date task")
        self.operations.create_task(title="Task with due date", due_date=now + timedelta(days=1))
        self.operations.create_task(title="Another no due date")

        # Filter for tasks with due dates
        with_due_date = self.operations.filter_by_due_date(True)

        self.assertEqual(len(with_due_date), 1)
        self.assertIsNotNone(with_due_date[0].due_date)

        # Sort all tasks by due date
        sorted_tasks = self.operations.sort_by_due_date()

        # Tasks with due dates should come first
        self.assertIsNotNone(sorted_tasks[0].due_date)
        self.assertIsNone(sorted_tasks[-1].due_date)

    def test_empty_search_results(self):
        """Test search returns empty list for no matches."""
        self.operations.create_task(title="Task 1")
        self.operations.create_task(title="Task 2")

        results = self.operations.search_tasks("nonexistent")

        self.assertEqual(results, [])

    def test_empty_filter_results(self):
        """Test filter returns empty list for no matches."""
        # Only create low priority tasks
        self.operations.create_task(title="Low task 1", priority=Priority.LOW)
        self.operations.create_task(title="Low task 2", priority=Priority.LOW)

        # Filter for high priority
        high_tasks = self.operations.filter_by_priority(Priority.HIGH)

        self.assertEqual(high_tasks, [])

    def test_formatter_with_filtered_results(self):
        """Test formatter displays filtered results correctly."""
        self.operations.create_task(title="High priority task", priority=Priority.HIGH)
        self.operations.create_task(title="Medium priority task", priority=Priority.MEDIUM)

        tasks = self.operations.filter_by_priority(Priority.HIGH)
        formatted = self.formatter.format_filter_result(tasks, 'high" priority"')

        self.assertIn("Found", formatted)
        self.assertIn("1", formatted)
        self.assertIn("high", formatted.lower())


if __name__ == "__main__":
    unittest.main()
