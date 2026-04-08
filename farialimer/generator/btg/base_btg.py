"""Módulo de geração BTG Pactual"""

from farialimer.generator.basic_generator import BasicGenerator


class BTGGenerator(BasicGenerator):
    """Gerador de arquivos BTG Pactual"""

    def __init__(self, provider: str = "btg"):
        super().__init__(provider=provider)
