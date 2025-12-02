import logging

from src.utilities import load_data, flatten

logger = logging.getLogger(__name__)

DAY = 2

ParsedType = tuple[int, int]


def parser(s: list[str]) -> list[ParsedType]:
    # fmt: off
    return [
        (int(range[0]), int(range[1]))
        for range
        in [r.split("-") for r in s[0].split(",")]
    ]
    # fmt: on


def invalid_ids(start: int, end: int, max_repeats: int | None) -> list[int]:
    result = []

    for _id in range(start, end + 1):
        string_id = str(_id)

        for repeats in range(2, (max_repeats or len(string_id)) + 1):
            length = len(string_id) // repeats

            if repeats * length != len(string_id):
                continue

            pattern = string_id[0:length]

            if pattern * repeats == string_id:
                result.append(_id)
                break

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)[0]
    return sum(flatten([invalid_ids(*t, 2) for t in data]))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)[0]
    return sum(flatten([invalid_ids(*t, None) for t in data]))
