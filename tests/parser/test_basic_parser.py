"""Test the basic parser module"""
import pytest

from farialimer.parser.basic_parser import BasicParser
import farialimer.utils.converters as conv


@pytest.mark.parametrize(
    "datatype, expected",
    [
        ("9(4)V9(2)", conv.febraban_convert_to_numeric),
        ("9(3)", conv.convert_to_int),
        ("X(3)", conv.convert_to_string),
    ],
)
def test_parse_data_mapper(datatype, expected):
    """Test the data mapper"""
    result = BasicParser.data_mapper(datatype)
    assert result is expected


@pytest.mark.parametrize(
    "datatype, expected",
    [
        ("9(4)V9(2)", "9V"),
        ("9(3)", "9"),
        ("X(3)", "X"),
    ],
)
def test_parse_get_core_type(datatype, expected):
    """Test the get core type"""
    result = BasicParser.get_core_type(datatype)
    assert result == expected


def test_parse_get_core_type_raises_value_error():
    """Test the get core type"""
    with pytest.raises(ValueError):
        BasicParser.get_core_type("invalid")
