"""Parse module"""

import re

from farialimer.parser.basic_parser import BasicParser
from farialimer.utils.converters import (
    convert_to_int,
    convert_to_string,
    b3_convert_to_numeric,
)


class B3Parser(BasicParser):
    """Read, parse and write"""

    def __init__(self, provider):
        super().__init__(provider=provider)

    def get_line_register(self, line: str):
        return line[:2]

    @staticmethod
    def get_filetype(line):
        """Return the filetype"""
        return line[2:11]

    @staticmethod
    def data_mapper(datatype):
        """for the spec datatype, return its respective converter"""
        core_type = B3Parser.get_core_type(datatype)

        _data_map = {
            "X": convert_to_string,
            "N": convert_to_int,
            "NV": b3_convert_to_numeric,
        }
        return _data_map[core_type]

    @staticmethod
    def get_core_type(datatype):
        result = re.sub(r"[^A-Z]", "", datatype)
        return result
