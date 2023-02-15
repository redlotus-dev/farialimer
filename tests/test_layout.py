""""Test Layout Properties"""

from farialimer.utils.math_ops import sum_layout_fields_size
from farialimer.parser import Parser


def test_layout_size():
    """Test the Sum of layout field sizes"""

    parser = Parser()
    layout = parser.get_doc_parser("imbarq014")
    result = sum_layout_fields_size(layout)

    expected = 1000

    assert result == expected
