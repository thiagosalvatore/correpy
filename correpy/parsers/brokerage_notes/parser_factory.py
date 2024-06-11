"""
    parser_factory.py
    ~~~~~~~~~
    :copyright: (c) 2024 by Alby
"""
import io
from typing import Optional, List

from correpy.domain.entities.brokerage_note import BrokerageNote
from correpy.parsers.brokerage_notes.b3_parser.b3_parser import B3Parser
from correpy.parsers.brokerage_notes.base_parser import BaseBrokerageNoteParser
from correpy.parsers.brokerage_notes.nuinvest_parser.nuinvest import NuInvestParser
from correpy.parsers.brokerage_notes.inter_parser.inter import InterParser
from correpy.parsers.fitz_parser import FitzParser


class ParserFactory:
    CNPJ_PARSER_MAP = {
        "62.169.875/0001-79": NuInvestParser,
        "18.945.670/0001-46": InterParser
    }

    def __init__(self, brokerage_note: io.BytesIO, password: Optional[str] = None):
        self.__brokerage_note = brokerage_note
        self.__password = password

    def get_parser(self) -> BaseBrokerageNoteParser:
        fitz_parser = FitzParser(file=self.__brokerage_note, password=self.__password)

        for cnpj, parser in self.CNPJ_PARSER_MAP.items():
            if fitz_parser.is_text_in_document(text=cnpj):
                return parser(brokerage_note=self.__brokerage_note, password=self.__password)

        return B3Parser(brokerage_note=self.__brokerage_note, password=self.__password)

    def parse(self) -> List[BrokerageNote]:
        parser = self.get_parser()

        return parser.parse_brokerage_note()
