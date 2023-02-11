"""Module for common and re-usable functions"""

from typing import List
from datetime import date

from farialimer.providers.b3.documents.imbarq014.layouts.layout_00 import Field


def sum_layout_fields_size(layout: List[Field]):
    """Given a layout, sum all the fields length"""
    sum_size = sum((item.end - item.start + 1) for item in layout)
    return sum_size


def convert_ymd(str_date):
    """
    Given a str like 20221020
    returns a date like date(2022,10,20)
    """
    year = int(str_date[:4])
    month = int(str_date[4:6])
    day = int(str_date[6:8])

    result = date(year, month, day)
    return result
