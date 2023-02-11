import farialimer.providers.b3.documents.imbarq014.layouts as layout
from farialimer.utils import sum_layout_fields_size


def test_layout_size():

    result = sum_layout_fields_size(layout.layout_00)
    expected = 1000

    assert result == expected
