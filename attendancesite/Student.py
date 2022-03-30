from .Attendance import Attendance
from .Subjects import Subjects


class Student(object):
    def __init__(self, dataset: list = None):
        self.total_classes = 0
        self.total_present = 0
        self.name = ''
        if dataset is not None:
            self.subjects = Subjects(dataset)

        self.classes_to_attend = 0
        self.classes_to_bunk = 0
        self.attendance = Attendance()

    # to send one attendance at a time
    def pass_data_to_relevant_subject(self, data: list):
        self.subjects.pass_attendance(data)

    def attendance_sheet(self, attendance: list):  # 2-d list
        self.subjects = Subjects(attendance)
        self.overall_percentage(attendance)

    def overall_percentage(self, dataset):
        for data in dataset:
            if data[2]!="":
                self.attendance.add_attendance({'attendance': data[1]}, double_attendance=self._is_lab_subject(data[2]))

    def _is_lab_subject(self, subject_name) -> bool:
        subject_name = subject_name.lower()
        if not subject_name.find('lab') == -1:
            return True
        return False
