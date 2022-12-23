from dataclasses import dataclass
from abc import ABC
from typing import List

CHAMBER_WIDTH = 7

@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y

        return False

    def __lt__(self, other) -> bool:
        return self.y < other.y


class Rock(ABC):
    _curr_pos: List[Position]

    def jet_move_rock(self, curr_rocks: List[Position], jet_dir: bool) -> None:
        # move rock right if jet_dir is True, left if False
        move_rock = 1 if jet_dir else -1

        new_positions = []
        for rock_pos in self._curr_pos:
            new_rock_x = rock_pos.x + move_rock
            temp_pos = Position(
                x=new_rock_x,
                y=rock_pos.y,
            )
            if temp_pos in curr_rocks or new_rock_x < 0 or new_rock_x >= CHAMBER_WIDTH:
                return

            new_positions.append(temp_pos)

        self._curr_pos = new_positions

    def rock_fall(self, curr_rocks: List[Position]) -> bool:
        new_positions = []
        for rock_pos in self._curr_pos:
            new_rock_y = rock_pos.y - 1
            temp_pos = Position(
                x=rock_pos.x,
                y=new_rock_y,
            )
            if temp_pos in curr_rocks or new_rock_y < 0:
                return False

            new_positions.append(temp_pos)

        self._curr_pos = new_positions
        return True

    def get_curr_position(self) -> List[Position]:
        return self._curr_pos
