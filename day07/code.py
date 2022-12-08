from __future__ import annotations

from typing import Optional
from dataclasses import dataclass, field


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
        """
        Adds directory to child_dirs if missing.
        Returns child object.
        """
        existing_entry = next(
            (item for item in self._child_dirs if item.name == name), None
        )
        if existing_entry:
            return existing_entry
        new_child_dir = Directory(name=name, parent=self)
        self._child_dirs.append(new_child_dir)
        return new_child_dir

    @property
    def child_file_size(self) -> int:
        """Size of files in this directory"""
        if not self.child_files:
            return 0
        return sum(file.size for file in self.child_files)

    @property
    def dir_size(self) -> int:
        """Includes all child directories"""
        total = self.child_file_size
        for child_dir in self.child_dirs:
            total += child_dir.dir_size
        return total

    def get_all_descendent_dirs(self) -> Optional[list[Directory]]:
        if not self.child_dirs:
            return None
        results = self.child_dirs
        for item in self.child_dirs:
            if item.child_dirs:
                results.extend(item.child_dirs)
        return results


@dataclass
class File:
    name: str
    size: int


def get_ls_results(line_idx: int, data: list[str]) -> Optional[list[File]]:
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
    if files:
        return files


def part_one(filesystem: Directory) -> int:
    all_dirs = filesystem.get_all_descendent_dirs()
    assert all_dirs
    selected_dirs = [item for item in all_dirs if item.dir_size <= 100000]
    return sum(item.dir_size for item in selected_dirs)


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
            if ls_results:
                current_dir.child_files = ls_results

    print(part_one(filesystem))


if __name__ == "__main__":
    main()
