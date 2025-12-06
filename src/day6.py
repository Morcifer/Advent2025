import logging
import math

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 6

ParsedType = list[str | int]


def parser(s: list[str]) -> ParsedType:
    # Gotta filter extra whitespace because of the weird formatting
    s = [x for x in s if x != ""]

    if s[0] == "+" or s[0] == "*":
        return s

    return [int(x) for x in s]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    result = 0

    for column in range(len(data[0])):
        match data[-1][column]:
            case "+":
                result += sum([x[column] for x in data[:-1]])
            case "*":
                result += math.prod([x[column] for x in data[:-1]])

    return result


def do_nasty_magic(data: list[str]) -> int:
    result = 0

    operators_row = data[-1]
    number_rows = data[:-1]

    operator_locations = [column for column in range(len(operators_row)) if operators_row[column] != " "]

    for operator_index in range(len(operator_locations)):
        numbers_to_operate = []

        start_column = operator_locations[operator_index]
        end_column = (
            operator_locations[operator_index + 1] - 1
            if operator_index < len(operator_locations) - 1
            else max(len(number_row) for number_row in number_rows)
        )

        for column in range(start_column, end_column):
            number_string = [number_row[column] for number_row in number_rows if len(number_row) > column]
            numbers_to_operate.append(int("".join(number_string)))

        match operators_row[operator_locations[operator_index]]:
            case "+":
                result += sum(numbers_to_operate)
            case "*":
                result += math.prod(numbers_to_operate)

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser=None, data_folder="data", strip=False, is_test=is_test)
    return do_nasty_magic(data)
