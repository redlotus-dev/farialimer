"""Gerador Sicredi Folha de Pagamento"""

from farialimer.generator.sicredi.base_sicredi import SicrediGenerator


class SicrediFolhaPagamentoGenerator(SicrediGenerator):
    """Gerador para Folha de Pagamento Sicredi - Layout CNAB 240 FEBRABAN"""

    def __init__(self):
        super().__init__(provider="sicredi")
