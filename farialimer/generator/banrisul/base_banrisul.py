"""Módulo de geração Banrisul"""

from farialimer.generator.basic_generator import BasicGenerator


class BanrisulGenerator(BasicGenerator):
    """Gerador de arquivos Banrisul"""

    def __init__(self, provider: str = "banrisul"):
        super().__init__(provider=provider)
