"""Test utils module"""

from datetime import date
from farialimer.utils.converters import convert_yyyymmdd


def test_convert_yyyymmdd():
    """Test year-month-date string conversion do datetime.date"""
    base = "20220526"
    expected = date(2022, 5, 26)
    result = convert_yyyymmdd(base)

    assert result == expected
