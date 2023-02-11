import farialimer.providers.b3.documents.imbarq014.layouts as layout
from typing import List
from farialimer.providers.b3.documents.imbarq014.layouts.layout_00 import (
    field,
    NUMERIC,
    TEXT,
    DATE,
)
from farialimer.utils import convert_ymd
from collections import OrderedDict


class Parser:
    @staticmethod
    def read_file(filepath):
        with open(filepath) as finput:
            content = finput.readlines()
        return content

    def parse_content(self, content):
        filetype = get_filetype(content[0])  # primeira linha do conteudo
        print(filetype)
        for line in content:
            line_register = self._get_line_register(line)
            layout = self._get_layout(line_register)
            print(filetype, line_register, layout)
            register = parse_line(line, layout)
        # qual é o tipo de arquivo
        # qual é o layout

    def write(self, filteype):
        pass

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
    return line[2:11]


def parse_line(line, layout: List[field]):

    parse_result = OrderedDict()
    for item in layout:
        parse_item = line[item.start - 1 : item.end]
        if item.datatype == NUMERIC:
            parse_item = int(parse_item)
        if item.datatype == TEXT:
            parse_item = parse_item.strip()
        if item.datatype == DATE:
            parse_item = convert_ymd(parse_item)
        parse_result[item.description] = parse_item
    return parse_result
