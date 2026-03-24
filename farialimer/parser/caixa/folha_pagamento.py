"""Caixa Econômica Federal Folha de Pagamento Parser - CNAB 240."""

from farialimer.parser.caixa.base_caixa import CaixaParser


class CaixaFolhaPagamento(CaixaParser):
    """Parser para Folha de Pagamento Caixa - CNAB 240 (SIACC 37.270).

    Tipos de registro (posição 8, index 7):
        '0' = Header de Arquivo
        '1' = Header de Lote
        '3' = Detalhe (Segmentos A, B)
        '5' = Trailer de Lote
        '9' = Trailer de Arquivo

    Para registro tipo '3', o segmento está na posição 14 (index 13).
    """

    def __init__(self, provider):
        super().__init__(provider=provider)

    def get_line_register(self, line: str):
        register_type = line[7]

        if register_type == "3":
            segment = line[13]
            return register_type + segment

        return register_type
