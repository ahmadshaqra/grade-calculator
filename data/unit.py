"""
    unit.py

    Contains the unit class.
"""

from utils.file_manager import FileManager

class Unit:
    """
        Stores and manages the unit information of the student.
    """

    def __init__(self) -> None:
        """
            Initialises the unit data from files.
        """

        # initialises unit dictionary
        self.unit = {}

        # gets unit files from file manager
        unit_files = FileManager.get_unit_files()

        # adds unit data to dictionary
        for unit_file in unit_files:
            self.unit[unit_file[:-4]] = FileManager.read_file(unit_file)

        # gets target data from file
        target = FileManager.read_file("target.txt")

        # initialises target from file data
        if target:
            self.target = target[0][1]
            self.target_type = target[0][0]

        # initialises target for the first time
        else:
            self.target_type = "Grade"
            self.target = "HD"
            FileManager.write_file("target.txt", [[self.target_type, self.target]])

    def add_unit(self, unit_code: str) -> None:
        """
            Adds a unit to the data.

            Args:
                unit_code (str): the unit code of the unit to add.
        """

        # adds unit to file system and refreshes
        FileManager.create_file(f"{unit_code}.txt")
        self.reset()

    def remove_unit(self, unit_code: str) -> None:
        """
            Removes a unit from the data.

            Args:
                unit_code (str): the unit code of the unit to remove.
        """

        # removes unit from file system and refreshes
        FileManager.delete_file(f"{unit_code}.txt")
        self.reset()

    def get_overview(self) -> list[list[str]]:
        """
            Returns the overview data.

            Returns:
                list[list[str]]: the overview data.
        """

        return [[unit_code, "-", "-", "-"] for unit_code in self.unit]

    def get_target(self) -> str:
        """
            Returns formated target string.

            Returns:
                str: the formated target string.
        """

        # returns target type and target value
        return f"Target {self.target_type}: {self.target}"

    def change_target(self, target_type: str, target: str) -> None:
        """
            Sets new target.

            Args:
                target_type (str): the new target type.
                target (str): the new target.
        """

        # sets new target type and target
        self.target_type = target_type
        self.target = target

        # saves new target to file
        FileManager.write_file("target.txt", [[self.target_type, self.target]])

    def reset(self) -> None:
        """
            Reinitialises the unit data from files.
        """

        # initialises unit dictionary
        self.unit = {}

        # gets unit files from file manager
        unit_files = FileManager.get_unit_files()

        # adds unit data to dictionary
        for unit_file in unit_files:
            self.unit[unit_file[:-4]] = FileManager.read_file(unit_file)

        # gets target data from file
        target = FileManager.read_file("target.txt")
        self.target = target[0][1]
        self.target_type = target[0][0]
