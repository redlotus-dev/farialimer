"""Tests for raising exceptions"""

import pytest

from farialimer.utils.raise_exceptions import raise_error_for_nonascii_character


def test_raise_exceptions():
    """Test raise exceptions"""
    with pytest.raises(ValueError):
        raise_error_for_nonascii_character(1, "aá")
