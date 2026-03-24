"""Caixa Econômica Federal Folha de Pagamento Parser tests"""

import pytest
from collections import OrderedDict

from farialimer.parser.caixa.folha_pagamento import CaixaFolhaPagamento


@pytest.mark.parametrize(
    "line, expected",
    [
        ("1040000" + "0" + " " * 232, "0"),
        ("1040001" + "1" + " " * 232, "1"),
        ("1040001" + "3" + "00001" + "A" + " " * 226, "3A"),
        ("1040001" + "3" + "00002" + "B" + " " * 226, "3B"),
        ("1040001" + "5" + " " * 232, "5"),
        ("1049999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    """Test that get_line_register correctly identifies the register type."""
    parser = CaixaFolhaPagamento("caixa")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_header_arquivo():
    """Test parsing a Header de Arquivo line."""
    parser = CaixaFolhaPagamento("caixa")

    line = ""
    line += "104"  # codigo_banco (1-3)
    line += "0000"  # lote_servico (4-7)
    line += "0"  # tipo_registro (8)
    line += " " * 9  # filler (9-17)
    line += "2"  # tipo_inscricao (18)
    line += "12345678000190"  # numero_inscricao (19-32)
    line += "123456"  # codigo_convenio (33-38)
    line += "01"  # parametro_transmissao (39-40)
    line += "P"  # ambiente_cliente (41)
    line += " "  # ambiente_caixa (42)
    line += "   "  # origem_aplicativo (43-45)
    line += "0000"  # numero_versao (46-49)
    line += "   "  # filler_2 (50-52)
    line += "01234"  # agencia (53-57)
    line += "5"  # dv_agencia (58)
    line += "000001234567"  # conta_corrente (59-70)
    line += "8"  # dv_conta (71)
    line += " "  # dv_agencia_conta (72)
    line += "EMPRESA TESTE LTDA            "  # nome_empresa (73-102) - 30
    line += "CAIXA ECONOMICA FEDERAL       "  # nome_banco (103-132) - 30
    line += " " * 10  # filler_3 (133-142)
    line += "1"  # tipo_arquivo (143)
    line += "23032026"  # data_geracao (144-151)
    line += "143000"  # hora_geracao (152-157)
    line += "000001"  # nsa (158-163)
    line += "080"  # versao_leiaute (164-166)
    line += "01600"  # densidade_gravacao (167-171)
    line += " " * 20  # exclusivo_pix (172-191)
    line += " " * 20  # reservado_empresa (192-211)
    line += " " * 11  # uso_exclusivo_febraban (212-222)
    line += "   "  # identificacao_cobranca (223-225)
    line += "000"  # uso_exclusivo_vans (226-228)
    line += "  "  # tipo_servico (229-230)
    line += " " * 10  # ocorrencia_cobranca_sem_papel (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["0"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 104
    assert result["tipo_registro"] == 0
    assert result["tipo_inscricao"] == 2
    assert result["numero_inscricao"] == 12345678000190
    assert result["codigo_convenio"] == 123456
    assert result["ambiente_cliente"] == "P"
    assert result["agencia"] == 1234
    assert result["conta_corrente"] == 1234567
    assert result["nome_empresa"] == "EMPRESA TESTE LTDA"
    assert result["nome_banco"] == "CAIXA ECONOMICA FEDERAL"
    assert result["tipo_arquivo"] == 1
    assert result["versao_leiaute"] == 80


def test_parse_segmento_a():
    """Test parsing a Segmento A detail line."""
    parser = CaixaFolhaPagamento("caixa")

    line = ""
    line += "104"  # codigo_banco (1-3)
    line += "0001"  # lote_servico (4-7)
    line += "3"  # tipo_registro (8)
    line += "00001"  # nsr (9-13)
    line += "A"  # segmento (14)
    line += "0"  # tipo_movimento (15)
    line += "00"  # codigo_instrucao_movimento (16-17)
    line += "000"  # camara_compensacao (18-20)
    line += "104"  # banco_destino (21-23)
    line += "04567"  # agencia_destino (24-28)
    line += " "  # dv_agencia_destino (29)
    line += "000009876543"  # conta_corrente_destino (30-41)
    line += "2"  # dv_conta_destino (42)
    line += " "  # dv_agencia_conta_destino (43)
    line += "JOAO DA SILVA                 "  # nome_favorecido (44-73) - 30
    line += "000001"  # numero_documento_empresa (74-79)
    line += " " * 13  # filler (80-92)
    line += "1"  # tipo_conta_finalidade_ted (93)
    line += "23032026"  # data_vencimento (94-101)
    line += "BRL"  # tipo_moeda (102-104)
    line += "000000000000000"  # quantidade_moeda (105-119)
    line += "000000000150000"  # valor_lancamento (120-134)
    line += "000000000"  # numero_documento_banco (135-143)
    line += "   "  # filler_2 (144-146)
    line += "01"  # quantidade_parcelas (147-148)
    line += "N"  # indicador_bloqueio (149)
    line += "0"  # indicador_parcelamento (150)
    line += "  "  # periodo_dia_vencimento (151-152)
    line += "00"  # numero_parcela (153-154)
    line += "00000000"  # data_efetivacao (155-162)
    line += "000000000000000"  # valor_real_efetivado (163-177)
    line += " " * 40  # informacao_2 (178-217)
    line += "00"  # finalidade_doc (218-219)
    line += " " * 10  # uso_febraban (220-229)
    line += "0"  # aviso_favorecido (230)
    line += " " * 10  # ocorrencias (231-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["3A"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 104
    assert result["tipo_registro"] == 3
    assert result["segmento"] == "A"
    assert result["banco_destino"] == 104
    assert result["agencia_destino"] == 4567
    assert result["nome_favorecido"] == "JOAO DA SILVA"
    assert result["numero_documento_empresa"] == 1
    assert result["tipo_conta_finalidade_ted"] == "1"
    assert result["tipo_moeda"] == "BRL"
    assert result["quantidade_parcelas"] == 1
    assert result["indicador_bloqueio"] == "N"
    assert result["aviso_favorecido"] == 0


def test_parse_trailer_arquivo():
    """Test parsing a Trailer de Arquivo line."""
    parser = CaixaFolhaPagamento("caixa")

    line = ""
    line += "104"  # codigo_banco (1-3)
    line += "9999"  # lote_servico (4-7)
    line += "9"  # tipo_registro (8)
    line += " " * 9  # uso_exclusivo_febraban (9-17)
    line += "000002"  # quantidade_lotes (18-23)
    line += "000012"  # quantidade_registros (24-29)
    line += "000000"  # quantidade_contas_conciliacao (30-35)
    line += " " * 205  # uso_exclusivo_febraban_2 (36-240)

    assert len(line) == 240

    fields = parser.get_spec_parser("folha_pagamento")["9"]
    result = parser.parse_line(line, fields)

    assert isinstance(result, OrderedDict)
    assert result["codigo_banco"] == 104
    assert result["lote_servico"] == 9999
    assert result["tipo_registro"] == 9
    assert result["quantidade_lotes"] == 2
    assert result["quantidade_registros"] == 12
    assert result["quantidade_contas_conciliacao"] == 0
