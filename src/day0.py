import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 0

ParsedType = str


def parser(s: list[str]) -> ParsedType:
    return s[0]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    return -1


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
