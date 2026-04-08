"""Interface base para geração de arquivos CNAB de largura fixa"""

from abc import ABC
from typing import List

import yaml

from farialimer.parser.models import Field
from farialimer.utils.converters import (
    reverse_convert_to_string,
    reverse_convert_to_int,
    reverse_febraban_numeric,
)
from farialimer.utils.spec_loader import (
    get_spec_dict,
    parse_spec,
    reverse_convert_mapper,
)


class BasicGenerator(ABC):
    """Classe base para geração de arquivos CNAB de largura fixa.

    Recebe uma lista de registros (tipo_registro, dados) e gera
    linhas de largura fixa baseadas nas specs YAML.
    """

    def __init__(self, provider: str):
        self.provider = provider
        self.spec_dict = get_spec_dict(self.provider)

    def get_spec_parser(self, spec: str) -> dict:
        """Carrega e retorna a spec YAML parseada"""
        filepath = self.spec_dict[spec]
        with open(filepath, encoding="utf-8") as yinput:
            yml = yaml.safe_load(yinput)
            return parse_spec(filepath, yml)

    def gerar(self, registros: list[tuple[str, dict]], spec: str) -> list[str]:
        """Gera linhas de largura fixa a partir de uma lista de registros.

        Args:
            registros: lista de tuplas (tipo_registro, dados).
            spec: nome da spec YAML a usar.

        Returns:
            Lista de strings de largura fixa.
        """
        linhas = []
        documento = self.get_spec_parser(spec)
        for tipo_registro, dados in registros:
            campos = documento[tipo_registro]
            linha = self.gerar_linha(dados, campos)
            linhas.append(linha)
        return linhas

    def gerar_linha(self, dados: dict, campos: List[Field]) -> str:
        """Gera uma linha de largura fixa a partir de um dict de valores.

        Args:
            dados: dicionário com nome_campo -> valor.
            campos: lista de Fields da spec.

        Returns:
            String de largura fixa.
        """
        comprimento_linha = campos[-1].end
        linha = list(" " * comprimento_linha)

        for campo in campos:
            largura = campo.end - campo.start + 1
            valor = dados.get(campo.name)

            if valor is None and campo.default is not None:
                valor_formatado = self._formatar_default(campo.default, campo, largura)
            elif valor is None:
                valor_formatado = self._valor_vazio(campo, largura)
            else:
                valor_formatado = self._formatar_valor(valor, campo, largura)

            if len(valor_formatado) != largura:
                raise ValueError(
                    f"Campo '{campo.name}' formatado com {len(valor_formatado)} caracteres, esperado {largura}"
                )

            linha[campo.start - 1 : campo.end] = list(valor_formatado)

        return "".join(linha)

    def gerar_arquivo(
        self,
        registros: list[tuple[str, dict]],
        spec: str,
        filepath: str,
        encoding: str = "latin1",
    ) -> None:
        """Gera e grava as linhas em um arquivo.

        Args:
            registros: lista de tuplas (tipo_registro, dados).
            spec: nome da spec YAML a usar.
            filepath: caminho do arquivo de saída.
            encoding: encoding do arquivo (padrão: latin1).
        """
        linhas = self.gerar(registros, spec)
        with open(filepath, "w", encoding=encoding) as foutput:
            for linha in linhas:
                foutput.write(linha + "\n")

    def _formatar_valor(self, valor, campo: Field, largura: int) -> str:
        """Formata um valor usando o conversor reverso adequado"""
        conversor_reverso = reverse_convert_mapper(campo.convert)
        if conversor_reverso:
            return conversor_reverso(valor, largura)
        unmapper = self.data_unmapper(campo.datatype)
        return unmapper(valor, campo.datatype, largura)

    def _formatar_default(self, default, campo: Field, largura: int) -> str:
        """Formata um valor default — defaults são strings no YAML"""
        core_type = self.get_core_type(campo.datatype)
        if core_type in ("X", "A"):
            return str(default).ljust(largura)
        return str(default).zfill(largura)

    def _valor_vazio(self, campo: Field, largura: int) -> str:
        """Gera valor vazio para um campo (zeros ou espaços)"""
        core_type = self.get_core_type(campo.datatype)
        if core_type in ("X", "A"):
            return " " * largura
        return "0" * largura

    @staticmethod
    def data_unmapper(datatype: str):
        """Retorna o conversor reverso para o datatype da spec"""
        core_type = BasicGenerator.get_core_type(datatype)
        _data_unmap = {
            "X": lambda valor, datatype, largura: reverse_convert_to_string(valor, largura),
            "A": lambda valor, datatype, largura: reverse_convert_to_string(valor, largura),
            "9": lambda valor, datatype, largura: reverse_convert_to_int(valor, largura),
            "9V": reverse_febraban_numeric,
        }
        return _data_unmap[core_type]

    @staticmethod
    def get_core_type(datatype: str) -> str:
        """Extrai o tipo base do datatype da spec.

        Verifica o prefixo do datatype para evitar falsos positivos
        (ex: 'X(009)' contém '9' mas é tipo texto).
        """
        if datatype.startswith("X"):
            return "X"
        if datatype.startswith("A"):
            return "A"
        if "V" in datatype:
            return "9V"
        if datatype.startswith("9"):
            return "9"
        raise ValueError(f"Tipo de dado invalido: {datatype}")
