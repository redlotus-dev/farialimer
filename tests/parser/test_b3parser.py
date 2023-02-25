"""B3 specific Specs tests"""

import pytest
from farialimer.parser.b3parser import _get_core_type


@pytest.mark.parametrize(
    "datatype, expected",
    [
        ("X(01)", "X"),
        ("N(19)V07", "NV"),
        ("N(02)", "N"),
    ],
)
def test__get_core_type(datatype, expected):
    "Test the get_core_type returns the core datatype from input"
    result = _get_core_type(datatype)

    assert result == expected
