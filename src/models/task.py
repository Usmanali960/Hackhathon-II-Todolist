"""Task entity class."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Set, Optional

from .enums import Status, Priority
from .recurrence_rule import RecurrenceRule


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique auto-incrementing identifier
        title: Task title (required, non-empty)
        description: Optional description (max 1000 chars)
        status: Completion status (INCOMPLETE or COMPLETE)
        priority: Task priority (HIGH, MEDIUM, or LOW)
        tags: Set of tags (each 1-50 chars)
        due_date: Optional due date
        reminder_time: Optional reminder time
        recurrence_rule: Optional recurrence rule
        created_at: Creation timestamp (immutable)
        updated_at: Last update timestamp
        reminder_notified: True if reminder has been displayed
    """

    id: int
    title: str
    description: Optional[str] = None
    status: Status = Status.INCOMPLETE
    priority: Priority = Priority.MEDIUM
    tags: Set[str] = field(default_factory=set)
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    recurrence_rule: Optional[RecurrenceRule] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    reminder_notified: bool = False

    def __post_init__(self):
        """Ensure timestamps are set correctly."""
        if self.updated_at == self.created_at:
            # Force them to differ by at least 1 microsecond
            self.updated_at = datetime.fromtimestamp(self.updated_at.timestamp() + 0.000001)

    def is_overdue(self) -> bool:
        """Check if task is overdue.

        Returns:
            True if task has a due_date, due_date is in the past,
            and status is INCOMPLETE
        """
        if self.due_date is None:
            return False

        return self.due_date < datetime.now() and self.status == Status.INCOMPLETE

    def should_remind(self) -> bool:
        """Check if task should trigger a reminder.

        Returns:
            True if task has a reminder_time, reminder_time is now or in the past,
            and reminder_notified is False
        """
        if self.reminder_time is None:
            return False

        return (
            self.reminder_time <= datetime.now() and not self.reminder_notified
        )

    def has_recurrence(self) -> bool:
        """Check if task is recurring.

        Returns:
            True if task has a recurrence_rule
        """
        return self.recurrence_rule is not None

    def can_complete(self) -> bool:
        """Check if task can be marked complete.

        Returns:
            True if task status is INCOMPLETE
        """
        return self.status == Status.INCOMPLETE
