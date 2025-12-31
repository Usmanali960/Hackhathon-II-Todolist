"""Recurring task generation service."""

from datetime import datetime, timedelta
from typing import Optional

from ..models.task import Task
from ..models.recurrence_rule import RecurrenceRule


class RecurrenceEngine:
    """Calculate next occurrence of recurring tasks."""

    def calculate_next_occurrence(self, current_task: Task) -> Task:
        """
        Calculate next occurrence task based on recurrence rule.

        Args:
            current_task: Completed task with recurrence_rule

        Returns:
            New Task for next occurrence with:
            - New ID (auto-assigned when added to store)
            - Same title, description, priority, tags
            - Updated due_date based on recurrence rule
            - Updated reminder_time (shifted by same interval)
            - Same recurrence_rule
            - status INCOMPLETE
            - reminder_notified False

        Raises:
            ValueError: If recurrence_rule is invalid or interval missing for CUSTOM type
        """
        if not current_task.has_recurrence():
            raise ValueError("Task does not have a recurrence rule.")

        recurrence_rule = current_task.recurrence_rule

        # Calculate next due date
        if current_task.due_date:
            next_due_date = self.calculate_next_due_date(
                current_task.due_date,
                recurrence_rule
            )
        else:
            # If no due date, use current date as base
            next_due_date = self.calculate_next_due_date(
                datetime.now(),
                recurrence_rule
            )

        # Calculate next reminder time
        if current_task.reminder_time:
            next_reminder_time = self.calculate_next_reminder_time(
                current_task.reminder_time,
                current_task.due_date,
                next_due_date
            )
        else:
            next_reminder_time = None

        # Create new task with same attributes but updated dates
        from ..models.enums import Status

        return Task(
            id=0,  # Will be assigned by store
            title=current_task.title,
            description=current_task.description,
            status=Status.INCOMPLETE,
            priority=current_task.priority,
            tags=current_task.tags,
            due_date=next_due_date,
            reminder_time=next_reminder_time,
            recurrence_rule=recurrence_rule,
            reminder_notified=False,
        )

    def calculate_next_due_date(
        self,
        current_due_date: datetime,
        recurrence_rule: RecurrenceRule
    ) -> datetime:
        """
        Calculate next due date based on recurrence rule.

        Args:
            current_due_date: Current task's due date
            recurrence_rule: Recurrence rule to apply

        Returns:
            Next due date datetime

        Raises:
            ValueError: If recurrence_rule is invalid
        """
        from ..models.recurrence_rule import RecurrenceType

        if recurrence_rule.type == RecurrenceType.DAILY:
            return current_due_date + timedelta(days=1)
        elif recurrence_rule.type == RecurrenceType.WEEKLY:
            return current_due_date + timedelta(weeks=1)
        elif recurrence_rule.type == RecurrenceType.CUSTOM:
            if recurrence_rule.interval_days <= 0:
                raise ValueError(
                    "Custom recurrence requires a positive interval in days."
                )
            return current_due_date + timedelta(days=recurrence_rule.interval_days)
        else:
            raise ValueError(f"Unknown recurrence type: {recurrence_rule.type}")

    def calculate_next_reminder_time(
        self,
        current_reminder_time: datetime,
        current_due_date: datetime,
        next_due_date: datetime
    ) -> datetime:
        """
        Calculate next reminder time based on recurrence interval.

        Args:
            current_reminder_time: Current task's reminder time
            current_due_date: Current task's due date
            next_due_date: Next task's due date

        Returns:
            Next reminder time (shifted by same interval as due_date)
        """
        # Calculate offset from reminder to due date
        offset = current_due_date - current_reminder_time

        # Apply same offset to next due date
        next_reminder_time = next_due_date - offset

        return next_reminder_time
