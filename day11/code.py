from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class MonkeyCollection:
    monkeys: list[Monkey] = field(default_factory=list)

    def get_by_id(self, id_: int) -> Monkey:
        return next(item for item in self.monkeys if item.id_ == id_)


@dataclass
class Monkey:
    id_: int
    items: list[int]
    operation_type: Literal["+", "*"]
    operation_value: int | Literal["old"]
    divisible_test_number: int
    target_if_true: int
    target_if_false: int
    items_inspected: int = 0

    def process_items(self, collection: MonkeyCollection) -> None:
        for item in self.items:
            self.items_inspected += 1
            # Item value is current worry level
            new_value = self.get_new_item_value(item)
            if new_value % self.divisible_test_number == 0:
                target_id = self.target_if_true
            else:
                target_id = self.target_if_false
            collection.get_by_id(target_id).items.append(new_value)
        self.items = []

    def get_new_item_value(self, item: int) -> int:
        item_two = (
            self.operation_value if isinstance(self.operation_value, int) else item
        )
        if self.operation_type == "+":
            return int((item + item_two) / 3)
        return int((item * item_two) / 3)

    @classmethod
    def from_input_data(cls, data: list[str]) -> Monkey:
        id_ = next(int(char) for char in data[0] if char.isdigit())
        items = [
            int(item) for item in data[1].replace("Starting items: ", "").split(",")
        ]
        operation_type = next(char for char in data[2] if char in ["+", "*"])
        operation_value = data[2].split()[-1]
        if operation_value.isdigit():
            operation_value = int(operation_value)
        divisible_test_number = int(data[3].split()[-1])
        target_if_true = int(data[4].split()[-1])
        target_if_false = int(data[5].split()[-1])
        return cls(
            **{
                key: value
                for key, value in locals().items()
                if key in cls.__dataclass_fields__
            }
        )


def divide_into_chunks(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i : i + size]


def parse_input(data: list[str]) -> MonkeyCollection:
    collection = MonkeyCollection()
    chunks = divide_into_chunks(data, 6)
    for chunk in chunks:
        collection.monkeys.append(Monkey.from_input_data(chunk))
    return collection


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    with open("day11/data.txt") as file:
        data = [line.strip() for line in file.readlines() if line.strip()]
    collection = parse_input(data)
    for round in range(20):
        logging.info(f"{round=}")
        for monkey in collection.monkeys:
            monkey.process_items(collection)
    items_inspected = [item.items_inspected for item in collection.monkeys]
    top_two = sorted(items_inspected, reverse=True)[:2]
    print(top_two[0] * top_two[1])


if __name__ == "__main__":
    main()
