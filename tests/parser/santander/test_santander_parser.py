"""Santander specific Specs tests"""

import pytest
from farialimer.parser.santander import _get_core_type, SantanderParser


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
    result = _get_core_type(datatype)

    assert result == expected


@pytest.mark.parametrize(
    "line, expected",
    [
        ("03300000C00000 0000", "0"),
        ("03300011C00000 0000", "1"),
        ("03300033C0000A 0000", "3A"),
        ("03300033C0000B 0000", "3B"),
        ("03300033C0000C 0000", "3C"),
        ("03300033C0000J 0000", "3J"),
        ("03300033C0000J 0052", "3J52"),
        ("0330003300000I 0000", "3I"),
        ("03300033C0000N 0000", "3N"),
        ("03300033C0000W 0000", "3W"),
        ("03300033C0000O 0000", "3O"),
        ("03300033C0000Z 0000", "3Z"),
        ("03300035C00000 0000", "5"),
        ("03300049C00000 0000", "9"),
    ],
)
def test_get_line_register(line, expected):
    """
    Test the get_line_register. For Santander, the register type is at the position 8 (index=7).
    If the register type == 3, then and additional segment type must be added to the register type.
    Segment is at Position 14 (index=13)
    If the register type == 3 and segment == J, another additional identifier
    type must be added to the register type.
    if the position 18-19 == 52, then register type is 3J52, else its 3J
    """
    result = SantanderParser.get_line_register(line)

    assert result == expected
