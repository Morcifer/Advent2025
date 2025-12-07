import logging
from collections import defaultdict

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 7

ParsedType = list[chr]


def parser(s: list[str]) -> ParsedType:
    return list(s[0])


def print_tachyon_manifold(manifold: list[ParsedType], beam_columns_and_timelines_per_row: list[dict[int, int]]):
    for row in manifold:
        print(''.join(row))


def do_magic(data: list[ParsedType]) -> tuple[int, int]:  # pylint: disable=unused-argument
    beam_columns_and_timelines_per_row = []
    splits = 0

    for row_index, row in enumerate(data):
        if row_index == 0:
            beam_columns_and_timelines_per_row.append({row.index("S"): 1})
            continue

        relevant_row_dictionary = defaultdict(int)
        beam_columns_and_timelines_per_row.append(relevant_row_dictionary)

        for (beam_column, timelines) in beam_columns_and_timelines_per_row[row_index - 1].items():
            if row[beam_column] == "^":
                splits += 1
                relevant_row_dictionary[beam_column - 1] += timelines
                relevant_row_dictionary[beam_column + 1] += timelines
            else:
                relevant_row_dictionary[beam_column] += timelines

    return splits, sum(beam_columns_and_timelines_per_row[-1].values())


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    # print_tachyon_manifold(data, [])
    return do_magic(data)[0]


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)[1]
