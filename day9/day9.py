from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import os

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"


class Direction(Enum):
    R = "RIGHT"
    L = "LEFT"
    D = "DOWN"
    U = "UP"


@dataclass(frozen=True)
class Instruction:
    direction: Direction
    distance: int


@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, other: "Position"):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"


class RopeBridge:
    _head: Position
    _tail: Position
    _visited: List[Position]

    def __init__(self):
        self._head = Position(x=0, y=0)
        self._tail = Position(x=0, y=0)
        self._visited = [Position(x=0, y=0)]

    def _is_tail_touching_head(self):
        return (
            abs(self._head.x - self._tail.x) < 2
            and abs(self._head.y - self._tail.y) < 2
        )

    def _move_head(self, direction: Direction):
        if direction == Direction.R:
            self._head.x += 1
        elif direction == Direction.L:
            self._head.x -= 1
        elif direction == Direction.D:
            self._head.y -= 1
        elif direction == Direction.U:
            self._head.y += 1
        else:
            raise ValueError("Invalid Direction")

    def _move_tail(self):  # relies on the head position
        if self._is_tail_touching_head():
            return

        x_distance_from_head = self._tail.x - self._head.x
        y_distance_from_head = self._tail.y - self._head.y

        # pretty nasty nested ifs
        if abs(x_distance_from_head) == 2:
            if x_distance_from_head < 0:
                # move right
                self._tail.x += 1
            else:
                # move left
                self._tail.x -= 1

            if y_distance_from_head < 0:
                # move down
                self._tail.y += 1
            elif y_distance_from_head > 0:
                # move up
                self._tail.y -= 1

        if abs(y_distance_from_head) == 2:
            if y_distance_from_head < 0:
                # move down
                self._tail.y += 1
            else:
                # move up
                self._tail.y -= 1

            if x_distance_from_head < 0:
                # move right
                self._tail.x += 1
            elif x_distance_from_head > 0:
                # move left
                self._tail.x -= 1

        if self._tail not in self._visited:
            self._visited.append(
                Position(
                    x=self._tail.x,
                    y=self._tail.y,
                )
            )

    def handle_instruction(self, instruction: Instruction):
        for _ in range(instruction.distance):
            # move head
            self._move_head(instruction.direction)
            # move tail
            self._move_tail()

    def get_num_tail_visited(self) -> int:
        return len(self._visited)


def create_instruction_from_raw_string(raw_string: str) -> Instruction:
    split_raw_string = raw_string.split(" ")
    assert len(split_raw_string) == 2

    return Instruction(
        direction=Direction[split_raw_string[0]],
        distance=int(split_raw_string[1]),
    )


def get_instructions(file_name: str) -> List[Instruction]:
    with open(file_name, "r") as file:
        data = file.read()

    data_lines = data.split("\n")
    instructions = [
        create_instruction_from_raw_string(data_line) for data_line in data_lines
    ]

    return instructions

# this runs pretty slow...
def solve_part_1(file_name: str):
    instructions = get_instructions(file_name)
    rope_bridge = RopeBridge()
    for instruction in instructions:
        rope_bridge.handle_instruction(instruction)

    num_of_visited = rope_bridge.get_num_tail_visited()
    print(num_of_visited)


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
