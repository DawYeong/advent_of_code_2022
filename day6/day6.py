
FILE_NAME = "input.txt"

def get_input(file_name: str) -> str:
    with open(file_name, "r") as file:
        return file.read()

def get_num_of_unique_chars(segment: str) -> int:
    segment_length = len(segment)
    for c in segment:
        occurrences  = segment.count(c)
        if occurrences > 1:
            return segment_length - occurrences + 1
    return segment_length



def get_first_marker(input: str) -> int:
    start = 0
    while start < len(input)-4:
        segment = input[start:start+4]
        num_of_uniques = get_num_of_unique_chars(segment)

        if num_of_uniques == 4:
            return start + 4

        start += 4 - num_of_uniques



def solve_part_1(file_name: str):
    input = get_input(file_name)
    print(get_first_marker(input))

if __name__ == "__main__":
    solve_part_1(FILE_NAME)
