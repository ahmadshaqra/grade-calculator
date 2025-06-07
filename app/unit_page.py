"""
    unit_page.py

    Contains the unit page logic.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from data.unit import Unit

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

        subpage_select_frame = tk.Frame(self)
        subpage_select_frame.pack(pady=0)

        subpage_frame = tk.Frame(self)

        self.summary_frame = tk.Frame(subpage_frame)
        self.edit_frame = tk.Frame(subpage_frame)

        # initialises available pages
        self.subpages = {
            "Summary": self.summary_frame,
            "Edit Units": self.edit_frame
        }

        # make two custom pages

        # initialises menu buttons dictionary
        self.subpage_btns = {}

        # iterates through pages
        for name, page in self.subpages.items():

            # places page in main content frame
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

            # creates and adds menu button
            self.subpage_btns[name] = tk.Button(subpage_select_frame, text=name, font=("Segoe UI", 10, "bold"), width=10, command=lambda name=name: self.show_page(name))
            self.subpage_btns[name].pack(side="left", expand=True, fill="both", padx=10)

    def show_page(self, name: str) -> None:
        """
            Displays selected page on the subpage content frame.

            Args:
                name (str): the name of the selected subpage.
        """

        # gets the page object from the pages dictionary
        subpage = self.subpages[name]

        # displays page contents and refreshes it
        subpage.lift()
        # subpage.load_page()

        # enables all menu buttons
        for btn in self.subpage_btns.values():
            btn.config(state="normal")

        # disables selected page menu button
        self.subpage_btns[name].config(state="disabled")

    def load_page(self) -> None:
        """
            Loads page from data.
        """

        # selects the first page
        self.show_page(next(iter(self.subpages)))
