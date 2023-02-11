"""Parse module"""

from collections import OrderedDict
from typing import List
import farialimer.providers.b3.documents.imbarq014.layouts as layout
from farialimer.providers.b3.documents.imbarq014.layouts.layout_00 import (
    Field,
    NUMERIC,
    TEXT,
    DATE,
)
from farialimer.utils import convert_ymd


class Parser:
    """Read, parse and write"""

    @staticmethod
    def read_file(filepath, encoding="utf-8"):
        """Read the contents from a given filepath"""
        with open(filepath, encoding=encoding) as finput:
            content = finput.readlines()
        return content

    def parse_content(self, content):
        """Parse the content and return a list of dicts"""
        filetype = get_filetype(content[0])  # primeira linha do conteudo
        print(filetype)
        for line in content:
            line_register = self._get_line_register(line)
            layout_type = self._get_layout(line_register)
            print(filetype, line_register, layout_type)
            register = parse_line(line, layout_type)
            print(register)
        # qual é o tipo de arquivo
        # qual é o layout

    def write(self):
        """Output the content on a given format"""
        return ""

    def _get_line_register(self, line: str):
        return line[:2]

    def _get_layout(self, line_register: str):
        _register_map = {
            "00": layout.layout_00,
            "18": layout.layout_18,
            "19": layout.layout_19,
            "31": layout.layout_31,
            "99": layout.layout_99,
        }
        return _register_map[line_register]


def get_filetype(line):
    """Return the filetype"""
    return line[2:11]


def parse_line(line, fields: List[Field]):
    """Given a line and a list of fields, extract the value from each layout item,
    parse it and return an OrderedDict"""

    parse_result = OrderedDict()
    for item in fields:
        parse_item = line[item.start - 1 : item.end]
        if item.datatype == NUMERIC:
            parse_item = int(parse_item)
        if item.datatype == TEXT:
            parse_item = parse_item.strip()
        if item.datatype == DATE:
            parse_item = convert_ymd(parse_item)
        parse_result[item.description] = parse_item
    return parse_result
