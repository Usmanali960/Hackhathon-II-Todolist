"""Enumerations for Task entity."""

from enum import Enum


class Status(Enum):
    """Task completion status."""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


class Priority(Enum):
    """Task priority level."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurrenceType(Enum):
    """Recurrence pattern type."""
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"  # Requires interval_days in RecurrenceRule
