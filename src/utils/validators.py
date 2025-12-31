"""Input validation utilities."""

from datetime import datetime
from typing import Set, Optional

from ..models.enums import Priority


class ValidationError(Exception):
    """Custom validation error with user-friendly messages."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def validate_title(title: str) -> None:
    """Validate task title.

    Args:
        title: Task title to validate

    Raises:
        ValidationError: If title is empty or exceeds max length
    """
    if not title or not title.strip():
        raise ValidationError("Title is required. Please provide a task title.")

    if len(title.strip()) > 200:
        raise ValidationError("Title exceeds maximum length of 200 characters.")


def validate_priority(priority: str) -> Priority:
    """Validate and parse priority value.

    Args:
        priority: Priority value as string

    Returns:
        Priority enum value

    Raises:
        ValidationError: If priority value is invalid
    """
    priority_map = {
        "high": Priority.HIGH,
        "medium": Priority.MEDIUM,
        "low": Priority.LOW,
    }

    priority_lower = priority.strip().lower()
    if priority_lower not in priority_map:
        raise ValidationError(
            f"Invalid priority '{priority}'. Allowed values: high, medium, low."
        )

    return priority_map[priority_lower]


def validate_tags(tags_str: str) -> Set[str]:
    """Validate and parse tags from comma-separated string.

    Args:
        tags_str: Comma-separated tags string

    Returns:
        Set of validated tags

    Raises:
        ValidationError: If any tag exceeds max length
    """
    if not tags_str or not tags_str.strip():
        return set()

    tags = set()
    for tag in tags_str.split(","):
        tag = tag.strip()
        if not tag:
            continue

        if len(tag) > 50:
            raise ValidationError(
                f"Tag '{tag}' exceeds maximum length of 50 characters."
            )

        tags.add(tag)

    return tags


def validate_description(description: Optional[str]) -> Optional[str]:
    """Validate task description.

    Args:
        description: Task description to validate

    Returns:
        Validated description (or None)

    Raises:
        ValidationError: If description exceeds max length
    """
    if not description:
        return None

    if len(description) > 1000:
        raise ValidationError(
            "Description exceeds maximum length of 1000 characters."
        )

    return description


def validate_due_date(due_date_str: Optional[str]) -> Optional[datetime]:
    """Validate and parse due date.

    Args:
        due_date_str: Due date as string (YYYY-MM-DD or MM/DD/YYYY format)

    Returns:
        Parsed datetime

    Raises:
        ValidationError: If date format is invalid or date is in past
    """
    if not due_date_str:
        return None

    from ..utils.datetime_parser import parse_date

    # Try to parse date
    try:
        due_date = parse_date(due_date_str)
    except ValueError as e:
        raise ValidationError(str(e))

    # Check if due date is in future
    if due_date < datetime.now():
        raise ValidationError("Due date must be in the future.")

    return due_date


def validate_reminder_time(
    reminder_time_str: Optional[str],
    due_date: Optional[datetime]
) -> Optional[datetime]:
    """Validate and parse reminder time.

    Args:
        reminder_time_str: Reminder time as string (HH:MM or HH:MM AM/PM format)
        due_date: Associated due date for validation

    Returns:
        Parsed datetime (with current date) or None

    Raises:
        ValidationError: If time format is invalid or reminder is after due date
    """
    if not reminder_time_str:
        return None

    if not due_date:
        raise ValidationError(
            "Reminder time requires a due date to be set first."
        )

    from ..utils.datetime_parser import parse_time

    reminder_time_str = reminder_time_str.strip()

    # Try to parse time
    try:
        hour, minute = parse_time(reminder_time_str)
    except ValueError as e:
        raise ValidationError(str(e))

    # Combine with due_date date
    reminder_datetime = due_date.replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )

    # Validate reminder is before or at due date
    if reminder_datetime > due_date:
        raise ValidationError(
            "Reminder time must be before or at due date."
        )

    return reminder_datetime


def validate_recurrence(
    recurrence_type: Optional[str],
    interval_days: Optional[int] = None
) -> None:
    """Validate recurrence parameters.

    Args:
        recurrence_type: Recurrence type (daily, weekly, custom)
        interval_days: Interval days for custom recurrence

    Returns:
        None (validation only - RecurrenceRule object created separately)

    Raises:
        ValidationError: If parameters are invalid
    """
    if not recurrence_type:
        return None

    recurrence_type_lower = recurrence_type.strip().lower()

    if recurrence_type_lower not in ["daily", "weekly", "custom"]:
        raise ValidationError(
            f"Invalid recurrence type '{recurrence_type}'. "
            "Allowed values: daily, weekly, custom."
        )

    if recurrence_type_lower == "custom":
        if interval_days is None or interval_days <= 0:
            raise ValidationError(
                "Custom recurrence requires a positive interval in days."
            )
