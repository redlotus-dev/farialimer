"""Santander specific Specs tests"""

import pytest
from farialimer.parser.santander.pagamento_fornecedores import (
    PagamentoFornecedoresParser,
)


@pytest.mark.parametrize(
    "header, line, expected",
    [
        ("", "03300000C00000 0000", "0"),
        ("", "03300011C00010 0000", "1CRE"),  # 01 = Crédito em Conta Corrente
        (
            "",
            "03300011C00030 0000",
            "1CRE",
        ),  # 03 = Transferências para outros bancos (DOC, TED CIP e TED STR)
        ("", "03300011C00050 0000", "1CRE"),  # 05 = Crédito em Conta Poupança
        ("", "03300011C00100 0000", "1CRE"),  # 10 = Ordem de Pagamento / Recibo
        (
            "",
            "03300011C00110 0000",
            "1TRC",
        ),  # 11 = Pagamento de Contas e Tributos com Código de Barras¹
        ("", "03300011C00160 0000", "1TRS"),  # 16 = DARF Normal – sem código de barras
        (
            "",
            "03300011C00170 0000",
            "1TRS",
        ),  # 17 = GPS - Guia da Previdência Social – sem código de barras
        ("", "03300011C00200 0000", "1CRE"),  # 20 = Caixa “Autenticação”
        ("", "03300011C00220 0000", "1TRS"),  # 22 = GARE SP ICMS – sem código de barras
        ("", "03300011C00230 0000", "1TRS"),  # 23 = GARE SP DR – sem código de barras
        (
            "",
            "03300011C00240 0000",
            "1TRS",
        ),  # 24 = GARE SP ITCMD – sem código de barras
        (
            "",
            "03300011C00250 0000",
            "1TRS",
        ),  # 25 = IPVA SP, PR e MG – Pagamento com o RENAVAM
        (
            "",
            "03300011C00260 0000",
            "1TRS",
        ),  # 26 = LICENCIAMENTO SP, PR e MG – Pagamento com o RENAVAM
        (
            "",
            "03300011C00270 0000",
            "1TRS",
        ),  # 27 = DPVAT SP, PR e MG – Pagamento com o RENAVAM
        (
            "",
            "03300011C00300 0000",
            "1TIT",
        ),  # 30 = Liquidação de títulos em carteira de cobrança próprio Santander
        ("", "03300011C00310 0000", "1TIT"),  # 31 = Liquidação de títulos outros Bancos
        (
            "",
            "03300011C00350 0000",
            "1OCT",
        ),  # 35 = Ordem de Crédito por Teleprocessamento – OCT
        ("", "03300011C00450 0000", "1PIX"),
        # 45 = Pix Transferência – Obrigatório o preenchimento dos Segmentos A e B,
        # Segmento C em caso de conta pagamento.
        (
            "",
            "03300011I00450 0000",
            "1CAP",
        ),  # Captura de Titulos de cobrança - "I" no index 8
        ("1CRE", "-------3-----A-----", "3ACRE"),
        ("1CRE", "-------3-----B-----", "3BCRE"),
        ("1CRE", "-------3-----C-----", "3CCRE"),
        ("1CRE", "-------3-----Z-----", "3ZCRE"),
        ("1PIX", "-------3-----A-----", "3APIX"),
        ("1PIX", "-------3-----B-----", "3BPIX"),
        ("1PIX", "-------3-----C-----", "3CPIX"),
        ("1PIX", "-------3-----J-----", "3JPIX"),
        ("1PIX", "-------3-----J---52", "3J52PIX"),
        ("1PIX", "-------3-----Z-----", "3ZPIX"),
        ("1OCT", "-------3-----I-----", "3IOCT"),
        ("1OCT", "-------3-----Z-----", "3ZOCT"),
        ("1TIT", "-------3-----J-----", "3JTIT"),
        ("1TIT", "-------3-----J---52", "3J52TIT"),
        ("1TIT", "-------3-----B-----", "3BTIT"),
        ("1TIT", "-------3-----Z-----", "3ZTIT"),
        ("1TRC", "-------3-----O-----", "3OTRC"),
        ("1TRC", "-------3-----B-----", "3BTRC"),
        ("1TRC", "-------3-----Z-----", "3ZTRC"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "17", "3N1TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "16", "3N2TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "22", "3N4TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "23", "3N4TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "24", "3N4TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "25", "3N5TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "27", "3N6TRS"),
        ("1TRS", "-------3-----N-----" + "-" * 113 + "26", "3N7TRS"),
        ("1TRS", "-------3-----B-----", "3BTRS"),
        ("1TRS", "-------3-----W-----" + "-" * 157 + "01", "3W1TRS"),
        ("1TRS", "-------3-----Z-----", "3ZTRS"),
        ("1CAP", "-------3-----G-----", "3GCAP"),
        ("1CAP", "-------3-----H-----", "3HCAP"),
        ("1CAP", "-------3-----Y---53", "3Y53CAP"),
        ("1CRE", "-------5-----------", "5CRE"),
        ("1PIX", "-------5-----------", "5PIX"),
        ("1OCT", "-------5-----------", "5OCT"),
        ("1TIT", "-------5-----------", "5TIT"),
        ("1TRC", "-------5-----------", "5TRC"),
        ("1TRS", "-------5-----------", "5TRS"),
        ("1CAP", "-------5-----------", "5CAP"),
        ("", "03300049C00000 0000", "9"),
    ],
)
def test_get_line_register(header, line, expected):
    """
    Test the get_line_register. For Santander, the register type is at the position 8 (index=7).

    If the register type == 1,
        then an additional identifier type must be added to the register type.
        Identifier is at Position 10-12 (index=[9-11]).
        if identifier in (01, 03, 05, 10, 20), then register type is 1CRE
        if identifier in (11), then register type is 1TRC
        if identifier in (16, 17, 22, 23, 24, 25, 26, 27), then register type is 1TRS
        if identifier in (30, 31), then register type is 1TIT
        if identifier in (35), then register type is 1OCT
        if identifier in (45), then register type is 1PIX

        an outlier is the captura de titulos, where the op_type is at position 09 (index=[08]),
        if op_type == "I" then register type is 1CAP

    If the register type == 3,
        then an additional segment type must be added to the register type.
        based on the batch header record (type = 1)

        Segment is at Position 14 (index=13)
        If segment == J, another additional identifier type must be added to the register type.
        if the position 18-19 == 52, then register type is 3J52, else its 3J

        if the segment == N, an additional identifier type must be added to the register type.
        it's located at position 133-134 (index=[132-133])

        if the segment == W, an additional identifier type must be added to the register type.
        it´s located at position 177-178 (index=[176-177])

    if the register type == 5,
        then an additional identifier type must be added to the register type.

    registers type 0 and 9 are the same for all services
    """
    parser = PagamentoFornecedoresParser("santander")
    parser.current_register_header = header

    result = parser.get_line_register(line)

    assert result == expected
