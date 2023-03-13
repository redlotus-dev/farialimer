"""Basic Interface for TXT Parsers"""

import os
from abc import ABC, abstractmethod
from collections import OrderedDict
from os import walk
from typing import List

import yaml

from farialimer.parser.models import Field, ParseObject
from farialimer.utils.converters import (
    convert_yyyymmdd,
    convert_yyyy_mm_dd,
    convert_to_string,
    convert_to_int,
    febraban_convert_to_numeric,
)
from farialimer.utils.raise_exceptions import raise_error_for_nonascii_character


class BasicParser(ABC):
    """Base Class for reading and parsing txt files"""

    def __init__(self, provider):
        self.provider = provider
        self.spec_dict = get_spec_dict(self.provider)

    @staticmethod
    def read_file(filepath, encoding="latin1"):
        """Read the contents from a given filepath"""
        content = []
        with open(filepath, encoding=encoding) as finput:
            for line in finput:
                content.append(line)
        return content

    @abstractmethod
    def get_line_register(self, line):
        """Given a line, returns the register type"""

    @staticmethod
    def data_mapper(datatype):
        """for the spec datatype, return its respective converter"""
        core_type = BasicParser.get_core_type(datatype)

        _data_map = {
            "X": convert_to_string,
            "9": convert_to_int,
            "9V": febraban_convert_to_numeric,
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

    def parse(self, content, spec):
        """Given a content and spec document, returns a list of dict with the parsed information"""
        parsed_lines = []
        document_parser = self.get_spec_parser(spec)
        for idx, line in enumerate(content, start=1):
            raise_error_for_nonascii_character(idx, line)
            line_register = self.get_line_register(line)
            layout_type = document_parser[line_register]
            register = self.parse_line(line, layout_type)
            parsed_lines.append(register)
        return parsed_lines

    def get_spec_parser(self, spec):
        """Given a spec, returns namedtuple list with its props"""
        filepath = self.spec_dict[spec]
        with open(filepath, encoding="utf-8") as yinput:
            yml = yaml.safe_load(yinput)
            document = {}

            for key, values in yml["register"].items():
                layout_list = []
                for item, prop in values.items():
                    layout_list.append(
                        Field(
                            item,
                            prop["description"],
                            prop["type"],
                            prop.get("convert"),
                            prop["pos"][0],
                            prop["pos"][1],
                        )
                    )
                document[key] = layout_list
        return document

    def parse_line(self, line, fields: List[Field]):
        """Given a line and a list of fields, extract the value from each layout item,
        parse it and return an OrderedDict"""
        parse_result = OrderedDict()
        for item in fields:
            parse_item = line[item.start - 1 : item.end]
            converter = convert_mapper(item.convert) or self.data_mapper(item.datatype)
            parse_obj = ParseObject(parse_item, converter, item.datatype)
            parse_item = converter(parse_obj)
            parse_result[item.name] = parse_item
        return parse_result


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


def convert_mapper(converter):
    """map the converter to it respective function"""
    _convert_map = {
        "aaaammdd": convert_yyyymmdd,
        "aaaa-mm-dd": convert_yyyy_mm_dd,
        "string": convert_to_string,
    }
    return _convert_map.get(converter)
