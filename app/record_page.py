"""
    record_page.py

    Contains the record page logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.record import Record
from utils.asset_manager import AssetManager
from re import fullmatch

class RecordPage(tk.Frame):
    """
        Manages the record page.
    """

    def __init__(self, root: tk.Frame, main_window: tk.Tk) -> None:
        """
            Initialises the record page.

            Args:
                root (tk.Frame): the main contents frame.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and record
        super().__init__(root)
        self.record = Record()
        self.main_window = main_window

        # sets frame to hold table
        table_frame = tk.Frame(self, width=500, height=275)
        table_frame.pack()
        table_frame.grid_propagate(False)

        # sets the style of the page
        style = ttk.Style(self)
        style.theme_use("alt")
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="lightgrey", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "lightgrey")], foreground=[("selected", "black")])
        style.map("Treeview.Heading", background=[("!active", "lightgrey"), ("active", "lightgrey"), ("pressed", "lightgrey")])
        self.option_add("*Entry.selectBackground", "lightgrey")
        self.option_add("*Entry.selectForeground", "black")

        # sets columns of the table
        self.columns = ["Unit #", "Unit Code", "Mark", "Grade", "Credit Points"]
        self.column_width = 96

        # initialises table
        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=12)

        # adds columns to the table
        for column in self.columns:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=self.column_width, minwidth=self.column_width, stretch=False)

        # binds keyboard and mouse actions
        self.table.bind("<Button-1>", self.select_row)
        self.table.bind("<BackSpace>", lambda e: self.remove_unit())
        self.table.bind("<Return>", lambda e: self.add_unit_form())

        # initialises scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # adds table and scrollbar to the frame
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # sets frame to hold control buttons
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # adds the control buttons
        tk.Button(control_frame, text="Add Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_unit_form()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Remove Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.remove_unit()).pack(side="left", expand=True, fill="both", padx=10)

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

    def select_row(self, event: tk.Event) -> None:
        """
            Handles a select row action.

            Args:
                event (tk.Event): a user input event.
        """

        # gets the row id of the event
        row = self.table.identify_row(event.y)

        # clicked on an unselected row
        if row and row not in self.table.selection():

            # sets the selection
            self.table.selection_set(row)

        # clicked on empty space or selected row
        else:

            # clears selection
            self.table.selection_remove(self.table.selection())

        # sets focus to the table
        self.table.focus_set()

        # stops default behaviour
        return "break"

    def load_page(self) -> None:
        """
            Loads page from data.
        """

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from record to table
        for unit in self.record.get_data():
            self.table.insert("", "end", values=unit)

        # set wam and gpa
        self.wam_lbl.config(text=self.record.get_wam())
        self.gpa_lbl.config(text=self.record.get_gpa())

        # scrolls table all the way up
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[0])

        # resets focus
        self.table.focus_set()

    def add_unit_form(self) -> None:
        """
            Creates the add unit form.
        """

        # checks if add unit form already exists
        if self.main_window.entry_window is None or not self.main_window.entry_window.winfo_exists():

            # creates the entry window
            self.main_window.entry_window = tk.Toplevel(self)
            self.main_window.entry_window.withdraw()

            # sets close protocol
            self.main_window.entry_window.protocol("WM_DELETE_WINDOW", self.on_close_add_unit_form)

            # sets title and icon
            self.main_window.entry_window.title("Add Unit")
            self.main_window.entry_window.iconbitmap(AssetManager.get_asset("icon.ico"))

            # sets the window dimensions
            window_width = 400
            window_height = 270

            # gets the screen dimensions
            screen_width = self.main_window.entry_window.winfo_screenwidth()
            screen_height = self.main_window.entry_window.winfo_screenheight()

            # calculates desired window position
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2) - 30

            # sets window size and position and disables resizing
            self.main_window.entry_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.main_window.entry_window.resizable(False, False)

            # adds title label
            tk.Label(self.main_window.entry_window, text="Add Details for New Unit", font=("Segoe UI", 10, "bold")).pack(pady=10)

            # sets entry frame
            entry_frame = tk.Frame(self.main_window.entry_window)
            entry_frame.pack(pady=0)

            # sets left frame
            left_frame = tk.Frame(entry_frame)
            left_frame.pack(side="left", expand=True, fill="both", padx=5)

            # sets right frame
            right_frame = tk.Frame(entry_frame)
            right_frame.pack(side="left", expand=True, fill="both", padx=5)

            # creates and sets unit code frame, label, and entry box
            unit_code_frame = tk.LabelFrame(left_frame, text="Unit Code", font=("Segoe UI", 10, "bold"))
            unit_code_frame.pack(pady=5)
            self.unit_code = tk.Entry(unit_code_frame, width=15, font=("Segoe UI", 10))
            self.unit_code.pack(padx=10, pady=10)
            self.unit_code.bind("<Return>", lambda e: self.mark.focus_set())

            # creates and sets mark frame, label, and entry box
            mark_frame = tk.LabelFrame(right_frame, text="Mark", font=("Segoe UI", 10, "bold"))
            mark_frame.pack(pady=5)
            self.mark = tk.Entry(mark_frame, width=15, font=("Segoe UI", 10))
            self.mark.pack(padx=10, pady=10)
            self.mark.bind("<Return>", lambda e: self.grade.focus_set())

            # creates and sets grade frame, label, and entry box
            grade_frame = tk.LabelFrame(left_frame, text="Grade", font=("Segoe UI", 10, "bold"))
            grade_frame.pack(pady=5)
            self.grade = tk.Entry(grade_frame, width=15, font=("Segoe UI", 10))
            self.grade.pack(padx=10, pady=10)
            self.grade.bind("<Return>", lambda e: self.credit_pts.focus_set())

            # creates and sets credit points frame, label, and entry box
            credit_pts_frame = tk.LabelFrame(right_frame, text="Credit Points", font=("Segoe UI", 10, "bold"))
            credit_pts_frame.pack(pady=5)
            self.credit_pts = tk.Entry(credit_pts_frame, width=15, font=("Segoe UI", 10))
            self.credit_pts.pack(padx=10, pady=10)
            self.credit_pts.bind("<Return>", lambda e: self.add_unit())

            # set frame for control buttons
            control_frame = tk.Frame(self.main_window.entry_window)
            control_frame.pack(pady=10)

            # adds control buttons
            tk.Button(control_frame, text="Cancel", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.main_window.entry_window.destroy()).pack(side="left", expand=True, fill="both", padx=10)
            tk.Button(control_frame, text="Add", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_unit()).pack(side="left", expand=True, fill="both", padx=10)

            # adds input error label
            self.input_error_lbl = tk.Label(self.main_window.entry_window, text="", font=("Segoe UI", 8, "italic"), fg="red")
            self.input_error_lbl.pack()

            # shows form
            self.main_window.entry_window.deiconify()

        # add unit form already open
        else:

            # brings the form to the front
            self.main_window.entry_window.deiconify()
            self.main_window.entry_window.lift()

        # sets focus on unit code entry box
        self.unit_code.focus_set()

    def on_close_add_unit_form(self) -> None:
        """
            Closes the add unit form.
        """

        # destroys window and sets pointer to none
        self.main_window.entry_window.destroy()
        self.main_window.entry_window = None

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
        if not fullmatch(r"[A-Z]{3}\d{4}", unit_code) or unit_code in [unit for _, unit, _, _, _ in self.record.get_data()]:
            self.unit_code.focus_set()
            self.input_error_lbl.config(text="Input Error: Unit code is invalid.")
            return

        # validates mark
        try:
            mark = int(mark)
            if mark < 0 or mark > 100:
                raise ValueError
        except ValueError:
            self.mark.focus_set()
            self.input_error_lbl.config(text="Input Error: Mark is invalid.")
            return

        # validates grade
        if (grade == "WN" and mark != 0) or \
           (0 <= mark <= 49 and grade not in ["WN", "N"]) or \
           (50 <= mark <= 59 and grade != "P") or \
           (60 <= mark <= 69 and grade != "C") or \
           (70 <= mark <= 79 and grade != "D") or \
           (80 <= mark <= 100 and grade != "HD"):
            self.grade.focus_set()
            self.input_error_lbl.config(text="Input Error: Grade is invalid.")
            return

        # validates credit points
        try:
            credit_pts = int(credit_pts)
            if credit_pts < 1 or credit_pts > 24:
                raise ValueError
        except ValueError:
            self.credit_pts.focus_set()
            self.input_error_lbl.config(text="Input Error: Credit points is invalid.")
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

        # closes add unit form
        self.main_window.entry_window.destroy()

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Add Unit", f"{unit_code} added.")

    def remove_unit(self) -> None:
        """
            Removes the selected unit.
        """

        # gets the selected row
        row = self.table.selection()

        # checks if no unit is selected
        if not row:
            messagebox.showerror("Remove Unit", "Select a unit to remove.")
            return

        # gets unit details
        unit = self.table.item(row[0])["values"]
        unit_no = int(unit[0])
        unit_code = unit[1]
 
        # confirms that user wants to remove unit
        if not messagebox.askyesno("Remove Unit", f"Are you sure you want to remove {unit_code}?"):
            return

        # scrolls table view to selected row
        self.table.see(row)

        # deletes the selected unit from record
        self.record.remove_unit(unit_no)

        # updates wam and gpa
        self.wam_lbl.config(text=self.record.get_wam())
        self.gpa_lbl.config(text=self.record.get_gpa())

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from record to table
        for unit in self.record.get_data():
            self.table.insert("", "end", values=unit)

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Remove Unit", f"{unit_code} removed.")
