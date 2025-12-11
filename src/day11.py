import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 11

ParsedType = tuple[str, list[str]]


def parser(s: list[str]) -> ParsedType:
    # ccc: ddd eee fff
    return s[0][:-1], s[1:]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    edges = dict(data)

    result = 0

    # Yay, another BFS! Let's hope there's no loop.
    queue = ["you"]

    while len(queue) > 0:
        current = queue.pop(0)

        if current == "out":
            result += 1
            continue

        for connected in edges[current]:
            queue.append(connected)

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
