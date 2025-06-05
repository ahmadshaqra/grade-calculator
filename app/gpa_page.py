"""
    gpa_page.py

    Contains the GPA page logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.gpa import GPA

class GPAPage(tk.Frame):
    """
        Manages the GPA page.
    """

    def __init__(self, root: tk.Frame) -> None:
        """
            Initialises the GPA page.

            Args:
                root (tk.Frame): the main contents frame.
        """

        # initialises the frame and initialises gpa
        super().__init__(root)
        self.gpa = GPA()

        # sets frame to hold table
        table_frame = tk.Frame(self, width=500, height=235)
        table_frame.pack()
        table_frame.grid_propagate(False)

        # sets the style of the table
        style = ttk.Style(self)
        style.theme_use("alt")
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="lightgrey", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("!active", "lightgrey"), ("active", "lightgrey"), ("pressed", "lightgrey")])

        # sets columns of the table
        self.columns = ["Unit #", "Grade", "Credit Points"]
        self.column_width = 160

        # initialises table
        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=10)

        # adds columns to the table
        for column in self.columns:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=self.column_width, minwidth=self.column_width, stretch=False)

        # disabling row selection and column size change
        self.table.bind("<<TreeviewSelect>>", self.disable_row_selection)
        self.table.bind("<ButtonRelease-1>", self.lock_column_sizes)

        # add tag for current record
        self.table.tag_configure("current", background="whitesmoke")

        # initialises scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # adds table and scrollbar to the frame
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # sets frame to hold add unit entry boxes
        add_unit_frame = tk.Frame(self)
        add_unit_frame.pack(pady=10)

        # adds grade label and entry box
        tk.Label(add_unit_frame, text="Grade: ", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(10,0))
        self.grade = tk.Entry(add_unit_frame, width=5, font=("Segoe UI", 10))
        self.grade.pack(side="left", expand=True, fill="both", padx=(0,10))
        self.grade.bind("<Return>", self.on_enter)

        # adds credit points label and entry box
        tk.Label(add_unit_frame, text="Credit Points: ", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(10,0))
        self.credit_pts = tk.Entry(add_unit_frame, width=5, font=("Segoe UI", 10))
        self.credit_pts.pack(side="left", expand=True, fill="both", padx=(0,10))
        self.credit_pts.bind("<Return>", self.on_enter)

        # sets frame to hold control buttons
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # adds the control buttons
        tk.Button(control_frame, text="Add Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_unit()).pack(side="left", expand=True, fill="both", padx=10)
        self.remove_unit_btn = tk.Button(control_frame, text="Remove Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.remove_unit())
        self.remove_unit_btn.pack(side="left", expand=True, fill="both", padx=10)

        # sets frame to hold results information
        results_frame = tk.Frame(self)
        results_frame.pack(pady=5)

        # adds current gpa information label
        tk.Label(results_frame, text="Current GPA:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.current_gpa_lbl = tk.Label(results_frame, text="0.000", font=("Segoe UI", 10))
        self.current_gpa_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

        # adds calculated gpa information label
        tk.Label(results_frame, text="Calculated GPA:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.calculated_gpa_lbl = tk.Label(results_frame, text="0.000", font=("Segoe UI", 10))
        self.calculated_gpa_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

        # creates a hidden focus point
        self.focus = tk.Canvas(self, width=0, height=0, highlightthickness=0)
        self.focus.pack()
        self.focus.focus_set()

    def on_enter(self, event: tk.Event) -> None:
        """
            Allows user to add unit by pressing enter.

            Args:
                event (tk.Event): a user input event.
        """

        # calls add unit function
        self.add_unit()

    def disable_row_selection(self, event: tk.Event) -> None:
        """
            Disables row selection by user.

            Args:
                event (tk.Event): a user input event.
        """

        # removes the selection from row
        self.table.selection_remove(self.table.selection())

    def lock_column_sizes(self, event: tk.Event) -> None:
        """
            Locks column resizing by user.

            Args:
                event (tk.Event): a user input event.
        """

        # sets all columns to the fixed width
        for column in self.columns:
            self.table.column(column, width=self.column_width)

    def load_page(self) -> None:
        """
            Loads page from data.
        """

        # resets gpa data
        self.gpa.reset()

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from gpa record data to table
        for unit in self.gpa.get_record():
            self.table.insert("", "end", values=unit, tags=("current",))

        # add units from gpa extra data to table
        for unit in self.gpa.get_data():
            self.table.insert("", "end", values=unit)

        # set current and calculated gpa
        self.current_gpa_lbl.config(text=self.gpa.get_current_gpa())
        self.calculated_gpa_lbl.config(text=self.gpa.get_calculated_gpa())

        # scrolls table all the way up
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[0])

        # clears entry boxes
        self.grade.delete(0, tk.END)
        self.credit_pts.delete(0, tk.END)

        # disables remove unit button if there are no units in extra gpa data
        if len(self.gpa.get_data()) == 0:
            self.remove_unit_btn.config(state="disabled")

        # enables remove unit button if there are units in extra gpa data
        else:
            self.remove_unit_btn.config(state="normal")

        # resets focus
        self.focus.focus_set()

    def add_unit(self) -> None:
        """
            Adds a unit to the GPA data.
        """

        # gets all the unit details from entry boxes
        grade = self.grade.get().upper()
        credit_pts = self.credit_pts.get()

        # validates grade
        if grade not in ["WN", "N", "P", "C", "D", "HD"]:
            messagebox.showerror("Input Error", "Grade is invalid.")
            return

        # validates credit points
        try:
            credit_pts = int(credit_pts)
            if credit_pts < 1 or credit_pts > 24:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Credit points is invalid.")
            return
        credit_pts = str(credit_pts)

        # adds unit to the gpa data and table
        self.gpa.add_unit([grade, credit_pts])
        self.table.insert("", "end", values=self.gpa.get_data()[-1])

        # scrolls table all the way down
        self.table.see(self.table.get_children()[-1])

        # updates calculated gpa
        self.calculated_gpa_lbl.config(text=self.gpa.get_calculated_gpa())

        # clears entry boxes
        self.grade.delete(0, tk.END)
        self.credit_pts.delete(0, tk.END)

        # enables remove button
        self.remove_unit_btn.config(state="normal")

        # resets focus
        self.focus.focus_set()

    def remove_unit(self) -> None:
        """
            Removes the last unit.
        """

        # deletes the last row of the table
        rows = self.table.get_children()
        if len(rows) > 0:
            self.table.delete(rows[-1])

        # removes the last unit in the gpa data
        self.gpa.remove_unit()

        # scrolls table all the way down
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[-1])

        # updates calculated gpa
        self.calculated_gpa_lbl.config(text=self.gpa.get_calculated_gpa())

        # disables remove unit button if there are no units
        if len(self.gpa.get_data()) == 0:
            self.remove_unit_btn.config(state="disabled")

        # resets focus
        self.focus.focus_set()
