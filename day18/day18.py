import os
from typing import List, Set, Tuple


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


def get_faces(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


def get_cubes(file_name: str) -> Set[Tuple[int, int, int]]:
    cubes = set()
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break
            pos = data_line.strip().split(",")
            cube = tuple(map(int, pos))
            cubes.add(cube)

    return cubes


def solve_part_1(file_name: str):
    cubes = get_cubes(file_name)
    faces = []
    for c in cubes:
        faces.extend(get_faces(x=c[0], y=c[1], z=c[2]))
    faces = [s for s in faces if s not in cubes]
    print(len(faces))


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
