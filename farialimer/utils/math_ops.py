"""Module for common and re-usable functions"""

from typing import List

from farialimer.parser import Field


def sum_layout_fields_size(layout: List[Field]):
    """Given a layout, sum all the fields length"""
    sum_size = sum((item.end - item.start + 1) for item in layout["00"])
    return sum_size
