"""Banco do Brasil Folha de Pagamento Parser tests"""

import pytest
from collections import OrderedDict

from farialimer.parser.bb.folha_pagamento import BBFolhaPagamento


@pytest.mark.parametrize(
    "line, expected",
    [
        ("0010000" + "0" + " " * 232, "0"),
        ("0010001" + "1" + " " * 232, "1"),
        ("0010001" + "3" + "00001" + "A" + " " * 226, "3A"),
        ("0010001" + "3" + "00002" + "B" + " " * 226, "3B"),
        ("0010001" + "3" + "00003" + "C" + " " * 226, "3C"),
        ("0010001" + "5" + " " * 232, "5"),
        ("0019999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    """Test that get_line_register correctly identifies the register type."""
    parser = BBFolhaPagamento("bb")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_header_arquivo():
    """Test parsing a Header de Arquivo line."""
    parser = BBFolhaPagamento("bb")

    line = ""
    line += "001"  # codigo_banco (1-3)
    line += "0000"  # lote_servico (4-7)
    line += "0"  # tipo_registro (8)
    line += " " * 9  # cnab (9-17)
    line += "2"  # tipo_inscricao_empresa (18)
    line += "12345678000190"  # numero_inscricao_empresa (19-32)
    line += "000123456"  # convenio_numero (33-41)
    line += "0126"  # convenio_codigo (42-45)
    line += " " * 5  # convenio_reservado_banco (46-50)
    line += "TS"  # arquivo_teste (51-52)
    line += "01234"  # agencia (53-57)
    line += "X"  # dv_agencia (58)
    line += "000001234567"  # conta_corrente (59-70)
    line += "8"  # dv_conta (71)
    line += "0"  # dv_agencia_conta (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30 chars
    line += "BANCO DO BRASIL               "  # nome_banco (103-132) - 30 chars
    line += " " * 10  # cnab_2 (133-142)
    line += "1"  # codigo_remessa_retorno (143)
    line += "23032026"  # data_geracao (144-151)
    line += "143000"  # hora_geracao (152-157)
    line += "000001"  # numero_sequencial_arquivo (158-163)
    line += "030"  # layout_arquivo (164-166)
    line += "00000"  # densidade_gravacao (167-171)
    line += " " * 20  # reservado_banco (172-191)
    line += " " * 20  # reservado_empresa (192-211)
    line += " " * 11  # cnab_3 (212-222)
    line += " " * 3  # identificacao (223-225)
    line += "000"  # controle_vans (226-228)
    line += "00"  # servico (229-230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["0"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 1
    assert result["lote_servico"] == 0
    assert result["tipo_registro"] == 0
    assert result["tipo_inscricao_empresa"] == 2
    assert result["numero_inscricao_empresa"] == 12345678000190
    assert result["convenio_numero"] == 123456
    assert result["convenio_codigo"] == 126
    assert result["arquivo_teste"] == "TS"
    assert result["agencia"] == 1234
    assert result["conta_corrente"] == 1234567
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["nome_banco"] == "BANCO DO BRASIL"
    assert result["codigo_remessa_retorno"] == 1
    assert result["layout_arquivo"] == 30
    assert result["controle_vans"] == 0
    assert result["servico"] == 0


def test_parse_segmento_a():
    """Test parsing a Segmento A detail line."""
    parser = BBFolhaPagamento("bb")

    line = ""
    line += "001"  # codigo_banco (1-3)
    line += "0001"  # lote_servico (4-7)
    line += "3"  # tipo_registro (8)
    line += "00001"  # numero_registro (9-13)
    line += "A"  # segmento (14)
    line += "0"  # tipo_movimento (15)
    line += "00"  # codigo_movimento (16-17)
    line += "000"  # camara (18-20)
    line += "001"  # banco_favorecido (21-23)
    line += "04567"  # agencia_favorecido (24-28)
    line += "X"  # dv_agencia (29)
    line += "000009876543"  # conta_corrente (30-41)
    line += "2"  # dv_conta (42)
    line += " "  # dv_agencia_conta (43)
    line += "JOAO DA SILVA                 "  # nome_favorecido (44-73) - 30 chars
    line += "DOC-00001           "  # seu_numero (74-93) - 20 chars
    line += "23032026"  # data_pagamento (94-101)
    line += "BRL"  # moeda_tipo (102-104)
    line += "000000000000000"  # quantidade_moeda (105-119) - 15 digits
    line += "000000000150000"  # valor_pagamento (120-134) - 1500.00
    line += "NOSSO-NUM-00001     "  # nosso_numero (135-154) - 20 chars
    line += "00000000"  # data_real (155-162)
    line += "000000000000000"  # valor_real (163-177)
    line += " " * 40  # informacao_2 (178-217)
    line += "CC"  # codigo_finalidade_doc (218-219)
    line += "00001"  # codigo_finalidade_ted (220-224)
    line += "  "  # codigo_finalidade_complementar (225-226)
    line += "   "  # cnab (227-229)
    line += "0"  # aviso (230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["3A"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 1
    assert result["tipo_registro"] == 3
    assert result["segmento"] == "A"
    assert result["banco_favorecido"] == 1
    assert result["agencia_favorecido"] == 4567
    assert result["nome_favorecido"] == "JOAO DA SILVA"
    assert result["seu_numero"] == "DOC-00001"
    assert result["moeda_tipo"] == "BRL"
    assert result["codigo_finalidade_doc"] == "CC"
    assert result["aviso"] == 0


def test_parse_trailer_arquivo():
    """Test parsing a Trailer de Arquivo line."""
    parser = BBFolhaPagamento("bb")

    line = ""
    line += "001"  # codigo_banco (1-3)
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

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 1
    assert result["lote_servico"] == 9999
    assert result["tipo_registro"] == 9
    assert result["quantidade_lotes"] == 2
    assert result["quantidade_registros"] == 12
    assert result["quantidade_contas_conciliacao"] == 0
