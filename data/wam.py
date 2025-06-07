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
        self.record = [[unit_code[3], mark, credit_pts] for unit_code, mark, _, credit_pts in FileManager.read_file("record.txt")]
        self.data = FileManager.read_file("wam.txt")

    def get_record(self) -> list[list[str]]:
        """
            Returns the record WAM data.

            Returns:
                list[list[str]]: the record WAM data.
        """

        # returns the record array
        return [[i + 1] + self.record[i] for i in range(len(self.record))]

    def get_data(self) -> list[list[str]]:
        """
            Returns the extra WAM data.

            Returns:
                list[list[str]]: the extra WAM data.
        """

        # returns the data array
        return [[i + len(self.record) + 1] + self.data[i] for i in range(len(self.data))]

    def get_current_wam(self) -> str:
        """
            Calculates and returns the current WAM.

            Returns:
                str: the WAM rounded to 3 decimal places.
        """

        # initialises total weighted marks and credits
        weighted_marks = 0
        weighted_credits = 0

        # iterates through each unit in the record
        for year_lvl, mark, credit_pts in self.record:

            # gets weighting of unit
            weight = 0.5 if year_lvl == '1' else 1.0

            # adds unit weighted marks and credits to totals
            weighted_marks += int(mark) * int(credit_pts) * weight
            weighted_credits += int(credit_pts) * weight

        # checks if there are no units in the record
        if weighted_credits == 0:
            return "00.000"

        # calculates and returns wam rounded to 3 decimal places
        wam = weighted_marks / weighted_credits
        return f"{wam:06.3f}"

    def get_calculated_wam(self) -> str:
        """
            Calculates and returns the WAM with extra data.

            Returns:
                str: the WAM rounded to 3 decimal places.
        """

        # initialises total weighted marks and credits
        weighted_marks = 0
        weighted_credits = 0

        # iterates through each unit in the record
        for year_lvl, mark, credit_pts in self.record + self.data:

            # gets weighting of unit
            weight = 0.5 if year_lvl == '1' else 1.0

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
        self.data.append(unit)

        # saves data to file
        FileManager.write_file("wam.txt", self.data)

    def remove_unit(self, unit_no: int) -> None:
        """
            Removes a unit in the WAM data.

            Args:
                unit_no (int): the unit to delete.
        """

        # deletes unit from data
        self.data.pop(unit_no - len(self.record) - 1)

        # saves data to file
        FileManager.write_file("wam.txt", self.data)

    def reset(self) -> None:
        """
            Reinitialises the WAM data from files.
        """

        # gets data from files
        self.record = [[unit_code[3], mark, credit_pts] for unit_code, mark, _, credit_pts in FileManager.read_file("record.txt")]
        self.data = FileManager.read_file("wam.txt")
