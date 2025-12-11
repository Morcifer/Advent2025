import functools
import logging
from collections import defaultdict

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 11

ParsedType = tuple[str, list[str]]


def parser(s: list[str]) -> ParsedType:
    return s[0][:-1], s[1:]


def get_node_depths(data: list[ParsedType], start_point: str) -> dict[str, int]:
    # TODO: might need to make sure you take the max distance, not the min.
    nodes_by_depths = defaultdict(set)

    edges = dict(data)

    queue = [(start_point, 0)]
    explored = set()

    while len(queue) > 0:
        current, depth = queue.pop(0)

        if current in explored:
            continue

        nodes_by_depths[depth].add(current)
        explored.add(current)

        for connected in edges.get(current, []):
            queue.append((connected, depth + 1))

    depths = {}

    for level, nodes in nodes_by_depths.items():
        for node in nodes:
            depths[node] = level

    return depths


def do_recursive_magic(
    data: list[ParsedType],
    start_point: str,
    end_point: str,
    _depths: dict[str, int],
) -> int:  # pylint: disable=unused-argument
    # TODO: use the depths, even though it already solves quickly.
    edges = dict(data)

    @functools.lru_cache(maxsize=None)
    def do_recursion(start: str):
        if start == end_point:
            return 1

        result = 0
        for connected in edges.get(start, []):
            result += do_recursion(connected)
        return result

    return do_recursion(start_point)


def do_hyper_magic(data: list[ParsedType]):
    depths = get_node_depths(data, "svr")

    dac_level = depths["dac"]
    fft_level = depths["fft"]

    if dac_level < fft_level:
        svr_dac = do_recursive_magic(data, start_point="svr", end_point="dac", _depths=depths)
        dac_fft = do_recursive_magic(data, start_point="dac", end_point="fft", _depths=depths)
        fft_out = do_recursive_magic(data, start_point="fft", end_point="out", _depths=depths)

        return svr_dac * dac_fft * fft_out

    svr_fft = do_recursive_magic(data, start_point="svr", end_point="fft", _depths=depths)
    fft_dac = do_recursive_magic(data, start_point="fft", end_point="dac", _depths=depths)
    dac_out = do_recursive_magic(data, start_point="dac", end_point="out", _depths=depths)

    return svr_fft * fft_dac * dac_out


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    depths = get_node_depths(data, "svr")

    return do_recursive_magic(data, start_point="svr" if is_test else "you", end_point="out", _depths=depths)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_hyper_magic(data)
