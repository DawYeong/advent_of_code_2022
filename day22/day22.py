from dataclasses import dataclass
from operator import attrgetter
import os
from typing import List, Optional, Tuple, Union

from orientations import ORIENTATION_INPUT, ORIENTATION_TEST

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


@dataclass
class Position:
    x: int
    y: int
    cube_side: Optional[int] = None
    is_wall: Optional[bool] = None

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return False


# utterly disgusting solution, so much hard coding here
class Map:
    positions: List[Position]
    instructions: List[Union[str, int]]
    _curr_direction: int  # 0: right, 1: down, 2: left, 3: up

    def __init__(self, positions: List[Position], instructions: List[Union[str, int]]):
        self.positions = positions
        self.instructions = instructions
        self._curr_direction = 0

    def traverse(self, part_2: bool = False) -> Tuple[Position, int]:
        curr_pos = Position(
            x=self.positions[0].x,
            y=self.positions[0].y,
            cube_side=self.positions[0].cube_side,
        )

        for instruction in self.instructions:
            if isinstance(instruction, int):
                curr_cube_face = curr_pos.cube_side
                if part_2:
                    relevant_positions = [
                        pos for pos in self.positions if pos.cube_side == curr_cube_face
                    ]
                else:
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

                for _ in range(instruction):
                    move_unit = (
                        1
                        if self._curr_direction == 0 or self._curr_direction == 1
                        else -1
                    )
                    if self._curr_direction == 0 or self._curr_direction == 2:
                        next_pos = (curr_pos.x + move_unit, curr_pos.y)
                    else:
                        next_pos = (curr_pos.x, curr_pos.y + move_unit)
                    if next_pos not in relevant_positions:
                        # out of bounds => move them back
                        filter_position = (
                            max(relevant_positions, key=attrgetter("x")).x
                            if self._curr_direction == 0
                            else (
                                min(relevant_positions, key=attrgetter("x")).x
                                if self._curr_direction == 2
                                else (
                                    max(relevant_positions, key=attrgetter("y")).y
                                    if self._curr_direction == 1
                                    else min(relevant_positions, key=attrgetter("y")).y
                                )
                            )
                        )
                        idx = [
                            pos
                            for pos in relevant_positions
                            if (
                                (self._curr_direction == 0 or self._curr_direction == 2)
                                and pos.x == filter_position
                            )
                            or (
                                (self._curr_direction == 1 or self._curr_direction == 3)
                                and pos.y == filter_position
                            )
                        ].index(curr_pos)
                        next_face = ORIENTATION_INPUT[curr_cube_face][
                            self._curr_direction
                        ]
                        next_dir = next_face[1]
                        next_cube = [
                            pos
                            for pos in self.positions
                            if pos.cube_side == next_face[0]
                        ]
                        if self._curr_direction == 0:
                            # reached past right bound
                            if part_2:
                                filter_pos = (
                                    min(next_cube, key=attrgetter("x")).x
                                    if next_dir == 0
                                    else (
                                        max(next_cube, key=attrgetter("x")).x
                                        if next_dir == 2
                                        else (
                                            min(next_cube, key=attrgetter("y")).y
                                            if next_dir == 1
                                            else max(next_cube, key=attrgetter("y")).y
                                        )
                                    )
                                )
                                next_row = [
                                    pos
                                    for pos in next_cube
                                    if (
                                        (next_dir == 1 or next_dir == 3)
                                        and pos.y == filter_pos
                                    )
                                    or (
                                        (next_dir == 0 or next_dir == 2)
                                        and pos.x == filter_pos
                                    )
                                ]
                                next_idx = (
                                    idx
                                    if next_dir == 0 or next_dir == 3
                                    else len(next_row) - 1 - idx
                                )
                                wrap_around_pos = next_row[next_idx]
                            else:
                                wrap_around_pos = min(
                                    relevant_positions, key=attrgetter("x")
                                )
                        elif self._curr_direction == 1:
                            # reached past down bound
                            if part_2:
                                filter_pos = (
                                    min(next_cube, key=attrgetter("y")).y
                                    if next_dir == 1
                                    else (
                                        max(next_cube, key=attrgetter("y")).y
                                        if next_dir == 3
                                        else (
                                            min(next_cube, key=attrgetter("x")).x
                                            if next_dir == 0
                                            else max(next_cube, key=attrgetter("x")).x
                                        )
                                    )
                                )
                                next_row = [
                                    pos
                                    for pos in next_cube
                                    if (
                                        (next_dir == 0 or next_dir == 2)
                                        and pos.x == filter_pos
                                    )
                                    or (
                                        (next_dir == 1 or next_dir == 3)
                                        and pos.y == filter_pos
                                    )
                                ]
                                next_idx = (
                                    idx
                                    if next_dir == 1 or next_dir == 2
                                    else len(next_row) - 1 - idx
                                )
                                wrap_around_pos = next_row[next_idx]

                            else:
                                wrap_around_pos = min(
                                    relevant_positions, key=attrgetter("y")
                                )
                        elif self._curr_direction == 2:
                            # reached past left bound
                            if part_2:
                                filter_pos = (
                                    max(next_cube, key=attrgetter("x")).x
                                    if next_dir == 2
                                    else (
                                        min(next_cube, key=attrgetter("x")).x
                                        if next_dir == 0
                                        else (
                                            max(next_cube, key=attrgetter("y")).y
                                            if next_dir == 3
                                            else min(next_cube, key=attrgetter("y")).y
                                        )
                                    )
                                )
                                next_row = [
                                    pos
                                    for pos in next_cube
                                    if (
                                        (next_dir == 1 or next_dir == 3)
                                        and pos.y == filter_pos
                                    )
                                    or (
                                        (next_dir == 0 or next_dir == 2)
                                        and pos.x == filter_pos
                                    )
                                ]
                                next_idx = (
                                    idx
                                    if next_dir == 2 or next_dir == 1
                                    else len(next_row) - 1 - idx
                                )
                                wrap_around_pos = next_row[next_idx]

                            else:
                                wrap_around_pos = max(
                                    relevant_positions, key=attrgetter("x")
                                )
                        else:
                            # reached past up bound
                            if part_2:
                                filter_pos = (
                                    max(next_cube, key=attrgetter("y")).y
                                    if next_dir == 3
                                    else (
                                        min(next_cube, key=attrgetter("y")).y
                                        if next_dir == 1
                                        else (
                                            max(next_cube, key=attrgetter("x")).x
                                            if next_dir == 2
                                            else min(next_cube, key=attrgetter("x")).x
                                        )
                                    )
                                )
                                next_row = [
                                    pos
                                    for pos in next_cube
                                    if (
                                        (next_dir == 0 or next_dir == 2)
                                        and pos.x == filter_pos
                                    )
                                    or (
                                        (next_dir == 1 or next_dir == 3)
                                        and pos.y == filter_pos
                                    )
                                ]
                                next_idx = (
                                    idx
                                    if next_dir == 3 or next_dir == 0
                                    else len(next_row) - 1 - idx
                                )
                                wrap_around_pos = next_row[next_idx]
                            else:
                                wrap_around_pos = max(
                                    relevant_positions, key=attrgetter("y")
                                )

                        if wrap_around_pos.is_wall:
                            break

                        curr_pos.x = wrap_around_pos.x
                        curr_pos.y = wrap_around_pos.y
                        curr_pos.cube_side = wrap_around_pos.cube_side
                        if part_2:
                            self._curr_direction = next_dir
                            relevant_positions = [
                                pos
                                for pos in self.positions
                                if pos.cube_side == curr_pos.cube_side
                            ]
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

    def print_map(self, print_cube: bool = False):
        curr_row = 1
        while True:
            row = [pos for pos in self.positions if pos.y == curr_row]
            if not row:
                break
            max_x = max(row, key=attrgetter("x")).x
            min_x = min(row, key=attrgetter("x")).x
            for i in range(max_x + 1):
                if i < min_x:
                    print(" ", end="")
                else:
                    print(
                        f"{(row[i-min_x].cube_side) if print_cube else ('#' if row[i-min_x].is_wall else '.')}",
                        end="",
                    )

            print()
            curr_row += 1


