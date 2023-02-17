"""Parse module"""
from collections import namedtuple

from farialimer.parser.basic_parser import BasicParser
from farialimer.utils.converters import (
    convert_to_int,
    convert_to_string,
    convert_to_numeric,
)

Field = namedtuple(
    "field", ["name", "description", "datatype", "convert", "start", "end"]
)


class B3Parser(BasicParser):
    """Read, parse and write"""

    def __init__(self, spec):
        super().__init__(spec=spec)

    @staticmethod
    def _get_line_register(line: str):
        return line[:2]

    @staticmethod
    def get_filetype(line):
        """Return the filetype"""
        return line[2:11]

    @staticmethod
    def _data_mapper(datatype):
        """for the spec datatype, return its respective converter"""
        _data_map = {
            "X(09)": convert_to_string,
            "X(04)": convert_to_string,
            "X(01)": convert_to_string,
            "N(04)": convert_to_string,
            "N(03)": convert_to_int,
            "N(07)": convert_to_int,
            "X(08)": convert_to_string,
            "N(15)": convert_to_int,
            "N(09)": convert_to_int,
            "N(08)": convert_to_int,
            "N(02)": convert_to_int,
            "N(19)": convert_to_int,
            "X(10)": convert_to_string,
            "X(15)": convert_to_string,
            "X(35)": convert_to_string,
            "X(20)": convert_to_string,
            "X(931)": convert_to_string,
            "N(18)V10": convert_to_numeric,
        }
        return _data_map[datatype]
