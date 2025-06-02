import tkinter as tk

class UnitPage(tk.Frame):

    def __init__(self, root: tk.Frame) -> None:
        super().__init__(root)
        tk.Label(self, text="UNIT PAGE HERE").pack()

    def refresh(self) -> None:
        pass