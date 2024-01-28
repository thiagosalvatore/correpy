from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List

from correpy.domain.entities.transaction import Transaction
from correpy.domain.enums import BrokerageNoteFeeType
from correpy.domain.exceptions import InvalidBrokerageNoteFeeTypeException


@dataclass
class BrokerageNote:  # pylint:disable=too-many-instance-attributes
    reference_id: int
    reference_date: date
    settlement_fee: Decimal = Decimal(0)
    registration_fee: Decimal = Decimal(0)
    term_fee: Decimal = Decimal(0)
    ana_fee: Decimal = Decimal(0)
    emoluments: Decimal = Decimal(0)
    operational_fee: Decimal = Decimal(0)
    execution: Decimal = Decimal(0)
    custody_fee: Decimal = Decimal(0)
    taxes: Decimal = Decimal(0)
    irrf: Decimal = Decimal(0)
    others: Decimal = Decimal(0)
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def update_fee_from_fee_type(self, fee_type: BrokerageNoteFeeType, fee_value: Decimal) -> None:
        if fee_type == BrokerageNoteFeeType.SETTLEMENT_FEE:
            self.settlement_fee += fee_value
        elif fee_type == BrokerageNoteFeeType.TERM_FEE:
            self.term_fee += fee_value
        elif fee_type == BrokerageNoteFeeType.REGISTRATION_FE:
            self.registration_fee += fee_value
        elif fee_type == BrokerageNoteFeeType.ANA_FEE:
            self.ana_fee += fee_value
        elif fee_type == BrokerageNoteFeeType.EMOLUMENTS:
            self.emoluments += fee_value
        elif fee_type == BrokerageNoteFeeType.OPERATIONAL_FEE:
            self.operational_fee += fee_value
        elif fee_type == BrokerageNoteFeeType.EXECUTION:
            self.execution += fee_value
        elif fee_type == BrokerageNoteFeeType.CUSTODY_FEE:
            self.custody_fee += fee_value
        elif fee_type == BrokerageNoteFeeType.TAXES:
            self.taxes += fee_value
        elif fee_type == BrokerageNoteFeeType.IRRF:
            self.irrf += fee_value
        elif fee_type == BrokerageNoteFeeType.OTHERS:
            self.others += fee_value
        else:
            raise InvalidBrokerageNoteFeeTypeException
