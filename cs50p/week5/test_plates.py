from plates import is_valid


def test_digit_start():
    assert is_valid('36008') == False


def test_punctuation():
    assert is_valid('csjan,') == False


def test_valid_letters():
    assert is_valid('Hggoo') == True
    assert is_valid('hello') == True


def test_zero_lead():
    assert is_valid('gh032') == False
    assert is_valid('CS50') == True
    assert is_valid('CS50P') == False
    assert is_valid('123ABC') == False
