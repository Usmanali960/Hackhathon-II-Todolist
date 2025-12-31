"""Datetime parsing utilities."""

from datetime import datetime, time
from typing import Tuple


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime.

    Supports:
        - YYYY-MM-DD format (recommended)
        - MM/DD/YYYY format

    Args:
        date_str: Date string to parse

    Returns:
        Parsed datetime

    Raises:
        ValueError: If date format is invalid
    """
    date_str = date_str.strip()

    # Try YYYY-MM-DD format
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass

    # Try MM/DD/YYYY format
    try:
        return datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        pass

    raise ValueError(
        f"Invalid date format '{date_str}'. Use YYYY-MM-DD or MM/DD/YYYY."
    )


def parse_time(time_str: str) -> Tuple[int, int]:
    """Parse time string to hour and minute components.

    Supports:
        - HH:MM format (24-hour)
        - HH:MM AM/PM format (12-hour)

    Args:
        time_str: Time string to parse

    Returns:
        Tuple of (hour, minute)

    Raises:
        ValueError: If time format is invalid
    """
    time_str = time_str.strip()

    # Try HH:MM format
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.hour, time_obj.minute
    except ValueError:
        pass

    # Try HH:MM AM/PM format
    try:
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        return time_obj.hour, time_obj.minute
    except ValueError:
        pass

    raise ValueError(
        f"Invalid time format '{time_str}'. Use HH:MM or HH:MM AM/PM."
    )


def format_datetime(dt: datetime) -> str:
    """Format datetime to human-readable string.

    Args:
        dt: Datetime to format

    Returns:
        Formatted date string (YYYY-MM-DD HH:MM)
    """
    return dt.strftime("%Y-%m-%d %H:%M")


def format_date(dt: datetime) -> str:
    """Format datetime to date string.

    Args:
        dt: Datetime to format

    Returns:
        Formatted date string (YYYY-MM-DD)
    """
    return dt.strftime("%Y-%m-%d")


def is_future(dt: datetime) -> bool:
    """Check if datetime is in the future.

    Args:
        dt: Datetime to check

    Returns:
        True if datetime is in future, False otherwise
    """
    return dt > datetime.now()


def is_past(dt: datetime) -> bool:
    """Check if datetime is in the past.

    Args:
        dt: Datetime to check

    Returns:
        True if datetime is in the past, False otherwise
    """
    return dt < datetime.now()
