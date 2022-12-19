from typing import List

FILE_NAME = "input.txt"


def get_trees(file_name: str) -> List[List[int]]:
    trees = []
    with open(file_name, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            row = [int(c) for c in line if c != "\n"]
            trees.append(row)

    return trees


def is_visible(tree_height: int, other_trees: List[int]) -> bool:
    return tree_height > max(other_trees)


def get_up(trees: List[List[int]], row: int, col: int) -> List[int]:
    result = []
    for i in reversed(range(row)):
        result.append(trees[i][col])
    return result


def get_down(trees: List[List[int]], row: int, col: int) -> List[int]:
    result = []
    for i in range(row+1, len(trees[row])):
        result.append(trees[i][col])
    return result


def get_interior_trees(trees: List[List[int]]) -> int:
    count = 0
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees[0]) - 1):
            # determine left, right, up, down
            tree_height = trees[i][j]
            left = is_visible(
                tree_height=tree_height,
                other_trees=trees[i][0:j],
            )
            right = is_visible(
                tree_height=tree_height,
                other_trees=trees[i][j + 1 : len(trees[i])],
            )
            up = is_visible(
                tree_height=tree_height,
                other_trees=get_up(
                    trees=trees,
                    row=i,
                    col=j,
                ),
            )
            down = is_visible(
                tree_height=tree_height,
                other_trees=get_down(
                    trees=trees,
                    row=i,
                    col=j,
                ),
            )

            if left or right or up or down:
                count += 1

    return count


def get_exterior_trees(trees: List[List[int]]) -> int:
    return 2 * (len(trees) + len(trees[0]) - 2)


def solve_part_1(file_name: str):
    trees = get_trees(file_name)
    visible_trees = get_interior_trees(trees) + get_exterior_trees(trees)
    print(visible_trees)


if __name__ == "__main__":
    solve_part_1(FILE_NAME)
