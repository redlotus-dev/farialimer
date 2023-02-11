"""Test utils module"""

from datetime import date
from farialimer.utils import convert_ymd


def test_convert_ymd():
    """Test year-month-date string conversion do datetime.date"""
    base = "20220526"
    expected = date(2022, 5, 26)
    result = convert_ymd(base)

    assert result == expected
