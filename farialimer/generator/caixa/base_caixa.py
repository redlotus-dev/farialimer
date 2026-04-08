"""Módulo de geração Caixa Econômica Federal"""

from farialimer.generator.basic_generator import BasicGenerator


class CaixaGenerator(BasicGenerator):
    """Gerador de arquivos Caixa"""

    def __init__(self, provider: str = "caixa"):
        super().__init__(provider=provider)
