from dictionary.jap2eng.jmdict import JMDict

if __name__ == '__main__':
    jmdict = JMDict('/database/test.db')
    result = jmdict.find_from_base_language('える')

    for i in result:
        print(i.kana)
        print(i.kanji)
        print(i.english)
        print(i.pos)