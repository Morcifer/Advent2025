import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 5

ParsedType = tuple[int, int] | int | None


def parser(s: list[str]) -> ParsedType:
    s = s[0]

    if s == "":
        return None

    if "-" not in s:
        return int(s)

    range_ = s.split("-")
    return int(range_[0]), int(range_[1])


def do_magic(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:  # pylint: disable=unused-argument
    result = 0

    for ingredient in ingredients:
        for range_ in ranges:
            if range_[0] <= ingredient <= range_[1]:
                result += 1
                break

    return result


def find_range_overlap(ranges: list[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]] | None:
    for i1, range_1 in enumerate(ranges):
        for range_2 in ranges[i1 + 1 :]:
            if range_1[1] < range_2[0] or range_2[1] < range_1[0]:
                continue

            return range_1, range_2

    return None


def do_other_magic(ranges: list[tuple[int, int]]) -> int:  # pylint: disable=unused-argument
    # The number of ranges is small enough that switching to a set for the removals
    # doesn't speed it up enough to compensate for the overlap search method being twice as slow,
    # plus the extra set overhead.
    overlapping_ranges = find_range_overlap(ranges)

    while overlapping_ranges is not None:
        range_1, range_2 = overlapping_ranges
        new_range = min(range_1[0], range_2[0]), max(range_1[1], range_2[1])

        ranges.remove(range_1)
        ranges.remove(range_2)
        ranges.append(new_range)

        overlapping_ranges = find_range_overlap(ranges)

    return sum((range_[1] - range_[0] + 1 for range_ in ranges))


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    split_index = data.index(None)
    return do_magic(data[:split_index], data[split_index + 1 :])


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    split_index = data.index(None)
    return do_other_magic(data[:split_index])
