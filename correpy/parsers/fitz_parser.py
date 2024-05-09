import io
import typing
from typing import List, Optional, Union

import fitz
from fitz import Document, TextPage

from correpy.parsers.brokerage_notes.word_rectangle import WordRectangle
from correpy.parsers.exceptions import InvalidPasswordException, ProblemParsingBrokerageNoteException


class FitzParser:
    def __init__(self, file: io.BytesIO, password: Optional[str]) -> None:
        self.document: Optional[Document] = None
        self.words: List[List[WordRectangle]] = []

        self.__parse(file=file, password=password)

    @classmethod
    def build_rectangle_from_beginning_first_rectangle_end_second_rectangle(
        cls, first_rect: fitz.Rect, second_rect: fitz.Rect
    ) -> fitz.Rect:
        return first_rect | second_rect

    @classmethod
    def is_word_in_rectangle(cls, *, rectangle: fitz.Rect, word: WordRectangle) -> bool:
        return typing.cast(bool, fitz.Rect(word.x0, word.y0, word.x1, word.y1).intersects(rectangle))

    @classmethod
    def search_and_extract_rectangle_from_text(cls, *, page: TextPage, text: Union[str, List[str]]) -> fitz.Rect:
        if isinstance(text, str):
            text = [text]
        for value in text:  # multi-text search
            if quadrilateral_position := page.search(value):
                break
        else:
            quadrilateral_position = None
        if not quadrilateral_position:
            raise ProblemParsingBrokerageNoteException
        return quadrilateral_position[0].rect

    def get_words_in_rectangle(self, *, page_number: int, rectangle: fitz.Rect) -> List[WordRectangle]:
        return [word for word in self.words[page_number] if self.is_word_in_rectangle(rectangle=rectangle, word=word)]

    def __parse(self, *, file: io.BytesIO, password: Optional[str]) -> None:
        doc: Document = fitz.open(stream=file, filetype="pdf")
        authenticated = doc.authenticate(password)
        if not authenticated:
            raise InvalidPasswordException

        self.document = doc
        self.__read_pages_and_words_from_pages()

    def __read_pages_and_words_from_pages(self) -> None:
        for page in self.document:  # type:ignore[union-attr]
            text_page = page.get_textpage()
            self.words.append(self.__parse_fitz_word_tuple_to_word_object(text_page))

    @staticmethod
    def __parse_fitz_word_tuple_to_word_object(text_page: fitz.TextPage) -> List[WordRectangle]:
        extracted_words = text_page.extractWORDS()
        return [WordRectangle(word[0], word[1], word[2], word[3], word[4]) for word in extracted_words]

    def is_text_in_document(self, *, text: str) -> bool:
        for page_document in self.document:
            if page_document.get_textpage().search(text):
                return True
        return False
