import os


SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
TEST_FILE_NAME = "test.txt"

SNAFU = [("2", 2), ("1", 1), ("0", 0), ("-", -1), ("=", -2)]

# value given: (carry, current symbol)
# work this out on paper
# this will work in x + y scenarios => anything more, the carry will be greater/less than +/-1 (like in every single number format)
SNAFU_CARRY = {
    -5: (-1, "0"),
    -4: (-1, "1"),
    -3: (-1, "2"),
    -2: (0, "="),
    -1: (0, "-"),
    0: (0, "0"),
    1: (0, "1"),
    2: (0, "2"),
    3: (1, "="),
    4: (1, "-"),
    5: (1, "0"),
}


def get_snafu_value(snafu_char: str) -> int:
    if snafu_char == "-":
        return -1
    elif snafu_char == "=":
        return -2

    return int(snafu_char)


def add_snafu(x: str, y: str) -> str:
    max_val = max(len(x), len(y))
    fill_x = x.rjust(max_val, "0")[::-1]
    fill_y = y.rjust(max_val, "0")[::-1]

    final_snafu = ""
    carry = 0
    for i in range(max_val):
        x_val = get_snafu_value(fill_x[i])
        y_val = get_snafu_value(fill_y[i])

        digit_value = x_val + y_val + carry

        carry, curr_snafu_char = SNAFU_CARRY[digit_value]
        final_snafu += curr_snafu_char

    if carry == -1:
        final_snafu += "-"
    elif carry == 1:
        final_snafu += "1"

    return final_snafu[::-1]


def get_final_snafu(file_name: str) -> str:
    with open(file_name, "r") as file:
        data = file.read()

    lines = [line for line in data.split("\n")]

    final_snafu = lines[0]
    for i in range(1, len(lines)):
        final_snafu = add_snafu(x=final_snafu, y=lines[i])

    return final_snafu


def solve_part_1(file_name: str):
    final_snafu = get_final_snafu(file_name)
    print(f"Final snafu: {final_snafu}")


if __name__ == "__main__":
    solve_part_1(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
