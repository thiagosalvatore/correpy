import factory
from factory.fuzzy import FuzzyChoice

from correpy.domain.entities.brokerage_note import BrokerageNote
from correpy.domain.entities.security import Security
from correpy.domain.entities.transaction import Transaction
from correpy.domain.enums import TransactionType


class SecurityFactory(factory.Factory):
    name = factory.Faker("name")

    class Meta:
        model = Security


class TransactionFactory(factory.Factory):
    transaction_type = FuzzyChoice(TransactionType)
    amount = factory.Faker("pydecimal", max_value=100000, min_value=1, positive=True)
    unit_price = factory.Faker("pydecimal", right_digits=2, max_value=10000, min_value=1, positive=True)
    security = factory.SubFactory(SecurityFactory)

    class Meta:
        model = Transaction


class BrokerageNoteFactory(factory.Factory):
    reference_date = factory.Faker("date_object")
    settlement_fee = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    registration_fee = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    term_fee = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    ana_fee = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    emoluments = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    operational_fee = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    execution = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    custody_fee = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    taxes = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    others = factory.Faker("pydecimal", right_digits=2, max_value=1000, min_value=1, positive=True)
    transactions = factory.List([factory.SubFactory(TransactionFactory) for _ in range(1)])

    class Meta:
        model = BrokerageNote
