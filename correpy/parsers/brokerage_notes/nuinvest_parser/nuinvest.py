import logging
from typing import List

from correpy.domain.enums import BrokerageNoteFeeType
from correpy.parsers.brokerage_notes.b3_parser.b3_parser import B3Parser
from correpy.parsers.brokerage_notes.brokerage_note_section import BrokerageNoteSection


class NuInvestParser(B3Parser):
    REFERENCE_NOTE_ID = "Número da nota"
    CI_TITLE = "Valor/Ajuste D/C"
    TRANSACTIONS_SECTION_TITLE = "Nome do Cliente"
    TRANSACTIONS_SUMMARY_TITLE = "Resumo dos Negócios"
    first_column_transactions = "Mercado"
    last_transaction_item = "BOVESPA"

    financial_summary_header_mapper = {
        "Taxa de Liquidação": BrokerageNoteFeeType.SETTLEMENT_FEE,
        "Taxa de Registro": BrokerageNoteFeeType.REGISTRATION_FE,
        "Taxa de Termo / Opções": BrokerageNoteFeeType.TERM_FEE,
        "Taxa A.N.A.": BrokerageNoteFeeType.ANA_FEE,
        "Emolumentos": BrokerageNoteFeeType.EMOLUMENTS,
        "Taxa Operacional": BrokerageNoteFeeType.OPERATIONAL_FEE,
        "Execução": BrokerageNoteFeeType.EXECUTION,
        "Taxa de Custódia": BrokerageNoteFeeType.CUSTODY_FEE,
        "Impostos": BrokerageNoteFeeType.TAXES,
        "Outros": BrokerageNoteFeeType.OTHERS,
    }

    def __is_transactions_line(self, line_text: str) -> bool:
        """checks whether the row of data represents an asset transaction."""
        return line_text[: len(self.last_transaction_item)] == self.last_transaction_item

    def _get_transaction_lines_text_from_words(
        self, transactions_brokerage_note_section: BrokerageNoteSection
    ) -> List[str]:
        transaction_lines_text = []
        can_include_transactions = False
        for transaction_full_line in transactions_brokerage_note_section.text_by_lines:
            if not self.__is_transactions_line(line_text=transaction_full_line):
                can_include_transactions = False

            if can_include_transactions:
                logging.info("Parsed transaction line: %s", transaction_full_line)
                transaction_lines_text.append(transaction_full_line)

            if self._is_transactions_header_line(line_text=transaction_full_line):
                can_include_transactions = True

        return transaction_lines_text
