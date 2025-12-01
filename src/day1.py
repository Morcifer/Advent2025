from src.utilities import load_data

DAY = 1


def parser(s: list[str]) -> tuple[chr, int]:
    value = s[0]
    return value[0], int(value[1:])


def do_magic(data: list[tuple[chr, int]], collect_200_dollars: bool) -> int:
    result = 0

    current = 50

    for c, i in data:
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

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, collect_200_dollars=False)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data, collect_200_dollars=True)


def part(part_number: int, is_test: bool) -> int:
    method = part_1 if part_number == 1 else part_2
    return method(is_test)


if __name__ == "__main__":
    TEST = False
    print(f"Day {DAY} result 1: {part(1, TEST)}")
    print(f"Day {DAY} result 2: {part(2, TEST)}")
