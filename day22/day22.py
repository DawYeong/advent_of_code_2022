from dataclasses import dataclass
from operator import attrgetter
import os
from typing import List, Optional, Tuple, Union


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


@dataclass
class Position:
    x: int
    y: int
    is_wall: Optional[bool] = None

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return False


class Map:
    positions: List[Position]
    instructions: List[Union[str, int]]
    _curr_direction: int  # 0: right, 1: down, 2: left, 3: up

    def __init__(self, positions: List[Position], instructions: List[Union[str, int]]):
        self.positions = positions
        self.instructions = instructions
        self._curr_direction = 0

    def traverse(self) -> Tuple[Position, int]:
        curr_pos = Position(x=self.positions[0].x, y=self.positions[0].y)

        for instruction in self.instructions:
            if isinstance(instruction, int):
                relevant_positions = (
                    [
                        position
                        for position in self.positions
                        if curr_pos.y == position.y
                    ]
                    if (self._curr_direction == 0 or self._curr_direction == 2)
                    else [
                        position
                        for position in self.positions
                        if curr_pos.x == position.x
                    ]
                )
                move_unit = (
                    1 if self._curr_direction == 0 or self._curr_direction == 1 else -1
                )
                for _ in range(instruction):
                    if self._curr_direction == 0 or self._curr_direction == 2:
                        next_pos = (curr_pos.x + move_unit, curr_pos.y)
                    else:
                        next_pos = (curr_pos.x, curr_pos.y + move_unit)

                    if next_pos not in relevant_positions:
                        # out of bounds => move them back
                        if self._curr_direction == 0:
                            # reached past right bound
                            wrap_around_pos = min(
                                relevant_positions, key=attrgetter("x")
                            )
                        elif self._curr_direction == 1:
                            # reached past down bound
                            wrap_around_pos = min(
                                relevant_positions, key=attrgetter("y")
                            )
                        elif self._curr_direction == 2:
                            # reached past left bound
                            wrap_around_pos = max(
                                relevant_positions, key=attrgetter("x")
                            )
                        else:
                            # reached past up bound
                            wrap_around_pos = max(
                                relevant_positions, key=attrgetter("y")
                            )

                        if wrap_around_pos.is_wall:
                            break

                        curr_pos.x = wrap_around_pos.x
                        curr_pos.y = wrap_around_pos.y
                        continue

                    if relevant_positions[relevant_positions.index(next_pos)].is_wall:
                        break

                    curr_pos.x = next_pos[0]
                    curr_pos.y = next_pos[1]
            else:
                # direction
                if instruction == "R":
                    # clockwise rotation
                    self._curr_direction = (self._curr_direction + 1) % 4
                else:
                    # counter-clockwise
                    self._curr_direction = (self._curr_direction - 1) % 4

        return curr_pos, self._curr_direction


def get_map(file_name: str) -> Map:
    with open(file_name, "r") as file:
        data = file.read()

    path, instructions = data.split("\n\n")
    positions = []
    for i, row in enumerate(path.split("\n")):
        for j, col in enumerate(row):
            if col == " ":
                continue
            position = Position(x=j + 1, y=i + 1)
            if col == ".":
                position.is_wall = False
            else:
                position.is_wall = True
            positions.append(position)

    insns = []
    num = ""
    for i in instructions:
        if not i.isnumeric():
            insns.append(int(num))
            insns.append(i)
            num = ""
        else:
            num += i
    insns.append(int(num))

    map = Map(positions=positions, instructions=insns)
    return map


def solve_part_1(file_name: str):
    map = get_map(file_name)
    end_pos, dir = map.traverse()
    password = 1000 * end_pos.y + 4 * end_pos.x + dir
    print(f"Final password: {password}")


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
