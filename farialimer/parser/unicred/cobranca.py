"""Unicred Cobrança (Remessa de Boletos) Parser - CNAB 240."""

from farialimer.parser.unicred.base_unicred import UnicredParser


class UnicredCobranca(UnicredParser):
    """Parser para Cobrança Unicred - CNAB 240.

    Tipos de registro (posição 8, index 7):
        '0' = Header de Arquivo
        '1' = Header de Lote
        '3' = Detalhe (Segmentos P, Q, Y)
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
