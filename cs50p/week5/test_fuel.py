from fuel import convert, gauge
import pytest


def test_convert():
    assert convert("3/4") == 75
    assert convert("1/3") == 33


def test_gauge():
    assert gauge(1) == "E"
    assert gauge(99) == "F"
    assert gauge(50) == "50%"


def test_x_greater():
    with pytest.raises(ValueError):
        convert("5/4")


def test_bad_format():
    with pytest.raises(ValueError):
        convert("oo")


def test_zero():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")
