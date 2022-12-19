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


class CRT:
    _total_signal_strength: int
    _display: List[str]

    def __init__(self):
        self._total_signal_strength = 0
        self._display = ['.'] * 240

    def add_to_total_signal_strength(self, signal_strength: int):
        self._total_signal_strength += signal_strength

    def draw(self, index: int):
        self._display[index] = "#"

    def get_total_signal_strength(self):
        return self._total_signal_strength

    def print_display(self):
        for i in range(6):
            for j in range(40):
                print(self._display[j + i*40], end="")
            print()
    

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


def is_in_range(sprite_position: int, curr_clock_cycle: int) -> bool:
    return sprite_position - 1 <= curr_clock_cycle%40 <= sprite_position + 1 


def get_crt(instructions: List[Instruction]) -> CRT:
    clock_cycle = 1
    x = 1
    curr_x = x
    curr_signal_level = 0
    
    crt = CRT()

    for instruction in instructions:
        if instruction.command == Command.NOOP:
            if is_in_range(sprite_position=x, curr_clock_cycle=clock_cycle-1):
                crt.draw(clock_cycle-1)
            clock_cycle += 1
        elif instruction.command == Command.ADDX:
            for _ in range(2):
                if is_in_range(sprite_position=x, curr_clock_cycle=clock_cycle-1):
                    crt.draw(clock_cycle-1)
                clock_cycle += 1
            curr_x = x
            x += instruction.value
        else:
            raise ValueError(f"Unexpected Command: {instruction.command}")

        if curr_signal_level < len(CHECKPOINTS):
            signal_x = x if clock_cycle == CHECKPOINTS[curr_signal_level] else curr_x

        if (
            curr_signal_level < len(CHECKPOINTS) and (
            clock_cycle == CHECKPOINTS[curr_signal_level]
            or clock_cycle == CHECKPOINTS[curr_signal_level] + 1
            )
        ):
            signal_strength = CHECKPOINTS[curr_signal_level] * signal_x
            crt.add_to_total_signal_strength(signal_strength)
            curr_signal_level += 1

        if clock_cycle >= 239:
            # reached 220th clock cycle
            break

    return crt

def solve_part_1(file_name: str):
    instructions = get_instructions(file_name)
    crt = get_crt(instructions)
    print(crt.get_total_signal_strength())

def solve_part_2(file_name: str):
    instructions = get_instructions(file_name)
    crt = get_crt(instructions)
    crt.print_display()


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
