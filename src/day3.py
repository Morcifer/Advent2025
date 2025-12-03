import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 3

ParsedType = list[int]


# TODO: Why is the input a list of strings and not just a string, again?
def parser(s: list[str]) -> ParsedType:
    return [int(c) for c in s[0]]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    return -1


def calculate_joltage(datum: ParsedType) -> int:
    max_joltage = 0

    for i, first in enumerate(datum):
        for second in datum[i + 1 :]:
            max_joltage = max(max_joltage, first * 10 + second)

    return max_joltage


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return sum((calculate_joltage(datum) for datum in data))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
