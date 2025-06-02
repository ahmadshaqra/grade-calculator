"""
    file_manager.py

    Contains the file manager class.
"""

import os

class FileManager:
    """
        Manages all files read and written in the program.
    """

    def __init__(self):
        self.folder = os.path.join(os.path.expanduser("~"), "GradeCalculator")
        os.makedirs(self.folder, exist_ok=True)
    
    def read_file(self, filename: str) -> list[list[str]]:
        try:
            with open(os.path.join(self.folder, filename), 'r') as file:
                return [line.split() for line in file]
        except FileNotFoundError:
            return []

    def write_file(self, filename: str, contents: list[list[str]]) -> None:
        with open(os.path.join(self.folder, filename), 'w') as file:
            for index, line in enumerate(contents):
                file.write(" ".join(line))
                if index < len(contents) - 1: file.write('\n')
            
if __name__ == "__main__":
    filemanager = FileManager()
    contents = filemanager.read_file("record.txt")
    filemanager.write_file("test.txt", contents)
