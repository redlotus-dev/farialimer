"""Test utils module"""

from datetime import date
from decimal import Decimal

from farialimer.parser.models import ParseObject
from farialimer.utils.converters import convert_yyyymmdd, b3_convert_to_numeric


def test_convert_yyyymmdd():
    """Test year-month-date string conversion do datetime.date"""
    base = ParseObject("20220526", "", "")
    expected = date(2022, 5, 26)
    result = convert_yyyymmdd(base)

    assert result == expected


def test_b3_convert_to_numeric():
    """Test given a raw numeric string and datatype, returns the correct decimal value"""
    base = ParseObject("0000000028701475025900000000", "", "N(18)V10")
    result = b3_convert_to_numeric(base)
    expected = Decimal("2870147502.59")

    assert result == expected
