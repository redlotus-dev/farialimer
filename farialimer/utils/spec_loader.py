"""Shared spec-loading utilities for parsers and generators"""

import os
from os import walk

from farialimer.parser.models import Field
from farialimer.utils.converters import (
    convert_yyyymmdd,
    convert_yyyy_mm_dd,
    convert_to_string,
    reverse_convert_yyyymmdd,
    reverse_convert_yyyy_mm_dd,
    reverse_convert_ddmmaaaa,
    reverse_convert_hhmmss,
    reverse_convert_to_string,
)


def get_spec_dict(provider):
    """
    Load a spec dict:
    key: spec name
    value: spec yaml filepath
    """
    spec_dict = {}
    for dirpath, _, filenames in walk(f"farialimer/specs/{provider}"):
        for filename in filenames:
            if filename.endswith("yaml"):
                spec_key = filename.split(".")[0]
                filepath = os.path.join(dirpath, filename)
                spec_dict[spec_key] = filepath
    return spec_dict


def parse_spec(filepath, yml):
    """Given a spec yaml, returns namedtuple list with its props"""
    document = {}
    for key, values in yml["register"].items():
        layout_list = []
        for item, prop in values.items():
            try:
                layout_list.append(
                    Field(
                        item,
                        prop["description"],
                        prop["type"],
                        prop.get("convert"),
                        prop["pos"][0],
                        prop["pos"][1],
                        prop.get("default"),
                    )
                )
            except KeyError as err:
                raise KeyError(f"Error in {filepath} in {key} {item} - {prop['description']}") from err
        document[key] = layout_list
    return document


def convert_mapper(converter):
    """map the converter to its respective function"""
    _convert_map = {
        "aaaammdd": convert_yyyymmdd,
        "aaaa-mm-dd": convert_yyyy_mm_dd,
        "string": convert_to_string,
    }
    return _convert_map.get(converter)


def reverse_convert_mapper(converter):
    """map the converter to its respective reverse function"""
    _reverse_convert_map = {
        "aaaammdd": reverse_convert_yyyymmdd,
        "aaaa-mm-dd": reverse_convert_yyyy_mm_dd,
        "ddmmaaaa": reverse_convert_ddmmaaaa,
        "hhmmss": reverse_convert_hhmmss,
        "string": reverse_convert_to_string,
    }
    return _reverse_convert_map.get(converter)
