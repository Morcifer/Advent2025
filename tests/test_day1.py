import pytest

from src import day1


@pytest.mark.parametrize(
    "part, is_test, expected_result",
    [(1, True, 3), (1, False, 1031), (2, True, 6), (2, False, 5831)],
)
def test_actual(part, is_test, expected_result):
    assert day1.part(part, is_test) == expected_result
