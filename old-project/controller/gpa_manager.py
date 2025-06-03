
from view.gpa_page import GPAPage

class GPAManager:

    def __init__(self, file_manager: 'FileManager', main_window: 'MainWindow') -> None:

        self.file_manager = file_manager
        self.page = GPAPage(main_window.main_frame)


