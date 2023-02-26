"""Parser Tests"""

import datetime
from collections import OrderedDict
from decimal import Decimal

import pytest

from farialimer.parser.b3parser import B3Parser as Parser


def test_get_filetype():
    """Test the getfiletype"""

    path = "tests/specs/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser("imbarq014")
    content = parser.read_file(path)
    result = parser.get_filetype(content[0])

    expected = "IMBARQ014"

    assert result == expected


@pytest.mark.parametrize(
    "spec, path",
    [
        (
            "imbarq001",
            "tests/specs/b3/samples/imbarq001/IMBARQ001_BV000272201610130000001000489051801.txt",
        ),
        (
            "imbarq002",
            "tests/specs/b3/samples/imbarq002/IMBARQ002_BV000272202204060000001000935130742.txt",
        ),
        (
            "imbarq004",
            "tests/specs/b3/samples/imbarq004/IMBARQ004_BV000272202204060000001001512113233.txt",
        ),
        (
            "imbarq006",
            "tests/specs/b3/samples/imbarq006/IMBARQ006_BV000272202204050000001000935195407.txt",
        ),
        (
            "imbarq007",
            "tests/specs/b3/samples/imbarq007/IMBARQ007_BV000272202108040000052019824225451.txt",
        ),
        (
            "imbarq009",
            "tests/specs/b3/samples/imbarq009/IMBARQ009_BV000272202108040000001000935212154.txt",
        ),
        (
            "imbarq014",
            "tests/specs/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt",
        ),
    ],
)
def test_parse_load_without_issues(spec, path):
    """Load a sample file and parse it without issues"""
    parser = Parser(spec)
    content = parser.read_file(path)

    result = parser.parse(content, spec=spec)

    assert len(result) > 0


def test_parse_imbarq014():
    """Test the parser for imbarq014 sample file"""
    path = "tests/specs/b3/samples/imbarq014/IMBARQ014_BV000272202205260000001000935071656.txt"
    parser = Parser("imbarq014")
    content = parser.read_file(path)

    head = content[0]
    l18 = content[1]
    l19 = content[42]
    l31 = content[47]
    trail = content[-1]
    sample = [head, l18, l19, l31, trail]
    result = parser.parse(sample, spec="imbarq014")

    expected = [
        OrderedDict(
            [
                ("tipo_registro", "00"),
                ("codigo_arquivo", "IMBARQ014"),
                ("codigo_categoria_usuario", 1),
                ("codigo_usuario", 935),
                ("codigo_origem", "BVMF"),
                ("codigo_destino", 935),
                ("numero_movimento", 1),
                ("data_geracao_arquivo", datetime.date(2022, 5, 27)),
                ("data_movimento", datetime.date(2022, 5, 26)),
                ("reserva", ""),
            ]
        ),
        OrderedDict(
            [
                ("tipo_registro", "18"),
                ("codigo_participante_solicitante", "935"),
                ("codigo_investidor_solicitante", "10021"),
                ("codigo_participante_solicitado", "935"),
                ("codigo_investidor_solicitado", "10021"),
                ("data_referencia", datetime.date(2022, 5, 26)),
                ("codigo_tipo_garantia", "8"),
                ("codigo_instrumento", "10000001"),
                ("codigo_origem_identificacao_instrumento", "8"),
                ("codigo_bolsa_valor", "BVMF"),
                ("finalidade_cobertura", 1),
                ("codigo_categoria_titular", "CL"),
                ("identificador_garantia", "Real - Netting"),
                ("numero_garantia", 2021000000611),
                ("identificador_cobertura", "2"),
                ("identificador_titularidade", "1"),
                ("data_vencimento", None),
                ("quantidade_depositada", Decimal("2870147502.5900000000")),
                ("quantidade_aceita", Decimal("2870147502.5900000000")),
                ("quantidade_valorizada", Decimal("870147502.5900000000")),
                ("quantidade_distribuida", Decimal("0.0")),
                ("quantidade_bloqueada", Decimal("0.0")),
                ("isin", ""),
                ("carteira", ""),
                ("valor_garantia", Decimal("2870147502.59")),
                ("valor_bloqueado_retirada", Decimal("0.0")),
                ("codigo_custodiante", ""),
                ("codigo_investidor_custodiante", ""),
                ("reserva", ""),
            ]
        ),
        OrderedDict(
            [
                ("tipo_registro", "19"),
                ("codigo_participante_solicitante", "935"),
                ("codigo_investidor_solicitante", "11123"),
                ("codigo_participante_solicitado", "935"),
                ("codigo_investido_solicitado", "11123"),
                ("data_movimento", datetime.date(2022, 5, 26)),
                ("finalidade_cobertura", 1),
                ("sinal", "+"),
                ("risco_sem_garantias", Decimal("3498360274.71")),
                ("chamada_margem_inicial", Decimal("823646773.37")),
                ("valor_margem_inicial", Decimal("0.0")),
                ("valor_total_garantias", Decimal("2674713501.34")),
                ("perdas_permanentes", Decimal("823646773.3700000")),
                ("perdas_transitorias", Decimal("0.0")),
                ("sinal_2", "-"),
                ("saldo_garantias", Decimal("823646773.37")),
                ("reserva", ""),
            ]
        ),
        OrderedDict(
            [
                ("tipo_registro", "31"),
                ("codigo_participante_solicitante", "935"),
                ("codigo_investidor_solicitante", "544111635"),
                ("codigo_participante_solicitado", "935"),
                ("codigo_investidor_solicitado", "544111635"),
                ("data_referencia", datetime.date(2022, 5, 26)),
                ("codigo_tipo_garantia", "3"),
                ("codigo_instrumento", "200000153650"),
                ("codigo_origem_identificacao_instrumento", "8"),
                ("codigo_bolsa_valor", "BVMF"),
                ("finalidade_cobertura", 1),
                ("codigo_categoria_titular", "CL"),
                ("identificador_garantia", "PETR4"),
                ("numero_garantia", 2021000001729),
                ("identificador_cobertura", "2"),
                ("identificador_titularidade", "1"),
                ("data_vencimento", None),
                ("quantidade_depositada", Decimal("10.0")),
                ("quantidade_aceita", Decimal("10.0")),
                ("quantidade_valorizada", Decimal("10.0")),
                ("quantidade_distribuida", Decimal("0.0")),
                ("quantidade_bloqueada", Decimal("0.0")),
                ("isin", "BRPETRACNPR6"),
                ("carteira", "23906"),
                ("valor_garantia", Decimal("380.97")),
                ("valor_bloqueado_retirada", Decimal("0.0")),
                ("codigo_participante_negociacao_liquidacao", "935"),
                ("codigo_investidor_negocicacao_liquidacao", "544111635"),
                ("reserva", ""),
            ]
        ),
        OrderedDict(
            [
                ("tipo_registro", "99"),
                ("codigo_arquivo", "IMBARQ014"),
                ("codigo_categoria_usuario", 1),
                ("codigo_usuario", 935),
                ("codigo_origem", "BVMF"),
                ("codigo_destino", 935),
                ("numero_movimento", 1),
                ("data_geracao_arquivo", datetime.date(2022, 5, 27)),
                ("total_registros_gerados", 65),
                ("data_movimento", datetime.date(2022, 5, 26)),
                ("reserva", ""),
            ]
        ),
    ]

    assert result == expected
