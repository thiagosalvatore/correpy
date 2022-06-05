from dataclasses import dataclass, field
from typing import Iterable, List

from correpy.parsers.brokerage_notes.word_rectangle import WordRectangle


@dataclass
class BrokerageNoteSection:
    words_grouped_by_line: Iterable[Iterable[WordRectangle]] = field(default_factory=list)

    @staticmethod
    def get_text_line_from_list_of_words(*, words: Iterable[WordRectangle]) -> List[str]:
        return [word.value for word in words]

    @property
    def text_by_lines(self) -> List[str]:
        return [self.get_text_from_words(words=words) for words in self.words_grouped_by_line]

    def get_text_from_words(self, words: Iterable[WordRectangle]) -> str:
        line = self.get_text_line_from_list_of_words(words=words)
        return " ".join(line)

    @property
    def full_text(self) -> str:
        return "".join(self.get_text_from_words(words=words) for words in self.words_grouped_by_line)
