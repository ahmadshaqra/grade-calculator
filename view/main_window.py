"""
    main_window.py

    Contains the main window UI logic.
"""

import tkinter as tk
# from controller.app import App

class MainWindow(tk.Tk):
    """
        Manages the main window of the application.
    """

    def __init__(self, app: 'App') -> None:
        """
            Initialises the main window of the application.
        """

        # initialises main window and app
        super().__init__()
        self.app = app

        # sets title
        self.title("Grade Calculator")

        # sets the window dimensions
        window_width = 600
        window_height = 400

        # gets the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculates desired window position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 25

        # sets window size and position and disables resizing
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        # sets title of main window
        tk.Label(self, text="Grade Calculator", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # sets frame to hold menu buttons
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(pady=5)

        # sets main content frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, pady=5)

    def set_menu(self, pages: list[str]) -> None:

        # initialises menu buttons dictionary
        self.menu_btns = {}

        # iterates through pages
        for name in pages:

            # creates and adds menu button
            self.menu_btns[name] = tk.Button(self.menu_frame, text=name, font=("Segoe UI", 10, "bold"), width=10, command=lambda name=name: self.app.show_page(name))
            self.menu_btns[name].pack(side="left", expand=True, fill="both", padx=10)

        # selects the first page
        self.app.show_page(next(iter(pages)))

    def select_button(self, name: str) -> None:

        # enables all menu buttons
        for btn in self.menu_btns.values():
            btn.config(state="normal")

        # disables selected page menu button
        self.menu_btns[name].config(state="disabled")

    # def show_page(self, name: str) -> None:
    #     """
    #         Displays selected page on the main content frame.

    #         Args:
    #             name (str): the name of the selected page.
    #     """

    #     # gets the page object from the pages dictionary
    #     page = self.pages[name]

    #     # displays page contents and refreshes it
    #     page.lift()
    #     page.refresh()

    #     # enables all menu buttons
    #     for btn in self.menu_btns.values():
    #         btn.config(state="normal")

    #     # disables selected page menu button
    #     self.menu_btns[name].config(state="disabled")

    # def start(self) -> None:
    #     """
    #         Starts the window.
    #     """

    #     # calls the main loop of the window.
    #     self.mainloop()
