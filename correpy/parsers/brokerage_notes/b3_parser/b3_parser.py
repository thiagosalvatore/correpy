import logging
from datetime import date
from typing import List

import fitz
from fitz import TextPage

from correpy.domain.entities.brokerage_note import BrokerageNote
from correpy.domain.enums import BrokerageNoteFeeType
from correpy.parsers.brokerage_notes.base_parser import BaseBrokerageNoteParser
from correpy.parsers.brokerage_notes.brokerage_note_section import BrokerageNoteSection
from correpy.parsers.exceptions import ProblemParsingBrokerageNoteException
from correpy.utils import extract_date_from_line, extract_value_from_line


class B3Parser(BaseBrokerageNoteParser):
    BROKERAGE_NOTE_X_AXIS_START_COORDINATE = 0
    BROKERAGE_NOTE_X_AXIS_END_COORDINATE = 601
    BROKERAGE_NOTE_FINANCIAL_SUMMARY_Y_AXIS_END = 842
    TRANSACTIONS_SECTION_TITLE = "Negócios realizados"
    TRANSACTIONS_SUMMARY_TITLE = "Resumo dos Negócios"
    FINANCIAL_SUMMARY_TITLE = "Resumo Financeiro"
    REFERENCE_DATE_TITLE = "Data pregão"
    CI_TITLE = "C.I"
    NET_VALUE_SECTION_TITLE = "Líquido para"

    buy_transaction_indicator_on_brokerage_note = "C"
    sell_transaction_indicator_on_brokerage_note = "V"
    first_column_transactions = "Q"
    transaction_columns_index = {
        "transaction_type": 1,
        "start_short_name": 3,
        "end_short_name": -4,
        "unit_value": -3,
        "amount": -4,
    }
    financial_summary_header_mapper = {
        "Taxa de liquidação": BrokerageNoteFeeType.SETTLEMENT_FEE,
        "Taxa de Registro": BrokerageNoteFeeType.REGISTRATION_FE,
        "Taxa de termo/opções": BrokerageNoteFeeType.TERM_FEE,
        "Taxa A.N.A.": BrokerageNoteFeeType.ANA_FEE,
        "Emolumentos": BrokerageNoteFeeType.EMOLUMENTS,
        "Taxa Operacional": BrokerageNoteFeeType.OPERATIONAL_FEE,
        "Execução": BrokerageNoteFeeType.EXECUTION,
        "Taxa de Custódia": BrokerageNoteFeeType.CUSTODY_FEE,
        "Impostos": BrokerageNoteFeeType.TAXES,
        "Outros": BrokerageNoteFeeType.OTHERS,
    }
    last_transaction_item = "Resumo dos Negócios"

    @classmethod
    def __get_reference_date_from_section(cls, brokerage_note_section: BrokerageNoteSection) -> date:
        return extract_date_from_line(line=brokerage_note_section.full_text)

    def __build_full_width_rectangle(self, *, y_axis_start: int, y_axis_end: int) -> fitz.Rect:
        return fitz.Rect(
            self.BROKERAGE_NOTE_X_AXIS_START_COORDINATE,
            y_axis_start,
            self.BROKERAGE_NOTE_X_AXIS_END_COORDINATE,
            y_axis_end,
        )

    def __is_transactions_header_line(self, line_text: str) -> bool:
        return line_text[: len(self.first_column_transactions)] == self.first_column_transactions

    def __is_transactions_last_line(self, line_text: str) -> bool:
        return line_text[: len(self.last_transaction_item)] == self.last_transaction_item

    def __get_transaction_lines_text_from_words(
        self, transactions_brokerage_note_section: BrokerageNoteSection
    ) -> List[str]:
        transaction_lines_text = []
        can_include_transactions = False
        for transaction_full_line in transactions_brokerage_note_section.text_by_lines:
            if self.__is_transactions_last_line(line_text=transaction_full_line):
                can_include_transactions = False

            if can_include_transactions:
                logging.info("Parsed transaction line: %s", transaction_full_line)
                transaction_lines_text.append(transaction_full_line)

            if self.__is_transactions_header_line(line_text=transaction_full_line):
                can_include_transactions = True

        return transaction_lines_text

    def _get_or_create_brokerage_note_by_page(self, page: TextPage, page_number: int) -> BrokerageNote:
        reference_date_rect = self.fitz_parser.search_and_extract_rectangle_from_text(
            page=page, text=self.REFERENCE_DATE_TITLE
        )
        ci_rect = self.fitz_parser.search_and_extract_rectangle_from_text(page=page, text=self.CI_TITLE)
        brokerage_note_summary_section = self._build_brokerage_note_section_from_two_rectangles(
            first_rectangle=reference_date_rect, second_rectangle=ci_rect, page_number=page_number
        )
        current_reference_date = self.__get_reference_date_from_section(
            brokerage_note_section=brokerage_note_summary_section
        )
        if current_reference_date not in self.brokerage_notes:
            brokerage_note = BrokerageNote(reference_date=current_reference_date)
            self.brokerage_notes[current_reference_date] = brokerage_note
        return self.brokerage_notes[current_reference_date]

    def set_brokerage_note_transactions(self) -> None:
        for page_document in self.fitz_parser.document:  # type:ignore[union-attr]
            page = page_document.get_textpage()
            page_number = page_document.number
            try:
                brokerage_note = self._get_or_create_brokerage_note_by_page(page=page, page_number=page_number)
                transactions_title_rectangle = self.fitz_parser.search_and_extract_rectangle_from_text(
                    page=page, text=self.TRANSACTIONS_SECTION_TITLE
                )
                transactions_summary_title_rectangle = self.fitz_parser.search_and_extract_rectangle_from_text(
                    page=page, text=self.TRANSACTIONS_SUMMARY_TITLE
                )

                rectangle_before_transactions = self.__build_full_width_rectangle(
                    y_axis_start=transactions_title_rectangle.y0,  # pylint:disable=no-member
                    y_axis_end=transactions_title_rectangle.y1,  # pylint:disable=no-member
                )
                rectangle_after_transactions = self.__build_full_width_rectangle(
                    y_axis_start=transactions_summary_title_rectangle.y0,  # pylint:disable=no-member
                    y_axis_end=transactions_summary_title_rectangle.y1,  # pylint:disable=no-member
                )
                transactions_brokerage_note_section = self._build_brokerage_note_section_from_two_rectangles(
                    first_rectangle=rectangle_before_transactions,
                    second_rectangle=rectangle_after_transactions,
                    page_number=page_number,
                )
                transactions = self.__get_transaction_lines_text_from_words(
                    transactions_brokerage_note_section=transactions_brokerage_note_section
                )
                for transaction in transactions:
                    transaction_item = self._create_transaction(line=transaction)
                    brokerage_note.add_transaction(transaction=transaction_item)

            except ProblemParsingBrokerageNoteException:
                continue

    def __build_net_value_title_rectangle(self, page: TextPage) -> fitz.Rect:
        if net_value_title_rectangle := self.fitz_parser.search_and_extract_rectangle_from_text(
            page=page, text=self.NET_VALUE_SECTION_TITLE
        ):
            end_point = (self.BROKERAGE_NOTE_X_AXIS_END_COORDINATE, self.BROKERAGE_NOTE_FINANCIAL_SUMMARY_Y_AXIS_END)
            return self.fitz_parser.build_rectangle_from_beginning_first_rectangle_end_second_rectangle(
                first_rect=net_value_title_rectangle, second_rect=end_point
            )
        return fitz.Rect(
            self.BROKERAGE_NOTE_X_AXIS_START_COORDINATE, self.BROKERAGE_NOTE_FINANCIAL_SUMMARY_Y_AXIS_END, 0, 0
        )

    def set_brokerage_note_fees(self) -> None:
        for page_document in self.fitz_parser.document:  # type:ignore[union-attr]
            page = page_document.get_textpage()
            page_number = page_document.number
            try:
                financial_summary_title_rectangle = self.fitz_parser.search_and_extract_rectangle_from_text(
                    page=page, text=self.FINANCIAL_SUMMARY_TITLE
                )
                net_value_title_rectangle = self.__build_net_value_title_rectangle(page=page)
                financial_summary_brokerage_note_section = self._build_brokerage_note_section_from_two_rectangles(
                    first_rectangle=financial_summary_title_rectangle,
                    second_rectangle=net_value_title_rectangle,
                    page_number=page_number,
                )

                self.__set_brokerage_note_fees(
                    financial_summary_brokerage_note_section=financial_summary_brokerage_note_section,
                    page=page,
                    page_number=page_number,
                )

            except ProblemParsingBrokerageNoteException:
                continue

    def __set_brokerage_note_fees(
        self, financial_summary_brokerage_note_section: BrokerageNoteSection, page: fitz.TextPage, page_number: int
    ) -> None:
        for line in financial_summary_brokerage_note_section.text_by_lines:
            self.__parse_brokerage_note_fee_from_summary_line(
                financial_summary_line=line, page=page, page_number=page_number
            )

    def __parse_brokerage_note_fee_from_summary_line(
        self, financial_summary_line: str, page: fitz.TextPage, page_number: int
    ) -> None:
        for header, brokerage_note_fee_type in self.financial_summary_header_mapper.items():
            line_header_value = financial_summary_line[: len(header)]
            if line_header_value == header:
                brokerage_note = self._get_or_create_brokerage_note_by_page(page=page, page_number=page_number)
                brokerage_note.update_fee_from_fee_type(
                    fee_type=brokerage_note_fee_type, fee_value=extract_value_from_line(line=financial_summary_line)
                )
