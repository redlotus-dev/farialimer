"""Gerador Bradesco Folha de Pagamento"""

from farialimer.generator.bradesco.base_bradesco import BradescoGenerator


class FolhaPagamentoGenerator(BradescoGenerator):
    """Gerador para Folha de Pagamento Bradesco - Layout CNAB 240 FEBRABAN"""

    def __init__(self):
        super().__init__(provider="bradesco")
