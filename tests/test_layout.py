""""Test Layout Properties"""
import pytest

from farialimer.utils.math_ops import sum_layout_fields_size
from farialimer.parser.b3parser import B3Parser as Parser


@pytest.mark.parametrize(
    "register, expected",
    [
        ("00", 1000),
        ("18", 1000),
        ("19", 1000),
        ("31", 1000),
        ("99", 1000),
    ],
)
def test_layout_size(register, expected):
    """Test the Sum of layout field sizes"""

    parser = Parser("imabarq014")
    layout = parser.get_doc_parser("imbarq014")
    result = sum_layout_fields_size(layout, register)

    assert result == expected
