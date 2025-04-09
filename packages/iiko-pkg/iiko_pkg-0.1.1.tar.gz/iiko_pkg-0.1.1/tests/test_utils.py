"""
Tests for iiko_pkg.utils
"""

import unittest
from datetime import datetime, timezone

from iiko_pkg.utils import format_datetime, parse_datetime, filter_none_values, ensure_list


class TestUtils(unittest.TestCase):
    """Test utils"""

    def test_format_datetime(self):
        """Test format_datetime function"""
        dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        formatted = format_datetime(dt)
        self.assertEqual(formatted, "2023-01-01T12:00:00+00:00")
        
        # Test with naive datetime
        dt = datetime(2023, 1, 1, 12, 0, 0)
        formatted = format_datetime(dt)
        self.assertEqual(formatted, "2023-01-01T12:00:00+00:00")

    def test_parse_datetime(self):
        """Test parse_datetime function"""
        dt_str = "2023-01-01T12:00:00+00:00"
        dt = parse_datetime(dt_str)
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.tzinfo, timezone.utc)
        
        # Test with Z timezone
        dt_str = "2023-01-01T12:00:00Z"
        dt = parse_datetime(dt_str)
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.tzinfo, timezone.utc)
        
        # Test with no timezone
        dt_str = "2023-01-01T12:00:00"
        dt = parse_datetime(dt_str)
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        
        # Test with milliseconds
        dt_str = "2023-01-01T12:00:00.123"
        dt = parse_datetime(dt_str)
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)
        self.assertEqual(dt.microsecond, 123000)
        
        # Test with space separator
        dt_str = "2023-01-01 12:00:00"
        dt = parse_datetime(dt_str)
        self.assertEqual(dt.year, 2023)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)

    def test_filter_none_values(self):
        """Test filter_none_values function"""
        data = {
            "key1": "value1",
            "key2": None,
            "key3": 0,
            "key4": "",
            "key5": False
        }
        
        filtered = filter_none_values(data)
        self.assertEqual(filtered, {
            "key1": "value1",
            "key3": 0,
            "key4": "",
            "key5": False
        })

    def test_ensure_list(self):
        """Test ensure_list function"""
        # Test with string
        result = ensure_list("test")
        self.assertEqual(result, ["test"])
        
        # Test with list
        result = ensure_list(["test1", "test2"])
        self.assertEqual(result, ["test1", "test2"])
        
        # Test with empty list
        result = ensure_list([])
        self.assertEqual(result, [])
        
        # Test with None
        result = ensure_list(None)
        self.assertEqual(result, [None])


if __name__ == "__main__":
    unittest.main()
