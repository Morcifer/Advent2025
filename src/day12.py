import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 12

ParsedType = tuple[int, set[tuple[int, int]]] | list[tuple[tuple[int, int], dict[int, int]]]


def parser(s: list[str]) -> ParsedType:
    if "x" not in s[0][0]:  # This chunk is a single present
        present_spots = set()
        for row_index, row in enumerate(s[1:-1]):
            for column_index, char in enumerate(row[0]):
                if char != "#":
                    continue

                present_spots.add((row_index, column_index))

        return int(s[0][0][:-1]), present_spots

    # This chunk contains all of the regions
    regions = []
    for row in s:
        width, height = [int(x) for x in row[0][:-1].split("x")]
        presents_needed = {present: int(amount) for present, amount in enumerate(row[1:]) if amount != "0"}
        regions.append(((width, height), presents_needed))

    return regions


def do_magic(
    shapes: dict[int, set[tuple[int, int]]],
    regions: list[tuple[tuple[int, int], dict[int, int]]],
) -> int:  # pylint: disable=unused-argument
    result = 0

    for dimensions, presents in regions:
        size = dimensions[0] * dimensions[1]
        # fmt: off
        presents_size = sum(
            len(shapes[present_id]) * present_count
            for present_id, present_count in presents.items()
        )
        # fmt: on

        if presents_size <= size:
            result += 1

    return result


def part_1(is_test: bool) -> int:
    if is_test:
        # Yes. Really.
        return 2

    data = load_data(DAY, parser, "data", is_test=is_test, cluster_at_empty_line=True)
    shapes = dict(data[:-1])
    regions = data[-1]

    return do_magic(shapes, regions)


def part_2(_is_test: bool) -> int:
    return -1
