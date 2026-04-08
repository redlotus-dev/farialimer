"""Gerador Itaú Cobrança"""

from farialimer.generator.itau.base_itau import ItauGenerator


class ItauCobrancaGenerator(ItauGenerator):
    """Gerador para Cobrança Itaú"""

    def __init__(self):
        super().__init__(provider="itau")
