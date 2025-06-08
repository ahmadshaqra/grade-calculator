"""
    unit_page.py

    Contains the unit page logic.
"""

import tkinter as tk
from data.unit import Unit
from app.summary_page import SummaryPage
from app.edit_page import EditPage

class UnitPage(tk.Frame):
    """
        Manages the unit page.
    """

    def __init__(self, root: tk.Frame, main_window: tk.Tk) -> None:
        """
            Initialises the unit page.

            Args:
                root (tk.Frame): the main contents frame.
                main_window (tk.Tk): the main window.
        """

        # initialises the frame and unit data
        super().__init__(root)
        self.unit = Unit()
        self.main_window = main_window

        # sets frame to hold menu buttons
        self.subpage_select_frame = tk.Frame(self)
        self.subpage_select_frame.pack(pady=0)

        # sets main content frame
        self.subpage_frame = tk.Frame(self)
        self.subpage_frame.pack(fill="both", expand=True, pady=15)

        # initialises available subpages
        self.subpages = {
            "Summary": SummaryPage(self.subpage_frame, self.unit, self.main_window),
            "Edit": EditPage(self.subpage_frame, self.unit, self.main_window)
        }

        # initialises menu buttons dictionary
        self.subpage_btns = {}

        # iterates through subpages
        for name, subpage in self.subpages.items():

            # places subpage in subpage content frame
            subpage.place(relx=0, rely=0, relwidth=1, relheight=1)

            # creates and adds menu button
            self.subpage_btns[name] = tk.Button(self.subpage_select_frame, text=name, font=("Segoe UI", 10, "bold"), width=10, command=lambda name=name: self.show_subpage(name))
            self.subpage_btns[name].pack(side="left", expand=True, fill="both", padx=10)

    def show_subpage(self, name: str) -> None:
        """
            Displays selected subpage on the subpage content frame.

            Args:
                name (str): the name of the selected subpage.
        """

        # prevents an entry window from remaining open
        if self.main_window.entry_window and self.main_window.entry_window.winfo_exists():
            self.main_window.entry_window.destroy()
            self.main_window.entry_window = None

        # gets the subpage object from the subpages dictionary
        subpage = self.subpages[name]

        # displays subpage contents and refreshes it
        subpage.lift()
        subpage.load_page()

        # enables all subpage select buttons
        for btn in self.subpage_btns.values():
            btn.config(state="normal")

        # disables selected subpage select button
        self.subpage_btns[name].config(state="disabled")

    def load_page(self) -> None:
        """
            Loads page.
        """

        # selects the summary subpage
        self.show_subpage("Summary")
