from collections import Counter
from operator import add, sub
import os
from typing import List, Set, Tuple


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
# 0: North, 1: South, 2: West, 3: East
# Round:
# part 1 => figure out which direction to move, if possible => proposed direction
# part 2 => check for any collisions, move in proposed direction if possible, don't move if multiple elves moving there


class Map:
    _elves: Set[Tuple[int, int]]

    def __init__(self, elves: List[Tuple[int, int]]):
        self._elves = elves

    def __str__(self) -> str:
        return f"{self._elves}"

    def get_empty_tiles(self, rounds: int) -> int:
        for x in range(rounds):
            curr_direction = x % 4
            self._update_elves(curr_direction)

        return self._get_map_size() - len(self._elves)

    def get_rounds(self) -> int:
        round = 0
        curr_elves = {}
        while curr_elves != self._elves:
            curr_elves = self._elves
            self._update_elves(round)
            round += 1

        return round

    def _update_elves(self, dir: int) -> Set[Tuple[int, int]]:
        propose = {
            elf: self._check_elf_direction(elf=elf, curr_dir=dir) for elf in self._elves
        }
        move_count = Counter(propose.values())
        elves_moving = {elf for elf in propose if move_count[propose[elf]] == 1}
        elves_still = self._elves - elves_moving
        self._elves = elves_still | {propose[elf] for elf in elves_moving}

    def _check_elf_direction(
        self, elf: Tuple[int, int], curr_dir: int
    ) -> Tuple[int, int]:
        adj = self._elves & {
            (elf[0] - 1, elf[1]),
            (elf[0] + 1, elf[1]),
            (elf[0], elf[1] - 1),
            (elf[0], elf[1] + 1),
            (elf[0] - 1, elf[1] - 1),
            (elf[0] - 1, elf[1] + 1),
            (elf[0] + 1, elf[1] - 1),
            (elf[0] + 1, elf[1] + 1),
        }
        if not adj:
            return elf
        for i in range(4):
            check_dir = DIRS[(curr_dir + i) % 4]
            adj = self._elves & {
                tuple(map(add, elf, check_dir)),
                tuple(map(add, tuple(map(add, elf, check_dir)), check_dir[::-1])),
                tuple(map(sub, tuple(map(add, elf, check_dir)), check_dir[::-1])),
            }
            if not adj:
                return tuple(map(add, elf, check_dir))

        return elf

    def _get_map_size(self):
        x = [elf[0] for elf in self._elves]
        y = [elf[1] for elf in self._elves]
        width = max(x) - min(x) + 1
        length = max(y) - min(y) + 1
        return width * length


def get_map(file_name: str) -> Map:
    with open(file_name, "r") as file:
        data = file.read().split("\n")

    elves = set()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "#":
                elves.add(
                    (
                        j,
                        i,
                    )
                )

    return Map(elves)


def solve_part_1(file_name: str):
    map = get_map(file_name)
    empty_tiles = map.get_empty_tiles(rounds=10)
    print(f"Empty tiles: {empty_tiles}")


def solve_part_1(file_name: str):
    map = get_map(file_name)
    rounds = map.get_rounds()
    print(f"Rounds: {rounds}")


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
