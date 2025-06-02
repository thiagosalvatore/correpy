"""
    test_parser_factory.py
    ~~~~~~~~~
    :copyright: (c) 2024 by Alby
"""

import io
import pathlib
from datetime import date
from decimal import Decimal

from testfixtures import compare

from correpy.domain.entities.brokerage_note import BrokerageNote
from correpy.domain.entities.security import Security
from correpy.domain.entities.transaction import Transaction
from correpy.domain.enums import TransactionType
from correpy.parsers.brokerage_notes.parser_factory import ParserFactory

fixtures_folder = f"{pathlib.Path(__file__).parent.parent.parent.resolve()}/fixtures"


def test_parser_factory_WHEN_called_with_brokerage_note_not_from_nu_invest_THEN_correctly_parses_brokerage_note_with_b3_parser():
    with open(f'{fixtures_folder}/b3_one_page.pdf', 'rb') as f:
        content = io.BytesIO(f.read())
        content.seek(0)
        expected_result = [
            BrokerageNote(
                reference_id=4535159,
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
                irrf=Decimal("0.79"),
                others=Decimal("0"),
                net_amount_date=date(2022, 5, 4),
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
                        amount=65,
                        unit_price=Decimal('15.94'),
                        security=Security(
                            name='BR PARTNERS UNT N2'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.BUY,
                        amount=300,
                        unit_price=Decimal('15.85'),
                        security=Security(
                            name='BR PARTNERS UNT N2'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=40,
                        unit_price=Decimal('32.91'),
                        security=Security(
                            name='BRASIL ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=1,
                        unit_price=Decimal('32.91'),
                        security=Security(
                            name='BRASIL ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=44,
                        unit_price=Decimal('20.90'),
                        security=Security(
                            name='ENERGIAS BR ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=100,
                        unit_price=Decimal('20.86'),
                        security=Security(
                            name='ENERGIAS BR ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=16,
                        unit_price=Decimal('41.65'),
                        security=Security(
                            name='ENGIE BRASIL ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=11,
                        unit_price=Decimal('41.65'),
                        security=Security(
                            name='ENGIE BRASIL ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=73,
                        unit_price=Decimal('20.80'),
                        security=Security(
                            name='KLABIN S/A UNT N2'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=83,
                        unit_price=Decimal('26.34'),
                        security=Security(
                            name='SUL AMERICA UNT N2'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=100,
                        unit_price=Decimal('26.34'),
                        security=Security(
                            name='SUL AMERICA UNT N2'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.SELL,
                        amount=100,
                        unit_price=Decimal('26.34'),
                        security=Security(
                            name='SUL AMERICA UNT N2'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.BUY,
                        amount=100,
                        unit_price=Decimal('24.68'),
                        security=Security(
                            name='BLAU ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.BUY,
                        amount=100,
                        unit_price=Decimal('24.67'),
                        security=Security(
                            name='BLAU ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.BUY,
                        amount=200,
                        unit_price=Decimal('17.29'),
                        security=Security(
                            name='MOVIDA ON NM'
                        )
                    ),
                    Transaction(
                        transaction_type=TransactionType.BUY,
                        amount=100,
                        unit_price=Decimal('17.29'),
                        security=Security(
                            name='MOVIDA ON NM'
                        )
                    )
                ]
            )
        ]
        factory = ParserFactory(brokerage_note=content, password="048")

        brokerage_notes = factory.parse()

        compare(brokerage_notes, expected_result)
