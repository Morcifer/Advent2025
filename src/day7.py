import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 7

ParsedType = list[chr]


def parser(s: list[str]) -> ParsedType:
    return list(s[0])


def print_tachyon_manifold(manifold: list[ParsedType], beam_columns_per_row: list[set[int]]):
    for row in manifold:
        print(''.join(row))


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    beam_columns_per_row = []
    splits = 0

    for row_index, row in enumerate(data):
        if row_index == 0:
            beam_columns_per_row.append({row.index("S")})
            continue

        relevant_row_set = set()
        beam_columns_per_row.append(relevant_row_set)

        for beam_column in beam_columns_per_row[row_index - 1]:
            if row[beam_column] == "^":
                splits += 1
                relevant_row_set.add(beam_column - 1)
                relevant_row_set.add(beam_column + 1)
            else:
                relevant_row_set.add(beam_column)

    return splits


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    # print_tachyon_manifold(data, [])
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
