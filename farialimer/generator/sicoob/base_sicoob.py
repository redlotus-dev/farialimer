"""Módulo de geração Sicoob"""

from farialimer.generator.basic_generator import BasicGenerator


class SicoobGenerator(BasicGenerator):
    """Gerador de arquivos Sicoob"""

    def __init__(self, provider: str = "sicoob"):
        super().__init__(provider=provider)
