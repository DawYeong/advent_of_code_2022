from dataclasses import dataclass
import os
from typing import Dict, List, Set, Tuple


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


@dataclass
class Cube:
    x: int
    y: int
    z: int
    sides: int = 6


def get_cubes(file_name: str) -> List[Cube]:
    cubes = []
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break
            pos = data_line.strip().split(",")
            cube = Cube(
                x=int(pos[0]),
                y=int(pos[1]),
                z=int(pos[2]),
            )

            # check if cube touching other cubes
            update_cubes(cubes=cubes, new_cube=cube)
            cubes.append(cube)

    return cubes


def update_cubes(
    cubes: List[Cube],
    new_cube: Cube,
):
    for cube in cubes:
        is_touching = (
            (
                cube.x == new_cube.x
                and cube.y == new_cube.y
                and abs(cube.z - new_cube.z) <= 1
            )
            or (
                cube.x == new_cube.x
                and cube.z == new_cube.z
                and abs(cube.y - new_cube.y) <= 1
            )
            or (
                cube.y == new_cube.y
                and cube.z == new_cube.z
                and abs(cube.x - new_cube.x) <= 1
            )
        )

        if is_touching:
            cube.sides -= 1
            new_cube.sides -= 1


def get_surface_area(cubes: List[Cube]) -> int:
    return sum([cube.sides for cube in cubes])


def solve_part_1(file_name: str):
    cubes = get_cubes(file_name)
    surface_area = get_surface_area(cubes)
    print(surface_area)


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
