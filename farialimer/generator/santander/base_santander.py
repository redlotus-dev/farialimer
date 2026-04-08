"""Módulo de geração Santander"""

from farialimer.generator.basic_generator import BasicGenerator


class SantanderGenerator(BasicGenerator):
    """Gerador de arquivos Santander"""

    def __init__(self, provider: str = "santander"):
        super().__init__(provider=provider)
