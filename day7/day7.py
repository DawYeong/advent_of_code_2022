from typing import Dict, List, Optional
import os

SCRIPT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "input.txt"
DIR_NAME = "dir"
CD_NAME = "cd"


# dirty classes => hybrid between object oriented and dataclass :/
# has logic and getters => can in the future try to fix these classes to be cleaner
class Folder:
    _folder_name: str
    _parent: Optional["Folder"]
    _files: Dict[str, int]
    _folders: List["Folder"]

    def __init__(self, folder_name: str, parent: Optional["Folder"]):
        self._folder_name = folder_name
        self._parent = parent
        self._files = {}
        self._folders = []

    def add_child_folder(self, folder_name: str):
        new_folder = Folder(
            folder_name=folder_name,
            parent=self,
        )
        self._folders.append(new_folder)

    def add_file(self, file_name: str, file_size: int):
        self._files[file_name] = file_size

    def get_matching_folder(self, folder_name: str) -> Optional["Folder"]:
        for folder in self._folders:
            if folder._folder_name == folder_name:
                return folder
        return None

    def get_parent(self) -> Optional["Folder"]:
        return self._parent

    def get_total_file_sizes(self) -> int:
        return sum(self._files.values())

    def get_folders(self) -> List["Folder"]:
        return self._folders

    def get_folder_name(self) -> str:
        return self._folder_name


class FileSystem:
    _root: Folder
    _curr_folder: Folder
    _total_sizes: Dict[str, int]

    def __init__(self, root: Folder):
        self._root = root
        self._curr_folder = root
        self._total_sizes = {}

    def move_to_folder(self, folder_name: str):
        move_folder = self._curr_folder.get_matching_folder(folder_name)
        if move_folder:
            self._curr_folder = move_folder

    def move_to_root(self):
        self._curr_folder = self._root

    def move_back(self):
        parent = self._curr_folder.get_parent()
        if parent:
            self._curr_folder = parent

    def add_folder(self, folder_name: str):
        self._curr_folder.add_child_folder(folder_name)

    def add_file(self, file_name: str, file_size: int):
        self._curr_folder.add_file(
            file_name=file_name,
            file_size=file_size,
        )

    def get_total_sizes(self, folder: Folder) -> int:
        # add files at this level
        # then add folders => step into folder
        file_sizes = folder.get_total_file_sizes()
        for child_folder in folder.get_folders():
            file_sizes += self.get_total_sizes(child_folder)

        folder_name = folder.get_folder_name()
        # pretty hacky, there are going to be folders with the same name that will be overwritten
        # adding prefix if folder name already exists (can change it to path name to avoid this hack)
        key_name = (
            f"{folder_name}_{len(self._total_sizes.items())}"
            if self._total_sizes.get(folder_name, None)
            else folder_name
        )
        self._total_sizes[key_name] = file_sizes
        return file_sizes

    def get_root(self) -> Folder:
        return self._root

    def get_folder_sizes(self) -> Dict[str, int]:
        return self._total_sizes


def get_input_data(file_name: str) -> List[str]:
    with open(file_name, "r") as file:
        data = file.read()

    return data.split("\n")


def build_file_system(commands: str) -> FileSystem:
    root = Folder(
        folder_name="/",
        parent=None,
    )
    file_system = FileSystem(root)

    for command in commands:
        command_values = command.split(" ")
        if command_values[0] == "$":
            if command_values[1] == CD_NAME:
                if command_values[2] == "/":
                    file_system.move_to_root()
                elif command_values[2] == "..":
                    file_system.move_back()
                else:
                    file_system.move_to_folder(command_values[2])
        elif command_values[0] == DIR_NAME:
            file_system.add_folder(command_values[1])
        else:
            file_system.add_file(
                file_name=command_values[1], file_size=int(command_values[0])
            )
    file_system.get_total_sizes(file_system.get_root())

    return file_system


def find_smallest_folder_to_delete(space_required: int, folder_sizes: List[int]) -> int:
    for folder_size in folder_sizes:
        if folder_size > space_required:
            return folder_size


def solve_part_1(file_name: str):
    commands = get_input_data(file_name)
    file_system = build_file_system(commands)
    folder_sizes = file_system.get_folder_sizes()
    filtered_folders = {k: v for k, v in folder_sizes.items() if v <= 100000}

    print(sum(filtered_folders.values()))


def solve_part_2(file_name: str):
    commands = get_input_data(file_name)
    file_system = build_file_system(commands)
    folder_sizes = list(file_system.get_folder_sizes().values())
    folder_sizes.sort()

    space_required = 30000000 - (70000000 - folder_sizes[len(folder_sizes) - 1])
    smallest_folder = find_smallest_folder_to_delete(
        space_required=space_required,
        folder_sizes=folder_sizes,
    )
    print(smallest_folder)


if __name__ == "__main__":
    solve_part_2(f"{SCRIPT_FOLDER_PATH}/{FILE_NAME}")
