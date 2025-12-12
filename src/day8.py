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


class DisjointSet:
    def __init__(self, node_count: int):
        self.parents = list(range(node_count))
        self.sets = {n: {n} for n in range(node_count)}
        self.length = node_count

    def find_set(self, v: int) -> int:
        # The performance of this can be improved by updating the parent of v with the result of find_set,
        # to reduce the recursion in the next iterations.
        # But I'm not going to bother.
        if v == self.parents[v]:
            return v

        return self.find_set(self.parents[v])

    def union_sets(self, element_1: int, element_2: int):
        # The performance of this can be improved by making sure the smaller tree is put on the root of the larger.
        #  But I'm not going to bother.
        parent_1 = self.find_set(element_1)
        parent_2 = self.find_set(element_2)

        if parent_1 == parent_2:
            return

        set_1 = self.sets[parent_1]
        set_2 = self.sets[parent_2]

        new_set = set_1.union(set_2)

        logger.info(
            "Removed %(set_1)s and %(set_2)s to make %(new_set)s",
            {"set_1": set_1, "set_2": set_2, "new_set": new_set},
        )

        self.parents[parent_2] = parent_1

        self.sets.pop(parent_1)
        self.sets.pop(parent_2)

        self.sets[parent_1] = new_set

    def __len__(self) -> int:
        return len(self.sets)


class Forest:
    def __init__(self, data: list[ParsedType]):
        self.nodes = data
        self.distances = {}

        for node_1_id, node_1 in enumerate(self.nodes):
            for node_2_id, node_2 in enumerate(self.nodes):
                if node_1_id >= node_2_id:
                    continue

                self.distances[(node_1_id, node_2_id)] = euclidean_distance(node_1, node_2)

        self.pairs_by_distance = [pair for pair, _ in sorted(self.distances.items(), key=lambda kvp: kvp[1])]


def do_magic(data: list[ParsedType], connections: int) -> int:  # pylint: disable=unused-argument
    forest = Forest(data)
    disjoint_set = DisjointSet(len(forest.nodes))

    connection = 1

    while connection < connections:
        connection += 1

        closest_tuple = forest.pairs_by_distance[connection]

        # Find sets the two elements of the tuple belong to
        disjoint_set.union_sets(*closest_tuple)

        if len(disjoint_set) == 1:
            box_1 = forest.nodes[closest_tuple[0]]
            box_2 = forest.nodes[closest_tuple[1]]
            return box_1[0] * box_2[0]

    longest_set_sizes = sorted([len(s) for s in disjoint_set.sets.values()])

    return math.prod(longest_set_sizes[-3:])


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, 10 if is_test else 1000)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, float("inf"))
