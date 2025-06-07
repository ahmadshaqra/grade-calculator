import tkinter as tk
class UnitPage(tk.Frame):
    def __init__(self, root: tk.Frame, main_window: tk.Tk) -> None:
        super().__init__(root)
        tk.Label(self, text="UNIT PAGE HERE").pack()
    def load_page(self) -> None:
        pass
