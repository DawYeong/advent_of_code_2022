from dataclasses import dataclass
import os
from typing import Set

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __gt__(self, other):
        return self.y > other.y


def get_rocks(file_name: str) -> Set[Position]:
    rocks = set()
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break

            positions = [
                list(map(int, pos.split(",")))
                for pos in data_line.replace("\n", "").split(" -> ")
            ]

            # gets all pairs
            for (x1, y1), (x2, y2) in zip(positions, positions[1:]):
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])

                # builds out the horizontal lines
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        rocks.add(
                            Position(
                                x=x,
                                y=y,
                            )
                        )
    return rocks


def drop_sand(
    rocks: Set[Position],
    max_height: int,
    part_2: bool,
) -> bool:
    curr_sand_pos = Position(
        x=500,
        y=0,
    )

    while True:
        check_pos = Position(
            x=curr_sand_pos.x,
            y=curr_sand_pos.y + 1,
        )

        if part_2 and curr_sand_pos.y == (max_height + 1):
            rocks.add(curr_sand_pos)
            return True
        elif not part_2 and curr_sand_pos.y >= max_height:
            return False

        if not check_pos in rocks:
            # not blocked
            curr_sand_pos = check_pos
            continue

        check_pos = Position(
            x=curr_sand_pos.x - 1,
            y=curr_sand_pos.y + 1,
        )
        if not check_pos in rocks:
            curr_sand_pos = check_pos
            continue

        check_pos = Position(
            x=curr_sand_pos.x + 1,
            y=curr_sand_pos.y + 1,
        )
        if not check_pos in rocks:
            curr_sand_pos = check_pos
            continue

        rocks.add(curr_sand_pos)
        return True if curr_sand_pos.y != 0 else False


def simulate_sand(
    rocks: Set[Position],
    part_2: bool,
) -> int:
    sand_added = 0
    max_height = max(rocks).y
    while True:
        # check if anything is directly below
        if drop_sand(
            rocks=rocks,
            max_height=max_height,
            part_2=part_2,
        ):
            sand_added += 1
        else:
            break

    return sand_added + 1 if part_2 else sand_added


def solve_part_1(file_name: str):
    rocks = get_rocks(file_name)
    num_sand = simulate_sand(
        rocks=rocks,
        part_2=False,
    )
    print(num_sand)


def solve_part_2(file_name: str):
    rocks = get_rocks(file_name)
    num_sand = simulate_sand(
        rocks=rocks,
        part_2=True,
    )
    print(num_sand)


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
