"""Gerador Santander Pagamento Fornecedores"""

from farialimer.generator.santander.base_santander import SantanderGenerator


class PagamentoFornecedoresGenerator(SantanderGenerator):
    """Gerador para Pagamento de Fornecedores Santander"""

    def __init__(self):
        super().__init__(provider="santander")
