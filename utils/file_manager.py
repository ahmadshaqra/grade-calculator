"""
    file_manager.py

    Contains the file manager utility class.
"""

import os
from re import compile

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
            with open(os.path.join(cls.folder, filename), "r") as file:

                # returns the table of contents in the file
                return [line.strip().split(",") for line in file]

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
        with open(os.path.join(cls.folder, filename), "w") as file:

            # iterates through the data
            for index, line in enumerate(data):

                # writes a space-separated line of the data line
                file.write(",".join(line))
                if index < len(data) - 1: file.write("\n")

    @classmethod
    def create_file(cls, filename: str) -> None:
        """
            Creates a file.

            Args:
                filename (str): the name of the file to created.
        """

        # gets filepath
        filepath = os.path.join(cls.folder, filename)

        # creates file
        with open(filepath, "w") as file:
            pass

    @classmethod
    def delete_file(cls, filename: str) -> None:
        """
            Deletes a file.

            Args:
                filename (str): the name of the file to delete.
        """

        # gets filepath
        filepath = os.path.join(cls.folder, filename)

        # checks if file exists
        if os.path.exists(filepath):

            # deletes file
            os.remove(filepath)

    @classmethod
    def get_unit_files(cls) -> list[str]:
        """
            Finds the filenames of all unit files in the project directory.

            Returns:
                list[str]: the list of unit filenames.
        """

        # sets the unit filename regular expression
        unit_filename = compile(r"[A-Z]{3}\d{4}\.txt")

        # finds all unit filenames
        unit_files = [
            file for file in os.listdir(cls.folder)
            if os.path.isfile(os.path.join(cls.folder, file)) and unit_filename.match(file)
        ]

        # returns the list of unit filenames
        return unit_files
