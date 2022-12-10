from typing import NamedTuple, Optional


class Coord(NamedTuple):
    x: int
    y: int


class View(NamedTuple):
    """
    The view from the tree outwards in each direction.

    The start of the list is closest to the tree.
    """

    left: Optional[list[int]]
    right: Optional[list[int]]
    above: Optional[list[int]]
    below: Optional[list[int]]


class Tree(NamedTuple):
    height: int
    view: View


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
            height=height, view=get_view_from_tree(coord, height_grid, max_idx)
        )
    return tree_grid


def get_view_from_tree(coord: Coord, height_grid: HeightGrid, max_idx: int) -> View:
    coords = {
        "left": [Coord(i, coord.y) for i in reversed(range(0, coord.x))],
        "right": [Coord(i, coord.y) for i in range(coord.x + 1, max_idx + 1)],
        "above": [Coord(coord.x, i) for i in reversed(range(0, coord.y))],
        "below": [Coord(coord.x, i) for i in range(coord.y + 1, max_idx + 1)],
    }
    return View(
        **{key: [height_grid[key] for key in value] for key, value in coords.items()}
    )


def test_is_tree_visible(coord: Coord, tree: Tree, max_idx: int) -> bool:
    if coord.x == 0 or coord.x == max_idx or coord.y == 0 or coord.y == max_idx:
        # Trees on edge are always visible
        return True
    if any(
        [
            tree.height > max(tree.view.left or [0]),
            tree.height > max(tree.view.right or [0]),
            tree.height > max(tree.view.above or [0]),
            tree.height > max(tree.view.below or [0]),
        ]
    ):
        return True
    return False


def get_score_for_view(tree_height: int, view: Optional[list[int]]) -> int:
    if not view:
        return 0
    counter = 0
    for item in view:
        if item >= tree_height:
            counter += 1
            break
        else:
            counter += 1
    return counter


def get_total_scenic_score(tree: Tree) -> int:
    return (
        get_score_for_view(tree.height, tree.view.left)
        * get_score_for_view(tree.height, tree.view.right)
        * get_score_for_view(tree.height, tree.view.above)
        * get_score_for_view(tree.height, tree.view.below)
    )


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
    for coord, tree in tree_grid.items():
        new_score = get_total_scenic_score(tree)
        if new_score > top_score:
            top_score = new_score
    print(top_score)


if __name__ == "__main__":
    main()
