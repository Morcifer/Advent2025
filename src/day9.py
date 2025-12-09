import logging

from src.utilities import load_data, chain2

logger = logging.getLogger(__name__)


DAY = 9

ParsedType = tuple[int, int]


def parser(s: list[str]) -> ParsedType:
    values = [int(x) for x in s[0].split(",")]
    return values[0], values[1]


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    max_size = 0
    for tile_1 in data:
        for tile_2 in data:
            height = abs(tile_1[0] - tile_2[0]) + 1
            width = abs(tile_1[1] - tile_2[1]) + 1
            max_size = max(max_size, height * width)

    return max_size


def flood_fill(tiles: list[list[chr]], start: tuple[int, int]):
    neighbour_deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    queue = [start]

    while len(queue) > 0:
        n = queue.pop(0)
        if tiles[n[1]][n[0]] == "X":
            continue

        tiles[n[1]][n[0]] = "X"
        for dx, dy in neighbour_deltas:
            new_x = n[0] + dx
            new_y = n[1] + dy
            queue.append((new_x, new_y))


def do_other_magic(data: list[ParsedType]) -> int:
    xs = {x: i for i, x in enumerate(sorted({datum[0] for datum in data}))}
    ys = {y: i for i, y in enumerate(sorted({datum[1] for datum in data}))}

    tiles = [["."] * len(xs) for _ in range(len(ys))]

    # Do green edges, including closing the shape
    for tile_1, tile_2 in chain2(data + data[0:1]):
        # TODO: clean this if-else, it's ugly
        if tile_1[1] == tile_2[1]:  # y is the same, iterate over x
            start = min(tile_1[0], tile_2[0])
            end = max(tile_1[0], tile_2[0])

            for x in range(start, end + 1):
                if x in xs:
                    tiles[ys[tile_1[1]]][xs[x]] = "X"
        else:  # x is the same, iterate over y
            start = min(tile_1[1], tile_2[1])
            end = max(tile_1[1], tile_2[1])

            for y in range(start, end + 1):
                if y in ys:
                    tiles[ys[y]][xs[tile_1[0]]] = "X"

    # Flood-fill for additional green tiles
    # TODO: figure out a generic way to find a good starting point.
    starting_point = (2, 1) if len(xs) < 10 else (120, 2)
    flood_fill(tiles, starting_point)

    # Override the red tiles
    for tile in data:
        tiles[ys[tile[1]]][xs[tile[0]]] = "#"

    # Draw whatever this is
    for row in tiles:
        print("".join(row))

    # Now do greedy
    max_size = 0
    for tile_1 in data:
        for tile_2 in data:
            height = abs(tile_1[0] - tile_2[0]) + 1
            width = abs(tile_1[1] - tile_2[1]) + 1

            tile_1_condensed_x = xs[tile_1[0]]
            tile_1_condensed_y = ys[tile_1[1]]

            tile_2_condensed_x = xs[tile_2[0]]
            tile_2_condensed_y = ys[tile_2[1]]

            x_start = min(tile_1_condensed_x, tile_2_condensed_x)
            y_start = min(tile_1_condensed_y, tile_2_condensed_y)

            x_end = max(tile_1_condensed_x, tile_2_condensed_x)
            y_end = max(tile_1_condensed_y, tile_2_condensed_y)

            is_valid = True

            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    is_valid = is_valid and tiles[y][x] != "."

            if is_valid:
                max_size = max(max_size, height * width)

    return max_size


def do_cheating_magic(data: list[ParsedType]) -> int:
    from shapely.geometry import Polygon

    polya = Polygon(data)

    max_size = 0
    for tile_1 in data:
        for tile_2 in data:
            polyb = Polygon([tile_1, (tile_2[0], tile_1[1]), tile_2, (tile_1[0], tile_2[1])])

            height = abs(tile_1[0] - tile_2[0]) + 1
            width = abs(tile_1[1] - tile_2[1]) + 1

            if polya.contains(polyb):
                max_size = max(max_size, height * width)

    return max_size


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_other_magic(data)