def get_map(file_name: str, cube_size: int) -> Map:
    def get_next_cube_side_start(cube_sides: List[int], cube_size: int):
        for i in range(len(cube_sides)):
            if cube_sides[i] == cube_size * cube_size:
                return i + 1

    cube_sides = [cube_size * cube_size] * 6
    with open(file_name, "r") as file:
        data = file.read()

    cube_start = 1
    curr_cube_side = 1
    side_count = 0
    path, instructions = data.split("\n\n")
    positions = []
    for i, row in enumerate(path.split("\n")):
        for j, col in enumerate(row):
            if col == " ":
                continue
            position = Position(x=j + 1, y=i + 1, cube_side=curr_cube_side)
            cube_sides[curr_cube_side - 1] -= 1
            side_count += 1
            if side_count % cube_size == 0:
                side_count = 0
                curr_cube_side += 1
            if col == ".":
                position.is_wall = False
            else:
                position.is_wall = True
            positions.append(position)

        if cube_sides[cube_start - 1] == 0:
            # finished getting this cube_side
            cube_start = get_next_cube_side_start(
                cube_sides=cube_sides, cube_size=cube_size
            )
        curr_cube_side = cube_start

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


def solve_part_1(file_name: str, cube_size: int):
    map = get_map(file_name=file_name, cube_size=cube_size)
    end_pos, dir = map.traverse()
    password = 1000 * end_pos.y + 4 * end_pos.x + dir
    print(f"Final password: {password}")


def solve_part_2(file_name: str, cube_size: int):
    # currently built out the cube side sections on flat map
    # we can transform them into cube sides =>
    # figure out wrap around face landing and orientation => might be easier to hard code it
    map = get_map(file_name=file_name, cube_size=cube_size)
    map.print_map()
    map.print_map(print_cube=True)
    end_pos, dir = map.traverse(part_2=True)
    password = 1000 * end_pos.y + 4 * end_pos.x + dir
    print(f"Final password: {password}")


if __name__ == "__main__":
    solve_part_2(file_name=f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}", cube_size=50)
