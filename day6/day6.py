FILE_NAME = "input.txt"


def get_input(file_name: str) -> str:
    with open(file_name, "r") as file:
        return file.read()


def get_num_of_unique_chars(segment: str) -> int:
    segment_length = len(segment)
    for c in segment:
        occurrences = segment.count(c)
        if occurrences > 1:
            return segment_length - occurrences + 1
    return segment_length


def get_first_marker(input: str, marker_length: int) -> int:
    start = 0
    while start < len(input) - marker_length:
        segment = input[start : start + marker_length]
        num_of_uniques = get_num_of_unique_chars(segment)

        if num_of_uniques == marker_length:
            return start + marker_length

        start += marker_length - num_of_uniques


def solve_part_1(file_name: str):
    input = get_input(file_name)
    print(
        get_first_marker(
            input=input,
            marker_length=4,
        )
    )


def solve_part_2(file_name: str):
    input = get_input(file_name)
    print(
        get_first_marker(
            input=input,
            marker_length=14,
        )
    )


if __name__ == "__main__":
    solve_part_2(FILE_NAME)
