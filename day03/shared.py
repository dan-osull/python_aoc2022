from string import ascii_lowercase, ascii_uppercase


def get_score(char: str) -> int:
    letter_score_map = {
        key: value + 1 for value, key in enumerate(ascii_lowercase + ascii_uppercase)
    }
    return letter_score_map[char]
