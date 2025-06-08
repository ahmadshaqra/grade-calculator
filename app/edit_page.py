"""
    edit_page.py

    Contains the unit edit subpage logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.unit import Unit

class EditPage(tk.Frame):
    """
        Manages the unit edit subpage.
    """

    def __init__(self, root: tk.Frame, unit: Unit, main_window: tk.Tk) -> None:
        """
            Initialises the unit edit subpage.

            Args:
                root (tk.Frame): the subpage contents frame.
                unit (Unit): the unit data.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and unit data
        super().__init__(root)
        self.unit = unit
        self.main_window = main_window

        # sets the style of the table and drop down menu
        style = ttk.Style(self)
        style.theme_use("alt")
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="lightgrey", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "lightgrey")], foreground=[("selected", "black")])
        style.map("Treeview.Heading", background=[("!active", "lightgrey"), ("active", "lightgrey"), ("pressed", "lightgrey")])
        style.map("TCombobox", fieldbackground=[("readonly", "white")], selectbackground=[("readonly", "white")], selectforeground=[("readonly", "black")])
        self.option_add("*TCombobox*Listbox.selectBackground", "lightgrey")
        self.option_add("*TCombobox*Listbox.selectForeground", "black")

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
        print("select unit")
        self.add_assessment_btn.config(state="normal")
        self.remove_assessment_btn.config(state="normal")

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

        units = list(self.unit.data.keys())
        self.select_unit.config(values=units)
        self.select_unit.set("")
        self.add_assessment_btn.config(state="disabled")
        self.remove_assessment_btn.config(state="disabled")

        # sets focus to the table
        self.table.focus_set()

    def add_assessment_form(self) -> None:
        # check if a unit is selected
        print("add assessment form")

    def add_assessment(self) -> None:
        pass

    def remove_assessment(self) -> None:
        # check if a unit is selected
        print("remove assessment")
