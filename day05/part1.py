with open("day05/data.txt") as f:
    # Not using .strip() here as it makes parsing more difficult
    data = f.readlines()

CrateStack = dict[int, list[str]]
"""
Key is number of stack. 
Value is contents of stack. 
End of list = accessible crate at top of stack. 
"""
crate_stack: CrateStack = {}


def get_data_at_idx(data: list[str], idx: int) -> list:
    results = []
    for line in data:
        if line[idx] == " ":
            break
        results.append(line[idx])
    return results


def parse_start_position_data(data: list[str], crate_stack: CrateStack) -> CrateStack:
    """
    Input start position data from top of file.
    Output a populated crate_stack data structure.
    """
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


def move_items(
    crate_stack: CrateStack, count: int, source: int, target: int
) -> CrateStack:
    for _ in range(count):
        item = crate_stack[source].pop()
        crate_stack[target].append(item)
    return crate_stack


def part_one(crate_stack: CrateStack, instructions: list[str]):
    for line in instructions:
        line = line.strip()
        split = line.split(" ")
        crate_stack = move_items(
            crate_stack, int(split[1]), int(split[3]), int(split[5])
        )
    return crate_stack


# Data about start position of crates is above empty line
empty_line_idx = data.index("\n")
crate_stack = parse_start_position_data(data[:empty_line_idx], crate_stack)
# Rest of file is instructions
instructions = data[empty_line_idx + 1 :]

crate_stack = part_one(crate_stack, instructions)

p1_results = ""
for value in crate_stack.values():
    p1_results += value[-1]
print(p1_results)
