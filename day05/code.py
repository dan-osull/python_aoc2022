from typing import Callable

CrateStack = dict[int, list[str]]
"""
Key is ID of stack. 
Value is contents of stack. 
End of list = accessible crate at top of stack. 
"""


def get_data_at_idx(data: list[str], idx: int) -> list:
    results = []
    for line in data:
        if line[idx] == " ":
            break
        results.append(line[idx])
    return results


def new_crate_stack(data: list[str]) -> CrateStack:
    """
    Input start position data from top of file.
    Output a populated CrateStack data structure.
    """
    crate_stack = {}
    data.reverse()
    data = [line.replace("\n", "") for line in data]
    top_line = data.pop(0)
    # Step through top line to find index that contain data
    for idx in range(len(top_line)):
        stack_number = top_line[idx]
        if stack_number != " ":
            # Get data from other lines at index
            crate_stack[int(stack_number)] = get_data_at_idx(data, idx)
    return crate_stack


def part_one_move_strategy(
    crate_stack: CrateStack, count: int, source: int, target: int
) -> CrateStack:
    for _ in range(count):
        item = crate_stack[source].pop()
        crate_stack[target].append(item)
    return crate_stack


def part_two_move_strategy(
    crate_stack: CrateStack, count: int, source: int, target: int
) -> CrateStack:
    items_to_move = crate_stack[source][-count:]
    # Remove from source
    crate_stack[source] = crate_stack[source][:-count]
    # Add to target
    crate_stack[target].extend(items_to_move)
    return crate_stack


def move_items(
    crate_stack: CrateStack, instructions: list[str], move_func: Callable
) -> CrateStack:
    for line in instructions:
        split = line.strip().split(" ")
        crate_stack = move_func(
            crate_stack, int(split[1]), int(split[3]), int(split[5])
        )
    return crate_stack


def print_results(crate_stack: CrateStack) -> None:
    results = ""
    for value in crate_stack.values():
        results += value[-1]
    print(results)


def main() -> None:
    with open("day05/data.txt") as f:
        # Not using .strip() here as it makes parsing more difficult
        data = f.readlines()

    # Data about start position of crates is above empty line
    empty_line_idx = data.index("\n")
    # Rest of file is instructions
    instructions = data[empty_line_idx + 1 :]

    # Part 1
    crate_stack = new_crate_stack(data[:empty_line_idx])
    crate_stack = move_items(crate_stack, instructions, part_one_move_strategy)
    print_results(crate_stack)

    # Part 2
    crate_stack = new_crate_stack(data[:empty_line_idx])
    crate_stack = move_items(crate_stack, instructions, part_two_move_strategy)
    print_results(crate_stack)


if __name__ == "__main__":
    main()
