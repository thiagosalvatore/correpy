import io
from unittest.mock import create_autospec, patch, MagicMock

import fitz
import pytest

from correpy.parsers.brokerage_notes.word_rectangle import WordRectangle
from correpy.parsers.exceptions import InvalidPasswordException, ProblemParsingBrokerageNoteException
from correpy.parsers.fitz_parser import FitzParser


class TestConnectBankAccount:
    def setup_method(self):
        self.brokerage_note = io.BytesIO(b"abcde")
        self.document_mock = MagicMock()
        self.page_mock = create_autospec(fitz.Page)
        self.text_page_mock = create_autospec(fitz.TextPage)
        self.document_mock.__iter__ = lambda _: iter([self.page_mock])
        self.document_mock.__next__.side_effect = StopIteration
        self.document_mock.authenticate.return_value = True
        self.page_mock.get_textpage.return_value = self.text_page_mock

        self.patcher = patch("correpy.parsers.fitz_parser.fitz.open")
        self.fitz_open_mock = self.patcher.start()
        self.fitz_open_mock.return_value = self.document_mock

    def teardown_method(self):
        self.patcher.stop()

    def test_initialize_fitz_parser_when_called_with_invalid_password_then_raises_invalid_password_exception(self):
        self.document_mock.authenticate.return_value = None

        with pytest.raises(InvalidPasswordException):
            FitzParser(file=self.brokerage_note, password="wrong")

    def test_initialize_fitz_parser_when_called_with_valid_data_then_sets_instance_document_same_as_document_returned_by_open(
        self,
    ):
        fitz_parser = FitzParser(file=self.brokerage_note, password="123")

        assert fitz_parser.document == self.document_mock

    def test_initialize_fitz_parser_when_called_with_valid_data_then_calls_page_get_text_page(self):
        FitzParser(file=self.brokerage_note, password="123")

        self.page_mock.get_textpage.assert_called()

    def test_initialize_fitz_parser_when_called_with_valid_data_then_calls_text_page_extract_words(self):
        FitzParser(file=self.brokerage_note, password="123")

        self.text_page_mock.extractWORDS.assert_called()

    def test_initialize_fitz_parser_when_called_with_valid_data_then_append_words_from_text_page_using_word_rectangle_object(
        self,
    ):
        word_rectangle_text_page = (0, 0, 1, 1, "test")
        self.text_page_mock.extractWORDS.return_value = [word_rectangle_text_page]
        expected_words = [
            WordRectangle(
                x0=word_rectangle_text_page[0],
                y0=word_rectangle_text_page[1],
                x1=word_rectangle_text_page[2],
                y1=word_rectangle_text_page[3],
                value=word_rectangle_text_page[4],
            )
        ]

        fitz_parser = FitzParser(file=self.brokerage_note, password="123")

        assert fitz_parser.words == [expected_words]

    def test_is_word_in_rectangle_when_called_with_rectangle_surrounding_word_then_returns_true(self):
        word = WordRectangle(x0=1, y0=1, x1=2, y1=2, value="test")
        surrounding_rectangle = fitz.Rect(0, 0, 3, 3)

        is_in_rectangle = FitzParser.is_word_in_rectangle(rectangle=surrounding_rectangle, word=word)

        assert is_in_rectangle is True

    def test_is_word_in_rectangle_when_called_without_rectangle_surrounding_word_then_returns_false(self):
        word = WordRectangle(x0=1, y0=1, x1=2, y1=2, value="test")
        surrounding_rectangle = fitz.Rect(-1, -1, 0, 0)

        is_in_rectangle = FitzParser.is_word_in_rectangle(rectangle=surrounding_rectangle, word=word)

        assert is_in_rectangle is False

    def test_get_words_in_rectangle_when_called_with_rectangle_surrounding_words_then_returns_all_words(self):
        word_rectangle_text_page = (1, 1, 2, 2, "test")
        surrounding_rectangle = fitz.Rect(0, 0, 3, 3)
        self.text_page_mock.extractWORDS.return_value = [word_rectangle_text_page]

        fitz_parser = FitzParser(file=self.brokerage_note, password="123")

        result = fitz_parser.get_words_in_rectangle(page_number=0, rectangle=surrounding_rectangle)

        assert result == [word_rectangle_text_page]

    def test_get_words_in_rectangle_when_called_without_rectangle_surrounding_words_then_returns_empty_list(self):
        word_rectangle_text_page = (1, 1, 2, 2, "test")
        surrounding_rectangle = fitz.Rect(-1, -1, 0, 0)
        self.text_page_mock.extractWORDS.return_value = [word_rectangle_text_page]

        fitz_parser = FitzParser(file=self.brokerage_note, password="123")

        result = fitz_parser.get_words_in_rectangle(page_number=0, rectangle=surrounding_rectangle)

        assert result == []

    def test_build_rectangle_from_beginning_first_rectangle_end_second_rectangle_when_called_then_returns_x0_y0_first_rectangle_x1_y1_second_rectangle(
        self,
    ):
        first_rectangle = fitz.Rect(1, 1, 2, 2)
        second_rectangle = fitz.Rect(3, 3, 4, 4)
        expected_rectangle = fitz.Rect(1, 1, 4, 4)

        result = FitzParser.build_rectangle_from_beginning_first_rectangle_end_second_rectangle(
            first_rect=first_rectangle, second_rect=second_rectangle
        )

        assert result == expected_rectangle

    def test_search_and_extract_rectangle_from_text_when_called_with_text_in_rectangle_then_returns_rectangle_containing_text(
        self,
    ):
        quad_containing_text = fitz.Quad()
        expected_result = quad_containing_text.rect
        self.text_page_mock.search.return_value = [quad_containing_text]

        rectangle_result = FitzParser.search_and_extract_rectangle_from_text(page=self.text_page_mock, text="test")

        assert rectangle_result == expected_result

    def test_search_and_extract_rectangle_from_text_when_called_with_text_not_in_rectangle_then_raises_problem_parsing_brokerage_note_exception(
        self,
    ):
        self.text_page_mock.search.return_value = None

        with pytest.raises(ProblemParsingBrokerageNoteException):
            FitzParser.search_and_extract_rectangle_from_text(page=self.text_page_mock, text="test")
