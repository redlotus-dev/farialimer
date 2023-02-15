"""Parse module"""
import os
from collections import OrderedDict
from collections import namedtuple
from os import walk
from typing import List

import yaml

from farialimer.utils.converters import convert_yyyymmdd

Field = namedtuple(
    "field", ["name", "description", "datatype", "convert", "start", "end"]
)


class Parser:
    """Read, parse and write"""

    def __init__(self):
        self.spec_dict = get_spec_dict()

    @staticmethod
    def read_file(filepath, encoding="utf-8"):
        """Read the contents from a given filepath"""
        with open(filepath, encoding=encoding) as finput:
            content = finput.readlines()
        return content

    def parse(self, content, spec):
        """Given the content and the doc spec, return the parsed lines"""
        parsed_lines = []
        try:
            document_parser = self.get_doc_parser(spec)
            for line in content[:1]:
                line_register = self._get_line_register(line)
                layout_type = document_parser[line_register]
                register = parse_line(line, layout_type)
                parsed_lines.append(register)
        except KeyError as err:
            print(err)
        return parsed_lines

    def write(self):
        """Output the content on a given format"""
        return ""

    def _get_line_register(self, line: str):
        return line[:2]

    def get_doc_parser(self, spec):
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


def get_filetype(line):
    """Return the filetype"""
    return line[2:11]


def parse_line(line, fields: List[Field]):
    """Given a line and a list of fields, extract the value from each layout item,
    parse it and return an OrderedDict"""
    parse_result = OrderedDict()
    for item in fields:
        print(item)
        parse_item = line[item.start - 1 : item.end]
        converter = convert_mapper(item.convert) or data_mapper(item.datatype)
        parse_item = converter(parse_item)
        parse_result[item.name] = parse_item
    return parse_result


def convert_to_int(parse_item):
    """given a string-like int, convert it to int"""
    return int(parse_item)


def convert_to_string(parse_item):
    """given a string, removes leading/trailing blank spaces"""
    return parse_item.strip()


def convert_mapper(converter):
    """map the converter to it respective function"""
    _convert_map = {"aaaammdd": convert_yyyymmdd, "string": convert_to_string}
    return _convert_map.get(converter)


def data_mapper(datatype):
    """for the spec datatype, return its respective converter"""
    _data_map = {
        "X(09)": convert_to_string,
        "N(03)": convert_to_int,
        "N(07)": convert_to_int,
        "X(08)": convert_to_string,
        "N(15)": convert_to_int,
        "N(09)": convert_to_int,
        "N(08)": convert_to_int,
        "N(02)": convert_to_int,
        "X(931)": convert_to_string,
    }
    return _data_map.get(datatype)


def get_spec_dict():
    """
    Load a spec dict:
    key: spec name
    value: spec yaml filepath
    """
    spec_dict = {}
    for dirpath, _, filenames in walk("farialimer/specs"):
        for filename in filenames:
            if filename.endswith("yaml"):
                spec_key = filename.split(".")[0]
                filepath = os.path.join(dirpath, filename)
                spec_dict[spec_key] = filepath
    return spec_dict
