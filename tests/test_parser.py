"""Parser Tests"""

from collections import OrderedDict
from datetime import date
from farialimer.parser import Parser, get_filetype, parse_line
import farialimer.providers.b3.documents.imbarq014.layouts as lay


def test_get_filetype():
    """Test the getfiletype"""

    path = "tests/providers/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser()
    content = parser.read_file(path)
    result = get_filetype(content[0])

    expected = "IMBARQ014"

    assert result == expected


def test_parse_layout00():
    """Test the parsing of layout 00"""
    path = "tests/providers/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser()
    content = parser.read_file(path)

    layout = lay.layout_00
    line = content[0]
    result = parse_line(line, layout)

    expected = OrderedDict(
        tipo_de_registro="00",
        codigo_do_arquivo="IMBARQ014",
        codigo_da_categoria_do_usuario=1,
        codigo_do_usuario=935,
        codigo_da_origem="BVMF",
        codigo_do_destino=935,
        numero_do_movimento=1,
        data_da_geracao_do_arquivo=date(2022, 5, 27),
        data_do_movimento=date(2022, 5, 26),
        reserva="",
    )

    assert result == expected
