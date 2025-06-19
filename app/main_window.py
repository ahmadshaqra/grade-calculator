"""
    main_window.py

    Contains the main window logic.
"""

import tkinter as tk
from utils.asset_manager import AssetManager
from app.record_page import RecordPage
from app.wam_page import WAMPage
from app.gpa_page import GPAPage
from app.unit_page import UnitPage

class MainWindow(tk.Tk):
    """
        Manages the main window of the application.
    """

    def __init__(self) -> None:
        """
            Initialises the main window of the application.
        """

        # initialises main window and entry window
        super().__init__()
        self.withdraw()
        self.entry_window = None

        # sets title and icon
        self.title("Grade Calculator")
        self.iconbitmap(AssetManager.get_asset("icon.ico"))

        # sets the window dimensions
        window_width = 700
        window_height = 500

        # gets the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates desired window position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 30

        # sets window size and position and disables resizing
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        # sets title of main window
        tk.Label(self, text="Grade Calculator", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # sets frame to hold menu buttons
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(pady=10)

        # sets main content frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, pady=10)

        # initialises available pages
        self.pages = {
            "Record": RecordPage(self.main_frame, self),
            "WAM": WAMPage(self.main_frame, self),
            "GPA": GPAPage(self.main_frame, self),
            "Unit": UnitPage(self.main_frame, self)
        }

        # initialises menu buttons dictionary
        self.menu_btns = {}

        # iterates through pages
        for name, page in self.pages.items():

            # places page in main content frame
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

            # creates and adds menu button
            self.menu_btns[name] = tk.Button(self.menu_frame, text=name, font=("Segoe UI", 10, "bold"), width=10, command=lambda name=name: self.show_page(name))
            self.menu_btns[name].pack(side="left", expand=True, fill="both", padx=10)

        # shows window
        self.deiconify()

        # selects the first page
        self.show_page(next(iter(self.pages)))

    def show_page(self, name: str) -> None:
        """
            Displays selected page on the main content frame.

            Args:
                name (str): the name of the selected page.
        """

        # prevents an entry window from remaining open
        if self.entry_window and self.entry_window.winfo_exists():
            self.entry_window.destroy()
            self.entry_window = None

        # gets the page object from the pages dictionary
        page = self.pages[name]

        # displays page contents and refreshes it
        page.lift()
        page.load_page()

        # enables all menu buttons
        for btn in self.menu_btns.values():
            btn.config(state="normal")

        # disables selected page menu button
        self.menu_btns[name].config(state="disabled")

    def start(self) -> None:
        """
            Starts the window.
        """

        # calls the main loop of the window.
        self.mainloop()
