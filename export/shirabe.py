import pathlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

#db.execute('insert into d (i, p, n, s, l, x, q) values (62, 8, "test", 0, 1, 5, "5DPhbCLdHBLhAADQ1BCwpB")')


class Folder(Base):
    __tablename__ = 'f'

    id = Column(name='i', type=Integer, autoincrement=True, unique=True, primary_key=True)
    parent = Column(name='p', type=Integer)
    name = Column(name='n', type=String)
    _unknown1 = Column(name='s', type=Integer)
    _unknown2 = Column(name='l', type=Integer)
    _unknown3 = Column(name='x', type=Integer)
    rhash = Column(name='q', type=String)

#insert into b (i,f,t,k,l,p,x) values (485, 62, 0, 1273720, 1, "公算", 0


class Word(Base):
    __tablename__ = 'b'

    id = Column(name='i', type=Integer, autoincrement=True, unique=True, primary_key=True)
    folder = Column(name='f', type=ForeignKey('f.p'))
    _unknown1 = Column(name='t', type=Integer)
    jmdict_id = Column(name='k', type=Integer)
    order = Column(name='l', type=Integer) # dunno how to make a rule
    name = Column(name='p', type=String)
    _unknown2 = Column(name='x', type=Integer)


#class ShirabeJishoExporter(object):
#    def __init__(self, bookmarks_path: pathlib.Path, ):
