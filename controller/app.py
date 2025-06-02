


from controller.file_manager import FileManager
from view.main_window import MainWindow

from controller.record_manager import RecordManager
from controller.wam_manager import WAMManager
from controller.gpa_manager import GPAManager
from controller.unit_manager import UnitManager

class App:

    def __init__(self):

        self.file_manager = FileManager()
        self.main_window = MainWindow(self)

        self.controllers = {
            "Record": RecordManager(self.file_manager, self.main_window),
            "WAM": WAMManager(self.file_manager, self.main_window),
            "GPA": GPAManager(self.file_manager, self.main_window),
            "Unit": UnitManager(self.file_manager, self.main_window)
        }

        self.main_window.set_menu(self.controllers.keys())

    def start(self):
        self.main_window.mainloop()


    def show_page(self, name: str) -> None:
        """
            Displays selected page on the main content frame.

            Args:
                name (str): the name of the selected page.
        """

        # gets the page object from the pages dictionary
        page = self.controllers[name].page

        # displays page contents and refreshes it
        page.lift()
        # page.refresh()

        self.main_window.select_button(name)
