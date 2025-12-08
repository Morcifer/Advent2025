import pytest

from src.day6 import part_1, part_2


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 4277556), (1, False, 4722948564882), (2, True, 3263827), (2, False, 9581313737063)],
)
def test_actual(part, is_test, expected_result):
    method = part_1 if part == 1 else part_2
    assert method(is_test) == expected_result
