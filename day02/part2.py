# Part 2

WIN_SCORE_MAP = {
    "X": 0, # need to lose
    "Y": 3, # need to draw
    "Z": 6, # need to win
}

GAME_SCORE_MAP = {
    "A X": 3,  # LOSE with scissors
    "A Y": 1,  # DRAW with rock
    "A Z": 2,  # WIN with paper
    "B X": 1,  # LOSE with rock
    "B Y": 2,  # DRAW with paper
    "B Z": 3,  # WIN with scissors
    "C X": 2,  # LOSE with paper
    "C Y": 3,  # DRAW with scissors
    "C Z": 1,  # WIN with rock
}

with open("day02/data.txt") as f:
    data = f.readlines()

total = 0
for line in data:
    line = line.strip()
    # Points for win/draw/loss
    total += WIN_SCORE_MAP[line[-1]]
    # Determine shape to use
    total += GAME_SCORE_MAP[line]

print(total)