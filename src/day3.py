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


def recalculate_joltage(datum: list[int], start_index: int, remaining_digits: int) -> int:
    if remaining_digits == 1:
        return max(datum[start_index:])

    max_joltage = max(datum[start_index : -remaining_digits + 1])
    max_joltage_index = datum.index(max_joltage, start_index)

    result = max_joltage * 10 ** (remaining_digits - 1) + recalculate_joltage(
        datum, max_joltage_index + 1, remaining_digits - 1
    )

    logger.debug(
        "%(result)s for %(datum)s from %(start_index)s with %(remaining_digits)s remaining digits "
        "because max joltage is %(max_joltage)s and it's at index %(max_joltage_index)s",
        {
            "result": result,
            "datum": datum,
            "start_index": start_index,
            "remaining_digits": remaining_digits,
            "max_joltage": max_joltage,
            "max_joltage_index": max_joltage_index,
        },
    )

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return sum((recalculate_joltage(datum, 0, 2) for datum in data))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return sum((recalculate_joltage(datum, 0, 12) for datum in data))
