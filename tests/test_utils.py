from farialimer.utils import convert_ymd
from datetime import date


def test_convert_ymd():
    base = "20220526"
    expected = date(2022, 5, 26)
    result = convert_ymd(base)

    assert result == expected
