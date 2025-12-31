"""Recurrence rule dataclass for recurring tasks."""

from dataclasses import dataclass
from datetime import datetime

from .enums import RecurrenceType


@dataclass
class RecurrenceRule:
    """Defines recurrence pattern for recurring tasks.

    Attributes:
        type: Recurrence type (daily, weekly, or custom)
        interval_days: Number of days for custom recurrence (default: 1)
            Only used when type is RecurrenceType.CUSTOM
    """

    type: RecurrenceType
    interval_days: int = 1  # Only used for CUSTOM type
