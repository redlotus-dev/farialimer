"""Gerador BTG Pagamento"""

from farialimer.generator.btg.base_btg import BTGGenerator


class BTGPagamentoGenerator(BTGGenerator):
    """Gerador para Pagamento BTG Pactual"""

    def __init__(self):
        super().__init__(provider="btg")
