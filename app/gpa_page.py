"""
    gpa_page.py

    Contains the GPA page logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.gpa import GPA
from utils.asset_manager import AssetManager

class GPAPage(tk.Frame):
    """
        Manages the GPA page.
    """

    def __init__(self, root: tk.Frame, main_window: tk.Tk) -> None:
        """
            Initialises the GPA page.

            Args:
                root (tk.Frame): the main contents frame.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and gpa data
        super().__init__(root)
        self.gpa = GPA()
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
        self.columns = ["Unit #", "Grade", "Credit Points"]
        self.column_width = 160

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

        # add tag for current record
        self.table.tag_configure("current", background="whitesmoke")

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

        # adds current gpa information label
        tk.Label(results_frame, text="Current GPA:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.current_gpa_lbl = tk.Label(results_frame, text="00.000", font=("Segoe UI", 10))
        self.current_gpa_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

        # adds calculated gpa information label
        tk.Label(results_frame, text="Calculated GPA:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.calculated_gpa_lbl = tk.Label(results_frame, text="00.000", font=("Segoe UI", 10))
        self.calculated_gpa_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

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

        # resets gpa data
        self.gpa.reset()

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from gpa record data to table
        for unit in self.gpa.get_record():
            self.table.insert("", "end", values=unit, tags=("current",))

        # adds units from gpa extra data to table
        for unit in self.gpa.get_data():
            self.table.insert("", "end", values=unit)

        # set current and calculated gpa
        self.current_gpa_lbl.config(text=self.gpa.get_current_gpa())
        self.calculated_gpa_lbl.config(text=self.gpa.get_calculated_gpa())

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

            # creates and sets mark frame, label, and entry box
            grade_frame = tk.LabelFrame(self.main_window.entry_window, text="Grade", font=("Segoe UI", 10, "bold"))
            grade_frame.pack(pady=5)
            self.grade = tk.Entry(grade_frame, width=15, font=("Segoe UI", 10))
            self.grade.pack(padx=10, pady=10)
            self.grade.bind("<Return>", lambda e: self.credit_pts.focus_set())

            # creates and sets credit points frame, label, and entry box
            credit_pts_frame = tk.LabelFrame(self.main_window.entry_window, text="Credit Points", font=("Segoe UI", 10, "bold"))
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

        # add unit form already open
        else:

            # brings the form to the front
            self.main_window.entry_window.deiconify()
            self.main_window.entry_window.lift()

        # sets focus on grade entry box
        self.grade.focus_set()

    def on_close_add_unit_form(self) -> None:
        """
            Closes the add unit form.
        """

        # destroys window and sets pointer to none
        self.main_window.entry_window.destroy()
        self.main_window.entry_window = None

    def add_unit(self) -> None:
        """
            Adds a unit to the GPA data.
        """

        # gets all the unit details from entry boxes
        grade = self.grade.get().upper()
        credit_pts = self.credit_pts.get()

        # validates grade
        if grade not in ["WN", "N", "P", "C", "D", "HD"]:
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
        credit_pts = str(credit_pts)

        # adds unit to the gpa and table
        self.gpa.add_unit([grade, credit_pts])
        self.table.insert("", "end", values=self.gpa.get_data()[-1])

        # scrolls table all the way down
        self.table.see(self.table.get_children()[-1])

        # updates calculated gpa
        self.calculated_gpa_lbl.config(text=self.gpa.get_calculated_gpa())

        # closes add unit form
        self.main_window.entry_window.destroy()

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Add Unit", f"Unit {len(self.gpa.get_record()) + len(self.gpa.get_data())} added.")

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
 
        # confirms that user wants to remove unit
        if not messagebox.askyesno("Remove Unit", f"Are you sure you want to remove Unit {unit_no}?"):
            return

        # scrolls table view to selected row
        self.table.see(row)

        # deletes the selected unit from gpa
        self.gpa.remove_unit(unit_no)

        # updates calculated gpa
        self.calculated_gpa_lbl.config(text=self.gpa.get_calculated_gpa())

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from gpa record data to table
        for unit in self.gpa.get_record():
            self.table.insert("", "end", values=unit, tags=("current",))

        # adds units from gpa extra data to table
        for unit in self.gpa.get_data():
            self.table.insert("", "end", values=unit)

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Remove Unit", f"Unit {unit_no} removed.")
