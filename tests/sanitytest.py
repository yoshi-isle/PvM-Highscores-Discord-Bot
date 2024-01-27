import pytest


def test_sanity():
    assert True == True


@pytest.mark.parametrize(
    "number, expected", [(2, True), (3, False), (4, True), (5, False)]
)
def test_is_even(number, expected):
    assert (number % 2 == 0) == expected
