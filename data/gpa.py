"""
    gpa.py

    Contains the GPA class.
"""

from utils.file_manager import FileManager

class GPA:
    """
        Stores and manages the GPA information of the student.
    """

    def __init__(self) -> None:
        """
            Initialises the GPA data from files.
        """

        # gets data from files
        self.record = [[grade, credit_pts] for _, _, grade, credit_pts in FileManager.read_file("record")]
        self.data = FileManager.read_file("gpa")

    def get_record(self) -> list[list[str]]:
        """
            Returns the record GPA data.

            Returns:
                list[list[str]]: the record gpa data.
        """

        # returns the record array
        return [[i + 1] + self.record[i] for i in range(len(self.record))]

    def get_data(self) -> list[list[str]]:
        """
            Returns the extra GPA data.

            Returns:
                list[list[str]]: the extra GPA data.
        """

        # returns the data array
        return [[i + len(self.record) + 1] + self.data[i] for i in range(len(self.data))]

    def get_current_gpa(self) -> str:
        """
            Calculates and returns the current GPA.

            Returns:
                str: the gpa rounded to 3 decimal places.
        """

        # initialises total grade value and credits
        total_grade = 0
        total_credits = 0

        # iterates through each unit in the record
        for grade, credit_pts in self.record:

            # gets grade value
            match grade:
                case "WN":
                    grade_value = 0.0
                case "NH":
                    grade_value = 0.3
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
                case _:
                    continue

            # adds unit grade value and credits to totals
            total_grade += grade_value * int(credit_pts)
            total_credits += int(credit_pts)

        # checks if there are no units in the record
        if total_credits == 0:
            return "0.000"

        # calculates and returns gpa rounded to 3 decimal places
        gpa = total_grade / total_credits
        return f"{gpa:05.3f}"

    def get_calculated_gpa(self) -> str:
        """
            Calculates and returns the GPA with extra data.

            Returns:
                str: the GPA rounded to 3 decimal places.
        """

        # initialises total grade value and credits
        total_grade = 0
        total_credits = 0

        # iterates through each unit in the record
        for grade, credit_pts in self.record + self.data:

            # gets grade value
            match grade:
                case "WN":
                    grade_value = 0.0
                case "NH":
                    grade_value = 0.3
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
                case _:
                    continue

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
            Adds a unit to the GPA data.

            Args:
                unit (list[str]): the unit to add.
        """

        # appends the unit to the data array
        self.data.append(unit)

        # saves data to file
        FileManager.write_file("gpa", self.data)

    def remove_unit(self, unit_no: int) -> None:
        """
            Removes a unit in the GPA data.

            Args:
                unit_no (int): the unit to delete.
        """

        # deletes unit from data
        self.data.pop(unit_no - len(self.record) - 1)

        # saves data to file
        FileManager.write_file("gpa", self.data)

    def reset(self) -> None:
        """
            Reinitialises the GPA data from files.
        """

        # gets data from files
        self.record = [[grade, credit_pts] for _, _, grade, credit_pts in FileManager.read_file("record")]
        self.data = FileManager.read_file("gpa")
