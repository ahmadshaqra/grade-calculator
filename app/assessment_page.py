"""
    assessment_page.py

    Contains the unit assessment subpage logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.unit import Unit
from utils.asset_manager import AssetManager

class AssessmentPage(tk.Frame):
    """
        Manages the unit assessment subpage.
    """

    def __init__(self, root: tk.Frame, unit: Unit, main_window: tk.Tk) -> None:
        """
            Initialises the unit assessment subpage.

            Args:
                root (tk.Frame): the subpage contents frame.
                unit (Unit): the unit data.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and unit data
        super().__init__(root)
        self.unit = unit
        self.main_window = main_window

        # sets the style of the page
        style = ttk.Style(self)
        style.theme_use("alt")
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="lightgrey", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "lightgrey")], foreground=[("selected", "black")])
        style.map("Treeview.Heading", background=[("!active", "lightgrey"), ("active", "lightgrey"), ("pressed", "lightgrey")])
        style.map("TCombobox", fieldbackground=[("readonly", "white")], selectbackground=[("readonly", "white")], selectforeground=[("readonly", "black")])
        self.option_add("*TCombobox*Listbox.selectBackground", "lightgrey")
        self.option_add("*TCombobox*Listbox.selectForeground", "black")
        self.option_add("*Entry.selectBackground", "lightgrey")
        self.option_add("*Entry.selectForeground", "black")

        # sets select unit frame
        select_unit_frame = tk.Frame(self)
        select_unit_frame.pack(pady=10)

        # adds label and drop down menu
        tk.Label(select_unit_frame, text="Select Unit: ", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(10, 0))
        self.select_unit = ttk.Combobox(select_unit_frame, font=("Segoe UI", 10), state="readonly", width=10)
        self.select_unit.pack(side="left", expand=True, fill="both", padx=(0, 10))
        self.select_unit.bind("<<ComboboxSelected>>", self.on_selection)

        # sets frame to hold table
        table_frame = tk.Frame(self, width=500, height=185)
        table_frame.pack(pady=10)
        table_frame.grid_propagate(False)

        # sets columns of the table
        self.columns = ["Assessment", "Weight", "Mark"]
        self.column_width = 160

        # initialises table
        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=8)

        # adds columns to the table
        for column in self.columns:
            self.table.heading(column, text=column)
            self.table.column(column, anchor="center", width=self.column_width, minwidth=self.column_width, stretch=False)

        # binds keyboard and mouse actions
        self.table.bind("<Button-1>", self.select_row)
        self.table.bind("<BackSpace>", lambda e: self.remove_assessment())
        self.table.bind("<Return>", lambda e: self.add_assessment_form())

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
        self.add_assessment_btn = tk.Button(control_frame, text="Add Assessment", font=("Segoe UI", 10, "bold"), width=20, command=lambda: self.add_assessment_form())
        self.add_assessment_btn.pack(side="left", expand=True, fill="both", padx=10)
        self.remove_assessment_btn = tk.Button(control_frame, text="Remove Assessment", font=("Segoe UI", 10, "bold"), width=20, command=lambda: self.remove_assessment())
        self.remove_assessment_btn.pack(side="left", expand=True, fill="both", padx=10)

    def on_selection(self, event: tk.Event) -> None:
        """
            Handles a select action for the dropdown menu.

            Args:
                event (tk.Event): a user input event.
        """

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from unit data to table
        for unit in self.unit.get_unit_assessments(self.select_unit.get()):
            self.table.insert("", "end", values=unit)

        # scrolls table all the way up
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[0])

        # enables add and remove assessment buttons
        self.add_assessment_btn.config(state="normal")
        self.remove_assessment_btn.config(state="normal")

        # resets focus
        self.table.focus_set()

    def select_row(self, event: tk.Event) -> None:
        """
            Handles a select row action.

            Args:
                event (tk.Event): a user input event.
        """

        # gets the row id of the event
        row = self.table.identify_row(event.y)

        # clicked on an unselected and untagged row
        if row and row not in self.table.selection() and not self.table.item(row)["tags"]:

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

        # gets list of units
        units = list(self.unit.data.keys())

        # sets up dropdown menu
        self.select_unit.config(values=units)
        self.select_unit.set("")

        # disables add and remove assessment buttons
        self.add_assessment_btn.config(state="disabled")
        self.remove_assessment_btn.config(state="disabled")

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # sets focus to the table
        self.table.focus_set()

    def add_assessment_form(self) -> None:
        """
            Creates the add assessment form.
        """

        # checks if no unit is selected
        if self.select_unit.get() == "":
            return

        # closes form if it already exists
        if self.main_window.entry_window is not None and self.main_window.entry_window.winfo_exists():
            self.on_close_form_close()

        # creates the entry window
        self.main_window.entry_window = tk.Toplevel(self)
        self.main_window.entry_window.withdraw()

        # sets close protocol
        self.main_window.entry_window.protocol("WM_DELETE_WINDOW", self.on_close_form_close)

        # sets title and icon
        self.main_window.entry_window.title("Add Assessment")
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
        tk.Label(self.main_window.entry_window, text="Add Details for New Assessment", font=("Segoe UI", 10, "bold")).pack(pady=10)

        # sets entry frame
        entry_frame = tk.Frame(self.main_window.entry_window)
        entry_frame.pack(pady=0)

        # sets left frame
        left_frame = tk.Frame(entry_frame)
        left_frame.pack(side="left", expand=True, fill="both", padx=5)

        # sets right frame
        right_frame = tk.Frame(entry_frame)
        right_frame.pack(side="left", expand=True, fill="both", padx=5)

        # creates and sets assessment name frame, label, and entry box
        assessment_name_frame = tk.LabelFrame(left_frame, text="Assessment Name", font=("Segoe UI", 10, "bold"))
        assessment_name_frame.pack(pady=5)
        self.assessment_name = tk.Entry(assessment_name_frame, width=15, font=("Segoe UI", 10))
        self.assessment_name.pack(padx=10, pady=10)
        self.assessment_name.bind("<Return>", lambda e: self.weight.focus_set())

        # creates and sets weight frame, label, and entry box
        weight_frame = tk.LabelFrame(left_frame, text="Weight", font=("Segoe UI", 10, "bold"))
        weight_frame.pack(pady=5)
        self.weight = tk.Entry(weight_frame, width=15, font=("Segoe UI", 10))
        self.weight.pack(padx=10, pady=10)
        self.weight.bind("<Return>", lambda e: self.obtained_marks.focus_set())

        # creates and sets obtained marks frame, label, and entry box
        obtained_marks_frame = tk.LabelFrame(right_frame, text="Obtained Marks", font=("Segoe UI", 10, "bold"))
        obtained_marks_frame.pack(pady=5)
        self.obtained_marks = tk.Entry(obtained_marks_frame, width=15, font=("Segoe UI", 10))
        self.obtained_marks.pack(padx=10, pady=10)
        self.obtained_marks.bind("<Return>", lambda e: self.total_marks.focus_set())

        # creates and sets total marks frame, label, and entry box
        total_marks_frame = tk.LabelFrame(right_frame, text="Total Marks", font=("Segoe UI", 10, "bold"))
        total_marks_frame.pack(pady=5)
        self.total_marks = tk.Entry(total_marks_frame, width=15, font=("Segoe UI", 10))
        self.total_marks.pack(padx=10, pady=10)
        self.total_marks.bind("<Return>", lambda e: self.add_assessment())

        # set frame for control buttons
        control_frame = tk.Frame(self.main_window.entry_window)
        control_frame.pack(pady=10)

        # adds control buttons
        tk.Button(control_frame, text="Cancel", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.main_window.entry_window.destroy()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Add", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_assessment()).pack(side="left", expand=True, fill="both", padx=10)

        # adds input error label
        self.input_error_lbl = tk.Label(self.main_window.entry_window, text="", font=("Segoe UI", 8, "italic"), fg="red")
        self.input_error_lbl.pack()

        # shows form
        self.main_window.entry_window.deiconify()

        # sets focus on unit code entry box
        self.assessment_name.focus_set()

    def on_close_form_close(self) -> None:
        """
            Closes a form.
        """

        # destroys window and sets pointer to none
        self.main_window.entry_window.destroy()
        self.main_window.entry_window = None

    def add_assessment(self) -> None:
        """
            Adds an assessment.
        """

        # gets unit code
        unit_code = self.select_unit.get()

        # gets all the assessment details from entry boxes
        assessment_name = self.assessment_name.get()
        weight = self.weight.get()
        obtained_marks = self.obtained_marks.get()
        total_marks = self.total_marks.get()

        # validates assessment name
        if len(assessment_name) == 0 or \
           len(assessment_name) > 15 or \
           assessment_name in [assessment for assessment, _, _, _ in self.unit.data[unit_code]]:
            self.assessment_name.focus_set()
            self.input_error_lbl.config(text="Input Error: Assessment name is invalid.")
            return

        # validates weight
        try:
            weight = float(weight)
            if weight < 0 or \
               round(weight, 2) != weight or \
               weight + sum(float(weight) for _, weight, _, _ in self.unit.data[unit_code]) > 100:
                raise ValueError
        except ValueError:
            self.weight.focus_set()
            self.input_error_lbl.config(text="Input Error: Weight is invalid.")
            return

        # validates obtained marks
        try:
            obtained_marks = float(obtained_marks)
            if obtained_marks < 0:
                raise ValueError
        except ValueError:
            self.obtained_marks.focus_set()
            self.input_error_lbl.config(text="Input Error: Obtained marks is invalid.")
            return

        # validates total marks
        try:
            total_marks = float(total_marks)
            if total_marks <= 0:
                raise ValueError
        except ValueError:
            self.total_marks.focus_set()
            self.input_error_lbl.config(text="Input Error: Total marks is invalid.")
            return

        # validates that obtained marks is less than or equal to total marks
        if obtained_marks > total_marks:
            self.obtained_marks.focus_set()
            self.input_error_lbl.config(text="Input Error: Obtained marks is invalid.")
            return

        # converts details back to strings
        weight = f"{weight:.2f}"
        obtained_marks = str(obtained_marks)
        total_marks = str(total_marks)

         # adds unit to the record and table
        self.unit.add_assessment(unit_code, [assessment_name, weight, obtained_marks, total_marks])
        self.table.insert("", "end", values=self.unit.get_unit_assessments(unit_code)[-1])

        # scrolls table all the way down
        self.table.see(self.table.get_children()[-1])

        # closes add unit form
        self.main_window.entry_window.destroy()

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Add Assessment", f"{assessment_name} added.")

    def remove_assessment(self) -> None:
        """
            Removes the selected assessment.
        """

        # gets selected unit
        unit_code = self.select_unit.get()

        # checks if no unit is selected
        if unit_code == "":
            return

        # gets the selected row
        row = self.table.selection()

        # checks if no assessment is selected
        if not row:
            messagebox.showerror("Remove Assessment", "Select an assessment to remove.")
            return

        # gets unit details
        assessment = self.table.item(row[0])["values"][0]
        assessment_no = self.table.get_children().index(row[0])

        # confirms that user wants to remove assessment
        if not messagebox.askyesno("Remove Assessment", f"Are you sure you want to remove {assessment}?"):
            return

        # scrolls table view to selected row
        self.table.see(row)

        # deletes the selected unit from unit data
        self.unit.remove_assessment(unit_code, assessment_no)

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds assessments from overview data to table
        for unit in self.unit.get_unit_assessments(unit_code):
            self.table.insert("", "end", values=unit)

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Remove Unit", f"{assessment} removed.")
