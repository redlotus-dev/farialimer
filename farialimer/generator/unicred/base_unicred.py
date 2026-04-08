"""Módulo de geração Unicred"""

from farialimer.generator.basic_generator import BasicGenerator


class UnicredGenerator(BasicGenerator):
    """Gerador de arquivos Unicred"""

    def __init__(self, provider: str = "unicred"):
        super().__init__(provider=provider)
