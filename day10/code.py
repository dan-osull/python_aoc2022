from dataclasses import dataclass

PART_ONE_CYCLES = [20, 60, 100, 140, 180, 220]
PART_TWO_ROW_LENGTH = 40

RegisterHistory = dict[int, int]
"""Key = register.cycle, value = register.value"""
SpriteMap = dict[int, bool]
"""Key = register.cycle, value = sprite True/False"""


@dataclass
class Register:
    _current_value = 1
    _future_value = 0
    _current_cycle = 1
    _unlock_at_cycle = 0

    @property
    def value(self) -> int:
        return self._current_value

    @property
    def cycle(self) -> int:
        return self._current_cycle

    @property
    def locked(self) -> bool:
        return self._unlock_at_cycle > self._current_cycle

    def addx(self, value: int) -> None:
        if self.locked:
            raise ValueError(
                'Register is locked. Test "locked" property before invoking "addx".'
            )
        self._unlock_at_cycle = self._current_cycle + 2
        self._future_value = self.value + value

    def noop(self) -> None:
        self._future_value = self.value
        self._unlock_at_cycle = self._current_cycle + 1

    def advance_cycle(self) -> None:
        self._current_cycle += 1
        if not self.locked:
            self._current_value = self._future_value


def save_register_data(
    saved_register_data: dict,
    register: Register,
    cycles_of_interest: list[int],
) -> RegisterHistory:
    if register.cycle in cycles_of_interest:
        saved_register_data[register.cycle] = register.value
    return saved_register_data


def test_sprite_hit(register: Register) -> bool:
    sprite_position = register.cycle
    while sprite_position > PART_TWO_ROW_LENGTH:
        sprite_position -= PART_TWO_ROW_LENGTH
    if register.value <= sprite_position <= register.value + 2:
        return True
    return False


def part_one_loop(
    data: list[str], register: Register, cycles_of_interest: list[int]
) -> RegisterHistory:
    register_history: RegisterHistory = {}
    save_register_data(register_history, register, cycles_of_interest)

    for command in data:
        split = command.split()
        if len(split) == 1:
            register.noop()
        else:
            register.addx(int(split[1]))
        while register.locked:
            register.advance_cycle()
            save_register_data(register_history, register, cycles_of_interest)

    return register_history


def part_two_loop(data: list[str], register: Register) -> SpriteMap:
    sprite_map: SpriteMap = {}

    sprite_map[register.cycle] = test_sprite_hit(register)
    for command in data:
        split = command.split()
        if len(split) == 1:
            register.noop()
        else:
            register.addx(int(split[1]))
        while register.locked:
            register.advance_cycle()
            sprite_map[register.cycle] = test_sprite_hit(register)

    return sprite_map


def part_one_solution(data: list[str]) -> None:
    register = Register()
    register_history = part_one_loop(data, register, PART_ONE_CYCLES)

    total = 0
    for key, value in register_history.items():
        total += key * value
    print(total)


def part_two_solution(data: list[str]) -> None:
    register = Register()
    sprite_map = part_two_loop(data, register)
    counter = 0
    for sprite in sprite_map.values():
        if sprite:
            print("#", end="")
        else:
            print(".", end="")
        counter += 1
        if counter == PART_TWO_ROW_LENGTH:
            print()
            counter = 0


if __name__ == "__main__":
    with open("day10/data.txt") as file:
        data = [line.strip() for line in file.readlines()]
    part_one_solution(data)
    part_two_solution(data)
