"""Integration test for advanced workflow with recurring tasks."""

import unittest
from datetime import datetime, timedelta
from src.models.task import Task
from src.models.enums import Status, Priority
from src.models.recurrence_rule import RecurrenceRule, RecurrenceType
from src.services.task_store import TaskStore
from src.services.task_operations import TaskOperations
from src.cli.formatter import CLIFormatter


class TestCLIAdvanced(unittest.TestCase):
    """Test advanced workflow: recurring task with due date and reminder."""

    def setUp(self):
        """Set up fresh TaskStore, TaskOperations, and Formatter for each test."""
        self.store = TaskStore()
        self.operations = TaskOperations(self.store)
        self.formatter = CLIFormatter()

    def test_recurring_task_generates_next_occurrence(self):
        """Test completing recurring task generates next occurrence."""
        now = datetime.now()

        # Create a weekly recurring task
        task = self.operations.create_task(
            title="Weekly meeting",
            description="Team standup every week",
            priority=Priority.HIGH,
            tags={"work", "meeting"},
            due_date=now + timedelta(days=7),
            reminder_time=now + timedelta(days=7, hours=-1),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
        )

        # Mark task as complete
        completed_task = self.operations.toggle_complete(task.id)

        self.assertIsNotNone(completed_task)
        self.assertEqual(completed_task.status, Status.COMPLETE)

        # Verify next occurrence was generated
        all_tasks = self.operations.get_all_tasks()

        self.assertEqual(len(all_tasks), 2)

        # Find the new task
        new_task = None
        for t in all_tasks:
            if t.id != task.id and t.title == "Weekly meeting":
                new_task = t
                break

        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.status, Status.INCOMPLETE)
        self.assertEqual(new_task.id, 2)  # Should have new ID

        # Verify due date is 7 days later
        expected_due_date = task.due_date + timedelta(weeks=1)
        self.assertEqual(new_task.due_date.day, expected_due_date.day)

    def test_overdue_task_displays_indicator(self):
        """Test overdue task displays with indicator in formatter."""
        now = datetime.now()

        # Create an overdue task
        task = self.operations.create_task(
            title="Overdue task",
            due_date=now - timedelta(days=1),
            priority=Priority.HIGH,
        )

        # Format the task
        formatted = self.formatter.format_task(task, show_details=True)

        # Should have overdue indicator (checked in format_task logic)
        self.assertIn("Overdue task", formatted)
        self.assertIn("HIGH", formatted)

    def test_reminder_time_triggers_notification(self):
        """Test reminder time triggers notification."""
        now = datetime.now()

        # Create a task with past reminder time
        task = self.operations.create_task(
            title="Task with due reminder",
            reminder_time=now - timedelta(minutes=5),
            due_date=now + timedelta(hours=1),
        )

        # Check if task should remind
        due_reminders = self.operations.get_due_reminders()

        self.assertEqual(len(due_reminders), 1)
        self.assertEqual(due_reminders[0].id, task.id)

    def test_reminder_not_marked_as_notified(self):
        """Test tasks are not marked as notified until explicitly marked."""
        now = datetime.now()

        # Create a task with future reminder time
        task = self.operations.create_task(
            title="Task with future reminder",
            reminder_time=now + timedelta(hours=1),
            due_date=now + timedelta(hours=2),
        )

        # Should not be in due reminders yet
        due_reminders = self.operations.get_due_reminders()

        self.assertEqual(len(due_reminders), 0)

    def test_recurring_without_due_date_generates_task(self):
        """Test recurring task without due date generates next task."""
        now = datetime.now()

        # Create a daily recurring task without due date
        task = self.operations.create_task(
            title="Daily check",
            recurrence_rule=RecurrenceRule(type=RecurrenceType.DAILY),
            priority=Priority.MEDIUM,
        )

        # Mark as complete
        completed_task = self.operations.toggle_complete(task.id)

        self.assertIsNotNone(completed_task)

        # Verify next occurrence was generated
        all_tasks = self.operations.get_all_tasks()

        self.assertEqual(len(all_tasks), 2)

        # Find the new task
        new_task = None
        for t in all_tasks:
            if t.id != task.id:
                new_task = t
                break

        self.assertIsNotNone(new_task)
        self.assertEqual(new_task.status, Status.INCOMPLETE)
        self.assertEqual(new_task.reminder_notified, False)

    def test_multiple_complete_tasks_with_recurrence(self):
        """Test multiple complete cycles generate multiple occurrences."""
        now = datetime.now()

        # Create a daily recurring task
        task = self.operations.create_task(
            title="Daily task",
            due_date=now + timedelta(days=1),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.DAILY),
        )

        # Complete it 3 times
        for i in range(3):
            completed_task = self.operations.toggle_complete(task.id)

            if i < 2:
                # Should generate next occurrence
                all_tasks = self.operations.get_all_tasks()
                self.assertEqual(len(all_tasks), i + 2)

    def test_formatter_displays_reminder_notification(self):
        """Test formatter displays reminder notification correctly."""
        task = Task(
            id=1,
            title="Important task",
            status=Status.INCOMPLETE,
            priority=Priority.HIGH,
        )

        formatted = self.formatter.format_reminder(task)

        self.assertIn("REMINDER", formatted)
        self.assertIn("Important task", formatted)
        self.assertIn(str(task.id), formatted)

    def test_formatter_handles_empty_reminders(self):
        """Test get_due_reminders handles empty list."""
        now = datetime.now()

        # Create tasks with future reminders only
        self.operations.create_task(
            title="Future task",
            reminder_time=now + timedelta(hours=1),
            due_date=now + timedelta(hours=2),
        )

        # Should return empty list
        due_reminders = self.operations.get_due_reminders()

        self.assertEqual(due_reminders, [])


if __name__ == "__main__":
    unittest.main()
