"""Sicoob Folha de Pagamento Parser tests"""

import pytest
from collections import OrderedDict

from farialimer.parser.sicoob.folha_pagamento import SicoobFolhaPagamento


@pytest.mark.parametrize(
    "line, expected",
    [
        ("7560000" + "0" + " " * 232, "0"),
        ("7560001" + "1" + " " * 232, "1"),
        ("7560001" + "3" + "00001" + "A" + " " * 226, "3A"),
        ("7560001" + "3" + "00002" + "B" + " " * 226, "3B"),
        ("7560001" + "5" + " " * 232, "5"),
        ("7569999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    parser = SicoobFolhaPagamento("sicoob")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_header_arquivo():
    parser = SicoobFolhaPagamento("sicoob")
    line = ""
    line += "756"  # codigo_banco (1-3)
    line += "0000"  # lote_servico (4-7)
    line += "0"  # tipo_registro (8)
    line += " " * 9  # cnab (9-17)
    line += "2"  # tipo_inscricao_empresa (18)
    line += "12345678000190"  # numero_inscricao_empresa (19-32)
    line += "CONVENIO SICOOB     "  # codigo_convenio_banco (33-52) - 20 chars
    line += "01234"  # agencia (53-57)
    line += "5"  # dv_agencia (58)
    line += "000001234567"  # conta_corrente (59-70)
    line += "8"  # dv_conta (71)
    line += " "  # dv_agencia_conta (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30
    line += "SICOOB                        "  # nome_banco (103-132) - 30
    line += " " * 10  # cnab_2 (133-142)
    line += "1"  # codigo_remessa_retorno (143)
    line += "23032026"  # data_geracao (144-151)
    line += "143000"  # hora_geracao (152-157)
    line += "000001"  # numero_sequencial_arquivo (158-163)
    line += "087"  # layout_arquivo (164-166)
    line += "00000"  # densidade_gravacao (167-171)
    line += " " * 20  # reservado_banco (172-191)
    line += " " * 20  # reservado_empresa (192-211)
    line += " " * 29  # cnab_3 (212-240)
    assert len(line) == 240
    fields = parser.get_spec_parser("folha_pagamento")["0"]
    result = parser.parse_line(line, fields)
    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 756
    assert result["tipo_registro"] == 0
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["layout_arquivo"] == 87


def test_parse_trailer_arquivo():
    parser = SicoobFolhaPagamento("sicoob")
    line = ""
    line += "756"  # codigo_banco (1-3)
    line += "9999"  # lote_servico (4-7)
    line += "9"  # tipo_registro (8)
    line += " " * 9  # cnab (9-17)
    line += "000002"  # quantidade_lotes (18-23)
    line += "000012"  # quantidade_registros (24-29)
    line += "000000"  # quantidade_contas_conciliacao (30-35)
    line += " " * 205  # cnab_2 (36-240)
    assert len(line) == 240
    fields = parser.get_spec_parser("folha_pagamento")["9"]
    result = parser.parse_line(line, fields)
    assert result["codigo_banco"] == 756
    assert result["quantidade_lotes"] == 2
    assert result["quantidade_registros"] == 12
