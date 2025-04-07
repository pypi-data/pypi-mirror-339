import pytest

from src.seqo import SequentialString

@pytest.mark.parametrize("n, s", [
    (0, '0'),
    (99, '\x0c'),
    (100, '00'),
    (441522222595592528221462, 'Hello World!')
])
def test_default_charset(n: int, s: str):
    ss = SequentialString()
    assert ss.get(n) == s
    assert ss.index_of(s) == n


@pytest.mark.parametrize("n, s", [
    (0, 'L'),
    (3, 'LL'),
    (5, 'LV')
])
def test_custom_charset(n: int, s: str):
    ss = SequentialString("LDV")
    assert ss.get(n) == s
    assert ss.index_of(s) == n
