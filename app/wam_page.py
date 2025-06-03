import tkinter as tk
class WAMPage(tk.Frame):
    def __init__(self, root: tk.Frame) -> None:
        super().__init__(root)
        tk.Label(self, text="WAM PAGE HERE").pack()
    def load_page(self) -> None:
        pass
