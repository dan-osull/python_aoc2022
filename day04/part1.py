with open("day04/data.txt") as f:
    data = f.readlines()


def get_range_bottom_and_top(elf: str) -> tuple[int, int]:
    bottom, top = elf.split("-")
    return int(bottom), int(top)


total = 0
for line in data:
    elf1, elf2 = line.strip().split(",")
    elf1bottom, elf1top = get_range_bottom_and_top(elf1)
    elf2bottom, elf2top = get_range_bottom_and_top(elf2)
    if (elf1bottom <= elf2bottom) and (elf1top >= elf2top):
        total += 1
    elif (elf1bottom >= elf2bottom) and (elf1top <= elf2top):
        total += 1

print(total)
