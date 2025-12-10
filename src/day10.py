import logging

from src.utilities import load_data

logger = logging.getLogger(__name__)


DAY = 10

ParsedType = tuple[list[chr], list[tuple], list[int]]


def parser(s: list[str]) -> ParsedType:
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    lights = list(s[0][1:-1])
    buttons = []
    joltages = [int(x) for x in s[-1][1:-1].split(",")]

    for substring in s[1:-1]:
        buttons.append(tuple([int(x) for x in substring[1:-1].split(",")]))

    return lights, buttons, joltages


def do_magic(data: list[ParsedType]) -> int:  # pylint: disable=unused-argument
    result = 0

    for lights, buttons, joltages in data:
        # BFS your way to christmas.
        '''
         1  procedure BFS(G, root) is
         2      let Q be a queue
         3      label root as explored
         4      Q.enqueue(root)
        '''
        # This algorithm assumes nothing needs to end completely off. Let's make sure.
        assert lights != ["."] * len(lights)

        explored = set()

        queue = [
            (["."] * len(lights), button, 0)
            for button in range(len(buttons))
        ]

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


def part_1(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)


def part_2(is_test: bool) -> int:
    data = load_data(DAY, parser, "data", is_test=is_test)
    return do_magic(data)
