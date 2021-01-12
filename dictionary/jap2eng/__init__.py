import typing

from dictionary.base import BaseDictionary


class JapaneseEnglishWord:
    kanji: str = ''
    kana: str = ''
    pos: str = ''
    english: str = ''


def word_remainder(response, query):
    return set(list(response)).difference(list(query))


class BaseJapEngDictionary(BaseDictionary):
    def __init__(self):
        super().__init__()

    @staticmethod
    def sort_japanese_search_result(word: str, results: typing.Iterable[JapaneseEnglishWord]) \
            -> typing.List[JapaneseEnglishWord]:
        return sorted(results, key=lambda x:
            min(abs(len(word_remainder(x.kana, word))), abs(len(word_remainder(x.kanji, word)))))

    @staticmethod
    def sort_english_search_result(word: str, results: typing.Iterable[JapaneseEnglishWord]) \
            -> typing.List[JapaneseEnglishWord]:
        return sorted(results, key=lambda x: abs(len(x.english) - len(word)))

    def to_table(self, response: typing.List[JapaneseEnglishWord]):
        return [['Kanji', 'Kana', 'English', 'POS']] + []

    def find_from_base_language(self, word) -> typing.List[JapaneseEnglishWord]:
        raise NotImplementedError()

    def find_from_reference_language(self, word) -> typing.List[JapaneseEnglishWord]:
        raise NotImplementedError()
