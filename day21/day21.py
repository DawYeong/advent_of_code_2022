import os
from typing import List, Optional


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


# not the cleanest class, could make a dataclass and then have a service class handle logic...
class Monkey:
    id: str
    value: int
    expression: Optional[str]
    children: Optional[List[str]]

    def __init__(
        self,
        id: str,
        value: int = 0,
        expression: Optional[str] = None,
        children: Optional[List[str]] = None,
    ):
        self.id = id
        self.value = value
        self.expression = expression
        self.children = children

    def __eq__(self, other) -> bool:
        if isinstance(other, Monkey):
            return self.id == other.id

        return False

    def __str__(self) -> str:
        return f"Monkey id: {self.id}, value: {self.value}, expression: {self.expression}, children: {self.children}"

    def __repr__(self):
        return str(self)


def get_monkeys(file_name: str) -> List[Monkey]:
    monkeys = []
    with open(file_name, "r") as file:
        while True:
            data_line = file.readline()
            if not data_line:
                break

            raw_string = data_line.strip().replace(":", "").split(" ")
            if len(raw_string) == 2:
                monkeys.append(
                    Monkey(
                        id=raw_string[0],
                        value=int(raw_string[1]),
                    )
                )
            elif len(raw_string) == 4:
                monkeys.append(
                    Monkey(
                        id=raw_string[0],
                        expression=raw_string[2],
                        children=[raw_string[1], raw_string[3]],
                    )
                )
            else:
                raise Exception(f"Unexpected line: {data_line}")

    return monkeys


def get_monkey_from_id(monkeys: List[Monkey], id: str) -> Monkey:
    for monkey in monkeys:
        if monkey.id == id:
            return monkey

    raise Exception(f"Can't find monkey: {id}")


def traverse_monkeys(monkeys: List[Monkey], monkey_id: str) -> int:
    monkey = get_monkey_from_id(
        monkeys=monkeys,
        id=monkey_id,
    )

    if not monkey.children or not monkey.expression:
        return monkey.value

    left = traverse_monkeys(
        monkeys=monkeys,
        monkey_id=monkey.children[0],
    )
    right = traverse_monkeys(
        monkeys=monkeys,
        monkey_id=monkey.children[1],
    )

    value = 0
    if monkey.expression == "+":
        value = left + right
    elif monkey.expression == "-":
        value = left - right
    elif monkey.expression == "*":
        value = left * right
    elif monkey.expression == "/":
        value = left // right
    else:
        raise Exception(f"Unexpected expression: {monkey.expression}")

    monkey.value = value
    return value


def solve_part_1(file_name: str):
    monkeys = get_monkeys(file_name)

    print(
        traverse_monkeys(
            monkeys=monkeys,
            monkey_id="root",
        )
    )


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
