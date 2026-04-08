![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/redlotus-dev/farialimer/faria-limer-tests.yaml)
[![codecov](https://codecov.io/gh/redlotus-dev/farialimer/branch/main/graph/badge.svg?token=DT5E8GHT8Q)](https://codecov.io/gh/redlotus-dev/farialimer)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=redlotus-dev_farialimer&metric=alert_status)](https://sonarcloud.io/dashboard?id=redlotus-dev_farialimer)
[![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=redlotus-dev_farialimer&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=redlotus-dev_farialimer)
[![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=redlotus-dev_farialimer&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=redlotus-dev_farialimer)

![Discord](https://img.shields.io/discord/1073033206686818304)
# farialimer
Parser / Writer for Brazilian Finance Documents
![farialimer](https://user-images.githubusercontent.com/8230037/219248391-ffad24cd-50f9-4fb5-8fc9-19a45561ab0e.png)

# Intro
Bem-vindo ao projeto de CNAB e IMBARQ! Este projeto tem como objetivo fornecer uma solução open source para processar e gerenciar arquivos de remessa e retorno de cobranças bancárias, de acordo com as normas CNAB e IMBARQ.

Chegou a hora de unificar nossos esforços e resolver de uma vez por todas essa implementação de layouts.

Nossa equipe acredita que a transparência e a colaboração são essenciais para o desenvolvimento de soluções financeiras eficientes e confiáveis. Nós convidamos a comunidade a participar deste projeto, compartilhar ideias, reportar bugs e contribuir com código. Juntos, podemos criar uma solução robusta e de alta qualidade para o setor financeiro.

## Uso

### Parsing (leitura de arquivos CNAB/IMBARQ)

```python
from farialimer.parser.bradesco.folha_pagamento import FolhaPagamentoParser

parser = FolhaPagamentoParser("bradesco")
content = parser.read_file("caminho/do/arquivo.rem")
registros = parser.parse(content, "folha_pagamento")

for registro in registros:
    print(registro)
# OrderedDict([('codigo_banco', 237), ('lote_servico', 0), ...])
```

### Gerador (escrita de arquivos CNAB)

O gerador recebe uma lista de tuplas `(tipo_registro, dados)` e produz linhas de largura fixa baseadas nas mesmas specs YAML usadas pelo parser.

```python
from decimal import Decimal
from farialimer.generator.bradesco.folha_pagamento import FolhaPagamentoGenerator

generator = FolhaPagamentoGenerator()

registros = [
    ("0", {  # Header de Arquivo
        "codigo_banco": 237,
        "lote_servico": 0,
        "tipo_registro": 0,
        "tipo_inscricao_empresa": 2,
        "numero_inscricao_empresa": 12345678000190,
        "nome_empresa": "EMPRESA TESTE LTDA",
        "nome_banco": "BANCO BRADESCO SA",
        "codigo_remessa_retorno": 1,
        "data_geracao_arquivo": 23032026,
        "hora_geracao_arquivo": 143000,
        "numero_sequencial_arquivo": 1,
        "layout_arquivo": 80,
        "densidade_gravacao_arquivo": 1600,
    }),
    ("3A", {  # Detalhe - Segmento A
        "codigo_banco": 237,
        "lote_servico": 1,
        "tipo_registro": 3,
        "numero_registro": 1,
        "segmento": "A",
        "tipo_movimento": 0,
        "codigo_movimento": 0,
        "banco_favorecido": 237,
        "agencia_favorecido": 4567,
        "nome_favorecido": "JOAO DA SILVA",
        "data_pagamento": 23032026,
        "valor_pagamento": Decimal("1500.00"),
    }),
    ("9", {  # Trailer de Arquivo
        "codigo_banco": 237,
        "lote_servico": 9999,
        "tipo_registro": 9,
        "quantidade_lotes": 1,
        "quantidade_registros": 3,
        "quantidade_contas_conciliacao": 1,
    }),
]

# Gerar lista de linhas
linhas = generator.gerar(registros, "folha_pagamento")
# ['23700000         2123456780001900000000000...', ...]

# Ou gravar direto em arquivo
generator.gerar_arquivo(registros, "folha_pagamento", "saida.rem")
```

Cada linha gerada tem exatamente a largura definida pela spec (240 caracteres para CNAB, ate 1000 para B3). Campos nao informados sao preenchidos com zeros (numericos) ou espacos (texto). Campos com `default` na spec YAML sao aplicados automaticamente.

### Geradores disponiveis

| Banco | Gerador | Spec |
|-------|---------|------|
| Bradesco | `FolhaPagamentoGenerator` | `folha_pagamento` |
| Itau | `ItauFolhaPagamentoGenerator`, `ItauCobrancaGenerator` | `folha_pagamento`, `cobranca_240` |
| Banco do Brasil | `BBFolhaPagamentoGenerator` | `folha_pagamento` |
| Santander | `PagamentoFornecedoresGenerator` | `pagamento_fornecedores` |
| Caixa | `CaixaFolhaPagamentoGenerator` | `folha_pagamento` |
| Sicoob | `SicoobFolhaPagamentoGenerator` | `folha_pagamento` |
| Sicredi | `SicrediFolhaPagamentoGenerator`, `SicrediPagamentoFornecedoresGenerator` | `folha_pagamento`, `pagamento_fornecedores` |
| Unicred | `UnicredCobrancaGenerator` | `cobranca` |
| BTG | `BTGPagamentoGenerator` | `pagamento` |
| Banrisul | `BanrisulContasAPagarGenerator` | `contas_a_pagar` |
| B3 | `B3Generator` | `imbarq001`, `imbarq002`, ... |

## CNAB
CNAB significa "Centro Nacional de Automação Bancária". É um padrão de arquivo utilizado por bancos no Brasil para a transferência de informações financeiras, como cobranças, pagamentos, boletos bancários, entre outras. O CNAB é um padrão estabelecido pela Febraban (Federação Brasileira de Bancos) que padroniza a forma como os arquivos são estruturados, tornando mais fácil e ágil a integração entre sistemas de diferentes bancos. O uso do CNAB permite a automação de processos bancários, melhorando a eficiência e a segurança nas transações financeiras.

## IMBARQ
IMBARQ significa "Interface para Movimentação Bancária de Retorno e Quitação". É um padrão de arquivo utilizado pela B3 (Bolsa Brasileira de Valores) para a transferência de informações financeiras entre instituições financeiras. O IMBARQ é utilizado para facilitar a integração de sistemas de diferentes bancos, permitindo a realização de operações bancárias de forma mais ágil e segura.

## Outros Projetos
Uma lista com outros projetos que serviram de inspiração:
- https://github.com/Trust-Code/python-cnab
- https://github.com/kivanio/brcobranca
- https://github.com/kmee/cnab240
- https://github.com/vintasoftware/aurorae
- https://github.com/glauberportella/cnab-layouts
