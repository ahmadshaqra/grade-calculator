"""
    overview_page.py

    Contains the unit overview subpage logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.unit import Unit
from utils.asset_manager import AssetManager
from re import fullmatch

class OverviewPage(tk.Frame):
    """
        Manages the unit overview subpage.
    """

    def __init__(self, root: tk.Frame, unit: Unit, main_window: tk.Tk) -> None:
        """
            Initialises the unit overview subpage.

            Args:
                root (tk.Frame): the subpage contents frame.
                unit (Unit): the unit data.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and sets unit data
        super().__init__(root)
        self.unit = unit
        self.main_window = main_window

        # sets frame to hold table
        table_frame = tk.Frame(self, width=500, height=185)
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
        self.columns = ["Unit Code", "Mark (Grade)", "Remaining", "Average Required"]
        self.column_width = 120

        # initialises table
        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=8)

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

        # sets change target type
        self.change_target_type = "Grade"

        # sets target label
        self.target_lbl = tk.Label(self, text=self.unit.get_target(), font=("Segoe UI", 10, "bold"))
        self.target_lbl.pack(pady=10)

        # sets frame to hold control buttons
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # adds the control buttons
        tk.Button(control_frame, text="Change Target", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.change_target_form()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Add Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_unit_form()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Remove Unit", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.remove_unit()).pack(side="left", expand=True, fill="both", padx=10)

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

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from unit data to table
        for unit in self.unit.get_overview():
            self.table.insert("", "end", values=unit)

        # scrolls table all the way up
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[0])

        # resets focus
        self.table.focus_set()

    def change_target_form(self) -> None:
        """
            Creates the change target form.
        """

        # closes form if it already exists
        if self.main_window.entry_window is not None and self.main_window.entry_window.winfo_exists():
            self.on_close_form_close()

        # creates the entry window
        self.main_window.entry_window = tk.Toplevel(self)

        # sets close protocol
        self.main_window.entry_window.protocol("WM_DELETE_WINDOW", self.on_close_form_close)

        # sets title and icon
        self.main_window.entry_window.title("Change Target")
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
        tk.Label(self.main_window.entry_window, text="Set New Target", font=("Segoe UI", 10, "bold")).pack(pady=15)

        # sets change target type
        self.change_target_type = "Grade"

        # creates and sets target frame, label, and entry box
        self.target_frame = tk.LabelFrame(self.main_window.entry_window, text=f"Target {self.change_target_type}", font=("Segoe UI", 10, "bold"))
        self.target_frame.pack(pady=5)
        self.target = tk.Entry(self.target_frame, width=15, font=("Segoe UI", 10))
        self.target.pack(padx=10, pady=10)
        self.target.bind("<Return>", lambda e: self.change_target())

        # creates and sets switch target type button
        tk.Button(self.main_window.entry_window, text="Switch Target Type", font=("Segoe UI", 10, "bold"), width=20, command=lambda: self.switch_target_type()).pack(pady=15)

        # set frame for control buttons
        control_frame = tk.Frame(self.main_window.entry_window)
        control_frame.pack(pady=10)

        # adds control buttons
        tk.Button(control_frame, text="Cancel", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.main_window.entry_window.destroy()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Set", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.change_target()).pack(side="left", expand=True, fill="both", padx=10)

        # adds input error label
        self.input_error_lbl = tk.Label(self.main_window.entry_window, text="", font=("Segoe UI", 8, "italic"), fg="red")
        self.input_error_lbl.pack()

        # sets focus on target entry box
        self.target.focus_set()

    def switch_target_type(self) -> None:
        """
            Switches target type.
        """

        # switches mark to grade
        if self.change_target_type == "Mark":
            self.change_target_type = "Grade"

        # switches grade to mark
        elif self.change_target_type == "Grade":
            self.change_target_type = "Mark"

        # updates new target entry label
        self.target_frame.config(text=f"Target {self.change_target_type}")

        # resets input error label
        self.input_error_lbl.config(text="")

    def add_unit_form(self) -> None:
        """
            Creates the add unit form.
        """

        # closes form if it already exists
        if self.main_window.entry_window is not None and self.main_window.entry_window.winfo_exists():
            self.on_close_form_close()

        # creates the entry window
        self.main_window.entry_window = tk.Toplevel(self)

        # sets close protocol
        self.main_window.entry_window.protocol("WM_DELETE_WINDOW", self.on_close_form_close)

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

        # creates and sets unit code frame, label, and entry box
        unit_code_frame = tk.LabelFrame(self.main_window.entry_window, text="Unit Code", font=("Segoe UI", 10, "bold"))
        unit_code_frame.pack(pady=30)
        self.unit_code = tk.Entry(unit_code_frame, width=15, font=("Segoe UI", 10))
        self.unit_code.pack(padx=10, pady=10)
        self.unit_code.bind("<Return>", lambda e: self.add_unit())

        # set frame for control buttons
        control_frame = tk.Frame(self.main_window.entry_window)
        control_frame.pack(pady=10)

        # adds control buttons
        tk.Button(control_frame, text="Cancel", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.main_window.entry_window.destroy()).pack(side="left", expand=True, fill="both", padx=10)
        tk.Button(control_frame, text="Add", font=("Segoe UI", 10, "bold"), width=15, command=lambda: self.add_unit()).pack(side="left", expand=True, fill="both", padx=10)

        # adds input error label
        self.input_error_lbl = tk.Label(self.main_window.entry_window, text="", font=("Segoe UI", 8, "italic"), fg="red")
        self.input_error_lbl.pack()

        # sets focus on unit code entry box
        self.unit_code.focus_set()

    def on_close_form_close(self) -> None:
        """
            Closes a form.
        """

        # destroys window and sets pointer to none
        self.main_window.entry_window.destroy()
        self.main_window.entry_window = None

    def change_target(self) -> None:
        """
            Changes the target.
        """

        # gets target from entry box
        target = self.target.get().upper()

        # validates target if target type is set to grade
        if self.change_target_type == "Grade":
            if target not in ["N", "P", "C", "D", "HD"]:
                self.target.focus_set()
                self.input_error_lbl.config(text="Input Error: Target grade is invalid.")
                return

        # validates target if target type is set to mark
        elif self.change_target_type == "Mark":
            try:
                target = int(target)
                if target < 0 or target > 100:
                    raise ValueError
            except ValueError:
                self.target.focus_set()
                self.input_error_lbl.config(text="Input Error: Target mark is invalid.")
                return
            target = str(target)

        # changes target in unit data
        self.unit.change_target(self.change_target_type, target)

        # closes change target form
        self.main_window.entry_window.destroy()

        # resets change target type
        self.change_target_type = "Grade"

        # updates target label
        self.target_lbl.config(text=self.unit.get_target())

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from unit data to table
        for unit in self.unit.get_overview():
            self.table.insert("", "end", values=unit)

        # scrolls table all the way up
        children = self.table.get_children()
        if len(children) > 0:
            self.table.see(children[0])

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Change Target", "Target changed.")

    def add_unit(self) -> None:
        """
            Adds a unit to the unit data.
        """

        # gets unit code from entry box
        unit_code = self.unit_code.get().upper()

        # validates unit code
        if not fullmatch(r"[A-Z]{3}\d{4}", unit_code) or unit_code in self.unit.data.keys():
            self.unit_code.focus_set()
            self.input_error_lbl.config(text="Input Error: Unit code is invalid.")
            return

        # adds unit to the unit data
        self.unit.add_unit(unit_code)

        # closes add unit form
        self.main_window.entry_window.destroy()

        # clear current table
        for row in self.table.get_children():
            self.table.delete(row)

        # add units from overview data to table
        for unit in self.unit.get_overview():
            self.table.insert("", "end", values=unit)

        # scrolls table all the way up
        self.table.see(self.table.get_children()[0])

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
        unit_code = unit[0]
 
        # confirms that user wants to remove unit
        if not messagebox.askyesno("Remove Unit", f"Are you sure you want to remove {unit_code}?"):
            return

        # scrolls table view to selected row
        self.table.see(row)

        # deletes the selected unit from unit data
        self.unit.remove_unit(unit_code)

        # clears current table
        for row in self.table.get_children():
            self.table.delete(row)

        # adds units from overview data to table
        for unit in self.unit.get_overview():
            self.table.insert("", "end", values=unit)

        # resets focus
        self.table.focus_set()

        # displays success message to user
        messagebox.showinfo("Remove Unit", f"{unit_code} removed.")
