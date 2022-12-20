from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key
import os
from typing import List, Tuple

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"


class Compare(str, Enum):
    EQ = "equal"
    GT = "greater_than"
    LT = "less_than"


@dataclass(frozen=True)
class Pair:
    first: List
    second: List


def build_list(raw_string: str, curr_index: int) -> Tuple[List, int]:
    new_list = []
    curr_number = ""

    while curr_index < len(raw_string):
        if raw_string[curr_index] == "[":
            # start of another list
            child_list, idx = build_list(
                raw_string=raw_string, curr_index=curr_index + 1
            )
            new_list.append(child_list)
            curr_index = idx
        elif raw_string[curr_index] == "]":
            # end
            if len(curr_number) > 0:
                new_list.append(int(curr_number))
            return (
                new_list,
                curr_index
                if (curr_index < len(raw_string) - 1)
                and raw_string[curr_index + 1] == "]"
                else curr_index + 1,
            )
        elif raw_string[curr_index] == ",":
            # finish number => add to list and move on
            new_list.append(int(curr_number))
            curr_number = ""
        else:
            # build number
            curr_number += raw_string[curr_index]
        curr_index += 1


def build_packet(raw_string: str) -> List:
    result_list, _ = build_list(raw_string=raw_string, curr_index=1)
    return result_list


def compare_left_right(left, right) -> Compare:
    if isinstance(left, List) and isinstance(right, List):
        return is_list_in_correct_order(left, right)
    elif isinstance(left, List) and not isinstance(right, List):
        temp_list = [right]
        return is_list_in_correct_order(left, temp_list)
    elif not isinstance(left, List) and isinstance(right, List):
        temp_list = [left]
        return is_list_in_correct_order(temp_list, right)
    else:
        if left < right:
            return Compare.GT
        elif left == right:
            return Compare.EQ
        else:
            return Compare.LT


def is_list_in_correct_order(left, right) -> Compare:
    min_length = min(len(left), len(right))

    for i in range(min_length):
        compare = compare_left_right(left[i], right[i])
        if compare == Compare.GT or compare == Compare.LT:
            return compare

    left_len = len(left)
    right_len = len(right)

    if left_len < right_len:
        return Compare.GT
    elif left_len == right_len:
        return Compare.EQ
    else:
        return Compare.LT


def get_pairs(file_name: str) -> List[Pair]:
    pairs = []
    with open(file_name, "r") as file:
        while True:
            first = file.readline().replace("\n", "")
            first_packet = build_packet(first)
            second = file.readline().replace("\n", "")
            second_packet = build_packet(second)

            pairs.append(
                Pair(
                    first=first_packet,
                    second=second_packet,
                )
            )

            transition = file.readline()
            if not transition:
                break

    return pairs


def compare(item1, item2):
    compare = is_list_in_correct_order(
        left=item1,
        right=item2,
    )
    if compare == Compare.GT:
        return -1
    elif compare == Compare.EQ:
        return 0
    else:
        return 1


def solve_part_1(file_name: str):
    pairs = get_pairs(file_name)
    result = 0
    for i in range(len(pairs)):
        compare = is_list_in_correct_order(
            left=pairs[i].first,
            right=pairs[i].second,
        )
        if compare == Compare.GT:
            result += i + 1

    print(result)


def solve_part_2(file_name: str):
    pairs = get_pairs(file_name)
    items = []
    for pair in pairs:
        items.append(pair.first)
        items.append(pair.second)
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]
    items.append(divider_packet_1)
    items.append(divider_packet_2)

    sorted_items = sorted(items, key=cmp_to_key(compare))
    decoder_key = (sorted_items.index(divider_packet_1) + 1) * (
        sorted_items.index(divider_packet_2) + 1
    )
    print(f"Decoder Key: {decoder_key}")


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
