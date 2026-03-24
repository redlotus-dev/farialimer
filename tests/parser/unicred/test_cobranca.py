"""Unicred Cobrança Parser tests"""

import pytest
from collections import OrderedDict

from farialimer.parser.unicred.cobranca import UnicredCobranca


@pytest.mark.parametrize(
    "line, expected",
    [
        ("1360000" + "0" + " " * 232, "0"),
        ("1360001" + "1" + " " * 232, "1"),
        ("1360001" + "3" + "00001" + "P" + " " * 226, "3P"),
        ("1360001" + "3" + "00002" + "Q" + " " * 226, "3Q"),
        ("1360001" + "5" + " " * 232, "5"),
        ("1369999" + "9" + " " * 232, "9"),
    ],
)
def test_get_line_register(line, expected):
    parser = UnicredCobranca("unicred")
    result = parser.get_line_register(line)
    assert result == expected


def test_parse_trailer_arquivo():
    parser = UnicredCobranca("unicred")
    line = ""
    line += "136"           # codigo_banco (1-3)
    line += "9999"          # lote_servico (4-7)
    line += "9"             # tipo_registro (8)
    line += " " * 9         # cnab (9-17)
    line += "000002"        # quantidade_lotes (18-23)
    line += "000012"        # quantidade_registros (24-29)
    line += "000000"        # quantidade_contas_conciliacao (30-35)
    line += " " * 205       # cnab_2 (36-240)
    assert len(line) == 240
    fields = parser.get_spec_parser("cobranca")["9"]
    result = parser.parse_line(line, fields)
    assert result["codigo_banco"] == 136
    assert result["quantidade_lotes"] == 2
    assert result["quantidade_registros"] == 12
