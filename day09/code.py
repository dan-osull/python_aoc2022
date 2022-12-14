import logging
from itertools import pairwise
from typing import Literal

LOG_LEVEL = logging.WARNING

Coord = tuple[int, int]
"""X and Y coordinates"""


def move_head(current_head_position: Coord, direction: str) -> Coord:
    new_position_table: dict[str, Coord] = {
        "L": (current_head_position[0] - 1, current_head_position[1]),
        "R": (current_head_position[0] + 1, current_head_position[1]),
        "U": (current_head_position[0], current_head_position[1] - 1),
        "D": (current_head_position[0], current_head_position[1] + 1),
    }
    new_head_position = new_position_table[direction]
    logging.info(f"HEAD {direction}: {current_head_position} -> {new_head_position}")
    return new_head_position


def move_tail(head_position: Coord, current_tail_position: Coord) -> Coord:
    x_axis_move = max_one(head_position[0] - current_tail_position[0])
    y_axis_move = max_one(head_position[1] - current_tail_position[1])
    new_tail_position = (
        current_tail_position[0] + x_axis_move,
        current_tail_position[1] + y_axis_move,
    )
    logging.info(f"TAIL {current_tail_position} -> {new_tail_position}")
    return new_tail_position


def max_one(number: int) -> Literal[0, 1, -1]:
    """Helper function that returns 1 for any positive int, -1 for any negative"""
    return 1 if number > 0 else -1 if number < 0 else 0


def test_adjacent(one: Coord, two: Coord) -> bool:
    """Helper function that returns True if two coordinates are next to each other"""
    return not any(abs(a - b) > 1 for a, b in zip(one, two))


def process_rope_moves(data: list[str], *, number_of_knots: int = 2) -> int:
    knots: dict[int, Coord] = {i: (0, 0) for i in range(number_of_knots)}
    max_idx = number_of_knots - 1
    tail_position_history: list[Coord] = [knots[max_idx]]

    for line in data:
        direction, distance = line.split()
        distance = int(distance)
        for _ in range(distance):
            knots[0] = move_head(knots[0], direction)
            pairs = pairwise(knots.keys())
            for one, two in pairs:
                if test_adjacent(knots[one], knots[two]):
                    break
                # Move second knot in pair if necessary
                knots[two] = move_tail(knots[one], knots[two])
            tail_position_history.append(knots[max_idx])

    return len(set(tail_position_history))


def main() -> None:
    logging.basicConfig(level=LOG_LEVEL)

    with open("day09/data.txt") as file:
        data = [line.strip() for line in file.readlines()]

    print(process_rope_moves(data))
    print(process_rope_moves(data, number_of_knots=10))


if __name__ == "__main__":
    main()
