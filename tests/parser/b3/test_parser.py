"""Specific test for the B3 Parser"""

from farialimer.parser.b3 import B3Parser as Parser


def test_get_filetype():
    """Test the getfiletype"""

    path = "tests/specs/samples/b3/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser("imbarq014")
    content = parser.read_file(path)
    result = parser.get_filetype(content[0])

    expected = "IMBARQ014"

    assert result == expected
