"""
    wam.py

    Contains the WAM class.
"""

from utils.file_manager import FileManager

class WAM:
    """
        Stores and manages the WAM information of the student.
    """

    def __init__(self) -> None:
        """
            Initialises the WAM data from files.
        """

        # gets data from files
        self.record = [[unit_no, unit_code[3], mark, credit_pts] for unit_no, unit_code, mark, _, credit_pts in FileManager.read_file("record.txt")]
        self.data = FileManager.read_file("wam.txt")

    def get_record(self) -> list[list[str]]:
        """
            Returns the record WAM data.

            Returns:
                list[list[str]]: the record WAM data.
        """

        # returns the record array
        return self.record

    def get_data(self) -> list[list[str]]:
        """
            Returns the extra WAM data.

            Returns:
                list[list[str]]: the extra WAM data.
        """

        # returns the data array
        return self.data

    def get_wam(self) -> str:
        """
            Calculates and returns the WAM.

            Returns:
                str: the WAM rounded to 3 decimal places.
        """

        # initialises total weighted marks and credits
        weighted_marks = 0
        weighted_credits = 0

        # iterates through each unit in the record
        for _, unit_code, mark, credit_pts in self.record + self.data:

            # gets weighting of unit
            weight = 0.5 if unit_code[3] == '1' else 1.0

            # adds unit weighted marks and credits to totals
            weighted_marks += int(mark) * int(credit_pts) * weight
            weighted_credits += int(credit_pts) * weight

        # checks if there are no units in the record
        if weighted_credits == 0:
            return "00.000"

        # calculates and returns wam rounded to 3 decimal places
        wam = weighted_marks / weighted_credits
        return f"{wam:06.3f}"

    def add_unit(self, unit: list[str]) -> None:
        """
            Adds a unit to the WAM data.

            Args:
                unit (list[str]): the unit to add.
        """

        # appends the unit to the data array
        self.data.append([str(len(self.record) + len(self.data) + 1)] + unit)

        # saves data to file
        FileManager.write_file("wam.txt", self.data)

    def remove_unit(self) -> None:
        """
            Removes the last unit in the WAM data.
        """

        # checks if there are units in the data array
        if len(self.data) > 0:

            # removes the last unit from the data array
            self.data.pop()

            # saves data to file
            FileManager.write_file("wam.txt", self.data)

    def reset(self) -> None:
        """
            Reinitialises the WAM data from files.
        """

        # gets data from files
        self.record = [[unit_no, unit_code[3], mark, credit_pts] for unit_no, unit_code, mark, _, credit_pts in FileManager.read_file("record.txt")]
        self.data = FileManager.read_file("wam.txt")
