"""Gerador Itaú Folha de Pagamento"""

from farialimer.generator.itau.base_itau import ItauGenerator


class ItauFolhaPagamentoGenerator(ItauGenerator):
    """Gerador para Folha de Pagamento Itaú - Layout CNAB 240 FEBRABAN"""

    def __init__(self):
        super().__init__(provider="itau")
