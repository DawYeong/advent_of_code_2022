from dataclasses import dataclass
from typing import List

FILE_NAME = "input.txt"


@dataclass(frozen=True)
class Section:
    start: int
    end: int


@dataclass(frozen=True)
class Pair:
    first: Section
    second: Section

    @staticmethod
    def from_raw_data(data: str) -> "Pair":
        raw_pairs = [raw_section.split("-") for raw_section in data.split(",")]

        assert len(raw_pairs) == 2
        assert len(raw_pairs[0]) == 2
        assert len(raw_pairs[1]) == 2

        return Pair(
            first=Section(
                start=int(raw_pairs[0][0]),
                end=int(raw_pairs[0][1]),
            ),
            second=Section(
                start=int(raw_pairs[1][0]),
                end=int(raw_pairs[1][1]),
            ),
        )


class PairService:
    @staticmethod
    def is_overlap(pair: Pair) -> bool:
        return (
            pair.first.start <= pair.second.start and pair.first.end >= pair.second.end
        ) or (
            pair.second.start <= pair.first.start and pair.second.end >= pair.first.end
        )


def get_pairs(file_name: str) -> List[Pair]:
    with open(file_name, "r") as file:
        data = file.read()

    data_lines = data.split("\n")
    pairings = [Pair.from_raw_data(pair) for pair in data_lines]

    return pairings


def solve_part_1(file_name: str):
    pairs = get_pairs(file_name)

    result = 0
    for pair in pairs:
        if PairService.is_overlap(pair):
            result += 1
    
    print(result)


if __name__ == "__main__":
    solve_part_1(FILE_NAME)
