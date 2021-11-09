import pytest


def cap_case(word: str) -> str:
    if not isinstance(word, str):
        raise TypeError("please provide a string argument")
    return word.capitalize()


@pytest.fixture(scope='module')
def test_cap_case():
    assert cap_case("toto") == "TOTO"


def test_raises_exception_on_non_string_arguments():
    with pytest.raises(TypeError):
        cap_case(9)
