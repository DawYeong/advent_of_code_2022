import os
from typing import Dict, List, Set, Tuple

from rock.RockService import RockService
from rock.RockFactory import RockFactory

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"
ROCK_START_X = 2
START_DISTANCE_OFFSET = 3
CHAMBER_WIDTH = 7

class Chamber:
    _curr_time: int
    _rock_count: int
    _rock_limit: int
    _rocks: Set[Tuple[int, int]]
    _jet_movements: List[bool]
    _cycle_check: Dict
    _cycle_height = int

    def __init__(self, jet_movements: List[bool], rock_limit: int):
        self._curr_time = 0
        self._rock_count = 0
        self._rock_limit = rock_limit
        self._rocks = set([(x, 0) for x in range(CHAMBER_WIDTH)])
        self._jet_movements = jet_movements
        self._cycle_check = {}
        self._cycle_height = 0

    def handle_rock_movement(self):
        jet_movement_size = len(self._jet_movements)
        while self._rock_count < self._rock_limit:
            max_height = self._get_max_height()
            # print(f"{self._rock_count}/{self._rock_limit}")
            curr_rock = RockFactory.create(
                curr_num_of_shapes=self._rock_count,
                start_x=ROCK_START_X,
                start_y=max_height + START_DISTANCE_OFFSET+1,
            )
            rock_falling = True
            while rock_falling:
                jet_rock = RockService.jet_move_rock(
                    curr_rock=curr_rock,
                    jet_dir=self._jet_movements[self._curr_time % jet_movement_size],
                )

                if not jet_rock & self._rocks:
                    curr_rock = jet_rock

                rock_fall = RockService.rock_fall(curr_rock)
                self._curr_time += 1
                if rock_fall & self._rocks:
                    # rock has rested => save position

                    # key is: current jet movement, rock piece, current surface
                    if self._rock_count > 2022: # don't bother with finding cycles for low rock counts
                        key = (self._curr_time % jet_movement_size, self._rock_count%5, self.get_surface(max_height))
                        if key in self._cycle_check:
                            # found a cycle => add cycle
                            prev_rock_count, prev_max_height = self._cycle_check[key]
                            height_diff = max_height - prev_max_height
                            rock_count_diff = self._rock_count - prev_rock_count
                            cycles = (self._rock_limit - self._rock_count) // rock_count_diff
                            self._cycle_height += cycles * height_diff
                            self._rock_count += cycles * rock_count_diff
                        self._cycle_check[key] = (self._rock_count, max_height)
                    # rest rock
                    break
                curr_rock = rock_fall

            self._rocks |= curr_rock
            self._rock_count += 1
            

    def _get_max_height(self) -> int:
        return max([y for (_, y) in self._rocks])

    def get_surface(self, max_height: int) -> Set[Tuple[int, int]]:
        # look at the rock surface 50 units deep => arbitrary number
        top = frozenset([(x, max_height - y) for (x, y) in self._rocks if max_height - y <= 50])
        return top

    def get_absolute_height(self) -> int:
        return self._get_max_height() + self._cycle_height

def get_jet_movements(file_name: str) -> List[bool]:
    with open(file_name, "r") as file:
        data = file.read()

    raw_string = data.strip()
    jet_movements = [True if jet_movement == ">" else False for jet_movement in raw_string]

    return jet_movements

# changing to set and Tuples, sped things up => now ~400ms
def solve_part_1(file_name: str):
    jet_movements = get_jet_movements(file_name)
    chamber = Chamber(
        jet_movements=jet_movements,
        rock_limit=2022,
    )
    chamber.handle_rock_movement()
    print(chamber.get_absolute_height())

# ~ 2 secs
def solve_part_2(file_name: str):
    jet_movements = get_jet_movements(file_name)
    chamber = Chamber(
        jet_movements=jet_movements,
        rock_limit=1000000000000,
    )
    chamber.handle_rock_movement()
    print(chamber.get_absolute_height())

if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
