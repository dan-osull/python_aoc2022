# Part 1

# Rock (1 pt if selected) = A + X
# Paper (2 pt) = B + Y
# Scissors (3 pt) = C + Z

# 0 pt loss, 3 pt draw, 6 pt win

# User plays second

GAME_SCORE_MAP = {
    "A X": 3,  # rock draws with rock
    "A Y": 6,  # paper wraps rock
    "A Z": 0,  # rock dulls scissors
    "B X": 0,  # paper wraps rock
    "B Y": 3,  # paper draws with paper
    "B Z": 6,  # scissors cut paper
    "C X": 6,  # rock dulls scissors
    "C Y": 0,  # scissors cut paper
    "C Z": 3,  # scissors draw with scissors
}

SELECTION_SCORE_MAP = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

with open("day02/data.txt") as f:
    data = f.readlines()

total = 0
for line in data:
    line = line.strip()
    total += SELECTION_SCORE_MAP[line[-1]]
    total += GAME_SCORE_MAP[line]

print(total)