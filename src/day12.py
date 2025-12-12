import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 12

ParsedType = tuple[int, set[tuple[int, int]]] | list[tuple[tuple[int, int]], dict[int, int]]


def parser(s: list[str]) -> ParsedType:
    if "x" not in s[0][0]:  # This is a present
        present_spots = set()
        for row_index, row in enumerate(s[1:-1]):
            for column_index, char in enumerate(row[0]):
                if char != "#":
                    continue

                present_spots.add((row_index, column_index))

        return int(s[0][0][:-1]), present_spots

    # This is the areas
    areas = []
    for row in s:
        width, height = [int(x) for x in row[0][:-1].split("x")]
        presents_needed = {present: int(amount) for present, amount in enumerate(row[1:]) if amount != "0" }
        areas.append(((width, height), presents_needed))

    return areas

def do_magic(data1: list[ParsedType], data2: ParsedType) -> int:  # pylint: disable=unused-argument
    return -1


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    present_shapes = data[:-1]
    areas = data[-1]

    return do_magic(present_shapes, areas)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    present_shapes = data[:-1]
    areas = data[-1]

    return do_magic(present_shapes, areas)
