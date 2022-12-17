from dataclasses import dataclass
from typing import List
from typing_extensions import TypedDict

FILE_NAME = "input.txt"

@dataclass(frozen=True)
class Rucksacks():
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
        similar = set(rucksack.first).intersection(rucksack.second)

        value = ord(next(iter(similar))) - ord('a') + 1
        if value <= 0:
            value += 58
        result += value

    print(result)


# nasty class
@dataclass(frozen=True)
class Group(Rucksacks):
    third: str

class GroupService:
    @staticmethod
    def find_badge_value(group: Group) -> int:
        common = set(group.first).intersection(group.second).intersection(group.third)
        value = ord(next(iter(common))) - ord('a') + 1

        return value if value > 0 else value + 58


def get_groups(file_name: str) -> List[Group]:
    with open(file_name, "r") as file:
        data = file.read()

    data_lines = data.split("\n")

    assert len(data_lines) % 3 == 0 # group has to contain 3 rucksacks 

    groups = []
    for i in range(0, len(data_lines), 3):
        groups.append(
            Group(
                first=data_lines[i],
                second=data_lines[i+1],
                third=data_lines[i+2],
            )
        )

    return groups

def solve_part_2():
    groups = get_groups(FILE_NAME)

    result = 0
    for group in groups:
        badge_value = GroupService.find_badge_value(group)
        result += badge_value
    
    print(result)


if __name__ == "__main__":
    solve_part_2()
