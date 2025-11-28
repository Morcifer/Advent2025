import os
import requests
from typing import TypeVar, Callable

ResultType = TypeVar("ResultType")


YEAR = 2022

AOC_TOKEN = os.getenv("AOC_TOKEN")

if AOC_TOKEN is None:
    raise ValueError("You need to export the AOC_TOKEN environment variable")


def get_date(
    day: int,
    data_folder: str,
    is_test: bool,
):
    file_path = os.path.join(
        "..",
        data_folder,
        "test" if is_test else "real",
        f"day{day}.txt",
    )

    if os.path.isfile(file_path):
        with open(file_path) as f:
            content = f.readlines()

        return content

    # Download from AoC website, but only for the real data.
    if is_test:
        open(file_path, "x")
        raise AssertionError("Test data has not been put inside the file!")

    url = f"https://adventofcode.com/{YEAR}/day/12/input"
    response = requests.get(url, headers={"Cookie": AOC_TOKEN}, timeout=5)
    content = response.content.decode("utf-8")

    with open(file_path, "w") as f:
        f.write(response.content.decode("utf-8"))

    return content


def load_data(
    day: int,
    parser: Callable[[list[str]], ResultType] | Callable[[list[list[str]]], ResultType],
    data_folder: str,
    is_test: bool,
    do_not_strip: bool = False,
    cluster_at_empty_line: bool = False,
) -> list[ResultType]:
    content = get_date(day, data_folder, is_test)

    content = [x.replace("\n", "") if do_not_strip else x.strip() for x in content]

    parsed_data = []
    cluster = []

    for line_number, line in enumerate(content):
        s = line if do_not_strip else line.split(" ")
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
) -> list[ResultType]:
    content = get_date(day, data_folder, is_test)

    return [x for x in content]
