import logging
import sys

from src.day10 import part_1, part_2, DAY


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s: %(message)s",
)


def part(part_number: int, is_test: bool) -> int:
    method = part_1 if part_number == 1 else part_2
    return method(is_test)


if __name__ == "__main__":
    print(f"Day {DAY} result 1 test: {part(1, is_test=True)}")
    print(f"Day {DAY} result 1 real: {part(1, is_test=False)}")

    print(f"Day {DAY} result 2 test: {part(2, is_test=True)}")
    print(f"Day {DAY} result 2 real: {part(2, is_test=False)}")
