"""Gerador BB Folha de Pagamento"""

from farialimer.generator.bb.base_bb import BBGenerator


class BBFolhaPagamentoGenerator(BBGenerator):
    """Gerador para Folha de Pagamento Banco do Brasil - Layout CNAB 240 FEBRABAN"""

    def __init__(self):
        super().__init__(provider="bb")
