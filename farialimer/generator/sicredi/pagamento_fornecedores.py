"""Gerador Sicredi Pagamento Fornecedores"""

from farialimer.generator.sicredi.base_sicredi import SicrediGenerator


class SicrediPagamentoFornecedoresGenerator(SicrediGenerator):
    """Gerador para Pagamento de Fornecedores Sicredi"""

    def __init__(self):
        super().__init__(provider="sicredi")
