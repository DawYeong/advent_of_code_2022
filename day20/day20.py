import os
from typing import List


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


def get_initial_state(file_name: str) -> List[int]:
    with open(file_name, "r") as file:
        data = file.read()

    initial_state = [int(num) for num in data.split("\n")]
    return initial_state


def encrypt(initial_state: List[int]) -> List[int]:
    indices = list(range(len(initial_state)))
    for i in indices * 1:
        location = indices.index(i)
        # remove and insert in correct location
        indices.pop(location)
        indices.insert((location + initial_state[i]) % len(indices), i)

    return indices


def determine_grove_sum(initial_state: List[int], encrypted_indices: List[int]) -> int:
    size = len(initial_state)
    groves = [1000, 2000, 3000]
    find_0 = encrypted_indices.index(initial_state.index(0))

    return sum(
        [initial_state[encrypted_indices[(find_0 + grove) % size]] for grove in groves]
    )


def solve_part_1(file_name: str):
    initial_state = get_initial_state(file_name)
    encrypted_indices = encrypt(initial_state)
    grove_sum = determine_grove_sum(
        initial_state=initial_state, encrypted_indices=encrypted_indices
    )
    print(f"Grove sum: {grove_sum}")


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
