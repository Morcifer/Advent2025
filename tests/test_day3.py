import pytest

from src.day3 import part_1, part_2


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 357), (1, False, 17229), (2, True, 3121910778619), (2, False, 170520923035051)],
)
def test_actual(part, is_test, expected_result):
    method = part_1 if part == 1 else part_2
    assert method(is_test) == expected_result
