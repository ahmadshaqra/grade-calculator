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

    def load_page(self) -> None:
        """
            Loads page from data.
        """

        pass
