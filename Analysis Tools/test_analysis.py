from _utils_ import corpus_extraction as ce


PATH1 = '/home/brunobrocai/Desktop/Code/moralization/Testfiles/test_gerichtsurteile_DE.xmi'
PATH2 = '/home/brunobrocai/Desktop/Code/moralization/Testfiles/test_plenar_FR.xmi'


def test_corpus():
    testc = ce.Corpus(PATH1)
    assert 1 == 1


def test_bigcorpus():
    testc = ce.Corpus([PATH1, PATH2])
    tests = ce.SubCorpus(PATH1)
    concat = testc.concat_annos("obj_morals")
    assert len(tests.obj_morals) < len(concat)
