UNIQUE_CHARS_NEEDED = 14


def main() -> None:
    with open("day06/data.txt") as f:
        data = f.read()
    current_idx = UNIQUE_CHARS_NEEDED
    while True:
        chars_found = data[current_idx - UNIQUE_CHARS_NEEDED : current_idx]
        if len(set(chars_found)) == UNIQUE_CHARS_NEEDED:
            break
        current_idx += 1

    print(current_idx)


if __name__ == "__main__":
    main()
