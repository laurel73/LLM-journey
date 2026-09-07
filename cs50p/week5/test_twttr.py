from twttr import shorten


def test_count():
    assert shorten('3') == '3'


def test_punctuation():
    assert shorten(',') == ','


def test_letter():
    assert shorten('a') == ''
    assert shorten('A') == ''
    assert shorten('g') == 'g'
