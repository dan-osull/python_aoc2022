from typing import NamedTuple
from functools import reduce


class Coord(NamedTuple):
    x: int
    y: int


class Views(NamedTuple):
    """
    The view from the tree outwards in each direction.

    The start of the list is closest to the tree.
    """

    left: list[int]
    right: list[int]
    above: list[int]
    below: list[int]


class Tree(NamedTuple):
    height: int
    views: Views


TreeGrid = dict[Coord, Tree]
HeightGrid = dict[Coord, int]


def get_height_grid(data: list[str]) -> tuple[HeightGrid, int]:
    height_grid: HeightGrid = {}
    for y_axis, line in enumerate(data):
        for x_axis, char in enumerate(line):
            height_grid[Coord(x=x_axis, y=y_axis)] = int(char)
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
    coords = {
        "left": [Coord(i, coord.y) for i in reversed(range(0, coord.x))],
        "right": [Coord(i, coord.y) for i in range(coord.x + 1, max_idx + 1)],
        "above": [Coord(coord.x, i) for i in reversed(range(0, coord.y))],
        "below": [Coord(coord.x, i) for i in range(coord.y + 1, max_idx + 1)],
    }
    return Views(
        **{key: [height_grid[key] for key in value] for key, value in coords.items()}
    )


def test_is_tree_visible(coord: Coord, tree: Tree, max_idx: int) -> bool:
    if coord.x == 0 or coord.x == max_idx or coord.y == 0 or coord.y == max_idx:
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
