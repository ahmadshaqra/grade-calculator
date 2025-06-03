
from view.unit_page import UnitPage

class UnitManager:

    def __init__(self, file_manager: 'FileManager', main_window: 'MainWindow') -> None:

        self.file_manager = file_manager
        self.page = UnitPage(main_window.main_frame)


