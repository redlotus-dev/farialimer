"""Módulo de geração Sicredi"""

from farialimer.generator.basic_generator import BasicGenerator


class SicrediGenerator(BasicGenerator):
    """Gerador de arquivos Sicredi"""

    def __init__(self, provider: str = "sicredi"):
        super().__init__(provider=provider)
