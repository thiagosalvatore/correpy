from dataclasses import dataclass, field
from decimal import Decimal

from correpy.domain.entities.security import Security
from correpy.domain.enums import TransactionType

BRAZIL_SOURCE_WITHHELD_TAX_PERCENTAGE = Decimal(0.005)


@dataclass
class Transaction:
    transaction_type: TransactionType
    amount: Decimal
    unit_price: Decimal
    security: Security
    source_withheld_taxes: Decimal = field(init=False, default=Decimal(0))

    def __post_init__(self) -> None:
        if self.transaction_type == TransactionType.SELL:
            self.source_withheld_taxes = Decimal(
                round(self.unit_price * self.amount * BRAZIL_SOURCE_WITHHELD_TAX_PERCENTAGE / 100, 2)
            )
