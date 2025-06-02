from model.record import Record
from view.record_page import RecordPage

class RecordManager:

    def __init__(self, file_manager: 'FileManager', main_window: 'MainWindow') -> None:

        self.file_manager = file_manager
        self.data = Record()
        self.page = RecordPage(main_window.main_frame)

        data = self.file_manager.read_file("record.txt")
        print(data)
        self.data.set_record(data)

        self.page.refresh(data, self.data.wam(), self.data.gpa())