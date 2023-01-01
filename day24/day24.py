from dataclasses import dataclass
import os
from typing import Set, Tuple


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"

PLAYER_MOVEMENT = ((1, 0), (0, 1), (-1, 0), (0, -1), (0, 0))


@dataclass
class Blizzard:
    x: int
    y: int
    # 0: right, 1: left, 2: up, 3: down
    dir: int


class Map:
    _blizzard: Set[Tuple[int, int, int, int]]
    _walls: Set[Tuple[int, int]]
    _max_height: int
    _max_width: int

    def __init__(
        self,
        blizzard: Set[Tuple[int, int, int, int]],
        walls: Set[Tuple[int, int]],
        max_height: int,
        max_width: int,
    ):
        self._blizzard = blizzard
        self._walls = walls
        self._max_height = max_height
        self._max_width = max_width

    def traverse(
        self,
        start_time: int,
        is_beginning: bool,
    ) -> int:
        start = (0, -1)
        exit = (self._max_width - 1, self._max_height)
        queue = {start if is_beginning else exit}
        end_goal = exit if is_beginning else start
        curr_time = start_time
        while True:
            curr_time += 1
            blizzard_state = {
                (
                    (px + curr_time * dx) % self._max_width,
                    (py + curr_time * dy) % self._max_height,
                )
                for (px, py, dx, dy) in self._blizzard
            }

            next_positions = {
                (px + dx if px + dx >= -1 else px, py + dy if py + dy >= -1 else py)
                for dx, dy in PLAYER_MOVEMENT
                for px, py in queue
            }
            queue = next_positions - blizzard_state - self._walls

            if end_goal in queue:
                return curr_time


def get_map(file_name: str) -> Map:
    with open(file_name, "r") as file:
        data = file.read()

    lines = data.split("\n")
    blizzard = set()
    walls = set()

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == ".":
                continue

            if lines[i][j] == "#":
                walls.add((j - 1, i - 1))
                continue

            if lines[i][j] == ">":
                blizzard.add((j - 1, i - 1, +1, 0))
            elif lines[i][j] == "<":
                blizzard.add((j - 1, i - 1, -1, 0))
            elif lines[i][j] == "^":
                blizzard.add((j - 1, i - 1, 0, -1))
            else:
                blizzard.add((j - 1, i - 1, 0, +1))

    return Map(
        blizzard=blizzard,
        walls=walls,
        max_height=max(y for x, y in walls),
        max_width=max(x for x, y in walls),
    )


def solve_part_1(file_name: str):
    map = get_map(file_name)
    time = map.traverse(
        start_time=0,
        is_beginning=True,
    )
    print(f"Final Time: {time}")


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
