import pytest

from day10.code import Register, part_one_loop


@pytest.fixture
def test_data():
    return [
        "noop",
        "addx 3",
        "addx -5",
    ]


def test_main_loop(test_data: list[str]):
    register_history = part_one_loop(test_data, Register(), [1, 2, 3, 4, 5, 6])
    assert register_history == {1: 1, 2: 1, 3: 1, 4: 4, 5: 4, 6: -1}
