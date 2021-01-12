import typing


class BaseTokenizer(object):
    def __init__(self):
        pass

    def tokenize_base_language(self, word):
        raise NotImplementedError()

    def tokenize_reference_language(self, word):
        raise NotImplementedError()
