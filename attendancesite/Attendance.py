class Attendance(object):
    def __init__(self):
        self.present = 0
        self.absent = 0
        self.percentage = 0
        self.classes_to_attend = 0
        self.classes_to_bunk = 0
        self.recordChanged = False
        self.adder = 1

    # eg: singleAttendance =  {'attendance': 'present'} or {'attendance': 'absent}
    def add_attendance(self, single_attendance: dict, double_attendance=False):
        self.adder = 1
        if double_attendance:
            self.adder = 2
        if single_attendance['attendance'] == 'Present':
            self.present += self.adder
            self.recordChanged = True
        elif single_attendance['attendance'] == 'Absent':
            self.absent += self.adder
            self.recordChanged = True
        else:
            print('Instead of attendance got: {}'.format(
                single_attendance))

    def get_full_information(self):
        if self.recordChanged:
            self._update_data()

        return {'present': self.present, 'absent': self.absent, 'percentage': self.percentage,
                'attend': self.classes_to_attend, 'bunk': self.classes_to_bunk, 'adder': self.adder}

    def get_percentage(self):
        if self.recordChanged:
            self._update_data()
        return self.percentage

    def _update_data(self):
        self._calculate_percentage()
        self._classes_to_bunk()
        self.recordChanged = False

    def _classes_to_bunk(self):
        total_classes = self.present + self.absent

        if self.percentage < 75.0:
            self.classes_to_attend = (
                                             (75 * total_classes) - (self.present * 100)) / 25
            self.classes_to_attend = int(self.classes_to_attend)
        else:
            self.classes_to_bunk = ((self.present * 100) / 75) - total_classes
            self.classes_to_bunk = int(self.classes_to_bunk)

    def _calculate_percentage(self):
        total_classes = self.present + self.absent
        self.percentage = (self.present / total_classes) * 100
