"""Tests for BasicGenerator"""

import pytest
from decimal import Decimal

from farialimer.parser.models import Field
from farialimer.generator.basic_generator import BasicGenerator


class ConcreteGenerator(BasicGenerator):
    """Implementação concreta para testes"""

    def __init__(self):
        super().__init__(provider="bradesco")


class TestGerarLinha:
    def setup_method(self):
        self.generator = ConcreteGenerator()

    def test_gerar_linha_campo_numerico_zero_padded(self):
        campos = [
            Field("codigo", "Código", "9(003)", None, 1, 3, None),
        ]
        linha = self.generator.gerar_linha({"codigo": 237}, campos)
        assert linha == "237"

    def test_gerar_linha_campo_texto_space_padded(self):
        campos = [
            Field("nome", "Nome", "X(010)", None, 1, 10, None),
        ]
        linha = self.generator.gerar_linha({"nome": "ABC"}, campos)
        assert linha == "ABC       "

    def test_gerar_linha_campo_decimal_febraban(self):
        campos = [
            Field("valor", "Valor", "9(013)V02", None, 1, 15, None),
        ]
        linha = self.generator.gerar_linha({"valor": Decimal("1500.00")}, campos)
        assert linha == "000000000150000"

    def test_gerar_linha_valor_padrao_numerico(self):
        campos = [
            Field("codigo", "Código", "9(003)", None, 1, 3, "237"),
        ]
        linha = self.generator.gerar_linha({}, campos)
        assert linha == "237"

    def test_gerar_linha_valor_padrao_texto(self):
        campos = [
            Field("tipo", "Tipo", "X(005)", None, 1, 5, "ABC"),
        ]
        linha = self.generator.gerar_linha({}, campos)
        assert linha == "ABC  "

    def test_gerar_linha_valor_vazio_numerico(self):
        campos = [
            Field("codigo", "Código", "9(003)", None, 1, 3, None),
        ]
        linha = self.generator.gerar_linha({}, campos)
        assert linha == "000"

    def test_gerar_linha_valor_vazio_texto(self):
        campos = [
            Field("nome", "Nome", "X(005)", None, 1, 5, None),
        ]
        linha = self.generator.gerar_linha({}, campos)
        assert linha == "     "

    def test_gerar_linha_multiplos_campos(self):
        campos = [
            Field("codigo", "Código", "9(003)", None, 1, 3, None),
            Field("lote", "Lote", "9(004)", None, 4, 7, None),
            Field("tipo", "Tipo", "9(001)", None, 8, 8, None),
        ]
        dados = {"codigo": 237, "lote": 0, "tipo": 0}
        linha = self.generator.gerar_linha(dados, campos)
        assert linha == "23700000"

    def test_gerar_linha_comprimento_correto(self):
        campos = [
            Field("codigo", "Código", "9(003)", None, 1, 3, None),
            Field("cnab", "CNAB", "X(237)", None, 4, 240, None),
        ]
        linha = self.generator.gerar_linha({"codigo": 237}, campos)
        assert len(linha) == 240

    def test_gerar_linha_overflow_raises_value_error(self):
        campos = [
            Field("codigo", "Código", "9(003)", None, 1, 3, None),
        ]
        with pytest.raises(ValueError):
            self.generator.gerar_linha({"codigo": 12345}, campos)


class TestGerar:
    def setup_method(self):
        self.generator = ConcreteGenerator()

    def test_gerar_multiplos_registros(self):
        registros = [
            ("0", {"codigo_banco": 237, "lote_servico": 0, "tipo_registro": 0}),
            ("9", {"codigo_banco": 237, "lote_servico": 9999, "tipo_registro": 9}),
        ]
        linhas = self.generator.gerar(registros, "folha_pagamento")
        assert len(linhas) == 2
        for linha in linhas:
            assert len(linha) == 240

    def test_gerar_registro_tipo_invalido_raises_key_error(self):
        registros = [("INVALIDO", {})]
        with pytest.raises(KeyError):
            self.generator.gerar(registros, "folha_pagamento")


class TestDataUnmapper:
    def test_get_core_type_numerico(self):
        assert BasicGenerator.get_core_type("9(003)") == "9"

    def test_get_core_type_texto(self):
        assert BasicGenerator.get_core_type("X(030)") == "X"

    def test_get_core_type_decimal(self):
        assert BasicGenerator.get_core_type("9(013)V02") == "9V"

    def test_get_core_type_alfanumerico(self):
        assert BasicGenerator.get_core_type("A(030)") == "A"

    def test_get_core_type_invalido_raises_value_error(self):
        with pytest.raises(ValueError):
            BasicGenerator.get_core_type("Z(003)")
