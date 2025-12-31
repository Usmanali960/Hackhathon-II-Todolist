"""Unit tests for RecurrenceEngine."""

import unittest
from datetime import datetime, timedelta
from src.models.task import Task
from src.models.enums import Status, Priority
from src.models.recurrence_rule import RecurrenceRule, RecurrenceType
from src.services.recurrence_engine import RecurrenceEngine


class TestRecurrenceEngine(unittest.TestCase):
    """Test RecurrenceEngine recurring task calculation."""

    def setUp(self):
        """Set up RecurrenceEngine for each test."""
        self.engine = RecurrenceEngine()

    def test_daily_recurrence_calculates_next_day(self):
        """Test daily recurrence increments due date by 1 day."""
        current_task = Task(
            id=1,
            title="Daily task",
            due_date=datetime(2025, 12, 31, 10, 0, 0),
            reminder_time=datetime(2025, 12, 31, 9, 0, 0),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.DAILY),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
            reminder_notified=False,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        self.assertEqual(next_task.due_date.day, 1)  # January 1st
        self.assertEqual(next_task.reminder_time.day, 1)  # January 1st
        self.assertEqual(next_task.status, Status.INCOMPLETE)
        self.assertEqual(next_task.title, "Daily task")
        self.assertEqual(next_task.priority, Priority.MEDIUM)
        self.assertFalse(next_task.reminder_notified)

    def test_weekly_recurrence_calculates_next_week(self):
        """Test weekly recurrence increments due date by 7 days."""
        current_task = Task(
            id=1,
            title="Weekly task",
            due_date=datetime(2025, 12, 31, 10, 0, 0),
            reminder_time=datetime(2025, 12, 31, 9, 0, 0),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
            reminder_notified=False,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        self.assertEqual(next_task.due_date.day, 7)  # January 7th
        self.assertEqual(next_task.reminder_time.day, 7)  # January 7th
        self.assertEqual(next_task.status, Status.INCOMPLETE)
        self.assertEqual(next_task.title, "Weekly task")

    def test_custom_recurrence_calculates_next_custom_interval(self):
        """Test custom recurrence increments by specified interval."""
        current_task = Task(
            id=1,
            title="Custom recurrence task",
            due_date=datetime(2025, 12, 31, 10, 0, 0),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.CUSTOM, interval_days=3),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
            reminder_notified=False,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        self.assertEqual(next_task.due_date.day, 3)  # January 3rd
        self.assertEqual(next_task.status, Status.INCOMPLETE)
        self.assertEqual(next_task.title, "Custom recurrence task")

    def test_recurrence_preserves_all_attributes(self):
        """Test recurrence preserves task attributes except id, status, and notification state."""
        current_task = Task(
            id=1,
            title="Recurring task",
            description="Task description",
            priority=Priority.HIGH,
            tags={"work", "recurring"},
            due_date=datetime(2025, 12, 31, 10, 0, 0),
            reminder_time=datetime(2025, 12, 31, 9, 0, 0),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
            status=Status.INCOMPLETE,
            reminder_notified=True,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        self.assertEqual(next_task.title, current_task.title)
        self.assertEqual(next_task.description, current_task.description)
        self.assertEqual(next_task.priority, current_task.priority)
        self.assertEqual(next_task.tags, current_task.tags)
        self.assertEqual(next_task.recurrence_rule, current_task.recurrence_rule)
        self.assertEqual(next_task.status, Status.INCOMPLETE)
        self.assertEqual(next_task.reminder_notified, False)  # Reset to False

    def test_recurrence_without_due_date(self):
        """Test recurrence handles tasks without due dates."""
        now = datetime.now()

        current_task = Task(
            id=1,
            title="Recurring task without due date",
            recurrence_rule=RecurrenceRule(type=RecurrenceType.DAILY),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
            reminder_notified=False,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        self.assertIsNotNone(next_task.due_date)
        self.assertGreater(next_task.due_date, now)

    def test_recurrence_without_reminder_time(self):
        """Test recurrence handles tasks without reminder times."""
        current_task = Task(
            id=1,
            title="Recurring task without reminder",
            due_date=datetime(2025, 12, 31, 10, 0, 0),
            recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
            reminder_notified=False,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        self.assertIsNone(next_task.reminder_time)

    def test_custom_recurrence_requires_positive_interval(self):
        """Test custom recurrence raises error for non-positive interval."""
        current_task = Task(
            id=1,
            title="Task",
            recurrence_rule=RecurrenceRule(type=RecurrenceType.CUSTOM, interval_days=0),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
        )

        with self.assertRaises(ValueError) as context:
            self.engine.calculate_next_occurrence(current_task)

        self.assertIn("positive interval", str(context.exception))

    def test_custom_recurrence_with_negative_interval(self):
        """Test custom recurrence raises error for negative interval."""
        current_task = Task(
            id=1,
            title="Task",
            recurrence_rule=RecurrenceRule(type=RecurrenceType.CUSTOM, interval_days=-1),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
        )

        with self.assertRaises(ValueError) as context:
            self.engine.calculate_next_occurrence(current_task)

        self.assertIn("positive interval", str(context.exception))

    def test_recurrence_without_rule_raises_error(self):
        """Test recurrence raises error when task has no recurrence rule."""
        current_task = Task(
            id=1,
            title="Non-recurring task",
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
        )

        with self.assertRaises(ValueError) as context:
            self.engine.calculate_next_occurrence(current_task)

        self.assertIn("recurrence rule", str(context.exception))

    def test_reminder_time_preserved_offset(self):
        """Test reminder time preserves offset from due date."""
        current_task = Task(
            id=1,
            title="Task with reminder",
            due_date=datetime(2025, 12, 31, 17, 0, 0),
            reminder_time=datetime(2025, 12, 31, 9, 0, 0),  # 8 hours before due date
            recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
            status=Status.INCOMPLETE,
            priority=Priority.MEDIUM,
            reminder_notified=False,
        )

        next_task = self.engine.calculate_next_occurrence(current_task)

        # Check that offset is preserved (8 hours before due date)
        offset = current_task.due_date - current_task.reminder_time
        expected_reminder = next_task.due_date - offset

        self.assertEqual(next_task.reminder_time, expected_reminder)

    def test_calculate_next_due_date_for_all_types(self):
        """Test calculate_next_due_date for all recurrence types."""
        from datetime import timedelta as td

        # Daily
        base_date = datetime(2025, 12, 31, 10, 0, 0)
        daily_rule = RecurrenceRule(type=RecurrenceType.DAILY)
        next_date = self.engine.calculate_next_due_date(base_date, daily_rule)
        self.assertEqual(next_date, base_date + td(days=1))

        # Weekly
        weekly_rule = RecurrenceRule(type=RecurrenceType.WEEKLY)
        next_date = self.engine.calculate_next_due_date(base_date, weekly_rule)
        self.assertEqual(next_date, base_date + td(weeks=1))

        # Custom (5 days)
        custom_rule = RecurrenceRule(type=RecurrenceType.CUSTOM, interval_days=5)
        next_date = self.engine.calculate_next_due_date(base_date, custom_rule)
        self.assertEqual(next_date, base_date + td(days=5))


if __name__ == "__main__":
    unittest.main()
