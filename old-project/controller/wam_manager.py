
from view.wam_page import WAMPage

class WAMManager:

    def __init__(self, file_manager: 'FileManager', main_window: 'MainWindow') -> None:

        self.file_manager = file_manager
        self.page = WAMPage(main_window.main_frame)


