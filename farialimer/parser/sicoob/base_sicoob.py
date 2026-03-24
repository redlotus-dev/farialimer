"""Parse module"""
from abc import abstractmethod

from farialimer.parser.basic_parser import BasicParser


class SicoobParser(BasicParser):
    """Read, parse and write"""

    def __init__(self, provider):
        super().__init__(provider=provider)

    @abstractmethod
    def get_line_register(self, line: str):
        """Given a line, returns the register type"""
