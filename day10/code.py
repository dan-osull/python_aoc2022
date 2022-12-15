from dataclasses import dataclass

CYCLES_OF_INTEREST = [20, 60, 100, 140, 180, 220]
RegisterHistory = dict[int, int]
"""Key = register.cycle, value = register.value"""


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

    def refresh_value(self) -> None:
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


def main_loop(
    data: list[str], register: Register, cycles_of_interest: list[int]
) -> RegisterHistory:
    register_history: RegisterHistory = {}

    for next_command in data:
        save_register_data(register_history, register, cycles_of_interest)
        split = next_command.split()
        if len(split) == 1:
            register.noop()
        else:
            register.addx(int(split[1]))
        while register.locked:
            register.advance_cycle()
            register.refresh_value()
            save_register_data(register_history, register, cycles_of_interest)

    return register_history


def part_one() -> None:
    with open("day10/data.txt") as file:
        data = [line.strip() for line in file.readlines()]

    register = Register()
    register_history = main_loop(data, register, CYCLES_OF_INTEREST)

    total = 0
    for key, value in register_history.items():
        total += key * value
    print(total)


if __name__ == "__main__":
    part_one()
