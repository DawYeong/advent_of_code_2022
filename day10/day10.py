from dataclasses import dataclass
from enum import Enum
import os
from typing import List, Optional

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
CHECKPOINTS = [20, 60, 100, 140, 180, 220]


class Command(str, Enum):
    NOOP = "noop"
    ADDX = "addx"


@dataclass(frozen=True)
class Instruction:
    command: Command
    value: Optional[int]


def get_instruction_from_raw_string(raw_string: str) -> Instruction:
    split_string = raw_string.split(" ")
    command = split_string[0]
    value = None if len(split_string) < 2 else split_string[1]

    return Instruction(
        command=command,
        value=int(value) if value else None,
    )


def get_instructions(file_name: str) -> List[Instruction]:
    with open(file_name, "r") as file:
        data = file.read()

    data_lines = data.split("\n")
    instructions = [
        get_instruction_from_raw_string(data_line) for data_line in data_lines
    ]

    return instructions


def get_total_signal_strength(instructions: List[Instruction]) -> int:
    clock_cycle = 1
    x = 1
    curr_x = x
    curr_signal_level = 0
    total_signal_strength = 0
    for instruction in instructions:
        if instruction.command == Command.NOOP:
            clock_cycle += 1
        elif instruction.command == Command.ADDX:
            clock_cycle += 2
            curr_x = x
            x += instruction.value
        else:
            raise ValueError(f"Unexpected Command: {instruction.command}")

        signal_x = x if clock_cycle == CHECKPOINTS[curr_signal_level] else curr_x

        if (
            clock_cycle == CHECKPOINTS[curr_signal_level]
            or clock_cycle == CHECKPOINTS[curr_signal_level] + 1
        ):
            total_signal_strength += CHECKPOINTS[curr_signal_level] * signal_x
            curr_signal_level += 1

        if curr_signal_level >= len(CHECKPOINTS):
            # reached 220th clock cycle
            break

    return total_signal_strength

def solve_part_1(file_name: str):
    instructions = get_instructions(file_name)
    total_signal_strength = get_total_signal_strength(instructions)
    print(total_signal_strength)


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
