from dataclasses import dataclass
from enum import Enum
import os
from typing import List, Optional

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


class OperationType(str, Enum):
    ADD = "+"
    MUL = "*"


@dataclass(frozen=True)
class Operation:
    op: OperationType
    value: Optional[int]


@dataclass(frozen=True)
class ItemSend:
    monkey_id: int
    item: int


class Monkey:
    _items: List[int]
    _operation: Operation
    _divisible_value: int
    _true_monkey: int
    _false_monkey: int
    _num_of_inspected_items: int

    def __init__(
        self,
        items: List[int],
        op: OperationType,
        op_value: Optional[int],
        div_value: int,
        true_monkey: int,
        false_monkey: int,
    ):
        self._items = items
        self._operation = Operation(
            op=op,
            value=op_value,
        )
        self._divisible_value = div_value
        self._true_monkey = true_monkey
        self._false_monkey = false_monkey
        self._num_of_inspected_items = 0

    def inspect(
        self, modulo: Optional[int] = None, is_relief: bool = True
    ) -> List[ItemSend]:
        sending_items = []
        while len(self._items) != 0:
            item = self._items.pop(0)
            op_value = self._operation.value if self._operation.value else item

            if self._operation.op == OperationType.ADD:
                new = item + op_value
            elif self._operation.op == OperationType.MUL:
                new = item * op_value
            else:
                raise ValueError(f"Unexpected Operation: {self._operation.op}")

            # idea for big numbers => (a mod M) mod m1 = a mod m1 where M = m1*m2*m3...
            # so instead of storing a (very large) we can store (a mod M), which is much smaller
            relief = new // 3 if is_relief else new % modulo

            monkey_send = (
                self._true_monkey
                if relief % self._divisible_value == 0
                else self._false_monkey
            )

            sending_items.append(
                ItemSend(
                    monkey_id=monkey_send,
                    item=relief,
                )
            )
            self._num_of_inspected_items += 1

        return sending_items

    def add_item(self, item: int):
        self._items.append(item)

    def get_num_of_inspected_items(self) -> int:
        return self._num_of_inspected_items


def get_monkeys(file_name: str) -> List[Monkey]:
    monkeys = []
    with open(file_name, "r") as file:
        while True:
            file.readline()  # Monkey line

            items_line = file.readline().replace(",", "").strip().split(" ")
            items = [int(item) for item in items_line[2 : len(items_line)]]

            operation_line = file.readline().strip().split(" ")
            op = operation_line[4]
            op_value = int(operation_line[5]) if operation_line[5] != "old" else None

            div_value = int(file.readline().strip().split(" ")[3])

            true_monkey = int(file.readline().strip().split(" ")[5])

            false_monkey = int(file.readline().strip().split(" ")[5])

            monkeys.append(
                Monkey(
                    items=items,
                    op=op,
                    op_value=op_value,
                    div_value=div_value,
                    true_monkey=true_monkey,
                    false_monkey=false_monkey,
                )
            )

            transition = file.readline()  # \n

            if not transition:
                break
    return monkeys


def handle_monkeys(
    monkeys: List[Monkey], rounds: int, modulo: int, is_relief: bool = True
) -> List[int]:
    for _ in range(rounds):
        for monkey in monkeys:
            monkey_sends = monkey.inspect(
                modulo=modulo,
                is_relief=is_relief,
            )
            for sends in monkey_sends:
                monkeys[sends.monkey_id].add_item(sends.item)

    num_of_inspected = [monkey.get_num_of_inspected_items() for monkey in monkeys]
    num_of_inspected.sort(reverse=True)
    return num_of_inspected


def solve_part_1(file_name: str):
    monkeys = get_monkeys(file_name)
    num_of_inspected = handle_monkeys(
        monkeys=monkeys,
        rounds=20,
        modulo=1,
    )
    monkey_business = num_of_inspected[0] * num_of_inspected[1]
    print(f"Monkey Business: {monkey_business}")


def solve_part_2(file_name: str):
    monkeys = get_monkeys(file_name)

    modulo = 1
    for monkey in monkeys:
        modulo *= monkey._divisible_value

    num_of_inspected = handle_monkeys(
        monkeys=monkeys,
        rounds=10000,
        modulo=modulo,
        is_relief=False,
    )
    monkey_business = num_of_inspected[0] * num_of_inspected[1]
    print(f"Monkey Business: {monkey_business}")


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
