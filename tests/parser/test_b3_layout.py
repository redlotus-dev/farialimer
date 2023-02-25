""""Test Layout Properties"""
from functools import lru_cache

import pytest

from farialimer.parser.b3parser import B3Parser as Parser
from farialimer.utils.math_ops import sum_layout_fields_size


@pytest.mark.parametrize(
    "layout, register",
    [
        ("imbarq001", "00"),
        ("imbarq001", "01"),
        ("imbarq001", "02"),
        ("imbarq001", "03"),
        ("imbarq001", "04"),
        ("imbarq001", "05"),
        ("imbarq001", "06"),
        ("imbarq001", "07"),
        ("imbarq001", "08"),
        ("imbarq001", "09"),
        ("imbarq001", "10"),
        ("imbarq001", "11"),
        ("imbarq001", "12"),
        ("imbarq001", "13"),
        ("imbarq001", "14"),
        ("imbarq001", "15"),
        ("imbarq001", "16"),
        ("imbarq001", "17"),
        ("imbarq001", "18"),
        ("imbarq001", "19"),
        ("imbarq001", "20"),
        ("imbarq001", "21"),
        ("imbarq001", "22"),
        ("imbarq001", "23"),
        ("imbarq001", "24"),
        ("imbarq001", "25"),
        ("imbarq001", "26"),
        ("imbarq001", "27"),
        ("imbarq001", "28"),
        ("imbarq001", "29"),
        ("imbarq001", "30"),
        ("imbarq001", "31"),
        ("imbarq001", "32"),
        ("imbarq001", "34"),
        ("imbarq001", "99"),
        ("imbarq002", "00"),
        ("imbarq002", "50"),
        ("imbarq002", "99"),
        ("imbarq014", "00"),
        ("imbarq014", "18"),
        ("imbarq014", "19"),
        ("imbarq014", "31"),
        ("imbarq014", "99"),
    ],
)
def test_layout_size(layout, register):
    """Test the Sum of layout field sizes"""

    layout = get_layout(layout)
    result = sum_layout_fields_size(layout, register)
    expected = 1000

    assert result == expected


@lru_cache(maxsize=None)
def get_layout(layout):
    """To avoid opening the spec file multiples times,
    we use a cache to store the layout object"""
    parser = Parser("b3")
    layout = parser.get_doc_parser(layout)
    return layout
