import pathlib
import typing

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, or_
from sqlalchemy.orm import sessionmaker

from dictionary.jap2eng import BaseJapEngDictionary, JapaneseEnglishWord

Base = declarative_base()
Session = sessionmaker()


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = Column(Integer, primary_key=True, unique=True)
    entry_id = Column(String, unique=True)
    kana = Column(String)
    kanji = Column(String)
    pos = Column(String)
    misc = Column(String)
    gloss = Column(String)
    lang = Column(String)

    def get_kanji(self):
        return self.kanji

    def get_kana(self):
        return self.kana

    def get_pos(self):
        return self.pos.split('^')

    def get_gloss(self):
        return self.gloss.split('^')


class JMDict(BaseJapEngDictionary):
    def __init__(self, jmdb_path: pathlib.Path):
        super().__init__()

        global Session
        self.jmdict_engine = create_engine('sqlite://' + str(jmdb_path), echo=False)
        assert self.jmdict_engine is not None
        Session.configure(bind=self.jmdict_engine)

    def _make_word(self, record: Warehouse) -> JapaneseEnglishWord:
        word = JapaneseEnglishWord()
        word.kanji = record.get_kanji()
        word.kana = record.get_kana()
        word.pos = record.get_pos()[0]
        word.english = record.get_gloss()[0]
        return word

    def find_from_base_language(self, word: str) -> typing.List[JapaneseEnglishWord]:
        global Session
        session = Session()
        result = session.query(Warehouse).filter(
            or_(Warehouse.kana.contains(word), Warehouse.kanji.contains(word))
        ).all()
        session.close()
        if result:
            return BaseJapEngDictionary.sort_japanese_search_result(word, map(self._make_word, result))
        return []

    def find_from_reference_language(self, word: str) -> typing.List[JapaneseEnglishWord]:
        global Session
        session = Session()
        result = session.query(Warehouse).filter(Warehouse.gloss.contains(word)).all()
        session.close()
        if result:
            return BaseJapEngDictionary.sort_english_search_result(word, map(self._make_word, result))
        return []
