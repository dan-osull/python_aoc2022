from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


TreeGrid = dict[Coord, int]


def get_source_grid(data: list[str]) -> tuple[TreeGrid, int]:
    source: TreeGrid = {}
    for y_axis, line in enumerate(data):
        for x_axis, char in enumerate(line):
            source[Coord(x_axis, y_axis)] = int(char)
    # Assumes a square grid
    max_idx = len(data) - 1
    return source, max_idx


def get_lines_of_sight(
    source: TreeGrid, tree: Coord
) -> tuple[list[int], list[int], list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    above: list[int] = []
    below: list[int] = []
    for key, value in source.items():
        if key.y == tree.y and key.x < tree.x:
            left.append(value)
        if key.y == tree.y and key.x > tree.x:
            right.append(value)
        if key.x == tree.x and key.y < tree.y:
            above.append(value)
        if key.x == tree.x and key.y > tree.y:
            below.append(value)

    # Start of list is closest to tree
    left.reverse()
    above.reverse()
    return left, right, above, below


def test_is_tree_visible(source: TreeGrid, tree: Coord, max_idx: int) -> bool:
    if tree.x == 0 or tree.x == max_idx or tree.y == 0 or tree.y == max_idx:
        # Trees on edge are always visible
        return True
    height = source[tree]
    left, right, above, below = get_lines_of_sight(source, tree)
    if any(
        [
            height > max(left),
            height > max(right),
            height > max(above),
            height > max(below),
        ]
    ):
        return True
    return False


def get_score_for_line_of_sight(tree_height: int, line_of_sight: list[int]) -> int:
    if len(line_of_sight) == 0:
        return 0
    counter = 0
    for item in line_of_sight:
        if item >= tree_height:
            counter += 1
            break
        else:
            counter += 1
    return counter


def get_total_scenic_score(source: TreeGrid, tree: Coord) -> int:
    height = source[tree]
    left, right, above, below = get_lines_of_sight(source, tree)
    return (
        get_score_for_line_of_sight(height, left)
        * get_score_for_line_of_sight(height, right)
        * get_score_for_line_of_sight(height, above)
        * get_score_for_line_of_sight(height, below)
    )


def main() -> None:
    with open("day08/data.txt") as file:
        data = [line.strip() for line in file.readlines() if line.strip()]

    source, max_idx = get_source_grid(data)

    # Part 1
    part_one: TreeGrid = {}
    for coord in source.keys():
        tree_visible = test_is_tree_visible(source, coord, max_idx)
        if tree_visible:
            part_one[coord] = source[coord]
    print(len(part_one))

    # Part 2
    top_score = 0
    for coord in source.keys():
        new_score = get_total_scenic_score(source, coord)
        if new_score > top_score:
            top_score = new_score
    print(top_score)


if __name__ == "__main__":
    main()
