""""Test Layout Properties"""

import pytest

from farialimer.utils.math_ops import sum_layout_fields_size
from tests.helpers import _get_spec_list, _get_spec


@pytest.mark.parametrize("provider, spec", _get_spec_list())
def test_spec_size(provider, spec):
    """Test the Sum of layout field sizes. Assumes that the last field has the correct size (end)"""

    spec_parser = _get_spec(provider, spec)
    for register, fields in spec_parser.items():
        result = sum_layout_fields_size(spec_parser, register)
        expected = fields[-1].end

        assert result == expected
