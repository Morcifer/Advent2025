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


def invalid_ids_doubles(start, end) -> list[int]:
    result = []

    for _id in range(start, end + 1):
        string_id = str(_id)
        length = len(string_id) // 2
        pattern = string_id[0:length]
        times = 2

        if pattern * times == string_id:
            result.append(_id)

    return result


def invalid_ids_all(start, end) -> list[int]:
    result = []

    for _id in range(start, end + 1):
        string_id = str(_id)

        for length in range(1, len(string_id) // 2 + 1):
            pattern = string_id[0:length]
            times = len(string_id) // length

            if times * len(pattern) != len(string_id):
                continue

            if pattern * times == string_id:
                result.append(_id)
                break

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)[0]
    return sum(flatten([invalid_ids_doubles(*t) for t in data]))


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)[0]
    return sum(flatten([invalid_ids_all(*t) for t in data]))
