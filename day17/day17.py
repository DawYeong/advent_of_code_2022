import os
from typing import List

from rock.models.Rock import Position
from rock.RockFactory import RockFactory

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"
ROCK_START_X = 2
START_DISTANCE_OFFSET = 3


class Chamber:
    _curr_time: int
    _rock_count: int
    _rock_limit: int
    _rocks: List[Position]
    _jet_movements: List[bool]

    def __init__(self, jet_movements: List[bool], rock_limit: int):
        self._curr_time = 0
        self._rock_count = 0
        self._rock_limit = rock_limit
        self._rocks = []
        self._jet_movements = jet_movements

    def handle_rock_movement(self):
        jet_movement_size = len(self._jet_movements)
        while self._rock_count < self._rock_limit:
            # print(f"{self._rock_count}/{self._rock_limit}")
            curr_rock = RockFactory.create(
                curr_num_of_shapes=self._rock_count,
                start_x=ROCK_START_X,
                start_y=self.get_max_height() + START_DISTANCE_OFFSET,
            )
            rock_falling = True
            while rock_falling:
                curr_rock.jet_move_rock(
                    curr_rocks=self._rocks,
                    jet_dir=self._jet_movements[self._curr_time % jet_movement_size],
                )
                rock_falling = curr_rock.rock_fall(self._rocks)
                self._curr_time += 1
            # rock has rested => save position
            self._rocks.extend(curr_rock.get_curr_position())
            self._rock_count += 1

    def get_max_height(self) -> int:
        return max(self._rocks).y + 1 if self._rocks else 0


def get_jet_movements(file_name: str) -> List[bool]:
    with open(file_name, "r") as file:
        data = file.read()

    raw_string = data.strip()
    jet_movements = [True if jet_movement == ">" else False for jet_movement in raw_string]

    return jet_movements

# pretty slow, takes around 1 min to finish
def solve_part_1(file_name: str):
    jet_movements = get_jet_movements(file_name)
    chamber = Chamber(
        jet_movements=jet_movements,
        rock_limit=2022,
    )
    chamber.handle_rock_movement()
    print(chamber.get_max_height())


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
