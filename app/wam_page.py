"""
    wam_page.py

    Contains the WAM page logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.wam import WAM
from utils.asset_manager import AssetManager

class WAMPage(tk.Frame):
    """
        Manages the WAM page.
    """

    def __init__(self, root: tk.Frame, main_window: tk.Tk) -> None:
        """
            Initialises the WAM page.

            Args:
                root (tk.Frame): the main contents frame.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and wam data
        super().__init__(root)
        self.wam = WAM()
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
        self.columns = ["Unit #", "Year Level", "Mark", "Credit Points"]
        self.column_width = 120

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

        # adds current wam information label
        tk.Label(results_frame, text="Current WAM:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.current_wam_lbl = tk.Label(results_frame, text="00.000", font=("Segoe UI", 10))
        self.current_wam_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

        # adds calculated wam information label
        tk.Label(results_frame, text="Calculated WAM:", font=("Segoe UI", 10, "bold")).pack(side="left", expand=True, fill="both", padx=(20, 0))
        self.calculated_wam_lbl = tk.Label(results_frame, text="00.000", font=("Segoe UI", 10))
        self.calculated_wam_lbl.pack(side="left", expand=True, fill="both", padx=(0, 20))

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

        # resets wam data
        self.wam.reset()

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from wam record data to table
        for unit in self.wam.get_record():
            self.table.insert("", "end", values=unit, tags=("current",))

        # adds units from wam extra data to table
        for unit in self.wam.get_data():
            self.table.insert("", "end", values=unit)

        # set current and calculated wam
        self.current_wam_lbl.config(text=self.wam.get_current_wam())
        self.calculated_wam_lbl.config(text=self.wam.get_calculated_wam())

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

            # sets entry frame
            entry_frame = tk.Frame(self.main_window.entry_window)
            entry_frame.pack(pady=0)

            # sets left frame
            left_frame = tk.Frame(entry_frame)
            left_frame.pack(side="left", expand=True, fill="both", padx=5)

            # sets right frame
            right_frame = tk.Frame(entry_frame)
            right_frame.pack(side="left", expand=True, fill="both", padx=5)

            # creates and sets year level frame, label, and entry box
            year_lvl_frame = tk.LabelFrame(left_frame, text="Year Level", font=("Segoe UI", 10, "bold"))
            year_lvl_frame.pack(pady=5)
            self.year_lvl = tk.Entry(year_lvl_frame, width=15, font=("Segoe UI", 10))
            self.year_lvl.pack(padx=10, pady=10)
            self.year_lvl.bind("<Return>", lambda e: self.mark.focus_set())

            # creates and sets mark frame, label, and entry box
            mark_frame = tk.LabelFrame(right_frame, text="Mark", font=("Segoe UI", 10, "bold"))
            mark_frame.pack(pady=5)
            self.mark = tk.Entry(mark_frame, width=15, font=("Segoe UI", 10))
            self.mark.pack(padx=10, pady=10)
            self.mark.bind("<Return>", lambda e: self.credit_pts.focus_set())

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

        # sets focus on year level entry box
        self.year_lvl.focus_set()

    def on_close_add_unit_form(self) -> None:
        """
            Closes the add unit form.
        """

        # destroys window and sets pointer to none
        self.main_window.entry_window.destroy()
        self.main_window.entry_window = None

    def add_unit(self) -> None:
        """
            Adds a unit to the WAM data.
        """

        # gets all the unit details from entry boxes
        year_lvl = self.year_lvl.get()
        mark = self.mark.get()
        credit_pts = self.credit_pts.get()

        # validates year level
        try:
            year_lvl = int(year_lvl)
            if year_lvl < 1 or year_lvl > 9:
                raise ValueError
        except ValueError:
            self.year_lvl.focus_set()
            self.input_error_lbl.config(text="Input Error: Year level is invalid.")
            return
        year_lvl = str(year_lvl)

        # validates mark
        try:
            mark = int(mark)
            if mark < 0 or mark > 100:
                raise ValueError
        except ValueError:
            self.mark.focus_set()
            self.input_error_lbl.config(text="Input Error: Mark is invalid.")
            return
        mark = str(mark)

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

        # adds unit to the wam and table
        self.wam.add_unit([year_lvl, mark, credit_pts])
        self.table.insert("", "end", values=self.wam.get_data()[-1])

        # scrolls table all the way down
        self.table.see(self.table.get_children()[-1])

        # updates calculated wam
        self.calculated_wam_lbl.config(text=self.wam.get_calculated_wam())

        # closes add unit form
        self.main_window.entry_window.destroy()

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Add Unit", f"Unit {len(self.wam.get_record()) + len(self.wam.get_data())} added.")

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

        # deletes the selected unit from wam
        self.wam.remove_unit(unit_no)

        # updates calculated wam
        self.calculated_wam_lbl.config(text=self.wam.get_calculated_wam())

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from wam record data to table
        for unit in self.wam.get_record():
            self.table.insert("", "end", values=unit, tags=("current",))

        # adds units from wam extra data to table
        for unit in self.wam.get_data():
            self.table.insert("", "end", values=unit)

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Remove Unit", f"Unit {unit_no} removed.")
