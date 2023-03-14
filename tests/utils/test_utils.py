"""Test utils module"""

from datetime import date
from decimal import Decimal

import pytest

from farialimer.parser.models import ParseObject
from farialimer.utils.converters import (
    convert_yyyymmdd,
    convert_yyyy_mm_dd,
    b3_convert_to_numeric,
    convert_to_int,
    febraban_convert_to_numeric,
)


@pytest.mark.parametrize(
    "value, datatype, expected",
    [
        ("20220526", "N(08)", date(2022, 5, 26)),
        ("00000000", "N(08", None),
    ],
)
def test_convert_yyyymmdd(value, datatype, expected):
    """Test year-month-date string conversion do datetime.date"""
    base = ParseObject(value, datatype, "")
    result = convert_yyyymmdd(base)

    assert result == expected


def test_convert_yyyy_mm_dd():
    """Test year-month-date string conversion do datetime.date"""
    base = ParseObject("2022-05-26", "X(10)", "")
    result = convert_yyyy_mm_dd(base)

    assert result == date(2022, 5, 26)


@pytest.mark.parametrize(
    "value, datatype, expected",
    [
        ("0000000028701475025900000000", "N(18)V10", Decimal("2870147502.59")),
        ("                            ", "N(18)V10", None),
        ("", "N(3)", None),
    ],
)
def test_b3_convert_to_numeric(value, datatype, expected):
    """Test given a raw numeric string and datatype, returns the correct decimal value"""
    base = ParseObject(value, "", datatype)
    result = b3_convert_to_numeric(base)

    assert result == expected


@pytest.mark.parametrize(
    "value, datatype, expected",
    [
        ("0000000028701475025900000000", "9(18)V10", Decimal("2870147502.59")),
        ("                            ", "9(18)V10", None),
        ("", "9(3)", None),
    ],
)
def test_febraban_convert_to_numeric(value, datatype, expected):
    """Test given a raw numeric string and datatype, returns the correct decimal value"""
    base = ParseObject(value, "", datatype)
    result = febraban_convert_to_numeric(base)

    assert result == expected


@pytest.mark.parametrize(
    "value, datatype, expected",
    [
        ("00005", "N(5)", 5),
        ("                            ", "N(28)", None),
        ("", "N(3)", None),
    ],
)
def test_b3_convert_to_int(value, datatype, expected):
    """Test given a raw numeric string and datatype, returns the correct decimal value"""
    base = ParseObject(value, "", datatype)
    result = convert_to_int(base)

    assert result == expected
