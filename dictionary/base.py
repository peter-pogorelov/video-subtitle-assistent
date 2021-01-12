import typing


class BaseDictionary(object):
    def __init__(self):
        pass

    def find_from_base_language(self, word):
        raise NotImplementedError()

    def find_from_reference_language(self, word):
        raise NotImplementedError()

    def to_table(self, response: list):
        pass
