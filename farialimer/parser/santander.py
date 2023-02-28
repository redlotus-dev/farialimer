"""Parse module"""

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

    @staticmethod
    def get_line_register(line: str):
        """For Santander, the register type is at the position 8 (index=7).
        If the register type == 3, then and additional segment type must be added to the
        register type. Segment is at Position 14 (index=13)
        If the register type == 3 and segment == J, another additional identifier type must be
         added to the register type.
        if the position 18-19 == 52, then register type is 3J52, else its 3J"""
        register_type = line[7]
        if register_type == "3":
            segment = line[13]
            if segment == "J":
                identifier = line[17:19]
                if identifier == "52":
                    return register_type + segment + identifier
                return register_type + segment
            return register_type + segment
        return register_type

    @staticmethod
    def get_filetype(line):
        """Return the filetype"""
        return line[2:11]

    @staticmethod
    def _data_mapper(datatype):
        """for the spec datatype, return its respective converter"""
        core_type = _get_core_type(datatype)

        _data_map = {
            "X": convert_to_string,
            "9": convert_to_int,
            "9V": santander_convert_to_numeric,
        }
        return _data_map[core_type]


def _get_core_type(datatype):
    """regex that returns only characters or strings that start with 9"""
    if "V" in datatype:
        return "9V"
    if "9" in datatype:
        return "9"
    if "X" in datatype:
        return "X"
    raise ValueError("Invalid datatype")
