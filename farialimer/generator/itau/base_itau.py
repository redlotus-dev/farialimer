"""Módulo de geração Itaú"""

from farialimer.generator.basic_generator import BasicGenerator


class ItauGenerator(BasicGenerator):
    """Gerador de arquivos Itaú"""

    def __init__(self, provider: str = "itau"):
        super().__init__(provider=provider)
