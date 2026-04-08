"""Módulo de geração B3"""

import re

from farialimer.generator.basic_generator import BasicGenerator
from farialimer.utils.converters import (
    reverse_convert_to_string,
    reverse_convert_to_int,
    reverse_b3_numeric,
)


class B3Generator(BasicGenerator):
    """Gerador de arquivos B3 IMBARQ"""

    def __init__(self, provider: str = "b3"):
        super().__init__(provider=provider)

    @staticmethod
    def data_unmapper(datatype: str):
        """Retorna o conversor reverso para datatypes B3 (N, NV, X)"""
        core_type = B3Generator.get_core_type(datatype)
        _data_unmap = {
            "X": lambda valor, datatype, largura: reverse_convert_to_string(valor, largura),
            "N": lambda valor, datatype, largura: reverse_convert_to_int(valor, largura),
            "NV": reverse_b3_numeric,
        }
        return _data_unmap[core_type]

    @staticmethod
    def get_core_type(datatype: str) -> str:
        """Extrai o tipo base removendo caracteres não-alfabéticos"""
        result = re.sub(r"[^A-Z]", "", datatype)
        return result
