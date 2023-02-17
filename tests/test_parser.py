"""Parser Tests"""

from collections import OrderedDict
from datetime import date
from farialimer.parser.b3parser import B3Parser as Parser


def test_get_filetype():
    """Test the getfiletype"""

    path = "tests/specs/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser("imbarq014")
    content = parser.read_file(path)
    result = parser.get_filetype(content[0])

    expected = "IMBARQ014"

    assert result == expected


def test_parse_imbarq014():
    """Test the parser for imbarq014 sample file"""
    path = "tests/specs/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser("imbarq014")
    content = parser.read_file(path)
    result = parser.parse(content, spec="imbarq014")

    expected = [
        OrderedDict(
            tipo_registro="00",
            codigo_arquivo="IMBARQ014",
            codigo_categoria_usuario=1,
            codigo_usuario=935,
            codigo_origem="BVMF",
            codigo_destino=935,
            numero_movimento=1,
            data_geracao_arquivo=date(2022, 5, 27),
            data_movimento=date(2022, 5, 26),
            reserva="",
        )
    ]

    assert result == expected
