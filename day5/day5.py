from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from typing import Dict, List

FILE_NAME = "input.txt"


@dataclass(frozen=True)
class Instruction:
    num_of_items: int
    sender: int
    recipient: int


class Cargo:
    _setup: Dict[int, List[str]]
    _instructions: List[Instruction]

    def __init__(self, setup: Dict[int, List[str]], instructions: List[Instruction]):
        self._setup = OrderedDict(sorted(setup.items()))
        self._instructions = instructions

    def _handle_instruction(self, instruction: Instruction):
        sender_num_items = len(self._setup[instruction.sender])
        num_items = min(sender_num_items, instruction.num_of_items)

        move_items = self._setup[instruction.sender][sender_num_items-num_items:sender_num_items]
        del self._setup[instruction.sender][sender_num_items-num_items:sender_num_items]
        move_items.reverse()
        self._setup[instruction.recipient].extend(move_items)


    def handle_instructions(self):
        while len(self._instructions) != 0:
            instruction = self._instructions.pop(0)
            self._handle_instruction(instruction)
        
    def print_result(self):
        result = ""
        for item in self._setup.items():
            result += item[1][-1]
        
        print(result)


def parse_initial_setup(
    data_line: str, initial_setup: Dict[int, List[str]]
) -> Dict[int, int]:
    start = 1
    index = 1
    new_initial_setup = initial_setup
    while index < len(data_line):
        if not data_line[index] == " ":
            new_initial_setup[start].insert(0, data_line[index])

        start += 1
        index += 4

    return new_initial_setup


def parse_instructions(data_line: str) -> Instruction:
    filter_words = (
        data_line.replace("move ", "").replace("from ", "").replace("to ", "")
    )
    values = filter_words.split(" ")

    assert len(values) == 3

    return Instruction(
        num_of_items=int(values[0]),
        sender=int(values[1]),
        recipient=int(values[2]),
    )


def get_cargo(file_name: str) -> Cargo:
    with open(file_name, "r") as file:
        data = file.read()

    data_lines = data.split("\n")
    initial_setup = defaultdict(list)
    is_initial_setup = True
    instructions = []
    for data_line in data_lines:
        if len(data_line) == 0:
            is_initial_setup = False
            continue

        if is_initial_setup:
            if data_line[1] == "1":
                continue
            initial_setup = parse_initial_setup(
                data_line=data_line,
                initial_setup=initial_setup,
            )
        else:
            instructions.append(parse_instructions(data_line))

    return Cargo(
        setup=initial_setup,
        instructions=instructions
    )

def solve_part_1(file_name: str):
    cargo = get_cargo(file_name)
    cargo.handle_instructions()
    cargo.print_result()


if __name__ == "__main__":
    solve_part_1(FILE_NAME)
