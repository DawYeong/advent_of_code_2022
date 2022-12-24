import os
from typing import List, Set, Tuple


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


class DFSService:
    _min_coord: int
    _max_coord: int
    _cubes: Set[Tuple[int, int, int]]
    _faces: List[Tuple[int, int, int]]

    def __init__(self, cubes: Set[Tuple[int, int, int]], faces: List[Tuple[int, int, int]]):
        self._min_coord = min([min(x, y, z) for (x, y, z) in faces])
        self._max_coord = max([max(x, y, z) for (x, y, z) in faces])
        self._cubes = cubes
        self._faces = faces

    def _is_face_exposed(
        self,
        face: Tuple[int, int, int],
    ) -> bool:
        stack = [face]
        visited = set()

        # performing dfs on face to check if it is not trapped
        while stack:
            item = stack.pop()

            if item in visited or item in self._cubes:
                continue

            for c in item:
                if not (self._min_coord <= c <= self._max_coord):
                    # not trapped
                    return True

            visited.add(item)
            stack.extend(
                get_faces(
                    x=item[0],
                    y=item[1],
                    z=item[2],
                )
            )

        return False


    def get_exposed_faces(self) -> int:
        return sum([self._is_face_exposed(face) for face in self._faces])


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


# ~ 3 sec => not horrible, not great 
def solve_part_2(file_name: str):
    cubes = get_cubes(file_name)
    faces = []
    for c in cubes:
        faces.extend(get_faces(x=c[0], y=c[1], z=c[2]))

    dfs_service = DFSService(cubes=cubes, faces=faces,)
    ans = dfs_service.get_exposed_faces()
    print(ans)


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
