"""
    academic_record.py

    Contains an academic record class.
"""

from utils.file_manager import FileManager

class AcademicRecord:
    """
        Stores and manages the academic record of the student.
    """

    def __init__(self) -> None:
        """
            Initialises the academic record.
        """

        # gets data from file
        self.data = FileManager.read_file("record.txt")

    def get_data(self) -> list[list[str]]:
        return self.data

    def get_wam(self) -> str:
        """
            Calculates and returns the WAM of the academic record.

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

        if weighted_credits == 0:
            return "00.000"

        # calculates and returns wam rounded to 3 decimal places
        wam = weighted_marks / weighted_credits
        return f"{wam:06.3f}"

    def get_gpa(self) -> str:
        """
            Calculates and returns the GPA of the academic record.

            Returns:
                str: the GPA rounded to 3 decimal places.
        """

        # initialises total grade value and credits
        total_grade = 0
        total_credits = 0

        # iterates through each unit in the record
        for _, _, _, grade, credit_pts in self.data:

            # adds unit grade value and credits to totals
            total_grade += self.grade_value(grade) * int(credit_pts)
            total_credits += int(credit_pts)

        if total_credits == 0:
            return "0.000"

        # calculates and returns gpa rounded to 3 decimal places
        gpa = total_grade / total_credits
        return f"{gpa:05.3f}"

    def grade_value(self, grade: str) -> float:
        
        match grade:
            case "WN":
                return 0.0
            case "N":
                return 0.3
            case "P":
                return 1.0
            case "C":
                return 2.0
            case "D":
                return 3.0
            case "HD":
                return 4.0

    def remove_unit(self) -> None:
        if len(self.data) > 0:
            self.data.pop()
    
    def add_unit(self, unit: list[str]) -> None:
        self.data.append(unit)
