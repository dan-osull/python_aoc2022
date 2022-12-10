import logging
from typing import Literal

Coord = tuple[int, int]
"""X and Y coordinates"""

logging.basicConfig(level=logging.INFO)


def max_one(number: int) -> Literal[0, 1, -1]:
    """Helper function that returns 1 for any positive int, -1 for any negative"""
    if number == 0:
        return 0
    if number > 0:
        return 1
    return -1


def move_tail(head_position: Coord, current_tail_position) -> Coord:
    x_axis_move = max_one(head_position[0] - current_tail_position[0])
    y_axis_move = max_one(head_position[1] - current_tail_position[1])
    new_tail_position = (
        current_tail_position[0] + x_axis_move,
        current_tail_position[1] + y_axis_move,
    )
    logging.info(f"TAIL {current_tail_position} -> {new_tail_position}")
    return new_tail_position


def move_head(current_head_position: Coord, direction: str) -> Coord:
    match direction:
        case "L":
            new_head_position = current_head_position[0] - 1, current_head_position[1]
        case "R":
            new_head_position = current_head_position[0] + 1, current_head_position[1]
        case "U":
            new_head_position = current_head_position[0], current_head_position[1] - 1
        case "D":
            new_head_position = current_head_position[0], current_head_position[1] + 1
        case _:
            raise ValueError("Invalid direction")
    logging.info(f"HEAD {direction}: {current_head_position} -> {new_head_position}")
    return new_head_position


def test_adjacent(one: Coord, two: Coord) -> bool:
    if any(
        [
            one[0] - two[0] > 1,
            two[0] - one[0] > 1,
            one[1] - two[1] > 1,
            two[1] - one[1] > 1,
        ]
    ):
        return False
    return True


def main() -> None:
    with open("day09/data.txt") as file:
        data = [line.strip() for line in file.readlines()]
    head_position = (0, 0)
    tail_position = head_position

    # Part 1
    tail_position_history: list[Coord] = [tail_position]
    for line in data:
        direction, distance = line.split()
        distance = int(distance)
        logging.info(f"Command: {line}")
        logging.info(f"{head_position=} {tail_position=}")
        for _ in range(0, distance):  #
            new_head_position = move_head(head_position, direction)
            head_position = new_head_position
            if test_adjacent(head_position, tail_position):
                logging.info("Head and Tail are adjacent. Do not move Tail.")
                continue
            new_tail_position = move_tail(head_position, tail_position)
            tail_position = new_tail_position
            tail_position_history.append(tail_position)
        logging.info(f"{head_position=} {tail_position=}")
        logging.info("End of command\n")
    print(len(set(tail_position_history)))


if __name__ == "__main__":
    main()
