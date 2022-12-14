FILE_NAME = "input.txt" # relative path name

def solve_part_1():
    with open(FILE_NAME, 'r') as file:
        data = file.read()

    elf_total_calories = [sum(map(int, elf_calories.replace('\n', " ").split(" "))) for elf_calories in data.split('\n\n')]
    max_elf_calories = max(elf_total_calories)
    print(max_elf_calories)

if __name__ == "__main__":
    solve_part_1()
