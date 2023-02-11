from farialimer.parser import Parser, get_filetype
import pytest


def test_get_filetype():
    path = "tests/providers/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser()
    content = parser.read_file(path)
    result = get_filetype(content[0])

    expected = "IMBARQ014"

    assert result == expected
