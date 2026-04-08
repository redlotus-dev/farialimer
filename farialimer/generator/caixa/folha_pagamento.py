"""Gerador Caixa Folha de Pagamento"""

from farialimer.generator.caixa.base_caixa import CaixaGenerator


class CaixaFolhaPagamentoGenerator(CaixaGenerator):
    """Gerador para Folha de Pagamento Caixa - Layout CNAB 240 FEBRABAN"""

    def __init__(self):
        super().__init__(provider="caixa")
