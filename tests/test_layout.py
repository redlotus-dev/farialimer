""""Test Layout Properties"""

import farialimer.specs.b3.imbarq014.layouts.layout_00 as layout
from farialimer.utils.math_ops import sum_layout_fields_size


def test_layout_size():
    """Test the Sum of layout field sizes"""

    result = sum_layout_fields_size(layout.layout)
    expected = 1000

    assert result == expected
