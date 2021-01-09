import MeCab
import requests

wakati = MeCab.Tagger("-Owakati")


def get_tokens(sentence):
    global wakati
    return wakati.parse(sentence).split()


class Jisho(object):
    def __init__(self):
        self.url = 'https://jisho.org/api/v1/search/words?keyword='

    def query_word(self, word):
        req = requests.get(self.url + word)
        content = req.content