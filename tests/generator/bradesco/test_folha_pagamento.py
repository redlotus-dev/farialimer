"""Round-trip tests for Bradesco Folha de Pagamento Generator.

Parses a known CNAB line with the parser, then regenerates it with the generator,
and asserts the output matches the original input.
"""

from farialimer.parser.bradesco.folha_pagamento import FolhaPagamentoParser
from farialimer.generator.bradesco.folha_pagamento import FolhaPagamentoGenerator


def _build_header_arquivo_line():
    """Builds a 240-char Header de Arquivo line for Bradesco."""
    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "0000"  # lote_servico (4-7)
    line += "0"  # tipo_registro (8)
    line += " " * 9  # cnab_1 (9-17)
    line += "2"  # tipo_inscricao_empresa (18)
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
    return line


def _build_trailer_arquivo_line():
    """Builds a 240-char Trailer de Arquivo line for Bradesco."""
    line = ""
    line += "237"  # codigo_banco (1-3)
    line += "9999"  # lote_servico (4-7)
    line += "9"  # tipo_registro (8)
    line += " " * 9  # cnab (9-17)
    line += "000002"  # quantidade_lotes (18-23)
    line += "000012"  # quantidade_registros (24-29)
    line += "000003"  # quantidade_contas_conciliacao (30-35)
    line += " " * 205  # cnab_2 (36-240)
    return line


def _build_segmento_a_line():
    """Builds a 240-char Segmento A detail line for Bradesco."""
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
    return line


class TestRoundTripHeaderArquivo:
    """Parse a header line, then regenerate it and compare."""

    def test_round_trip_header_arquivo(self):
        original = _build_header_arquivo_line()
        assert len(original) == 240

        parser = FolhaPagamentoParser("bradesco")
        fields = parser.get_spec_parser("folha_pagamento")["0"]
        parsed = parser.parse_line(original, fields)

        generator = FolhaPagamentoGenerator()
        regenerated = generator.gerar_linha(dict(parsed), fields)

        assert len(regenerated) == 240
        assert regenerated == original


class TestRoundTripTrailerArquivo:
    def test_round_trip_trailer_arquivo(self):
        original = _build_trailer_arquivo_line()
        assert len(original) == 240

        parser = FolhaPagamentoParser("bradesco")
        fields = parser.get_spec_parser("folha_pagamento")["9"]
        parsed = parser.parse_line(original, fields)

        generator = FolhaPagamentoGenerator()
        regenerated = generator.gerar_linha(dict(parsed), fields)

        assert len(regenerated) == 240
        assert regenerated == original


class TestRoundTripSegmentoA:
    def test_round_trip_segmento_a(self):
        original = _build_segmento_a_line()
        assert len(original) == 240

        parser = FolhaPagamentoParser("bradesco")
        fields = parser.get_spec_parser("folha_pagamento")["3A"]
        parsed = parser.parse_line(original, fields)

        generator = FolhaPagamentoGenerator()
        regenerated = generator.gerar_linha(dict(parsed), fields)

        assert len(regenerated) == 240
        assert regenerated == original


class TestGenerateFromValues:
    """Test generating lines from explicit values (not round-trip)."""

    def test_generate_header_arquivo_from_values(self):
        generator = FolhaPagamentoGenerator()
        dados = {
            "codigo_banco": 237,
            "lote_servico": 0,
            "tipo_registro": 0,
            "tipo_inscricao_empresa": 2,
            "numero_inscricao_empresa": 12345678000190,
            "nome_empresa": "EMPRESA TESTE LTDA",
            "nome_banco": "BANCO BRADESCO SA",
            "codigo_remessa_retorno": 1,
            "data_geracao_arquivo": 23032026,
            "hora_geracao_arquivo": 143000,
            "numero_sequencial_arquivo": 1,
            "layout_arquivo": 80,
            "densidade_gravacao_arquivo": 1600,
        }
        fields = generator.get_spec_parser("folha_pagamento")["0"]
        linha = generator.gerar_linha(dados, fields)

        assert len(linha) == 240
        assert linha[:3] == "237"
        assert linha[3:7] == "0000"
        assert linha[7] == "0"

    def test_generate_trailer_from_values(self):
        generator = FolhaPagamentoGenerator()
        dados = {
            "codigo_banco": 237,
            "lote_servico": 9999,
            "tipo_registro": 9,
            "quantidade_lotes": 2,
            "quantidade_registros": 12,
            "quantidade_contas_conciliacao": 3,
        }
        fields = generator.get_spec_parser("folha_pagamento")["9"]
        linha = generator.gerar_linha(dados, fields)

        assert len(linha) == 240
        assert linha[:3] == "237"
        assert linha[17:23] == "000002"
        assert linha[23:29] == "000012"
        assert linha[29:35] == "000003"
