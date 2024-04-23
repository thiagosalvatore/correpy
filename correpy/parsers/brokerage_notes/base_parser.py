import io
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from itertools import groupby
from typing import Dict, Iterable, List, Optional, Tuple

import fitz

from correpy.domain.entities.brokerage_note import BrokerageNote
from correpy.domain.entities.security import Security
from correpy.domain.entities.transaction import Transaction
from correpy.domain.enums import BrokerageNoteFeeType, TransactionType
from correpy.parsers.brokerage_notes.brokerage_note_section import BrokerageNoteSection
from correpy.parsers.brokerage_notes.word_rectangle import WordRectangle
from correpy.parsers.fitz_parser import FitzParser
from correpy.utils import extract_value_from_line, extract_amount_from_line

NoteKey = tuple[int, date]


class BaseBrokerageNoteParser(ABC):
    def __init__(self, brokerage_note: io.BytesIO, password: Optional[str] = None) -> None:
        self.fitz_parser = FitzParser(file=brokerage_note, password=password)
        self.brokerage_notes: Dict[NoteKey, BrokerageNote] = {}

    @property
    @abstractmethod
    def buy_transaction_indicator_on_brokerage_note(self) -> str:
        ...

    @property
    @abstractmethod
    def sell_transaction_indicator_on_brokerage_note(self) -> str:
        ...

    @property
    @abstractmethod
    def first_column_transactions(self) -> str:
        ...

    @property
    @abstractmethod
    def transaction_columns_index(self) -> Dict[str, int]:
        ...

    @property
    @abstractmethod
    def financial_summary_header_mapper(self) -> Dict[str, BrokerageNoteFeeType]:
        ...

    @property
    @abstractmethod
    def last_transaction_item(self) -> str:
        ...

    @classmethod
    def _group_words_by_line(cls, *, words: Iterable[WordRectangle]) -> List[List[WordRectangle]]:
        return [
            list(grouped_word[1])
            for grouped_word in groupby(words, key=lambda word: word.y1)  # type:ignore[no-any-return]
        ]

    @classmethod
    def _sort_words_per_line_then_per_column(cls, words: List[WordRectangle]) -> Iterable[WordRectangle]:
        return sorted(words, key=lambda word: (word.y1, word.x0))

    def _build_text_from_words(self, words: Iterable[WordRectangle]) -> str:
        line = self._get_text_line_from_list_of_words(words=words)
        return " ".join(line)

    def _build_text_from_all_words_in_line(
        self, words_grouped_by_line: Iterable[Tuple[float, Iterable[WordRectangle]]]
    ) -> str:
        return "".join(self._build_text_from_words(words=words) for _, words in words_grouped_by_line)

    @staticmethod
    def _get_text_line_from_list_of_words(*, words: Iterable[WordRectangle]) -> List[str]:
        return [word.value for word in words]

    def _sort_and_group_elements_by_line_on_file(
        self, elements: List[WordRectangle]
    ) -> Iterable[Iterable[WordRectangle]]:
        elements_text = self._sort_words_per_line_then_per_column(words=elements)
        return self._group_words_by_line(words=elements_text)

    def __parse_transaction_type(self, *, line_array: List[str]) -> TransactionType:
        transaction_type = line_array[self.transaction_columns_index["transaction_type"]]
        if transaction_type == self.buy_transaction_indicator_on_brokerage_note:
            return TransactionType.BUY
        return TransactionType.SELL

    def __parse_security_name(self, *, line_array: List[str]) -> str:
        security_name_array = line_array[
            self.transaction_columns_index["start_short_name"] : self.transaction_columns_index["end_short_name"]
        ]
        return " ".join(security_name_array)

    def __parse_transaction_unit_price(self, *, line_array: List[str]) -> Decimal:
        unit_value_string = line_array[self.transaction_columns_index["unit_value"]]
        return extract_value_from_line(line=unit_value_string)

    def __parse_transaction_amount(self, *, line_array: List[str]) -> Decimal:
        amount_string = line_array[self.transaction_columns_index["amount"]]
        return extract_amount_from_line(line=amount_string)

    def _create_transaction(self, *, line: str) -> Transaction:
        line_array = line.split(" ")
        transaction_type = self.__parse_transaction_type(line_array=line_array)
        security_name = self.__parse_security_name(line_array=line_array)
        unit_price = self.__parse_transaction_unit_price(line_array=line_array)
        amount = self.__parse_transaction_amount(line_array=line_array)

        return Transaction(
            transaction_type=transaction_type,
            amount=amount,
            unit_price=unit_price,
            security=Security(name=security_name),
        )

    def _build_brokerage_note_section_from_two_rectangles(
        self,
        first_rectangle: fitz.Rect,
        second_rectangle: fitz.Rect,
        page_number: int,
    ) -> BrokerageNoteSection:
        rectangle_between = self.fitz_parser.build_rectangle_from_beginning_first_rectangle_end_second_rectangle(
            first_rect=first_rectangle, second_rect=second_rectangle
        )
        rectangle_text_elements = self.fitz_parser.get_words_in_rectangle(
            page_number=page_number, rectangle=rectangle_between
        )
        grouped_words = self._sort_and_group_elements_by_line_on_file(elements=rectangle_text_elements)
        return BrokerageNoteSection(words_grouped_by_line=grouped_words)

    @abstractmethod
    def _get_or_create_brokerage_note_by_page(self, page: fitz.Page, page_number: int) -> BrokerageNote:
        raise NotImplementedError()

    @abstractmethod
    def set_brokerage_note_transactions(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def set_brokerage_note_fees(self) -> None:
        raise NotImplementedError()

    def parse_brokerage_note(self) -> List[BrokerageNote]:
        self.set_brokerage_note_transactions()
        self.set_brokerage_note_fees()
        return list(self.brokerage_notes.values())
