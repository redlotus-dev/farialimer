"""Test ItauCobranca class"""

import pytest

from farialimer.parser.itau.cobranca import ItauCobranca


def test_cobranca_parse_spec_raises_error():
    """Test if parse_spec raises error when register field is incomplete"""
    parser = ItauCobranca("itau")
    mock_yaml = {
        "register": {
            "0REM": {
                "field_name": {"description": "X(01)", "pos": [1, 2]},
            },
        }
    }

    with pytest.raises(KeyError):
        parser.parse_spec("test", mock_yaml)
