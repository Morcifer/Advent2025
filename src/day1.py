import math

from src.utilities import load_data

DAY = 1

ParsedType = tuple[chr, int]


def parser(s: list[str]) -> ParsedType:
    value = s[0]
    return value[0], int(value[1:])


def visualize(current: int, title: str) -> None:
    scale_ratio = 1.75

    rows = 21
    columns = int(rows * scale_ratio)

    radius = 9

    screen = [[" "] * columns for _ in range(rows)]

    x0 = columns // 2
    y0 = rows // 2

    for mark in range(100):
        angle = (mark / 100.0 - 0.25) * 2.0 * math.pi

        x1 = x0 + int(math.cos(angle) * radius * scale_ratio)
        y1 = y0 + int(math.sin(angle) * radius)

        if mark == 0:
            screen[y1][x1] = "0"
        else:
            screen[y1][x1] = "#"

    angle = (current / 100.0 - 0.25) * 2.0 * math.pi

    for r in range(radius + 1):
        x2 = x0 + int(math.cos(angle) * r * scale_ratio)
        y2 = y0 + int(math.sin(angle) * r)

        if current == 0:
            screen[y2][x2] = "0"
        else:
            screen[y2][x2] = "C"

    print(title)

    for row in screen:
        print("".join(row))


def do_magic(data: list[ParsedType], collect_200_dollars: bool) -> int:
    result = 0
    current = 50

    for c, i in data:
        # visualize(current, f"from {current}, going {c} for {i} clicks, total {result}")

        previous = current
        extra_0s = 0

        while i > 100:
            i -= 100

            if collect_200_dollars:
                extra_0s += 1

        match c:
            case "R":
                current += i
            case "L":
                current -= i

        mod_current = current % 100  # Only in python.

        if collect_200_dollars and mod_current != current and previous != 0:
            extra_0s += 1
        elif mod_current == 0:
            extra_0s += 1

        current = mod_current
        result += extra_0s

        # print(f"Rotation {(c, i)} got from {previous} to {current} with {extra_0s} extra zeros")

    # visualize(current, f"Ending at {current}, total {result}")

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, collect_200_dollars=False)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, collect_200_dollars=True)
