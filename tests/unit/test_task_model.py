"""Unit tests for Task model."""

import unittest
from datetime import datetime, timedelta
from src.models.task import Task
from src.models.enums import Status, Priority
from src.models.recurrence_rule import RecurrenceRule, RecurrenceType


class TestTaskModel(unittest.TestCase):
    """Test Task model creation and validation."""

    def test_task_creation_minimal(self):
        """Test creating a minimal task with required fields."""
        task = Task(
            id=1,
            title="Buy groceries"
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertIsNone(task.description)
        self.assertEqual(task.status, Status.INCOMPLETE)
        self.assertEqual(task.priority, Priority.MEDIUM)
        self.assertEqual(task.tags, set())
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.reminder_time)
        self.assertIsNone(task.recurrence_rule)
        self.assertIsInstance(task.created_at, datetime)
        self.assertIsInstance(task.updated_at, datetime)
        self.assertFalse(task.reminder_notified)

    def test_task_creation_full(self):
        """Test creating a task with all fields."""
        task = Task(
            id=2,
            title="Complete project docs",
            description="Finish all markdown files",
            status=Status.INCOMPLETE,
            priority=Priority.HIGH,
            tags={"work", "documentation"},
            due_date=datetime(2026, 1, 15, 17, 0, 0),
            reminder_time=datetime(2026, 1, 15, 9, 0, 0),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY)
        )

        self.assertEqual(task.id, 2)
        self.assertEqual(task.title, "Complete project docs")
        self.assertEqual(task.description, "Finish all markdown files")
        self.assertEqual(task.status, Status.INCOMPLETE)
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, {"work", "documentation"})
        self.assertIsNotNone(task.due_date)
        self.assertIsNotNone(task.reminder_time)
        self.assertIsNotNone(task.recurrence_rule)

    def test_is_overdue_incomplete_past_due_date(self):
        """Test is_overdue returns True for incomplete task with past due date."""
        task = Task(
            id=1,
            title="Overdue task",
            due_date=datetime.now() - timedelta(days=1),
            status=Status.INCOMPLETE
        )

        self.assertTrue(task.is_overdue())

    def test_is_overdue_complete_past_due_date(self):
        """Test is_overdue returns False for complete task with past due date."""
        task = Task(
            id=1,
            title="Complete task",
            due_date=datetime.now() - timedelta(days=1),
            status=Status.COMPLETE
        )

        self.assertFalse(task.is_overdue())

    def test_is_overdue_future_due_date(self):
        """Test is_overdue returns False for task with future due date."""
        task = Task(
            id=1,
            title="Future task",
            due_date=datetime.now() + timedelta(days=1),
            status=Status.INCOMPLETE
        )

        self.assertFalse(task.is_overdue())

    def test_is_overdue_no_due_date(self):
        """Test is_overdue returns False for task without due date."""
        task = Task(
            id=1,
            title="Task without due date"
        )

        self.assertFalse(task.is_overdue())

    def test_should_remind_with_due_reminder(self):
        """Test should_remind returns True for task with due reminder."""
        task = Task(
            id=1,
            title="Task with reminder",
            reminder_time=datetime.now() - timedelta(minutes=5),
            reminder_notified=False
        )

        self.assertTrue(task.should_remind())

    def test_should_remind_already_notified(self):
        """Test should_remind returns False for already notified task."""
        task = Task(
            id=1,
            title="Notified task",
            reminder_time=datetime.now() - timedelta(minutes=5),
            reminder_notified=True
        )

        self.assertFalse(task.should_remind())

    def test_should_remind_no_reminder_time(self):
        """Test should_remind returns False for task without reminder time."""
        task = Task(
            id=1,
            title="Task without reminder"
        )

        self.assertFalse(task.should_remind())

    def test_has_recurrence_with_rule(self):
        """Test has_recurrence returns True for task with recurrence rule."""
        task = Task(
            id=1,
            title="Recurring task",
            recurrence_rule=RecurrenceRule(type=RecurrenceType.DAILY)
        )

        self.assertTrue(task.has_recurrence())

    def test_has_recurrence_no_rule(self):
        """Test has_recurrence returns False for task without recurrence rule."""
        task = Task(
            id=1,
            title="One-time task"
        )

        self.assertFalse(task.has_recurrence())

    def test_can_complete_incomplete_task(self):
        """Test can_complete returns True for incomplete task."""
        task = Task(
            id=1,
            title="Incomplete task",
            status=Status.INCOMPLETE
        )

        self.assertTrue(task.can_complete())

    def test_can_complete_complete_task(self):
        """Test can_complete returns False for complete task."""
        task = Task(
            id=1,
            title="Complete task",
            status=Status.COMPLETE
        )

        self.assertFalse(task.can_complete())


if __name__ == "__main__":
    unittest.main()
