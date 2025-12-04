import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 4

ParsedType = list[chr]


def parser(s: list[str]) -> ParsedType:
    return list(s[0])


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


def calculate_adjacents(data: list[ParsedType]) -> dict[tuple[int, int], int]:
    height = len(data)
    width = len(data[0])

    adjacents = {}

    for row in range(height):
        for column in range(width):
            if data[row][column] != "@":
                continue

            adjacents[(row, column)] = 0

            for delta in neighbour_deltas:
                (neighbour_row, neighbour_column) = (row + delta[0], column + delta[1])

                if neighbour_row < 0 or neighbour_row >= height or neighbour_column < 0 or neighbour_column >= width:
                    continue

                if data[neighbour_row][neighbour_column] == "@":
                    adjacents[(row, column)] += 1

    return adjacents


def do_magic_once(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    adjacents = calculate_adjacents(data)
    accessible = [key for key, value in adjacents.items() if value < 4]

    for roll in accessible:
        data[roll[0]][roll[1]] = "x"

    return len(accessible)


def do_magic_efficiently_once(
    data: list[ParsedType],
    adjacents: dict[tuple[int, int], int] = None,
) -> tuple[dict[tuple[int, int], int], int]:  # pylint: disable=unused-argument
    height = len(data)
    width = len(data[0])

    if adjacents is None:
        adjacents = calculate_adjacents(data)

    rolls_to_remove = [key for key, value in adjacents.items() if value < 4]

    for roll_to_remove in rolls_to_remove:
        data[roll_to_remove[0]][roll_to_remove[1]] = "x"
        adjacents.pop(roll_to_remove)

        for delta in neighbour_deltas:
            neighbour = (roll_to_remove[0] + delta[0], roll_to_remove[1] + delta[1])

            if neighbour[0] < 0 or neighbour[0] >= height or neighbour[1] < 0 or neighbour[1] >= width:
                continue

            if neighbour in adjacents:
                adjacents[neighbour] -= 1

    return adjacents, len(rolls_to_remove)


def do_magic(data: list[ParsedType], once: bool) -> int:
    removed = do_magic_once(data)
    result = removed

    if once:
        return result

    while removed != 0:
        logger.info("Still removing, result is %(result)s", {"result": result})
        removed = do_magic_once(data)
        result += removed

    return result


def do_magic_efficiently(data: list[ParsedType], once: bool) -> int:
    adjacents, removed = do_magic_efficiently_once(data)
    result = removed

    if once:
        return result

    while removed != 0:
        logger.info("Still removing, result is %(result)s", {"result": result})
        adjacents, removed = do_magic_efficiently_once(data, adjacents)
        result += removed

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic_efficiently(data, once=True)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic_efficiently(data, once=False)
