import pytest

from src.day5 import part_1, part_2


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 3), (1, False, 821), (2, True, 14), (2, False, 344771884978261)],
)
def test_actual(part, is_test, expected_result):
    method = part_1 if part == 1 else part_2
    assert method(is_test) == expected_result
