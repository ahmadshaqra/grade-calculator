from model.record import Record
from view.record_page import RecordPage
from utils.file_manager import FileManager

class RecordManager:

    def __init__(self, page: RecordPage) -> None:

        self.filename = "record.txt"

        self.data = Record()
        self.page = page

        self.page.set_controller(self)

        data = FileManager.read_file(self.filename)

        self.data.set_data(data)

        self.page.refresh(data, self.data.wam(), self.data.gpa())

    def save_record(self, data: list[list[str]]) -> None:
        FileManager.write_file(self.filename, data)
        self.data.set_data(data)
        self.page.refresh(data, self.data.wam(), self.data.gpa())
        
