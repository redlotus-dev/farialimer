from typing import List
from datetime import date

from farialimer.providers.b3.documents.imbarq014.layouts.layout_00 import field


def sum_layout_fields_size(layout: List[field]):
    sum_size = sum([(item.end - item.start + 1) for item in layout])
    return sum_size


def convert_ymd(str_date):
    year = int(str_date[:4])
    month = int(str_date[4:6])
    day = int(str_date[6:8])

    result = date(year, month, day)
    return result
