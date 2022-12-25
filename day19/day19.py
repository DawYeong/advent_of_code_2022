from numpy import array, ndarray
import os
from typing import List, Tuple


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"

TIME_LIMIT_1 = 24
TIME_LIMIT_2 = 32


class Blueprint:
    id: int
    robot_purchase: Tuple[Tuple[ndarray, ndarray]]

    def __init__(self, id: int, costs: List[int]):
        self.id = id
        # 0: Geode, 1: Obsidian, 2: Clay, 3: Ore
        # Tuple[robot cost, robot created]
        self.robot_purchase = (
            (array([0, 0, 0, 0]), array([0, 0, 0, 0])),
            (array([0, 0, 0, costs[0]]), array([0, 0, 0, 1])),
            (array([0, 0, 0, costs[1]]), array([0, 0, 1, 0])),
            (array([0, 0, costs[3], costs[2]]), array([0, 1, 0, 0])),
            (array([0, costs[5], 0, costs[4]]), array([1, 0, 0, 0])),
        )


class BlueprintService:
    @staticmethod
    def get_most_geode_from_blueprint(blueprint: Blueprint, time_limit: int) -> int:
        def get_score_from_state(state: Tuple[ndarray, ndarray]) -> Tuple:
            next_production_state = state[0] + state[1]
            
            return tuple(next_production_state) + tuple(state[1])

        # start state => no resources, 1 ore bot
        stack: List[Tuple[ndarray, ndarray]] = [
            (array([0, 0, 0, 0]), array([0, 0, 0, 1]))
        ]
        max_val = 0
        for t in range(time_limit):
            next_stack = []
            for curr_resources, curr_production in stack:
                # traverse through all possible actions
                for robot_cost, robot_create in blueprint.robot_purchase:
                    # only consider actions we can afford
                    if all(robot_cost <= curr_resources):
                        # updates the (next_state_resources, next_state_production)
                        next_state_resources = (
                            curr_resources + curr_production - robot_cost
                        )
                        next_state_production = curr_production + robot_create
                        max_val = max(max_val, next_state_resources[0])
                        next_stack.append((next_state_resources, next_state_production))

            # sort by best state => look at first the best next resource state then the best production state
            next_stack.sort(key=lambda tup: get_score_from_state(tup))
            # for timing, look at the top x states
            stack = next_stack[-1000:]
        return max([w for ((w, x, y, z), _) in stack])


def get_blueprints(file_name: str) -> List[Blueprint]:
    configs = []
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break

            filtered_str = data_line.strip().replace(":", "").split(" ")
            blueprint = tuple(
                map(
                    int,
                    [
                        filtered_str[1],
                        filtered_str[6],
                        filtered_str[12],
                        filtered_str[18],
                        filtered_str[21],
                        filtered_str[27],
                        filtered_str[30],
                    ],
                )
            )
            config = Blueprint(
                id=blueprint[0],
                costs=blueprint[1:],
            )
            configs.append(config)

    return configs


def solve_part_1(file_name: str):
    blueprints = get_blueprints(file_name)

    ans = 0
    for blueprint in blueprints:
        ans += (
            BlueprintService.get_most_geode_from_blueprint(
                blueprint=blueprint,
                time_limit=TIME_LIMIT_1,
            )
            * blueprint.id
        )

    print(f"Quality level: {ans}")

def solve_part_2(file_name: str):
    blueprints = get_blueprints(file_name)[:3]

    ans = 1
    for blueprint in blueprints:
        ans *= (
            BlueprintService.get_most_geode_from_blueprint(
                blueprint=blueprint,
                time_limit=TIME_LIMIT_2,
            )
        )

    print(f"Part 2: {ans}")


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
