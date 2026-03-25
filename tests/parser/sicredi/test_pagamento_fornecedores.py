"""Sicredi Pagamento a Fornecedores Parser tests"""

import pytest

from farialimer.parser.sicredi.pagamento_fornecedores import SicrediPagamentoFornecedores


@pytest.mark.parametrize(
    "line, expected",
    [
        ("7480000" + "0" + " " * 232, "0"),
        ("7480001" + "1" + " " * 232, "1"),
        ("7480001" + "3" + "00001" + "A" + " " * 226, "3A"),
        ("7480001" + "3" + "00002" + "B" + " " * 226, "3B"),
        ("7480001" + "5" + " " * 232, "5"),
        ("7489999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    parser = SicrediPagamentoFornecedores("sicredi")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_trailer_arquivo():
    parser = SicrediPagamentoFornecedores("sicredi")
    line = ""
    line += "748"  # codigo_banco (1-3)
    line += "9999"  # lote_servico (4-7)
    line += "9"  # tipo_registro (8)
    line += " " * 9  # cnab (9-17)
    line += "000002"  # quantidade_lotes (18-23)
    line += "000012"  # quantidade_registros (24-29)
    line += "000000"  # quantidade_contas_conciliacao (30-35)
    line += " " * 205  # cnab_2 (36-240)
    assert len(line) == 240
    fields = parser.get_spec_parser("pagamento_fornecedores")["9"]
    result = parser.parse_line(line, fields)
    assert result["codigo_banco"] == 748
    assert result["quantidade_lotes"] == 2
    assert result["quantidade_registros"] == 12
