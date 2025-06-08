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

    def load_page(self) -> None:
        pass
