from shared import get_score

with open("day03/data.txt") as f:
    data = f.readlines()

lines_gen = (line.strip() for line in data)

total = 0
# Lines are in groups of 3
for _ in range(int(len(data) / 3)):
    # Get 3 lines from generator
    overlap = (
        set(next(lines_gen)).intersection(next(lines_gen)).intersection(next(lines_gen))
    )
    total += get_score(next(iter(overlap)))

print(total)
