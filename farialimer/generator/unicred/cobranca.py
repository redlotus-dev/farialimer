"""Gerador Unicred Cobrança"""

from farialimer.generator.unicred.base_unicred import UnicredGenerator


class UnicredCobrancaGenerator(UnicredGenerator):
    """Gerador para Cobrança Unicred"""

    def __init__(self):
        super().__init__(provider="unicred")
