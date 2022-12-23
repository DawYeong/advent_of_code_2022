import copy
from dataclasses import dataclass
import os
from typing import Dict, List, Optional, Tuple, Set
from pprint import pprint


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


@dataclass
class Valve:
    id: str
    pressure: int
    neighbors: List[str]
    is_on: bool = False
    is_visited: bool = False

    def __lt__(self, other):
        return self.pressure < other.pressure


def get_valve_graph(file_name: str) -> Dict[str, Valve]:
    graph = {}
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break

            parse = (
                data_line.strip()
                .replace("rate=", "")
                .replace(";", "")
                .replace(",", "")
                .split(" ")
            )

            graph[parse[1]] = Valve(
                id=parse[1], pressure=int(parse[4]), neighbors=parse[9:]
            )

    return graph


def get_valve_distances(graph: Dict[str, Valve]) -> Dict:
    dists = {}
    for key, item in graph.items():
        if item.pressure == 0 and key != "AA":
            continue

        dists[key] = {key: 0}
        visited = [key]
        queue = [(item, 0)]
        while queue:
            valve, distance = queue.pop(0)
            for neighbor in valve.neighbors:
                if neighbor in visited:
                    # already visited
                    continue

                visited.append(neighbor)
                if graph[neighbor].pressure > 0 or neighbor == "AA":
                    # only consider neighbors with positive pressure
                    dists[key][neighbor] = distance + 1

                queue.append((graph[neighbor], distance + 1))
        # remove self
        del dists[key][key]
        if key != "AA":
            del dists[key]["AA"]

    return dists


def traverse(
    graph: Dict[str, Valve],
    dists: Dict,
    visited: List[str],
    dp: Dict,
    time_left: int,
    valve: Valve,
):
    key = f"time_left={time_left},valve={valve.id},visited={visited}"
    if key in dp:
        return dp[key]

    # visited this node
    visited.append(valve.id)

    ans = 0
    for neighbor in dists[valve.id]:
        if neighbor in visited:
            continue
        
        # if neighbor not visited, visit it
        # travel to valve and turn on valve (-1)
        temp_time = time_left - dists[valve.id][neighbor] - 1

        # if that journey is below time limit => don't do it
        if temp_time < 0:
            continue

        ans = max(
            ans,
            traverse(
                graph=graph,
                dists=dists,
                dp=dp,
                visited=copy.deepcopy(visited),
                time_left=temp_time,
                valve=graph[neighbor],
            )
            + temp_time * graph[neighbor].pressure,
        )

    dp[key] = ans
    return ans


def solve_part_1(file_name: str):
    valve_graph = get_valve_graph(file_name)
    valve_distances = get_valve_distances(valve_graph)
    time_left = 30

    ans = traverse(
        graph=valve_graph,
        dists=valve_distances,
        visited=[],
        dp={},
        time_left=time_left,
        valve=valve_graph["AA"],
    )
    print(f"ans: {ans}")


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
