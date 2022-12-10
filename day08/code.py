from functools import reduce
from time import perf_counter
from typing import NamedTuple


Coord = tuple[int, int]
"""X and Y coordinates"""
Views = list[list[int]]
"""
The views from the tree looking outwards.

Each outer list is a direction. The inner list contains tree heights. The start of the list is closest to the tree.
"""


class Tree(NamedTuple):
    height: int
    views: Views


TreeGrid = dict[Coord, Tree]
HeightGrid = dict[Coord, int]


def get_height_grid(data: list[str]) -> tuple[HeightGrid, int]:
    height_grid: HeightGrid = {}
    for y_axis, line in enumerate(data):
        for x_axis, char in enumerate(line):
            height_grid[(x_axis, y_axis)] = int(char)
    # Assumes a square grid
    max_idx = len(data) - 1
    return height_grid, max_idx


def get_tree_grid(height_grid: HeightGrid, max_idx: int) -> TreeGrid:
    tree_grid: TreeGrid = {}
    for coord, height in height_grid.items():
        tree_grid[coord] = Tree(
            height=height, views=get_views_from_tree(coord, height_grid, max_idx)
        )
    return tree_grid


def get_views_from_tree(coord: Coord, height_grid: HeightGrid, max_idx: int) -> Views:
    left = [height_grid[i, coord[1]] for i in reversed(range(0, coord[0]))]
    right = [height_grid[i, coord[1]] for i in range(coord[0] + 1, max_idx + 1)]
    above = [height_grid[coord[0], i] for i in reversed(range(0, coord[1]))]
    below = [height_grid[coord[0], i] for i in range(coord[1] + 1, max_idx + 1)]
    return [left, right, above, below]


def test_is_tree_visible(coord: Coord, tree: Tree, max_idx: int) -> bool:
    if coord[0] == 0 or coord[0] == max_idx or coord[1] == 0 or coord[1] == max_idx:
        # Trees on edge are always visible
        return True
    for view in tree.views:
        if tree.height > max(view):
            return True
    return False


def get_score_for_view(tree_height: int, view: list[int]) -> int:
    counter = 0
    for item in view:
        if item >= tree_height:
            counter += 1
            break
        else:
            counter += 1
    return counter


def get_total_scenic_score(tree: Tree) -> int:
    scores: list[int] = []
    for view in tree.views:
        score = get_score_for_view(tree.height, view)
        if score == 0:
            return 0
        scores.append(score)
    return reduce((lambda x, y: x * y), scores)


def main() -> None:
    with open("day08/data.txt") as file:
        data = [line.strip() for line in file.readlines()]

    height_grid, max_idx = get_height_grid(data)
    tree_grid = get_tree_grid(height_grid, max_idx)

    # Part 1
    trees_visible = 0
    for coord, tree in tree_grid.items():
        if test_is_tree_visible(coord, tree, max_idx):
            trees_visible += 1
    print(trees_visible)

    # Part 2
    top_score = 0
    for tree in tree_grid.values():
        new_score = get_total_scenic_score(tree)
        if new_score > top_score:
            top_score = new_score
    print(top_score)


if __name__ == "__main__":
    main()
