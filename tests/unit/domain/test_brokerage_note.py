from decimal import Decimal

import pytest

from correpy.domain.enums import BrokerageNoteFeeType
from correpy.domain.exceptions import InvalidBrokerageNoteFeeTypeException
from tests.factories import BrokerageNoteFactory, TransactionFactory


def test_add_transaction_when_called_then_adds_transaction_to_list_of_transactions():
    brokerage_note = BrokerageNoteFactory(transactions=[])
    transaction = TransactionFactory()

    brokerage_note.add_transaction(transaction)

    assert brokerage_note.transactions == [transaction]


def test_update_fee_from_fee_type_when_called_with_settlement_fee_then_updates_settlement_fee_value():
    current_settlement_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(settlement_fee=current_settlement_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.SETTLEMENT_FEE, fee_value=updated_value)

    assert brokerage_note.settlement_fee == current_settlement_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_registration_fee_then_updates_registration_fee_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(registration_fee=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.REGISTRATION_FE, fee_value=updated_value)

    assert brokerage_note.registration_fee == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_ana_fee_then_updates_ana_fee_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(ana_fee=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.ANA_FEE, fee_value=updated_value)

    assert brokerage_note.ana_fee == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_emoluments_then_updates_emoluments_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(emoluments=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.EMOLUMENTS, fee_value=updated_value)

    assert brokerage_note.emoluments == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_operational_fee_then_updates_operational_fee_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(operational_fee=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.OPERATIONAL_FEE, fee_value=updated_value)

    assert brokerage_note.operational_fee == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_execution_fee_then_updates_execution_fee_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(execution=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.EXECUTION, fee_value=updated_value)

    assert brokerage_note.execution == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_custody_fee_then_updates_custody_fee_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(custody_fee=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.CUSTODY_FEE, fee_value=updated_value)

    assert brokerage_note.custody_fee == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_taxes_then_updates_taxes_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(taxes=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.TAXES, fee_value=updated_value)

    assert brokerage_note.taxes == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_others_then_updates_others_value():
    current_fee = Decimal(10)
    brokerage_note = BrokerageNoteFactory(others=current_fee)
    updated_value = Decimal(20)

    brokerage_note.update_fee_from_fee_type(fee_type=BrokerageNoteFeeType.OTHERS, fee_value=updated_value)

    assert brokerage_note.others == current_fee + updated_value


def test_update_fee_from_fee_type_when_called_with_invalid_fee_type_then_raises_invalid_brokerage_note_fee_type():
    brokerage_note = BrokerageNoteFactory()

    with pytest.raises(InvalidBrokerageNoteFeeTypeException):
        brokerage_note.update_fee_from_fee_type(fee_type="invalid", fee_value=Decimal(20))
