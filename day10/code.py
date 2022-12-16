from dataclasses import dataclass
from functools import partial
from typing import Callable

PART_ONE_CYCLES = [20, 60, 100, 140, 180, 220]
PART_TWO_ROW_LENGTH = 40

RegisterHistory = dict[int, int]
"""Key = register.cycle, value = register.value"""
SpriteMap = dict[int, bool]
"""Key = register.cycle, value = sprite True/False"""
RegisterValueFunction = Callable[["Register"], bool | int]
"""Function that returns a value based on the Register state"""


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


def test_cycle_of_interest(register: Register, cycles_of_interest: list[int]) -> int:
    if register.cycle in cycles_of_interest:
        return register.value
    return 0


def test_sprite_hit(register: Register, row_length: int) -> bool:
    sprite_position = register.cycle
    while sprite_position > row_length:
        sprite_position -= row_length
    if register.value <= sprite_position <= register.value + 2:
        return True
    return False


def run_command_loop(
    commands: list[str], register: Register, test_function: RegisterValueFunction
) -> dict:
    results = {}
    results[register.cycle] = test_function(register)
    for command in commands:
        split = command.split()
        if len(split) == 1:
            register.noop()
        else:
            register.addx(int(split[1]))
        while register.locked:
            register.advance_cycle()
            results[register.cycle] = test_function(register)
    return results


def part_one(
    commands: list[str], register: Register, test_function: RegisterValueFunction
) -> int:
    register_history: RegisterHistory = run_command_loop(
        commands, register, test_function
    )
    total = 0
    for key, value in register_history.items():
        total += key * value
    return total


def part_two(
    commands: list[str], register: Register, test_function: RegisterValueFunction
) -> str:
    results = str()
    sprite_map: SpriteMap = run_command_loop(commands, register, test_function)
    counter = 0
    for sprite in sprite_map.values():
        if sprite:
            results += "#"
        else:
            results += "."
        counter += 1
        if counter == PART_TWO_ROW_LENGTH:
            results += "\n"
            counter = 0
    return results


def main() -> None:
    with open("day10/data.txt") as file:
        commands = [line.strip() for line in file.readlines()]

    part_one_func = partial(test_cycle_of_interest, cycles_of_interest=PART_ONE_CYCLES)
    print(part_one(commands, Register(), part_one_func))

    part_two_func = partial(test_sprite_hit, row_length=PART_TWO_ROW_LENGTH)
    print(part_two(commands, Register(), part_two_func))


if __name__ == "__main__":
    main()
