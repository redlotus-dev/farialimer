"""Gerador Sicoob Folha de Pagamento"""

from farialimer.generator.sicoob.base_sicoob import SicoobGenerator


class SicoobFolhaPagamentoGenerator(SicoobGenerator):
    """Gerador para Folha de Pagamento Sicoob - Layout CNAB 240 FEBRABAN"""

    def __init__(self):
        super().__init__(provider="sicoob")
