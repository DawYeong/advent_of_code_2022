from typing import List

FILE_NAME = "input.txt" # relative path name

def solve_part_1(file_name: str) -> List[int]:
    with open(file_name, 'r') as file:
        data = file.read()

    elf_total_calories = [sum(map(int, elf_calories.replace('\n', " ").split(" "))) for elf_calories in data.split('\n\n')]
    # max_elf_calories = max(elf_total_calories)

    return elf_total_calories

def solve_part_2():
    elf_total_calories = solve_part_1(FILE_NAME)
    elf_total_calories.sort(reverse=True)

    assert len(elf_total_calories) >= 3
    top_3_calories = elf_total_calories[0] + elf_total_calories[1] + elf_total_calories[2]

    print(top_3_calories)


if __name__ == "__main__":
    solve_part_2()
