"""Módulo de geração Bradesco"""

from farialimer.generator.basic_generator import BasicGenerator


class BradescoGenerator(BasicGenerator):
    """Gerador de arquivos Bradesco"""

    def __init__(self, provider: str = "bradesco"):
        super().__init__(provider=provider)
