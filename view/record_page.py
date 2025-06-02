import tkinter as tk
class RecordPage(tk.Frame):

    def __init__(self, root: tk.Frame) -> None:
        super().__init__(root)
        tk.Label(self, text="RECORD PAGE HERE").pack()

    def refresh(self) -> None:
        pass