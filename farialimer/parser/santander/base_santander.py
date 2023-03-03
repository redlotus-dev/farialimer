"""Parse module"""
from abc import abstractmethod

from farialimer.parser.basic_parser import BasicParser
from farialimer.utils.converters import (
    convert_to_int,
    convert_to_string,
    santander_convert_to_numeric,
)


class SantanderParser(BasicParser):
    """Read, parse and write"""

    def __init__(self, provider):
        super().__init__(provider=provider)

    @abstractmethod
    def get_line_register(self, line: str):
        """Given a line, returns the register type"""

    @staticmethod
    def get_filetype(line):
        """Return the filetype"""
        return line[2:11]

    @staticmethod
    def data_mapper(datatype):
        """for the spec datatype, return its respective converter"""
        core_type = SantanderParser.get_core_type(datatype)

        _data_map = {
            "X": convert_to_string,
            "9": convert_to_int,
            "9V": santander_convert_to_numeric,
        }
        return _data_map[core_type]

    @staticmethod
    def get_core_type(datatype):
        """regex that returns only characters or strings that start with 9"""
        if "V" in datatype:
            return "9V"
        if "9" in datatype:
            return "9"
        if "X" in datatype:
            return "X"
        raise ValueError("Invalid datatype")
