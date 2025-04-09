"""
Utility functions for iiko.services API
"""

import datetime
from typing import Dict, Any, List, Union


def format_datetime(dt: datetime.datetime) -> str:
    """Format datetime to ISO 8601 format with timezone"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.isoformat()


def parse_datetime(dt_str: str) -> datetime.datetime:
    """Parse ISO 8601 datetime string to datetime object"""
    try:
        return datetime.datetime.fromisoformat(dt_str)
    except ValueError:
        # Handle case where the string doesn't include timezone
        try:
            dt = datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt
        except ValueError:
            # Try to parse with different format
            formats = [
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f",
            ]
            for fmt in formats:
                try:
                    return datetime.datetime.strptime(dt_str, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Could not parse datetime string: {dt_str}")


def filter_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}


def ensure_list(value: Union[List[str], str, None]) -> List[str]:
    """Ensure value is a list"""
    if value is None:
        return [None]
    if isinstance(value, str):
        return [value]
    return value
