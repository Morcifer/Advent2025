import pytest

from src.day8 import part_1, part_2


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 40), (1, False, 121770), (2, True, 25272), (2, False, 7893123992)],
)
def test_actual(part, is_test, expected_result):
    method = part_1 if part == 1 else part_2
    assert method(is_test) == expected_result
