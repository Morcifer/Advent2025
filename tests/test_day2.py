import pytest

from src.day2 import part_1, part_2


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 1227775554), (1, False, 38158151648), (2, True, 4174379265), (2, False, 45283684555)],
)
def test_actual(part, is_test, expected_result):
    method = part_1 if part == 1 else part_2
    assert method(is_test) == expected_result
