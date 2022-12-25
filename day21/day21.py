import os
from typing import List, Optional, Union


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


# not the cleanest class, could make a dataclass and then have a service class handle logic...
class Monkey:
    id: str
    value: Optional[int]
    expression: Optional[str]
    children: Optional[List[str]]

    def __init__(
        self,
        id: str,
        value: Optional[int] = 0,
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


def get_monkeys(file_name: str, part_2: bool = False) -> List[Monkey]:
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
                        value=int(raw_string[1])
                        if raw_string[0] != "humn" or not part_2
                        else None,
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


def traverse_monkeys(
    monkeys: List[Monkey], monkey_id: str
) -> Optional[Union[int, List]]:
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

    if not left or not right or isinstance(left, list) or isinstance(right, list):
        return (
            [left, monkey.expression, right] if monkey_id != "root" else [left, right]
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


def get_human(final_number: int, human: List) -> int:
    left = human[0]
    expression = human[1]
    right = human[2]

    num, list_express, is_list_on_right = (
        (
            left,
            right,
            True,
        )
        if isinstance(left, int)
        else (
            right,
            left,
            False,
        )
    )
    updated_number = 0
    if expression == "+":
        updated_number = final_number - num
    elif expression == "*":
        updated_number = final_number // num
    elif expression == "-":
        if is_list_on_right:
            updated_number = num - final_number
        else:
            updated_number = final_number + num
    elif expression == "/":
        if is_list_on_right:
            updated_number = num // final_number
        else:
            updated_number = final_number * num
    else:
        raise Exception(f"Unexpected expression: {expression}")

    if left == None or right == None:
        return updated_number

    return get_human(
        final_number=updated_number,
        human=list_express,
    )


def solve_part_1(file_name: str):
    monkeys = get_monkeys(file_name)

    print(
        traverse_monkeys(
            monkeys=monkeys,
            monkey_id="root",
        )
    )


def solve_part_2(file_name: str):
    monkeys = get_monkeys(
        file_name=file_name,
        part_2=True,
    )

    expression = traverse_monkeys(
        monkeys=monkeys,
        monkey_id="root",
    )
    left = expression[0]
    right = expression[1]

    final_number, human = (left, right) if isinstance(right, list) else (right, left)
    human = get_human(final_number=final_number, human=human)
    print(f"Human value: {human}")


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
