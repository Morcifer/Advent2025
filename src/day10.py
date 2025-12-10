import logging
import math

import numpy as np
import scipy.optimize as opt

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 10

ParsedType = tuple[list[chr], list[set[int]], list[int]]


def parser(s: list[str]) -> ParsedType:
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    lights = list(s[0][1:-1])
    buttons = []
    joltages = [int(x) for x in s[-1][1:-1].split(",")]

    for substring in s[1:-1]:
        buttons.append({int(x) for x in substring[1:-1].split(",")})

    return lights, buttons, joltages


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    result = 0

    for lights, buttons, _ in data:
        # BFS your way to christmas.
        # This algorithm assumes nothing needs to end completely off. Let's make sure.
        assert lights != ["."] * len(lights)

        explored = set()

        queue = [(["."] * len(lights), button, 0) for button in range(len(buttons))]

        while len(queue) > 0:
            to_explore_current_lights, to_explore_button_to_press, pressed_buttons = queue.pop(0)

            for button in buttons[to_explore_button_to_press]:
                if to_explore_current_lights[button] == ".":
                    to_explore_current_lights[button] = "#"
                else:
                    to_explore_current_lights[button] = "."

            if to_explore_current_lights == lights:
                result += pressed_buttons + 1
                break

            if "".join(to_explore_current_lights) in explored:
                continue

            explored.add("".join(to_explore_current_lights))

            for button in range(len(buttons)):
                queue.append((to_explore_current_lights[:], button, pressed_buttons + 1))

    return result


def do_linear_algebra_magic(data: list[ParsedType], part: int) -> int:
    result = 0

    for index, (lights, buttons, joltages) in enumerate(data):
        logger.info(
            "Handling row %(index)s out of %(total)s (joltages: %(joltages)s, total result is currently %(result)s",
            {"index": index, "total": len(data), "joltages": joltages, "result": result},
        )

        matrix = np.array(
            [[1 if location in button_list else 0 for location in range(len(joltages))] for button_list in buttons]
        ).transpose()

        # TODO: For this to work in part 1, we need to somehow introduce a modulo here, so allowing the target to have
        #  + [2, 2, 2, 2] - meaning having len(lights) extra parameters, but possibly no extra constraints.
        # TODO: Alternatively, or maybe in addition, try to avoid using the milp solver, even if it means implementing
        #  your own branch-and-bound solver.
        target = (
            np.array([0 if lights[location] == "." else 1 for location in range(len(lights))])
            if part == 1
            else np.array(joltages)
        )

        solution = opt.milp(
            c=np.ones(len(buttons)),
            bounds=opt.Bounds(lb=0, ub=1 if part == 1 else max(joltages)),
            constraints=opt.LinearConstraint(matrix, lb=target, ub=target),
            integrality=np.ones(len(buttons)),
        )

        result += math.ceil(solution.fun)

    return result


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_linear_algebra_magic(data, 2)
