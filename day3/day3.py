from typing import List, Tuple
from typing_extensions import TypedDict

FILE_NAME = "input.txt"

class Rucksacks(TypedDict):
    first: str
    second: str


def get_rucksacks(file_name: str) -> List[Rucksacks]:
    with open(file_name, "r") as file:
        data = file.read()

    data_lines = data.split("\n")

    all_rucksacks = [
        Rucksacks(
            first=data_line[0 : int(len(data_line) / 2)],
            second=data_line[int(len(data_line) / 2) : len(data_line)],
        )
        for data_line in data_lines
    ]

    return all_rucksacks


def solve_part_1():
    rucksacks = get_rucksacks(FILE_NAME)
    result = 0
    
    for rucksack in rucksacks:
        similar = set(rucksack["first"]).intersection(rucksack["second"])

        value = ord(next(iter(similar))) - ord('a') + 1
        if value <= 0:
            value += 58
        result += value

    print(result)


if __name__ == "__main__":
    solve_part_1()
