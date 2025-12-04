import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 4

ParsedType = str


def parser(s: list[str]) -> ParsedType:
    return s[0]


neighbour_deltas = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    height = len(data)
    width = len(data[0])

    accessible = []

    for row in range(height):
        for column in range(width):
            if data[row][column] != '@':
                continue

            adjacent = 0

            for delta in neighbour_deltas:
                (neighbour_row, neighbour_column) = (row + delta[0], column + delta[1])

                if neighbour_row < 0 or neighbour_row >= height or neighbour_column < 0 or neighbour_column >= width:
                    continue

                if data[neighbour_row][neighbour_column] == '@':
                    adjacent += 1

            if adjacent < 4:
                accessible.append((row, column))

    return len(accessible)


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
