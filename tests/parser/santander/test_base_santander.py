"""Test the base santander parser class"""

import pytest
from farialimer.parser.santander.base_santander import SantanderParser


@pytest.mark.parametrize(
    "datatype, expected",
    [
        ("X(01)", "X"),
        ("9(19)V07", "9V"),
        ("9(02)", "9"),
    ],
)
def test__get_core_type(datatype, expected):
    """Test the get_core_type returns the core datatype from input"""
    result = SantanderParser.get_core_type(datatype)

    assert result == expected
