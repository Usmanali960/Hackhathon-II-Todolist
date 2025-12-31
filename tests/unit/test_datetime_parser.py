"""Unit tests for datetime parser."""

import unittest
from datetime import datetime, timedelta
from src.utils.datetime_parser import parse_date, parse_time, format_datetime, format_date, is_future, is_past


class TestDatetimeParser(unittest.TestCase):
    """Test datetime parsing utilities."""

    def test_parse_date_yyyy_mm_dd_format(self):
        """Test parsing date in YYYY-MM-DD format."""
        result = parse_date("2025-12-31")

        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 31)

    def test_parse_date_mm_dd_yyyy_format(self):
        """Test parsing date in MM/DD/YYYY format."""
        result = parse_date("12/31/2025")

        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 31)

    def test_parse_date_invalid_format_raises_error(self):
        """Test parsing date with invalid format raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date("2025/12/31")  # Invalid format

    def test_parse_time_hh_mm_format_24hour(self):
        """Test parsing time in HH:MM format (24-hour)."""
        hour, minute = parse_time("14:30")

        self.assertEqual(hour, 14)
        self.assertEqual(minute, 30)

    def test_parse_time_hh_mm_format_12hour_am(self):
        """Test parsing time in HH:MM AM format."""
        hour, minute = parse_time("9:30 AM")

        self.assertEqual(hour, 9)
        self.assertEqual(minute, 30)

    def test_parse_time_hh_mm_format_12hour_pm(self):
        """Test parsing time in HH:MM PM format."""
        hour, minute = parse_time("9:30 PM")

        self.assertEqual(hour, 21)
        self.assertEqual(minute, 30)

    def test_parse_time_invalid_format_raises_error(self):
        """Test parsing time with invalid format raises ValueError."""
        with self.assertRaises(ValueError):
            parse_time("9:30")  # Missing AM/PM - will raise from parsing

    def test_format_datetime_to_string(self):
        """Test formatting datetime to human-readable string."""
        dt = datetime(2025, 12, 31, 14, 30, 0)
        result = format_datetime(dt)

        self.assertEqual(result, "2025-12-31 14:30")

    def test_format_date_to_string(self):
        """Test formatting datetime to date string."""
        dt = datetime(2025, 12, 31, 14, 30, 0)
        result = format_date(dt)

        self.assertEqual(result, "2025-12-31")

    def test_is_future_returns_true_for_future_datetime(self):
        """Test is_future returns True for future datetime."""
        future = datetime.now() + timedelta(hours=1)
        self.assertTrue(is_future(future))

    def test_is_future_returns_false_for_past_datetime(self):
        """Test is_future returns False for past datetime."""
        past = datetime.now() - timedelta(hours=1)
        self.assertFalse(is_future(past))

    def test_is_future_returns_true_for_current_datetime_with_offset(self):
        """Test is_future returns True for datetime slightly in future."""
        future = datetime.now() + timedelta(seconds=1)
        self.assertTrue(is_future(future))

    def test_is_past_returns_true_for_past_datetime(self):
        """Test is_past returns True for past datetime."""
        past = datetime.now() - timedelta(hours=1)
        self.assertTrue(is_past(past))

    def test_is_past_returns_false_for_current_datetime_with_offset(self):
        """Test is_past returns False for datetime slightly in future."""
        future = datetime.now() + timedelta(seconds=1)
        self.assertFalse(is_past(future))

    def test_parse_time_with_leading_zeros(self):
        """Test parsing time with leading zeros."""
        hour, minute = parse_time("09:05 AM")

        self.assertEqual(hour, 9)
        self.assertEqual(minute, 5)

    def test_parse_date_with_leading_zeros(self):
        """Test parsing date with leading zeros."""
        result = parse_date("01/05/2025")

        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 5)
        self.assertEqual(result.year, 2025)

    def test_parse_date_february_29(self):
        """Test parsing February 29 (valid in leap years)."""
        result = parse_date("02/29/2024")  # 2024 is a leap year

        self.assertEqual(result.month, 2)
        self.assertEqual(result.day, 29)
        self.assertEqual(result.year, 2024)


if __name__ == "__main__":
    unittest.main()
