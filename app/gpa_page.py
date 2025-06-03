import tkinter as tk
class GPAPage(tk.Frame):
    def __init__(self, root: tk.Frame) -> None:
        super().__init__(root)
        tk.Label(self, text="GPA PAGE HERE").pack()
    def refresh(self) -> None:
        pass
