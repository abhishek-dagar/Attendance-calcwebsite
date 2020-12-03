from .Attendance import Attendance


class Subjects(object):
    def __init__(self, dataset):
        self.subjectsDict = {}  # contains Subject object as value
        self.overall_percentage = None
        self.total_present = None
        self.total_absent = None
        if dataset is not None:
            for data in dataset:
                self.pass_attendance(data)

    # take one attendance at a time as an argument
    def pass_attendance(self, data: list):
        subject_name = data[2]
        if subject_name in self.subjectsDict:
            self.subjectsDict[subject_name].attendance.add_attendance(
                {'attendance': data[1]}, double_attendance=self._is_lab_subject(
                    subject_name))
        else:
            self.subjectsDict[subject_name] = Subject(subject_name)
            self.subjectsDict[subject_name].attendance.add_attendance({'attendance': data[1]},
                                                                      double_attendance=self._is_lab_subject(
                                                                          subject_name))

    def _is_lab_subject(self, subject_name) -> bool:
        subject_name = subject_name.lower()
        if not subject_name.find('lab') == -1:
            return True
        return False

    def all_subject_information(self):
        data = {}
        sub_name=[]
        for subject_name, subject_object in self.subjectsDict.items():
            data[subject_name] = subject_object.attendance.get_full_information()
            sub_name.append(subject_name)
        return data,sub_name


class Subject(object):
    def __init__(self, subject_name: str):
        self.name: str = subject_name
        self.attendance = Attendance()
