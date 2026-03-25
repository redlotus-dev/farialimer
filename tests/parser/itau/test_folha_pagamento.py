"""Itau Folha de Pagamento Parser tests"""

import pytest
from collections import OrderedDict

from farialimer.parser.itau.folha_pagamento import ItauFolhaPagamento


@pytest.mark.parametrize(
    "line, expected",
    [
        # Header de Arquivo - tipo_registro = '0'
        ("3410000" + "0" + " " * 232, "0"),
        # Header de Lote - tipo_registro = '1'
        ("3410001" + "1" + " " * 232, "1"),
        # Detalhe Segmento A
        ("3410001" + "3" + "00001" + "A" + " " * 226, "3A"),
        # Detalhe Segmento B
        ("3410001" + "3" + "00002" + "B" + " " * 226, "3B"),
        # Detalhe Segmento C
        ("3410001" + "3" + "00003" + "C" + " " * 226, "3C"),
        # Detalhe Segmento D (Holerite)
        ("3410001" + "3" + "00004" + "D" + " " * 226, "3D"),
        # Detalhe Segmento E (Holerite)
        ("3410001" + "3" + "00005" + "E" + " " * 226, "3E"),
        # Detalhe Segmento F (Holerite)
        ("3410001" + "3" + "00006" + "F" + " " * 226, "3F"),
        # Detalhe Segmento Z (Autenticação)
        ("3410001" + "3" + "00007" + "Z" + " " * 226, "3Z"),
        # Trailer de Lote - tipo_registro = '5'
        ("3410001" + "5" + " " * 232, "5"),
        # Trailer de Arquivo - tipo_registro = '9'
        ("3419999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    """Test that get_line_register correctly identifies the register type."""
    parser = ItauFolhaPagamento("itau")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_header_arquivo():
    """Test parsing a Header de Arquivo line."""
    parser = ItauFolhaPagamento("itau")

    line = ""
    line += "341"  # codigo_banco (1-3)
    line += "0000"  # codigo_lote (4-7)
    line += "0"  # tipo_registro (8)
    line += " " * 6  # brancos (9-14)
    line += "080"  # layout_arquivo (15-17)
    line += "2"  # tipo_inscricao_empresa (18)
    line += "12345678000190"  # inscricao_numero (19-32)
    line += " " * 20  # brancos_2 (33-52)
    line += "01234"  # agencia (53-57)
    line += " "  # brancos_3 (58)
    line += "000001234567"  # conta (59-70)
    line += " "  # brancos_4 (71)
    line += "8"  # dac (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30 chars
    line += "BANCO ITAU SA                 "  # nome_banco (103-132) - 30 chars
    line += " " * 10  # brancos_5 (133-142)
    line += "1"  # arquivo_codigo (143)
    line += "23032026"  # data_geracao (144-151)
    line += "143000"  # hora_geracao (152-157)
    line += "000000000"  # zeros (158-166)
    line += "01600"  # unidade_densidade (167-171)
    line += " " * 69  # brancos_6 (172-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["0"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 341
    assert result["codigo_lote"] == 0
    assert result["tipo_registro"] == 0
    assert result["layout_arquivo"] == 80
    assert result["tipo_inscricao_empresa"] == 2
    assert result["inscricao_numero"] == 12345678000190
    assert result["agencia"] == 1234
    assert result["conta"] == 1234567
    assert result["dac"] == 8
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["nome_banco"] == "BANCO ITAU SA"
    assert result["arquivo_codigo"] == 1
    assert result["data_geracao"] == 23032026


def test_parse_header_lote():
    """Test parsing a Header de Lote line."""
    parser = ItauFolhaPagamento("itau")

    line = ""
    line += "341"  # codigo_banco (1-3)
    line += "0001"  # codigo_lote (4-7)
    line += "1"  # tipo_registro (8)
    line += "C"  # tipo_operacao (9)
    line += "30"  # tipo_pagamento (10-11) - Salários
    line += "01"  # forma_pagamento (12-13) - CC
    line += "040"  # layout_lote (14-16)
    line += " "  # brancos (17)
    line += "2"  # tipo_inscricao_empresa (18)
    line += "12345678000190"  # inscricao_numero (19-32)
    line += "PGTO"  # identificacao_lancamento (33-36)
    line += " " * 16  # brancos_2 (37-52)
    line += "01234"  # agencia (53-57)
    line += " "  # brancos_3 (58)
    line += "000001234567"  # conta (59-70)
    line += " "  # brancos_4 (71)
    line += "8"  # dac (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30 chars
    line += "PAGAMENTO SALARIOS            "  # finalidade_lote (103-132) - 30 chars
    line += "HISTORICO "  # historico_cc (133-142) - 10 chars
    line += "RUA DAS FLORES                "  # endereco_empresa (143-172) - 30 chars
    line += "00100"  # numero (173-177)
    line += "SALA 101       "  # complemento (178-192) - 15 chars
    line += "SAO PAULO           "  # cidade (193-212) - 20 chars
    line += "01310100"  # cep (213-220) - 8 digits
    line += "SP"  # estado (221-222)
    line += " " * 8  # brancos_5 (223-230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["1"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 341
    assert result["tipo_registro"] == 1
    assert result["tipo_operacao"] == "C"
    assert result["tipo_pagamento"] == 30
    assert result["forma_pagamento"] == 1
    assert result["layout_lote"] == 40
    assert result["identificacao_lancamento"] == "PGTO"
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["finalidade_lote"] == "PAGAMENTO SALARIOS"
    assert result["endereco_empresa"] == "RUA DAS FLORES"
    assert result["numero"] == 100
    assert result["cidade"] == "SAO PAULO"
    assert result["cep"] == 1310100
    assert result["estado"] == "SP"


def test_parse_segmento_a():
    """Test parsing a Segmento A detail line."""
    parser = ItauFolhaPagamento("itau")

    line = ""
    line += "341"  # codigo_banco (1-3)
    line += "0001"  # codigo_lote (4-7)
    line += "3"  # tipo_registro (8)
    line += "00001"  # numero_registro (9-13)
    line += "A"  # segmento (14)
    line += "000"  # tipo_movimento (15-17)
    line += "000"  # camara (18-20)
    line += "341"  # banco_favorecido (21-23)
    line += "04567 000098765432  "  # agencia_conta (24-43) - 20 chars
    line += "JOAO DA SILVA                 "  # nome_favorecido (44-73) - 30 chars
    line += "DOC-00001           "  # seu_numero (74-93) - 20 chars
    line += "23032026"  # data_pagamento (94-101)
    line += "REA"  # moeda_tipo (102-104)
    line += "00000000"  # codigo_ispb (105-112)
    line += "  "  # identificacao_transferencia (113-114)
    line += "00000"  # zeros (115-119)
    line += "000000000150000"  # valor_pagamento (120-134) - 1500.00
    line += "NOSSO-NUM-00001"  # nosso_numero (135-149) - 15 chars
    line += " " * 5  # brancos (150-154)
    line += "00000000"  # data_efetiva (155-162)
    line += "000000000000000"  # valor_efetivo (163-177)
    line += "FINALIDADE DETALHE  "  # finalidade_detalhe (178-197) - 20 chars
    line += "000001"  # numero_documento (198-203)
    line += "00012345678909"  # numero_inscricao (204-217)
    line += "CC"  # finalidade_doc_status (218-219)
    line += "00001"  # finalidade_ted (220-224)
    line += " " * 5  # brancos_2 (225-229)
    line += "0"  # aviso (230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["3A"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 341
    assert result["tipo_registro"] == 3
    assert result["segmento"] == "A"
    assert result["banco_favorecido"] == 341
    assert result["nome_favorecido"] == "JOAO DA SILVA"
    assert result["seu_numero"] == "DOC-00001"
    assert result["moeda_tipo"] == "REA"
    assert result["numero_documento"] == 1
    assert result["numero_inscricao"] == 12345678909
    assert result["finalidade_doc_status"] == "CC"
    assert result["aviso"] == "0"


def test_parse_trailer_arquivo():
    """Test parsing a Trailer de Arquivo line."""
    parser = ItauFolhaPagamento("itau")

    line = ""
    line += "341"  # codigo_banco (1-3)
    line += "9999"  # codigo_lote (4-7)
    line += "9"  # tipo_registro (8)
    line += " " * 9  # brancos (9-17)
    line += "000002"  # total_quantidade_lotes (18-23)
    line += "000012"  # total_quantidade_registros (24-29)
    line += " " * 211  # brancos_2 (30-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["9"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 341
    assert result["codigo_lote"] == 9999
    assert result["tipo_registro"] == 9
    assert result["total_quantidade_lotes"] == 2
    assert result["total_quantidade_registros"] == 12
