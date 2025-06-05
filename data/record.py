"""
    record.py

    Contains the record class.
"""

from utils.file_manager import FileManager

class Record:
    """
        Stores and manages the record of the student.
    """

    def __init__(self) -> None:
        """
            Initialises the record from file.
        """

        # gets data from file
        self.data = FileManager.read_file("record.txt")

    def get_data(self) -> list[list[str]]:
        """
            Returns the record.

            Returns:
                list[list[str]]: the record.
        """

        # returns the data array
        return self.data

    def get_wam(self) -> str:
        """
            Calculates and returns the WAM of the record.

            Returns:
                str: the WAM rounded to 3 decimal places.
        """

        # initialises total weighted marks and credits
        weighted_marks = 0
        weighted_credits = 0

        # iterates through each unit in the record
        for _, unit_code, mark, _, credit_pts in self.data:

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

    def get_gpa(self) -> str:
        """
            Calculates and returns the GPA of the record.

            Returns:
                str: the GPA rounded to 3 decimal places.
        """

        # initialises total grade value and credits
        total_grade = 0
        total_credits = 0

        # iterates through each unit in the record
        for _, _, _, grade, credit_pts in self.data:

            # gets grade value
            match grade:
                case "WN":
                    grade_value = 0.0
                case "N":
                    grade_value = 0.3
                case "P":
                    grade_value = 1.0
                case "C":
                    grade_value = 2.0
                case "D":
                    grade_value = 3.0
                case "HD":
                    grade_value = 4.0

            # adds unit grade value and credits to totals
            total_grade += grade_value * int(credit_pts)
            total_credits += int(credit_pts)

        # checks if there are no units in the record
        if total_credits == 0:
            return "0.000"

        # calculates and returns gpa rounded to 3 decimal places
        gpa = total_grade / total_credits
        return f"{gpa:05.3f}"

    def add_unit(self, unit: list[str]) -> None:
        """
            Adds a unit to the record.

            Args:
                unit (list[str]): the unit to add.
        """

        # appends the unit to the data array
        self.data.append([str(len(self.data) + 1)] + unit)

    def remove_unit(self) -> None:
        """
            Removes the last unit in the record.
        """

        # checks if there are units in the data array
        if len(self.data) > 0:

            # removes the last unit from the data array
            self.data.pop()

    def save(self) -> None:
        """
            Saves the record to file.
        """

        # writes data to file
        FileManager.write_file("record.txt", self.data)

    def reset(self) -> None:
        """
            Reinitialises the record from file.
        """

        # gets data from file
        self.data = FileManager.read_file("record.txt")
