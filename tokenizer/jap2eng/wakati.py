import MeCab
import re

from tokenizer.base import BaseTokenizer


def get_tokens(sentence):
    global wakati
    return wakati.parse(sentence).split()


class WakatiTokenizer(BaseTokenizer):
    def __init__(self):
        super().__init__()
        self.wakati = MeCab.Tagger("-Owakati")

    def tokenize_base_language(self, sentence):
        return self.wakati.parse(sentence).split()

    def tokenize_reference_language(self, sentence):
        # solution from
        # https://stackoverflow.com/questions/50786841/regex-split-sentence-in-words-and-symbols-with-exceptions
        return re.findall(r"\w+|[^\w\s]", sentence, re.UNICODE)
