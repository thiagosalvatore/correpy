[![thiagosalvatore](https://circleci.com/gh/thiagosalvatore/correpy.svg?style=shield)](https://app.circleci.com/pipelines/github/thiagosalvatore/correpy?branch=main&filter=all)
[![PyPI version](https://badge.fury.io/py/correpy.svg)](https://badge.fury.io/py/correpy)
# CorrePy
CorrePy (Corretagem Python) é uma lib responsável por parsear notas de corretagem no padrão B3 (Sinacor) e retornar os
dados em um formato estruturado para que você possa utilizar em suas aplicações.

## Instalação
Este projeto suporta qualquer versão do python >= 3.8

`pip install correpy`

## Como usar
Depois de instalada, sua utilização é extremamente simples. Primeiramente vamos precisar abrir o PDF com a nota de corretagem.
Se você estiver utilizando essa lib em uma API, você precisará transformar seu arquivo PDF em BytesIO.

```python
import io

with open('path to your pdf file', 'rb') as f:
    content = io.BytesIO(f.read())
    content.seek(0)
```

O conteúdo da sua nota de corretagem estará na variável `content` e é ela quem iremos usar para inicializar a nossa lib.
Se a sua nota de corretagem possuir senha, você precisará informar também, caso contrário o parser nâo irá funcionar.

```python
import io

from correpy.parsers.brokerage_notes.parser_factory import ParserFactory

with open('path to your pdf file', 'rb') as f:
    content = io.BytesIO(f.read())
    content.seek(0)
    
    brokerage_notes = ParserFactory(brokerage_note=content, password="password").parse_brokerage_note()
```

### Resultado
Depois de efetuar o parser da sua nota de corretagem, `correpy` irá retornar uma lista no formato abaixo. Os valores de cada campo serão explicados em seguida.

```python
[
    BrokerageNote(
        reference_date=date(2022, 5, 2),
        settlement_fee=Decimal("7.92"),
        registration_fee=Decimal("0"),
        term_fee=Decimal("0"),
        ana_fee=Decimal("0"),
        emoluments=Decimal("1.58"),
        operational_fee=Decimal("0"),
        execution=Decimal("0"),
        custody_fee=Decimal("0"),
        taxes=Decimal("0"),
        others=Decimal("0"),
        transactions=[
            Transaction(
                transaction_type=TransactionType.SELL,
                amount=54,
                unit_price=Decimal('24.99'),
                security=Security(
                    name='BBSEGURIDADE ON NM'
                )
            ),
            Transaction(
                transaction_type=TransactionType.BUY,
                amount=200,
                unit_price=Decimal('17.29'),
                security=Security(
                    name='MOVIDA ON NM'
                )
            )
        ]
    )
]
```

### Descrição das entidades
Abaixo você pode encontrar a descrição de cada um dos campos retornados. 

#### Brokerage Note

| BrokerageNote         |                                     |
|-----------------------|-------------------------------------|
| reference_id          | Número da nota                      |
| reference_date        | Data do pregão                      |
| settlement_fee        | Taxa de liquidação                  |
| registration_fee      | Taxa de registro                    |
| term_fee              | Taxa de termo/opções                |
| ana_fee               | Taxa A.N.A                          |
| emoluments            | Emolumentos                         |
| operational_fee       | Taxa Operacional                    |
| execution             | Execução                            |
| custody_fee           | Taxa de custódia                    |
| source_withheld_taxes | IRRF                    |
| taxes                 | Impostos                            |
| others                | Outros                              |
| transactions          | Lista de [transações](#transaction) |

#### Transaction

| Transaction          |                                                            |
|----------------------|------------------------------------------------------------|
| transaction_type     | Enum com o tipo de transação (BUY - compra, SELL - venda)  |
| amount               | Quantidade                                                 |
| unit_price           | Valor unitário                                             |
| security             | Objeto [Security](#security) representando um título       |
| source_witheld_taxes | IRRF retido na fonte (0.005% sobre o valor total de venda) |

#### Security
| Security |                         |
|----------|-------------------------|
| name     | Especificação do título |


## Como contribuir
Estamos utilizando poetry para gerenciar o projeto e suas dependencias.

Este projeto ainda está em evolução e qualquer PR é bem vindo. Algumas ferramentas estão sendo utilizadas para melhorar a qualidade do código:

1. MyPy para checagem estática de tipos
2. PyLint
3. Black
4. isort

Para verificar se o seu código continua de acordo com os critérios definidos, basta rodar `./pipeline/lint.sh`.
