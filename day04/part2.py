with open("day04/data.txt") as f:
    data = f.readlines()


def get_numbers_in_range(number_range: str) -> set[int]:
    start, stop = number_range.split("-")
    return set(range(int(start), int(stop) + 1))


total = 0
for line in data:
    elf1, elf2 = line.strip().split(",")
    elf1_set = get_numbers_in_range(elf1)
    elf2_set = get_numbers_in_range(elf2)
    if elf1_set.intersection(elf2_set):
        total += 1

print(total)
