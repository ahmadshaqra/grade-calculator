


from view.main_window import MainWindow

from view.record_page import RecordPage
from view.wam_page import WAMPage
from view.gpa_page import GPAPage
from view.unit_page import UnitPage

from controller.record_manager import RecordManager
from controller.wam_manager import WAMManager
from controller.gpa_manager import GPAManager
from controller.unit_manager import UnitManager

class App:

    def __init__(self):

        self.main_window = MainWindow(self)

        self.pages = {
            "Record": RecordPage(self.main_window.main_frame),
            # "WAM": WAMPage(self.main_window.main_frame),
            # "GPA": GPAPage(self.main_window.main_frame),
            # "Unit": UnitPage(self.main_window.main_frame)
        }

        self.main_window.set_menu(self.pages.keys())

        self.controllers = {
            "Record": RecordManager(self.pages["Record"]),
            # "WAM": WAMManager(self.pages["WAM"]),
            # "GPA": GPAManager(self.pages["GPA"]),
            # "Unit": UnitManager(self.pages["Unit"])
        }

    def start(self):
        self.main_window.mainloop()

    def show_page(self, name: str) -> None:
        """
            Displays selected page on the main content frame.

            Args:
                name (str): the name of the selected page.
        """

        # gets the page object from the pages dictionary
        page = self.pages[name]

        # displays page contents and refreshes it
        page.lift()
        # page.refresh()

        self.main_window.select_button(name)
