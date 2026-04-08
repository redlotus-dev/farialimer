"""Gerador Banrisul Contas a Pagar"""

from farialimer.generator.banrisul.base_banrisul import BanrisulGenerator


class BanrisulContasAPagarGenerator(BanrisulGenerator):
    """Gerador para Contas a Pagar Banrisul"""

    def __init__(self):
        super().__init__(provider="banrisul")
