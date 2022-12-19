from dataclasses import dataclass
from typing import List
import os

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"


# class naming is meh
@dataclass(frozen=True)
class TreeView:
    is_visible: bool
    num_of_visible_trees: int


@dataclass(frozen=True)
class TreeVisibility:
    right: TreeView
    left: TreeView
    up: TreeView
    down: TreeView


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
    for i in range(row + 1, len(trees[row])):
        result.append(trees[i][col])
    return result


def get_tree_view(tree_height: int, other_trees: List[int]) -> TreeView:
    num_of_trees = 0
    for tree in other_trees:
        num_of_trees += 1
        if tree >= tree_height:
            break

    return TreeView(
        is_visible=is_visible(
            tree_height=tree_height,
            other_trees=other_trees,
        ),
        num_of_visible_trees=num_of_trees,
    )


def get_tree_visibilities(trees: List[List[int]]) -> List[TreeVisibility]:
    tree_visibilities = []
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees[0]) - 1):
            # determine left, right, up, down
            left_list = trees[i][0:j]
            left_list.reverse()
            tree_height = trees[i][j]

            left = get_tree_view(
                tree_height=tree_height,
                other_trees=left_list,
            )
            right = get_tree_view(
                tree_height=tree_height,
                other_trees=trees[i][j + 1 : len(trees[i])],
            )
            up = get_tree_view(
                tree_height=tree_height,
                other_trees=get_up(
                trees=trees,
                row=i,
                col=j,
            ),
            )
            down = get_tree_view(
                tree_height=tree_height,
                other_trees=get_down(
                    trees=trees,
                    row=i,
                    col=j,
                ),
            )
            tree_visibilities.append(
                TreeVisibility(
                    left=left,
                    right=right,
                    up=up,
                    down=down,
                )
            )
    return tree_visibilities


def get_interior_trees(tree_visibilities: List[TreeVisibility]) -> int:
    return len(
        [
            tree_visibility
            for tree_visibility in tree_visibilities
            if tree_visibility.left.is_visible
            or tree_visibility.right.is_visible
            or tree_visibility.up.is_visible
            or tree_visibility.down.is_visible
        ]
    )


def get_exterior_trees(trees: List[List[int]]) -> int:
    return 2 * (len(trees) + len(trees[0]) - 2)


def get_score(tree_visibility: TreeVisibility) -> int:
    return (
        tree_visibility.left.num_of_visible_trees
        * tree_visibility.right.num_of_visible_trees
        * tree_visibility.up.num_of_visible_trees
        * tree_visibility.down.num_of_visible_trees
    )


def get_max_score(tree_visibilities: List[TreeVisibility]) -> int:
    scores = [get_score(tree_visibility) for tree_visibility in tree_visibilities]
    
    return max(scores)


def solve_part_1(file_name: str):
    trees = get_trees(file_name)
    tree_visibilities = get_tree_visibilities(trees)
    visible_trees = get_interior_trees(tree_visibilities) + get_exterior_trees(trees)
    print(visible_trees)


def solve_part_2(file_name: str):
    trees = get_trees(file_name)
    tree_visibilities = get_tree_visibilities(trees)
    max_score = get_max_score(tree_visibilities)
    print(max_score)

if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
