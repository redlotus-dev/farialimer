"""Bradesco Folha de Pagamento Parser tests"""

import pytest
from collections import OrderedDict

from farialimer.parser.bradesco.folha_pagamento import FolhaPagamentoParser


@pytest.mark.parametrize(
    "line, expected",
    [
        # Header de Arquivo - tipo_registro = '0'
        ("2370000" + "0" + " " * 232, "0"),
        # Header de Lote - tipo_registro = '1'
        ("2370001" + "1" + " " * 232, "1"),
        # Detalhe Segmento A - tipo_registro = '3', segmento = 'A'
        ("2370001" + "3" + "00001" + "A" + " " * 226, "3A"),
        # Detalhe Segmento B - tipo_registro = '3', segmento = 'B'
        ("2370001" + "3" + "00002" + "B" + " " * 226, "3B"),
        # Detalhe Segmento C - tipo_registro = '3', segmento = 'C'
        ("2370001" + "3" + "00003" + "C" + " " * 226, "3C"),
        # Trailer de Lote - tipo_registro = '5'
        ("2370001" + "5" + " " * 232, "5"),
        # Trailer de Arquivo - tipo_registro = '9'
        ("2379999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    """Test that get_line_register correctly identifies the register type."""
    parser = FolhaPagamentoParser("bradesco")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_header_arquivo():
    """Test parsing a Header de Arquivo line."""
    parser = FolhaPagamentoParser("bradesco")

    # Build a 240-char Header de Arquivo line
    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "0000"  # lote_servico (4-7)
    line += "0"  # tipo_registro (8)
    line += " " * 9  # cnab_1 (9-17)
    line += "2"  # tipo_inscricao_empresa (18) - CNPJ
    line += "12345678000190"  # numero_inscricao_empresa (19-32)
    line += "CONVENIO BRADESCO   "  # codigo_convenio_banco (33-52) - 20 chars
    line += "01234"  # agencia_mantenedora_conta (53-57)
    line += "5"  # digito_verificador_agencia (58)
    line += "000001234567"  # numero_conta_corrente (59-70)
    line += "8"  # digito_verificador_conta (71)
    line += "9"  # digito_verificador_agencia_conta (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30 chars
    line += "BANCO BRADESCO SA             "  # nome_banco (103-132) - 30 chars
    line += " " * 10  # cnab_2 (133-142)
    line += "1"  # codigo_remessa_retorno (143)
    line += "23032026"  # data_geracao_arquivo (144-151)
    line += "143000"  # hora_geracao_arquivo (152-157)
    line += "000001"  # numero_sequencial_arquivo (158-163)
    line += "080"  # layout_arquivo (164-166)
    line += "01600"  # densidade_gravacao_arquivo (167-171)
    line += " " * 20  # reservado_banco (172-191)
    line += " " * 20  # reservado_empresa (192-211)
    line += " " * 29  # cnab_3 (212-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["0"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 237
    assert result["lote_servico"] == 0
    assert result["tipo_registro"] == 0
    assert result["tipo_inscricao_empresa"] == 2
    assert result["numero_inscricao_empresa"] == 12345678000190
    assert result["codigo_convenio_banco"] == "CONVENIO BRADESCO"
    assert result["agencia_mantenedora_conta"] == 1234
    assert result["digito_verificador_agencia"] == "5"
    assert result["numero_conta_corrente"] == 1234567
    assert result["digito_verificador_conta"] == "8"
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["nome_banco"] == "BANCO BRADESCO SA"
    assert result["codigo_remessa_retorno"] == 1
    assert result["data_geracao_arquivo"] == 23032026
    assert result["hora_geracao_arquivo"] == 143000
    assert result["numero_sequencial_arquivo"] == 1
    assert result["layout_arquivo"] == 80
    assert result["densidade_gravacao_arquivo"] == 1600


def test_parse_header_lote():
    """Test parsing a Header de Lote line."""
    parser = FolhaPagamentoParser("bradesco")

    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "0001"  # lote_servico (4-7)
    line += "1"  # tipo_registro (8)
    line += "C"  # tipo_operacao (9)
    line += "30"  # tipo_servico (10-11) - Pagamento Salários
    line += "01"  # forma_lancamento (12-13) - Crédito em Conta Corrente
    line += "040"  # layout_lote (14-16)
    line += " "  # cnab (17)
    line += "2"  # tipo_inscricao_empresa (18)
    line += "12345678000190"  # numero_inscricao_empresa (19-32)
    line += "CONVENIO BRADESCO   "  # codigo_convenio_banco (33-52) - 20 chars
    line += "01234"  # agencia_mantenedora_conta (53-57)
    line += "5"  # digito_verificador_agencia (58)
    line += "000001234567"  # numero_conta_corrente (59-70)
    line += "8"  # digito_verificador_conta (71)
    line += "9"  # digito_verificador_agencia_conta (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30 chars
    line += " " * 40  # informacao_1 (103-142)
    line += "RUA DAS FLORES                "  # logradouro (143-172) - 30 chars
    line += "00100"  # numero (173-177)
    line += "SALA 101       "  # complemento (178-192) - 15 chars
    line += "SAO PAULO           "  # cidade (193-212) - 20 chars
    line += "01310"  # cep (213-217)
    line += "100"  # complemento_cep (218-220)
    line += "SP"  # estado (221-222)
    line += " " * 8  # cnab_1 (223-230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["1"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 237
    assert result["lote_servico"] == 1
    assert result["tipo_registro"] == 1
    assert result["tipo_operacao"] == "C"
    assert result["tipo_servico"] == 30
    assert result["forma_lancamento"] == 1
    assert result["layout_lote"] == 40
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["logradouro"] == "RUA DAS FLORES"
    assert result["numero"] == 100
    assert result["complemento"] == "SALA 101"
    assert result["cidade"] == "SAO PAULO"
    assert result["cep"] == 1310
    assert result["complemento_cep"] == "100"
    assert result["estado"] == "SP"


def test_parse_segmento_a():
    """Test parsing a Segmento A detail line."""
    parser = FolhaPagamentoParser("bradesco")

    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "0001"  # lote_servico (4-7)
    line += "3"  # tipo_registro (8)
    line += "00001"  # numero_registro (9-13)
    line += "A"  # segmento (14)
    line += "0"  # tipo_movimento (15)
    line += "00"  # codigo_movimento (16-17)
    line += "000"  # camara (18-20)
    line += "237"  # banco_favorecido (21-23)
    line += "04567"  # agencia_favorecido (24-28)
    line += "8"  # digito_verificador_agencia (29)
    line += "000009876543"  # numero_conta_corrente (30-41)
    line += "2"  # digito_verificador_conta (42)
    line += "1"  # digito_verificador_agencia_conta (43)
    line += "JOAO DA SILVA                 "  # nome_favorecido (44-73) - 30 chars
    line += "DOC-00001           "  # numero_documento (74-93) - 20 chars
    line += "23032026"  # data_pagamento (94-101)
    line += "BRL"  # tipo_moeda (102-104)
    line += "000000000000000"  # quantidade_moeda (105-119) - 15 digits
    line += "000000000150000"  # valor_pagamento (120-134) - 1500.00
    line += "NOSSO-NUM-00001     "  # nosso_numero (135-154) - 20 chars
    line += "00000000"  # data_real (155-162)
    line += "000000000000000"  # valor_real (163-177) - 15 digits
    line += " " * 40  # informacao_2 (178-217)
    line += "CC"  # codigo_finalidade_doc (218-219)
    line += "00001"  # codigo_finalidade_ted (220-224)
    line += " " * 5  # cnab (225-229)
    line += "0"  # aviso (230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["3A"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 237
    assert result["tipo_registro"] == 3
    assert result["segmento"] == "A"
    assert result["banco_favorecido"] == 237
    assert result["agencia_favorecido"] == 4567
    assert result["nome_favorecido"] == "JOAO DA SILVA"
    assert result["numero_documento"] == "DOC-00001"
    assert result["tipo_moeda"] == "BRL"
    assert result["aviso"] == 0
    assert result["codigo_finalidade_doc"] == "CC"


def test_parse_segmento_b():
    """Test parsing a Segmento B detail line."""
    parser = FolhaPagamentoParser("bradesco")

    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "0001"  # lote_servico (4-7)
    line += "3"  # tipo_registro (8)
    line += "00002"  # numero_registro (9-13)
    line += "B"  # segmento (14)
    line += " " * 3  # cnab (15-17)
    line += "1"  # tipo_inscricao_favorecido (18)
    line += "00012345678909"  # numero_inscricao_favorecido (19-32)
    line += "AV PAULISTA                   "  # logradouro (33-62) - 30 chars
    line += "01000"  # numero (63-67)
    line += "ANDAR 10       "  # complemento (68-82) - 15 chars
    line += "BELA VISTA     "  # bairro (83-97) - 15 chars
    line += "SAO PAULO           "  # cidade (98-117) - 20 chars
    line += "01311"  # cep (118-122)
    line += "200"  # complemento_cep (123-125)
    line += "SP"  # estado (126-127)
    line += "23032026"  # data_vencimento (128-135)
    line += "000000000150000"  # valor_documento (136-150) - 1500.00
    line += "000000000000000"  # valor_abatimento (151-165)
    line += "000000000000000"  # valor_desconto (166-180)
    line += "000000000000000"  # valor_mora (181-195)
    line += "000000000000000"  # valor_multa (196-210)
    line += "DOC-FAVORECIDO "  # codigo_documento_favorecido (211-225) - 15 chars
    line += " " * 15  # cnab_2 (226-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["3B"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 237
    assert result["segmento"] == "B"
    assert result["tipo_inscricao_favorecido"] == 1
    assert result["numero_inscricao_favorecido"] == 12345678909
    assert result["logradouro"] == "AV PAULISTA"
    assert result["numero"] == 1000
    assert result["complemento"] == "ANDAR 10"
    assert result["bairro"] == "BELA VISTA"
    assert result["cidade"] == "SAO PAULO"
    assert result["cep"] == 1311
    assert result["complemento_cep"] == "200"
    assert result["estado"] == "SP"
    assert result["codigo_documento_favorecido"] == "DOC-FAVORECIDO"


def test_parse_trailer_arquivo():
    """Test parsing a Trailer de Arquivo line."""
    parser = FolhaPagamentoParser("bradesco")

    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "9999"  # lote_servico (4-7)
    line += "9"  # tipo_registro (8)
    line += " " * 9  # cnab (9-17)
    line += "000002"  # quantidade_lotes (18-23)
    line += "000012"  # quantidade_registros (24-29)
    line += "000003"  # quantidade_contas_conciliacao (30-35)
    line += " " * 205  # cnab_2 (36-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["9"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 237
    assert result["lote_servico"] == 9999
    assert result["tipo_registro"] == 9
    assert result["quantidade_lotes"] == 2
    assert result["quantidade_registros"] == 12
    assert result["quantidade_contas_conciliacao"] == 3
