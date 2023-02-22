"""Reusable models through parsers classes"""

from collections import namedtuple

Field = namedtuple(
    "field", ["name", "description", "datatype", "convert", "start", "end"]
)
ParseObject = namedtuple("parse_object", ["value", "converter", "datatype"])
