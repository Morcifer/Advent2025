from src.utilities import load_data

DAY = 1


def parser(s: list[str]) -> tuple[chr, int]:
    value = s[0]
    return value[0], int(value[1:])


def do_magic(data: list[tuple[chr, int]]) -> int:
    result = 0

    current = 50
    for (c, i) in data:
        match c:
            case "R":
                current += i
            case "L":
                current -= i

        while current > 99:
            current = current - 100

        while current < 0:
            current = current + 100

        if current == 0:
            result += 1

        print(f"Rotation {(c, i)} got to {current}")

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return -1


if __name__ == "__main__":
    is_test = False
    print(f"Day {DAY} result 1: {part_1(is_test)}")
    print(f"Day {DAY} result 2: {part_2(is_test)}")
