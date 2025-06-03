"""
    record_page.py

    Contains the record page logic.
"""

import tkinter as tk
from tkinter import ttk
from data.academic_record import AcademicRecord
from utils.file_manager import FileManager

class RecordPage(tk.Frame):
    """
        Manages the record page.
    """

    def __init__(self, root: tk.Frame, academic_record: AcademicRecord) -> None:
        """
            Initialises the record page.

            Args:
                root (tk.Frame): the main contents frame.
                academic_record (AcademicRecord): the academic record of the student.
        """

        # initialises the frame
        super().__init__(root)
        self.academic_record = academic_record

        # sets frame to hold table
        table_frame = tk.Frame(self, width=500, height=190)
        table_frame.pack(pady=5)
        table_frame.grid_propagate(False)

        # sets columns of the table
        columns = ["Unit #", "Unit Code", "Mark", "Grade", "Credit Points"]

        # initialises table
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        # adds columns to the table
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=96)

        # initialises scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # adds table and scrollbar to the frame
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # sets frame to hold control buttons
        control_frame = tk.Frame(self)
        control_frame.pack(pady=5)

        # adds the control buttons
        tk.Button(control_frame, text="Add Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_unit()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Remove Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.remove_unit()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Save Record", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.save_record()).pack(side="left", expand=True, fill="both", padx=10)

        # sets frame to hold results information
        results_frame = tk.Frame(self)
        results_frame.pack(pady=5)

        # adds wam information label
        tk.Label(results_frame, text="WAM:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.wam_lbl = tk.Label(results_frame, text="00.000", font=("Segoe UI", 10))
        self.wam_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

        # adds gpa information label
        tk.Label(results_frame, text="GPA:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.gpa_lbl = tk.Label(results_frame, text="0.000", font=("Segoe UI", 10))
        self.gpa_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

    def load_page(self) -> None:
        """
            Loads page from data.
        """

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from academic record to table
        for unit in self.academic_record.get_data():
            self.table.insert("", "end", values=unit)

        # set wam and gpa
        self.wam_lbl.config(text=self.academic_record.get_wam())
        self.gpa_lbl.config(text=self.academic_record.get_gpa())

    def add_unit(self) -> None:
        pass

        """
            Add entry boxes to record page.
            Entry boxes needed: Unit Code, Mark, Grade, Credit Points.
            Make main window bigger.
            Handle add unit logic.
        """

    def remove_unit(self) -> None:
        """
            Removes the last unit.
        """

        # deletes the last row of the table
        rows = self.table.get_children()
        if len(rows) > 0:
            self.table.delete(rows[-1])

        # removes the last unit in the record
        self.academic_record.remove_unit()

        # updates wam and gpa
        self.wam_lbl.config(text=self.academic_record.get_wam())
        self.gpa_lbl.config(text=self.academic_record.get_gpa())

    def save_record(self) -> None:
        """
            Saves the current record.
        """

        # gets the record data and writes it to a file
        FileManager.write_file("record.txt", self.academic_record.get_data())
