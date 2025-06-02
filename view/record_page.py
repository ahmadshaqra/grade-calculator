"""
    record_page.py

    Contains the record page UI logic.
"""

import tkinter as tk
from tkinter import ttk

class RecordPage(tk.Frame):
    """
        Manages the record page.
    """

    def __init__(self, root: tk.Frame) -> None:
        """
            Initialises the record page.

            Args:
                root (tk.Frame): the main contents frame.
        """

        # initialises the frame
        super().__init__(root)

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

    def refresh(self) -> None:
        pass

    def add_unit(self) -> None:
        pass

    def remove_unit(self) -> None:
        pass

    def save_record(self) -> None:
        pass
