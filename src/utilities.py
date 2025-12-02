import os
from itertools import chain
from typing import TypeVar, Callable

import requests


ResultTypeT = TypeVar("ResultTypeT")


YEAR = 2025

AOC_TOKEN = os.getenv("AOC_TOKEN")

if AOC_TOKEN is None:
    raise ValueError("You need to export the AOC_TOKEN environment variable")


def get_data(
    day: int,
    data_folder: str,
    is_test: bool,
) -> list[str]:
    file_path = os.path.join(
        "..",
        data_folder,
        "test" if is_test else "real",
        f"day{day}.txt",
    )

    if os.path.isfile(file_path):
        with open(file_path, encoding="utf-8") as f:
            content = f.readlines()

        return content

    # Download from AoC website, but only for the real data.
    if is_test:
        with open(file_path, "x", encoding="utf-8"):
            raise AssertionError("Test data has not been put inside the file!")

    url = f"https://adventofcode.com/{YEAR}/day/{day}/input"
    response = requests.get(url, headers={"Cookie": AOC_TOKEN}, timeout=5)
    content = response.content.decode("utf-8")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.content.decode("utf-8"))

    # Split by newline, and then get rid of the last one if it's empty
    result = content.split("\n")
    return result if result[-1].strip() != "" else result[:-1]


def load_data(
    day: int,
    parser: Callable[[list[str]], ResultTypeT] | Callable[[list[list[str]]], ResultTypeT],
    data_folder: str,
    is_test: bool,
    strip: bool = True,
    cluster_at_empty_line: bool = False,
) -> list[ResultTypeT]:
    content = get_data(day, data_folder, is_test)

    content = [x.strip() if strip else x.replace("\n", "") for x in content]

    parsed_data = []
    cluster = []

    for line_number, line in enumerate(content):
        s = line.split(" ") if strip else line
        if not cluster_at_empty_line:
            parsed_data.append(parser(s))
            continue

        cluster.append(s)

        if line == "" or line_number == len(content) - 1:
            parsed_data.append(parser(cluster))
            cluster = []

    return parsed_data


def load_data_un_parsed(
    day: int,
    data_folder: str,
    is_test: bool,
) -> list[str]:
    content = get_data(day, data_folder, is_test)

    list(content)


def flatten(sequence):
    return list(chain(*sequence))
