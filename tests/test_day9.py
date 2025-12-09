import pytest

from src.day9 import part_1, part_2


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 50), (1, False, 4741848414), (2, True, 24), (2, False, 1508918480)],
)
def test_actual(part, is_test, expected_result):
    method = part_1 if part == 1 else part_2
    assert method(is_test) == expected_result
