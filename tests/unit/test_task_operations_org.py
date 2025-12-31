"""Unit tests for TaskOperations organization methods."""

import unittest
from datetime import datetime, timedelta
from src.models.task import Task
from src.models.enums import Status, Priority
from src.services.task_store import TaskStore
from src.services.task_operations import TaskOperations
from src.models.recurrence_rule import RecurrenceRule, RecurrenceType


class TestTaskOperationsOrg(unittest.TestCase):
    """Test TaskOperations search, filter, and sort functionality."""

    def setUp(self):
        """Set up fresh TaskStore and TaskOperations for each test."""
        self.store = TaskStore()
        self.operations = TaskOperations(self.store)

        # Add some test tasks
        now = datetime.now()

        self.operations.create_task(
            title="Complete project docs",
            description="Finish all markdown files",
            priority=Priority.HIGH,
            tags={"work", "documentation"},
            due_date=now + timedelta(days=7),
        )

        self.operations.create_task(
            title="Review pull requests",
            priority=Priority.MEDIUM,
            tags={"work", "review"},
        )

        self.operations.create_task(
            title="Buy groceries",
            priority=Priority.LOW,
            tags={"personal"},
            due_date=now + timedelta(days=1),
        )

        self.operations.create_task(
            title="Read documentation",
            description="Learn new APIs",
            priority=Priority.MEDIUM,
            tags={"learning"},
            due_date=now + timedelta(days=3),
        )

    def test_search_tasks_by_keyword_in_title(self):
        """Test search finds tasks with keyword in title."""
        tasks = self.operations.search_tasks("project")

        self.assertEqual(len(tasks), 1)
        self.assertIn("project", tasks[0].title.lower())

    def test_search_tasks_by_keyword_in_description(self):
        """Test search finds tasks with keyword in description."""
        tasks = self.operations.search_tasks("markdown")

        self.assertEqual(len(tasks), 1)
        self.assertIn("markdown", tasks[0].description.lower())

    def test_search_tasks_case_insensitive(self):
        """Test search is case-insensitive."""
        tasks_upper = self.operations.search_tasks("PROJECT")
        tasks_lower = self.operations.search_tasks("project")

        self.assertEqual(tasks_upper, tasks_lower)

    def test_search_tasks_returns_empty_for_no_matches(self):
        """Test search returns empty list for no matches."""
        tasks = self.operations.search_tasks("nonexistent")

        self.assertEqual(tasks, [])

    def test_filter_by_status_complete(self):
        """Test filter returns only complete tasks."""
        # Mark a task as complete
        all_tasks = self.operations.get_all_tasks()
        self.operations.toggle_complete(all_tasks[0].id)

        tasks = self.operations.filter_by_status(Status.COMPLETE)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].status, Status.COMPLETE)

    def test_filter_by_status_incomplete(self):
        """Test filter returns only incomplete tasks."""
        tasks = self.operations.filter_by_status(Status.INCOMPLETE)

        self.assertEqual(len(tasks), 3)
        for task in tasks:
            self.assertEqual(task.status, Status.INCOMPLETE)

    def test_filter_by_priority_high(self):
        """Test filter returns only high priority tasks."""
        tasks = self.operations.filter_by_priority(Priority.HIGH)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].priority, Priority.HIGH)

    def test_filter_by_priority_medium(self):
        """Test filter returns only medium priority tasks."""
        tasks = self.operations.filter_by_priority(Priority.MEDIUM)

        self.assertEqual(len(tasks), 2)

    def test_filter_by_priority_low(self):
        """Test filter returns only low priority tasks."""
        tasks = self.operations.filter_by_priority(Priority.LOW)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].priority, Priority.LOW)

    def test_filter_by_due_date_has_due_date(self):
        """Test filter returns only tasks with due dates."""
        tasks = self.operations.filter_by_due_date(True)

        self.assertEqual(len(tasks), 2)
        for task in tasks:
            self.assertIsNotNone(task.due_date)

    def test_filter_by_due_date_no_due_date(self):
        """Test filter returns only tasks without due dates."""
        tasks = self.operations.filter_by_due_date(False)

        self.assertEqual(len(tasks), 2)
        for task in tasks:
            self.assertIsNone(task.due_date)

    def test_sort_by_due_date_ascending(self):
        """Test sort tasks by due date ascending."""
        tasks = self.operations.sort_by_due_date(ascending=True)

        self.assertEqual(len(tasks), 4)
        # Tasks with due dates should come first
        self.assertIsNotNone(tasks[0].due_date)
        self.assertIsNotNone(tasks[1].due_date)
        self.assertGreater(tasks[1].due_date, tasks[0].due_date)

    def test_sort_by_due_date_descending(self):
        """Test sort tasks by due date descending."""
        tasks = self.operations.sort_by_due_date(ascending=False)

        self.assertEqual(len(tasks), 4)
        # Tasks with due dates should come first, in descending order
        self.assertIsNotNone(tasks[0].due_date)
        self.assertIsNotNone(tasks[1].due_date)
        self.assertGreater(tasks[0].due_date, tasks[1].due_date)

    def test_sort_by_priority_descending_default(self):
        """Test sort tasks by priority descending (default)."""
        tasks = self.operations.sort_by_priority()

        self.assertEqual(len(tasks), 4)
        # HIGH > MEDIUM > LOW
        self.assertEqual(tasks[0].priority, Priority.HIGH)
        self.assertEqual(tasks[2].priority, Priority.LOW)

    def test_sort_by_priority_ascending(self):
        """Test sort tasks by priority ascending."""
        tasks = self.operations.sort_by_priority(ascending=True)

        self.assertEqual(len(tasks), 4)
        # LOW < MEDIUM < HIGH
        self.assertEqual(tasks[0].priority, Priority.LOW)
        self.assertEqual(tasks[3].priority, Priority.HIGH)

    def test_sort_by_title_ascending(self):
        """Test sort tasks by title ascending."""
        tasks = self.operations.sort_by_title(ascending=True)

        self.assertEqual(len(tasks), 4)
        # Check alphabetical order
        titles = [task.title for task in tasks]
        self.assertEqual(titles, sorted(titles, key=str.lower))

    def test_sort_by_title_descending(self):
        """Test sort tasks by title descending."""
        tasks = self.operations.sort_by_title(ascending=False)

        self.assertEqual(len(tasks), 4)
        # Check reverse alphabetical order
        titles = [task.title for task in tasks]
        self.assertEqual(titles, sorted(titles, key=str.lower, reverse=True))

    def test_get_overdue_tasks(self):
        """Test get overdue tasks returns past due incomplete tasks."""
        # Create an overdue task
        self.operations.create_task(
            title="Overdue task",
            due_date=datetime.now() - timedelta(days=1),
        )

        overdue_tasks = self.operations.get_overdue_tasks()

        self.assertGreater(len(overdue_tasks), 0)
        for task in overdue_tasks:
            self.assertTrue(task.is_overdue())

    def test_get_due_reminders(self):
        """Test get due reminders returns tasks with due reminders."""
        now = datetime.now()
        # Create a task with reminder
        self.operations.create_task(
            title="Task with reminder",
            reminder_time=now - timedelta(minutes=5),
            due_date=now + timedelta(hours=1),
        )

        due_reminders = self.operations.get_due_reminders()

        self.assertGreater(len(due_reminders), 0)
        for task in due_reminders:
            self.assertTrue(task.should_remind())


if __name__ == "__main__":
    unittest.main()
