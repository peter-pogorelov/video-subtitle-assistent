import MeCab
import requests
import json
import typing

from dictionary.jap2eng import JapaneseEnglishWord, BaseJapEngDictionary


class Jisho(BaseJapEngDictionary):
    def __init__(self):
        super().__init__()

        self.url = 'https://jisho.org/api/v1/search/words?keyword='

    def __query_word(self, word) -> dict:
        req = requests.get(self.url + word)
        return json.loads(req.content)

    def __parse_record(self, recdata: dict) -> JapaneseEnglishWord:
        record = JapaneseEnglishWord()

        if 'japanese' not in recdata.keys() or not recdata['japanese']:
            return record

        japanese = recdata['japanese'][0]
        if 'word' in japanese:
            record.kanji = japanese['word']
        if 'reading' in japanese:
            record.kana = japanese['reading']

        if 'senses' not in recdata.keys() or not recdata['senses']:
            return record

        senses = recdata['senses'][0]

        if 'english_definitions' in senses and senses['english_definitions']:
            record.english = senses['english_definitions'][0]

        if 'parts_of_speech' in senses and senses['parts_of_speech']:
            record.pos = senses['parts_of_speech'][0]

        return record

    def find_from_base_language(self, word) -> typing.List[JapaneseEnglishWord]:
        wordlist = self.__query_word(word)['data']
        result = list()
        for record in wordlist:
            result.append(self.__parse_record(record))
        return result

    def find_from_reference_language(self, word) -> typing.List[JapaneseEnglishWord]:
        # searching interface in jisho.org is symmetric
        return self.find_from_base_language(word)
