"""Tests for reverse converter functions"""

import pytest
from datetime import date, time
from decimal import Decimal

from farialimer.utils.converters import (
    reverse_convert_to_string,
    reverse_convert_to_int,
    reverse_febraban_numeric,
    reverse_b3_numeric,
    reverse_convert_yyyymmdd,
    reverse_convert_yyyy_mm_dd,
    reverse_convert_ddmmaaaa,
    reverse_convert_hhmmss,
)


class TestReverseConvertToString:
    def test_normal_value_pads_with_spaces(self):
        assert reverse_convert_to_string("ABC", 10) == "ABC       "

    def test_exact_width_no_padding(self):
        assert reverse_convert_to_string("ABC", 3) == "ABC"

    def test_none_returns_spaces(self):
        assert reverse_convert_to_string(None, 5) == "     "

    def test_overflow_raises_value_error(self):
        with pytest.raises(ValueError):
            reverse_convert_to_string("ABCDEF", 3)


class TestReverseConvertToInt:
    def test_normal_value_zero_padded(self):
        assert reverse_convert_to_int(237, 5) == "00237"

    def test_exact_width_no_padding(self):
        assert reverse_convert_to_int(237, 3) == "237"

    def test_none_returns_zeros(self):
        assert reverse_convert_to_int(None, 6) == "000000"

    def test_zero_value(self):
        assert reverse_convert_to_int(0, 4) == "0000"

    def test_overflow_raises_value_error(self):
        with pytest.raises(ValueError):
            reverse_convert_to_int(12345, 3)


class TestReverseFebrabanNumeric:
    def test_decimal_value_with_two_places(self):
        result = reverse_febraban_numeric(Decimal("1500.00"), "9(013)V02", 15)
        assert result == "000000000150000"

    def test_zero_value(self):
        result = reverse_febraban_numeric(Decimal("0.00"), "9(013)V02", 15)
        assert result == "000000000000000"

    def test_none_returns_zeros(self):
        result = reverse_febraban_numeric(None, "9(013)V02", 15)
        assert result == "000000000000000"

    def test_overflow_raises_value_error(self):
        with pytest.raises(ValueError):
            reverse_febraban_numeric(Decimal("99999999999999.99"), "9(013)V02", 15)


class TestReverseB3Numeric:
    def test_decimal_value_with_two_places(self):
        result = reverse_b3_numeric(Decimal("1500.00"), "N(13)V02", 15)
        assert result == "000000000150000"

    def test_none_returns_zeros(self):
        result = reverse_b3_numeric(None, "N(13)V02", 15)
        assert result == "000000000000000"


class TestReverseConvertYyyymmdd:
    def test_normal_date(self):
        assert reverse_convert_yyyymmdd(date(2026, 3, 23), 8) == "20260323"

    def test_none_returns_zeros(self):
        assert reverse_convert_yyyymmdd(None, 8) == "00000000"


class TestReverseConvertYyyyMmDd:
    def test_normal_date(self):
        assert reverse_convert_yyyy_mm_dd(date(2022, 10, 20), 10) == "2022-10-20"

    def test_none_returns_spaces(self):
        assert reverse_convert_yyyy_mm_dd(None, 10) == "          "


class TestReverseConvertDdmmaaaa:
    def test_normal_date(self):
        assert reverse_convert_ddmmaaaa(date(2026, 3, 23), 8) == "23032026"

    def test_none_returns_zeros(self):
        assert reverse_convert_ddmmaaaa(None, 8) == "00000000"


class TestReverseConvertHhmmss:
    def test_normal_time(self):
        assert reverse_convert_hhmmss(time(14, 30, 0), 6) == "143000"

    def test_none_returns_zeros(self):
        assert reverse_convert_hhmmss(None, 6) == "000000"
