from shared import get_score

with open("day03/data.txt") as f:
    data = f.readlines()

total = 0
for line in data:
    line = line.strip()
    compartment1 = set(line[: len(line) // 2])
    compartment2 = set(line[len(line) // 2 :])
    overlap = compartment1.intersection(compartment2)
    total += get_score(next(iter(overlap)))

print(total)
