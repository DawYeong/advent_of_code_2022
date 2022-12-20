from heapq import heapify, heappush, heappop
import os
import sys
from typing import List, Optional

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


class Position:
    _elevation: int
    _distance: int = sys.maxsize
    _is_visited: bool = False
    _neighbors: List["Position"]

    def __init__(
        self,
        elevation: int,
        distance: int = sys.maxsize,
        is_visited: bool = False,
    ):
        self._elevation = elevation
        self._distance = distance
        self._is_visited = is_visited
        self._neighbors = []

    def __lt__(self, other):
        return self._distance < other._distance

    def add_neighbor(self, neighbor: "Position"):
        self._neighbors.append(neighbor)

    def set_distance(self, distance: int):
        self._distance = distance

    def set_visited(self, visited: bool):
        self._is_visited = visited

    def get_distance(self) -> int:
        return self._distance

    def get_elevation(self) -> int:
        return self._elevation

    def get_visited(self) -> bool:
        return self._is_visited

    def get_neighbors(self) -> List["Position"]:
        return self._neighbors


def get_grid(file_name: str) -> List[List[Position]]:
    positions = []
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline().replace("\n", "")
            if not data_line:
                break

            row = []

            for c in data_line:
                if c == "S":
                    row.append(Position(elevation=0))
                elif c == "E":
                    row.append(Position(elevation=27))
                else:
                    row.append(Position(elevation=ord(c) - ord("a") + 1))
            positions.append(row)

    return positions


def update_neighbors(grid: List[List[Position]]):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            right = j + 1
            left = j - 1
            up = i - 1
            down = i + 1

            # updating the 4 neighbors
            max_elevation = grid[i][j].get_elevation() + 1

            if (
                right < len(grid[i])
                and not grid[i][right].get_visited()
                and grid[i][right].get_elevation() <= max_elevation
            ):
                grid[i][j].add_neighbor(grid[i][right])

            if (
                left >= 0
                and not grid[i][left].get_visited()
                and grid[i][left].get_elevation() <= max_elevation
            ):
                grid[i][j].add_neighbor(grid[i][left])

            if (
                up >= 0
                and not grid[up][j].get_visited()
                and grid[up][j].get_elevation() <= max_elevation
            ):
                grid[i][j].add_neighbor(grid[up][j])

            if (
                down < len(grid)
                and not grid[down][j].get_visited()
                and grid[down][j].get_elevation() <= max_elevation
            ):
                grid[i][j].add_neighbor(grid[down][j])


def build_heap(grid: List[List[Position]]) -> List[Position]:
    heap = []
    heapify(heap)
    for row in grid:
        for col in row:
            heap.append(col)

    return heap


def print_grid(grid: List[List[Position]]):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j].get_distance(), end=" ")

        print()


def explore(heap: List[Position]):
    while len(heap) != 0:
        curr_pos = heappop(heap)

        pos_distance = curr_pos.get_distance() + 1
        for neighbor in curr_pos.get_neighbors():
            if neighbor.get_visited():
                continue

            if pos_distance < neighbor.get_distance():
                neighbor.set_distance(pos_distance)

        curr_pos.set_visited(True)
        heapify(heap)


def find_end(grid: List[List[Position]]) -> Optional[Position]:
    for row in grid:
        for col in row:
            if col.get_elevation() == 27:
                return col

    return None


def find_start(grid: List[List[Position]]) -> Optional[Position]:
    for row in grid:
        for col in row:
            if col.get_elevation() == 0:
                return col

    return None


def find_a(grid: List[List[Position]]) -> List[Position]:
    result = []
    for row in grid:
        for col in row:
            if col.get_elevation() == 1:
                result.append(col)

    return result


def reset_grid(grid: List[List[Position]]):
    for row in grid:
        for col in row:
            col.set_distance(sys.maxsize)
            col.set_visited(False)


def solve_part_1(file_name: str):
    # solved using Dijkstra's
    # 1. treat each position as a node and the elevation rules as 1 cost edges
    # 2. build the graph and the min heap
    # 3. execute Dijkstra's using heap
    grid = get_grid(file_name)
    start = find_start(grid)
    start.set_distance(0)
    update_neighbors(grid)
    heap = build_heap(grid)
    explore(heap)

    end = find_end(grid)
    if end == None:
        print("Could not find an end...")

    print(f"Distance to end: {end.get_distance()}")


# Will take a while... performing same algorithm multiple times (a little over 10 mins...)
def solve_part_2(file_name: str):
    grid = get_grid(file_name)
    update_neighbors(grid)
    end = find_end(grid)
    if end == None:
        raise ValueError("End not found...")

    results = []
    starting_pos = [find_start(grid)]
    starting_pos.extend(find_a(grid))

    count = 0
    for pos in starting_pos:
        count += 1
        pos.set_distance(0)
        heap = build_heap(grid)
        explore(heap)
        results.append(end.get_distance())
        reset_grid(grid)
        print(f"Finished: {count}/{len(starting_pos)}")

    print(results)
    print(f"Shortest dist to end: {min(results)}")


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
