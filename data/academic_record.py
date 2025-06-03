"""
    academic_record.py

    Contains an academic record class.
"""

from data.grade import Grade

class AcademicRecord:
    """
        Stores and manages the academic record of the student.
    """

    def __init__(self, data: list[list[str]]) -> None:
        """
            Initialises the academic record.
        """

        # initialises the record array
        self.data = []
        self.record = []

        self.set_data(data)

    def set_data(self, data: list[list[str]]) -> None:
        """
            Sets the academic record.

            Args:
                data (list[list[str]]): the raw record information.
        """

        self.data = data

        # clears record
        self.record = []

        # iterates through each unit and adds it to the record
        for unit_no, unit_code, mark, grade, credit_pts in data:
            self.record.append({"unit_no": int(unit_no),
                                "unit_code": unit_code,
                                "mark": int(mark),
                                "grade": Grade[grade],
                                "credit_pts": int(credit_pts)})
 
    def get_data(self) -> list[list[str]]:
        return self.data

    def wam(self) -> str:
        """
            Calculates and returns the WAM of the academic record.

            Returns:
                str: the WAM rounded to 3 decimal places.
        """

        # initialises total weighted marks and credits
        weighted_marks = 0
        weighted_credits = 0

        # iterates through each unit in the record
        for unit in self.record:

            # gets weighting of unit
            weight = 0.5 if unit["unit_code"][3] == '1' else 1.0

            # adds unit weighted marks and credits to totals
            weighted_marks += unit["mark"] * unit["credit_pts"] * weight
            weighted_credits += unit["credit_pts"] * weight

        if weighted_credits == 0:
            return "00.000"

        # calculates and returns wam rounded to 3 decimal places
        wam = weighted_marks / weighted_credits
        return f"{wam:06.3f}"

    def gpa(self) -> str:
        """
            Calculates and returns the GPA of the academic record.

            Returns:
                str: the GPA rounded to 3 decimal places.
        """

        # initialises total grade value and credits
        total_grade = 0
        total_credits = 0

        # iterates through each unit in the record
        for unit in self.record:

            # adds unit grade value and credits to totals
            total_grade += unit["grade"].value * unit["credit_pts"]
            total_credits += unit["credit_pts"]

        if total_credits == 0:
            return "0.000"

        # calculates and returns gpa rounded to 3 decimal places
        gpa = total_grade / total_credits
        return f"{gpa:05.3f}"
