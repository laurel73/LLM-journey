from bank import value


def test_number():
    assert value("3") == 100


def test_punctuation():
    assert value(",") == 100


def test_letter():
    assert value("hello") == 0
    assert value("h") == 20
