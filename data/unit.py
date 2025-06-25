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

        # initialises data dictionary
        self.data = {}

        # gets unit files from file manager
        unit_files = FileManager.get_unit_files()

        # adds unit data to dictionary
        for unit_file in unit_files:
            self.data[unit_file] = FileManager.read_file(unit_file)

        # gets target data from file
        target = FileManager.read_file("target")

        # initialises target from file data
        if target:
            self.target = target[0][1]
            self.target_type = target[0][0]

        # initialises target for the first time
        else:
            self.target_type = "Grade"
            self.target = "HD"
            FileManager.write_file("target", [[self.target_type, self.target]])

    def add_unit(self, unit_code: str) -> None:
        """
            Adds a unit to the data.

            Args:
                unit_code (str): the unit code of the unit to add.
        """

        # adds unit to file system and refreshes
        FileManager.create_file(f"{unit_code}")
        self.reset()

    def remove_unit(self, unit_code: str) -> None:
        """
            Removes a unit from the data.

            Args:
                unit_code (str): the unit code of the unit to remove.
        """

        # removes unit from file system and refreshes
        FileManager.delete_file(f"{unit_code}")
        self.reset()

    def add_assessment(self, unit_code: str, assessment: list[str]) -> None:
        """
            Adds an assessment to the unit data.

            Args:
                unit_code (str): the unit code of the unit to add the assessment to.
                assessment (list[str]): the assessment to add.
        """

        # appends the assessment to the unit in the data dictionary
        self.data[unit_code].append(assessment)

        # saves data to file
        FileManager.write_file(f"{unit_code}", self.data[unit_code])

    def remove_assessment(self, unit_code: str, assessment_no: int) -> None:
        """
            Removes an assessment from the unit data.

            Args:
                unit_code (str): the unit code of the unit to remove an assessment from.
                assessment_no (int): the assessment to remove.
        """

        # removes the assessment from the unit in the data dictionary
        self.data[unit_code].pop(assessment_no)

        # saves data to file
        FileManager.write_file(f"{unit_code}", self.data[unit_code])

    def get_overview(self) -> list[list[str]]:
        """
            Returns the overview data.

            Returns:
                list[list[str]]: the overview data.
        """

        # gets overview for each unit and returns overview data
        return [self.get_unit_overview(unit_code) for unit_code in self.data]

    def get_unit_overview(self, unit_code: str) -> list[str]:
        """
            Gets the overview for a unit.

            Args:
                unit_code (str): the unit code of the unit.

            Returns:
                list[str]: the unit overview data.
        """

        # sets target if target type is grade
        if self.target_type == "Grade":
            match self.target:
                case "P":
                    target = 50
                case "C":
                    target = 60
                case "D":
                    target = 70
                case "HD":
                    target = 80

        # sets target if target type is mark
        elif self.target_type == "Mark":
            target = int(self.target)

        # initialises mark and weight totals
        total_mark = 0
        total_weight = 0

        # iterates through each assessment
        for _, weight, score, total in self.data[unit_code]:

            # adds mark and weight of assessment to totals
            total_mark += float(weight) * (float(score) / float(total))
            total_weight += float(weight)

        # checks if at least one assessment is in data
        if total_weight > 0:

            # calculates mark
            mark = round(total_mark * 100 / total_weight)

            # calculates grade
            if mark < 50:
                grade = "N"
            elif mark < 60:
                grade = "P"
            elif mark < 70:
                grade = "C"
            elif mark < 80:
                grade = "D"
            else:
                grade = "HD"

            # sets mark/grade string
            mark_grade = f"{mark} ({grade})"

        # no assessments entered
        else:
            mark_grade = "-"

        # calculates remaining assessments
        remaining = f"{100 - total_weight:.2f}"

        # calculates average required
        if total_weight < 100:
            avg_req_float = (target - total_mark) * 100 / (100 - total_weight)
        else:
            avg_req_float = -1

        # checks if average required is feasible
        if avg_req_float < 0 or avg_req_float > 100:
            avg_req = "-"

        # sets average required string
        else:
            avg_req = f"{avg_req_float:.2f}"

        # returns unit overview
        return [unit_code, mark_grade, remaining, avg_req]

    def get_unit_assessments(self, unit_code: str) -> list[list[str]]:
        """
            Gets the assessments of a unit for the assessments page.

            Args:
                unit_code (str): the unit code of the unit.

            Returns:
                list[list[str]]: the assessments for the unit.
        """

        # gets and returns the assessments for the unit
        return [[assessment, weight, f"{float(score) * 100 / float(total):.2f}"] for assessment, weight, score, total in self.data[unit_code]]

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
        FileManager.write_file("target", [[self.target_type, self.target]])

    def reset(self) -> None:
        """
            Reinitialises the unit data from files.
        """

        # initialises unit dictionary
        self.data = {}

        # gets unit files from file manager
        unit_files = FileManager.get_unit_files()

        # adds unit data to dictionary
        for unit_file in unit_files:
            self.data[unit_file] = FileManager.read_file(unit_file)

        # gets target data from file
        target = FileManager.read_file("target")
        self.target = target[0][1]
        self.target_type = target[0][0]
