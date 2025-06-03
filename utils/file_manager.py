"""
    file_manager.py

    Contains the file manager utility class.
"""

import os

class FileManager:
    """
        Manages all files read and written in the program.
    """

    # initialises folder path and creates the directory
    folder = os.path.join(os.path.expanduser("~"), "GradeCalculator")
    os.makedirs(folder, exist_ok=True)

    @classmethod
    def read_file(cls, filename: str) -> list[list[str]]:
        """
            Reads and processes a file.

            Args:
                filename (str): the name of the file to read.

            Returns:
                list[list[str]]: the contents of the file.
        """

        # attempts to open the file
        try:
            with open(os.path.join(cls.folder, filename), 'r') as file:

                # returns the table of contents in the file
                return [line.split() for line in file]

        # file does not exist
        except FileNotFoundError:

            # returns an empty array
            return []

    @classmethod
    def write_file(cls, filename: str, data: list[list[str]]) -> None:
        """
            Writes data to a file.

            Args:
                filename (str): the name of the file to write to.
                data (list[list[str]]): the data to write to the file.
        """

        # opens the file
        with open(os.path.join(cls.folder, filename), 'w') as file:

            # iterates through the data
            for index, line in enumerate(data):

                # writes a space-separated line of the data line
                file.write(" ".join(line))
                if index < len(data) - 1: file.write('\n')
