import os
from typing import List, Optional, Union


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


def get(file_name: str):
    with open(file_name, "r") as file:
        data = file.read()

    path, instructions = data.split("\n\n")
    print(path)
    print(instructions)

def solve_part_1(file_name: str):
    test = get(file_name)


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{TEST_FILE_NAME}")
