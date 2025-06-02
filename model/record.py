"""
    record.py

    Contains a singleton academic record class.
"""

from __future__ import annotations
from model.grade import Grade
from controller.file_manager import FileManager

class Record:
    """
        Stores and manages the academic record of the student.
    """

    # initialises the instance pointer
    instance = None

    def __new__(cls) -> Record:
        """
            Returns the only instance of the academic record.
        """

        # checks if an instance exists
        if cls.instance is None:

            # creates a new instance
            cls.instance = super().__new__(cls)

        # returns the instance
        return cls.instance

    def __init__(self) -> None:
        """
            Initialises the academic record.
        """

        # initialises the record array
        self.record = []

    def set_record(self, record: list[list[str]]) -> None:
        # unit_code:str mark:str grade:str credit_pts:str
        pass

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

        # calculates and returns gpa rounded to 3 decimal places
        gpa = total_grade / total_credits
        return f"{gpa:05.3f}"
