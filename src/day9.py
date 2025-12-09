import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 9

ParsedType = tuple[int, int]


def parser(s: list[str]) -> ParsedType:
    values = [int(x) for x in s[0].split(",")]
    return values[0], values[1]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    max_size = 0
    for tile_1 in data:
        for tile_2 in data:
            height = abs(tile_1[0] - tile_2[0] + 1)
            width = abs(tile_1[1] - tile_2[1] + 1)
            max_size = max(max_size, height * width)

    return max_size


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
