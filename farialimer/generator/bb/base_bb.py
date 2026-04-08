"""Módulo de geração Banco do Brasil"""

from farialimer.generator.basic_generator import BasicGenerator


class BBGenerator(BasicGenerator):
    """Gerador de arquivos Banco do Brasil"""

    def __init__(self, provider: str = "bb"):
        super().__init__(provider=provider)
