with open("advent/day1_data.txt") as f:
    data = f.readlines()

totals: list[int] = []
current_total = 0

for line in data:
    if line == "\n":
        totals.append(current_total)
        current_total = 0
    else:
        current_total += int(line)

totals.sort(reverse=True)

sum(totals[:3])