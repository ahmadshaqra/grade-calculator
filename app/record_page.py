"""
    record_page.py

    Contains the record page logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.record import Record
from re import fullmatch

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

        # initialises the frame and initialises record
        super().__init__(root)
        self.record = Record()

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
        self.columns = ["Unit #", "Unit Code", "Mark", "Grade", "Credit Points"]
        self.column_width = 96

        # initialises table
        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=10)

        # adds columns to the table
        for column in self.columns:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=self.column_width, minwidth=self.column_width, stretch=False)

        # disabling row selection and column size change
        self.table.bind("<<TreeviewSelect>>", self.disable_row_selection)
        self.table.bind("<ButtonRelease-1>", self.lock_column_sizes)

        # initialises scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # adds table and scrollbar to the frame
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # sets frame to hold add unit entry boxes
        add_unit_frame = tk.Frame(self)
        add_unit_frame.pack(pady=10)

        # adds unit code label and entry box
        tk.Label(add_unit_frame, text="Unit Code: ", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(10,0))
        self.unit_code = tk.Entry(add_unit_frame, width=10, font=("Segoe UI", 10))
        self.unit_code.pack(side="left", expand=True, fill="both", padx=(0,10))
        self.unit_code.bind("<Return>", self.on_enter)

        # adds mark label and entry box
        tk.Label(add_unit_frame, text="Mark: ", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(10,0))
        self.mark = tk.Entry(add_unit_frame, width=5, font=("Segoe UI", 10))
        self.mark.pack(side="left", expand=True, fill="both", padx=(0,10))
        self.mark.bind("<Return>", self.on_enter)

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
        self.save_changes_btn = tk.Button(control_frame, text="Save Changes", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.save_changes(), state="disabled")
        self.save_changes_btn.pack(side="left", expand=True, fill="both", padx=10)
        self.discard_changes_btn = tk.Button(control_frame, text="Discard Changes", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.discard_changes(), state="disabled")
        self.discard_changes_btn.pack(side="left", expand=True, fill="both", padx=10)

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

        # creates a hidden focus point
        self.focus = tk.Canvas(self, width=0, height=0, highlightthickness=0)
        self.focus.pack()
        self.focus.focus_set()

    def on_enter(self, event: tk.Event) -> None:
        """
            Enables user to add unit by pressing enter.

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

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from record to table
        for unit in self.record.get_data():
            self.table.insert("", "end", values=unit)

        # set wam and gpa
        self.wam_lbl.config(text=self.record.get_wam())
        self.gpa_lbl.config(text=self.record.get_gpa())

        # scrolls table all the way up
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[0])

        # clears entry boxes
        self.unit_code.delete(0, tk.END)
        self.mark.delete(0, tk.END)
        self.grade.delete(0, tk.END)
        self.credit_pts.delete(0, tk.END)

        # disables remove unit button if there are no units
        if len(self.record.get_data()) == 0:
            self.remove_unit_btn.config(state="disabled")

        # enables remove unit button if there are units
        else:
            self.remove_unit_btn.config(state="normal")

        # resets focus
        self.focus.focus_set()

    def add_unit(self) -> None:
        """
            Adds a unit to the record.
        """

        # gets all the unit details from entry boxes
        unit_code = self.unit_code.get().upper()
        mark = self.mark.get()
        grade = self.grade.get().upper()
        credit_pts = self.credit_pts.get()

        # validates unit code
        if not fullmatch(r"[A-Z]{3}\d{4}", unit_code):
            messagebox.showerror("Input Error", "Unit code is invalid.")
            return

        # validates mark
        try:
            mark = int(mark)
            if mark < 0 or mark > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Mark is invalid.")
            return

        # validates grade
        if (grade == "WN" and mark != 0) or \
           (0 <= mark <= 49 and grade not in ["WN", "N"]) or \
           (50 <= mark <= 59 and grade != "P") or \
           (60 <= mark <= 69 and grade != "C") or \
           (70 <= mark <= 79 and grade != "D") or \
           (80 <= mark <= 100 and grade != "HD"):
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

        # converts mark and credit points back to strings
        mark = str(mark)
        credit_pts = str(credit_pts)

        # adds unit to the record and table
        self.record.add_unit([unit_code, mark, grade, credit_pts])
        self.table.insert("", "end", values=self.record.get_data()[-1])

        # scrolls table all the way down
        self.table.see(self.table.get_children()[-1])

        # updates wam and gpa
        self.wam_lbl.config(text=self.record.get_wam())
        self.gpa_lbl.config(text=self.record.get_gpa())

        # clears entry boxes
        self.unit_code.delete(0, tk.END)
        self.mark.delete(0, tk.END)
        self.grade.delete(0, tk.END)
        self.credit_pts.delete(0, tk.END)

        # enables remove, save, and discard buttons
        self.remove_unit_btn.config(state="normal")
        self.save_changes_btn.config(state="normal")
        self.discard_changes_btn.config(state="normal")

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

        # removes the last unit in the record
        self.record.remove_unit()

        # scrolls table all the way down
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[-1])

        # updates wam and gpa
        self.wam_lbl.config(text=self.record.get_wam())
        self.gpa_lbl.config(text=self.record.get_gpa())

        # enables save and discard buttons
        self.save_changes_btn.config(state="normal")
        self.discard_changes_btn.config(state="normal")

        # disables remove unit button if there are no units
        if len(self.record.get_data()) == 0:
            self.remove_unit_btn.config(state="disabled")

        # resets focus
        self.focus.focus_set()

    def save_changes(self) -> None:
        """
            Saves the changes made to the record.
        """

        # confirms that user wants to save changes
        if not messagebox.askyesno("Save Changes", "Are you sure you want to save changes?"):

            # cancels save changes action
            messagebox.showinfo("Save Changes", "Action cancelled.")
            return

        # saves the current record to file
        self.record.save()

        # disables save and discard buttons
        self.save_changes_btn.config(state="disabled")
        self.discard_changes_btn.config(state="disabled")

        # reloads page
        self.load_page()

        # displays success message to user
        messagebox.showinfo("Save Changes", "Changes saved.")

    def discard_changes(self) -> None:
        """
            Discard the changes made to the record.
        """

        # confirms that user wants to discard changes
        if not messagebox.askyesno("Discard Changes", "Are you sure you want to discard changes?"):

            # cancels discard changes action
            messagebox.showinfo("Discard Changes", "Action cancelled.")
            return

        # resets the record data
        self.record.reset()

        # disables save and discard buttons
        self.save_changes_btn.config(state="disabled")
        self.discard_changes_btn.config(state="disabled")

        # reloads page
        self.load_page()

        # displays success message to user
        messagebox.showinfo("Discard Changes", "Changes discarded.")
