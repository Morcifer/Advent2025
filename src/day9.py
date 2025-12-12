import logging
from itertools import pairwise

from src.utilities import load_data

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


# pylint: disable=too-many-branches
def do_other_magic(data: list[ParsedType]) -> int:
    xs = {x: i for i, x in enumerate(sorted({datum[0] for datum in data}))}
    ys = {y: i for i, y in enumerate(sorted({datum[1] for datum in data}))}

    tiles = [["."] * len(xs) for _ in range(len(ys))]

    # Do green edges, including closing the shape
    for tile_1, tile_2 in pairwise(data + data[0:1]):
        if tile_1[1] == tile_2[1]:  # y is the same, iterate over x
            start, end = sorted((tile_1[0], tile_2[0]))

            for x in range(start, end + 1):
                if x in xs:
                    tiles[ys[tile_1[1]]][xs[x]] = "X"
        else:  # x is the same, iterate over y
            start, end = sorted((tile_1[1], tile_2[1]))

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
    for tile_1_index, tile_1 in enumerate(data):
        for tile_2 in data[tile_1_index + 1 :]:
            height = abs(tile_1[0] - tile_2[0]) + 1
            width = abs(tile_1[1] - tile_2[1]) + 1

            tile_1_condensed_x = xs[tile_1[0]]
            tile_1_condensed_y = ys[tile_1[1]]

            tile_2_condensed_x = xs[tile_2[0]]
            tile_2_condensed_y = ys[tile_2[1]]

            x_start, x_end = sorted((tile_1_condensed_x, tile_2_condensed_x))
            y_start, y_end = sorted((tile_1_condensed_y, tile_2_condensed_y))

            is_valid = True

            for x in range(x_start, x_end + 1):
                for y in range(y_start, y_end + 1):
                    is_valid = is_valid and tiles[y][x] != "."

            if is_valid:
                max_size = max(max_size, height * width)

    return max_size


def do_other_magic_more_simply(data: list[ParsedType]) -> int:
    # It's enough to check that there's no tile inside the shape (other than the ones currently checked).
    #  no need for the fancy floodfill hubbub.
    # However, this method isn't actually much faster, though I don't completely understand why.
    max_size = 0
    for tile_1_index, tile_1 in enumerate(data):
        for tile_2 in data[tile_1_index + 1 :]:
            min_x, max_x = sorted((tile_1[0], tile_2[0]))
            min_y, max_y = sorted((tile_1[1], tile_2[1]))

            rectangle_in_polygon = True

            for line_start, line_end in pairwise(data + data[0:1]):
                min_line_x, max_line_x = sorted((line_start[0], line_end[0]))
                min_line_y, max_line_y = sorted((line_start[1], line_end[1]))

                if (min_x < max_line_x and min_line_x < max_x) and (min_y < max_line_y and min_line_y < max_y):
                    rectangle_in_polygon = False
                    break

            if not rectangle_in_polygon:
                continue

            height = (max_y - min_y) + 1
            width = (max_x - min_x) + 1

            max_size = max(max_size, height * width)

    return max_size


# pylint: disable=import-outside-toplevel
def do_cheating_magic(data: list[ParsedType]) -> int:
    from shapely.geometry import Polygon

    polya = Polygon(data)

    max_size = 0
    for tile_1_index, tile_1 in enumerate(data):
        for tile_2 in data[tile_1_index + 1 :]:
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
