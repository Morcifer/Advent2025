import logging
import math

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 8

ParsedType = tuple[int, int, int]


def parser(s: list[str]) -> ParsedType:
    values = [int(x) for x in s[0].split(",")]
    return values[0], values[1], values[2]


def euclidean_distance(node_1: ParsedType, node_2: ParsedType) -> float:
    dx = node_1[0] - node_2[0]
    dy = node_1[1] - node_2[1]
    dz = node_1[2] - node_2[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)

class Forest:
    def __init__(self, data: list[ParsedType]):
        self.nodes = {i: node for i, node in enumerate(data)}
        self.distances = dict()

        for node_1_id, node_1 in enumerate(data):
            for node_2_id, node_2 in enumerate(data):
                # TODO: Consider only having one entry per pair, depends on part 2
                if node_1_id == node_2_id:
                    continue

                self.distances[(node_1_id, node_2_id)] = euclidean_distance(node_1, node_2)

        self.distances_by_length = [node_tuple for node_tuple in sorted(self.distances.items(), key=lambda kvp: kvp[1])]



def do_magic(data: list[ParsedType], connections: int) -> int:  # pylint: disable=unused-argument
    forest = Forest(data)
    sets = [{n} for n in forest.nodes.keys()]

    for connection in range(connections):
        shortest_tuple = forest.distances_by_length[connection*2][0]

        # Find sets the two belong two
        set_1 = set()
        set_2 = set()

        for s in sets:
            if shortest_tuple[0] in s:
                set_1 = s
            if shortest_tuple[1] in s:
                set_2 = s

        if set_1 == set_2:
            continue

        new_set = set_1.union(set_2)

        sets.remove(set_1)
        sets.remove(set_2)
        sets.append(new_set)

        # print(f"Removed {set_1} and {set_2} to make {new_set}")

    longest_set_sizes = sorted([len(s) for s in sets])

    return math.prod(longest_set_sizes[-3:])


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, 10 if is_test else 1000)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, 10 if is_test else 1000)
