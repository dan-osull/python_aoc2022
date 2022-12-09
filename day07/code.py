from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Directory:
    name: str
    parent: Optional[Directory] = None
    child_files: list[File] = field(default_factory=list)
    _child_dirs: list[Directory] = field(default_factory=list)

    @property
    def child_dirs(self) -> list[Directory]:
        return self._child_dirs

    def navigate_to_child(self, name: str) -> Directory:
        """Adds directory to child_dirs. Returns child object."""
        new_child_dir = Directory(name=name, parent=self)
        self._child_dirs.append(new_child_dir)
        return new_child_dir

    def get_child_file_size(self) -> int:
        """Size of files in this directory only"""
        return sum(file.size for file in self.child_files) if self.child_files else 0

    def get_dir_size(self) -> int:
        """Size of directory including all child directories"""
        total = self.get_child_file_size()
        for child_dir in self.child_dirs:
            total += child_dir.get_dir_size()
        return total

    def get_descendent_dirs(self) -> list[Directory]:
        results = self.child_dirs.copy()
        for item in self.child_dirs:
            if item.child_dirs:
                child_items = item.get_descendent_dirs()
                results.extend(child_items)
        return results


@dataclass
class File:
    name: str
    size: int


def get_ls_results(line_idx: int, data: list[str]) -> list[File]:
    files: list[File] = []
    for line in data[line_idx + 1 :]:
        if line[0] == "$":
            # End of file list reached
            break
        split = line.split()
        if split[0] == "dir":
            # Not collecting dir info at this point
            continue
        files.append(File(split[1], int(split[0])))
    return files


def part_one(filesystem: Directory) -> int:
    all_dirs = filesystem.get_descendent_dirs()
    assert all_dirs
    selected_dirs = [item for item in all_dirs if item.get_dir_size() <= 100000]
    return sum(item.get_dir_size() for item in selected_dirs)


def part_two(filesystem: Directory) -> int:
    space_needed = 30000000 - (70000000 - filesystem.get_dir_size())
    all_dirs = filesystem.get_descendent_dirs()
    assert all_dirs
    return min(
        item.get_dir_size() for item in all_dirs if item.get_dir_size() >= space_needed
    )


def main() -> None:
    with open("day07/data.txt") as file:
        data = [line.strip() for line in file.readlines()]

    filesystem = Directory(name="/")
    current_dir = filesystem

    for i, line in enumerate(data):
        if line == "$ cd /":
            # Root has already been made
            continue
        elif line == "$ cd ..":
            assert current_dir.parent, "No parent to navigate to"
            current_dir = current_dir.parent
        elif line.startswith("$ cd "):
            current_dir = current_dir.navigate_to_child(line.split()[2])
        elif line == "$ ls":
            ls_results = get_ls_results(i, data)
            current_dir.child_files = ls_results

    print(part_one(filesystem))
    print(part_two(filesystem))


if __name__ == "__main__":
    main()
