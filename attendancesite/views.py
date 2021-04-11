from django.shortcuts import render
from .Student import Student
import requests
from bs4 import BeautifulSoup

def index(request):
    return render(request,'attendui/index.html')

def attendance(request):
    if request.method=='POST':
        Username=request.POST['Uname']
        Password=request.POST['Password']
        student = main(Username, Password)
        if student is not None:
            attendance_info = student.attendance.get_full_information()
            subject_info,sub_name=student.subjects.all_subject_information()
            sub_name.sort()
            params={}
            if attendance_info['attend'] == 0:
                params={'name':student.name, 'percentage':round(attendance_info['percentage'],2), 'bunk': attendance_info['bunk'],'attend': attendance_info['attend']}
            else:
                params={'name':student.name, 'percentage':round(attendance_info['percentage'],2), 'bunk': attendance_info['bunk'], 'attend': attendance_info['attend']}
            sub_info={}
            for i in sub_name:
                sub_info[i]=subject_info[i]
            params['subject_info']=sub_info
            params['total_percentage'] = round(attendance_info['percentage'],2)
        else:
            return render(request,'attendui/index.html',{'error': 'wrong credentials'})

        return render(request,'attendui/show.html',params)

def main(username, password, retry=1):
    if retry:
        print('retrying: {}'.format(retry))
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.88 Safari/537.36"}

        # opts = webdriverOptions()
        # options.add_argument("--headless") # Runs Chrome in headless mode.
        attendance_url = 'http://app.bmiet.net/student/attendance/view'
        url = 'http://app.bmiet.net/student/login'
        form_action_url = 'http://app.bmiet.net/student/student-login'
        login_data = {'username': username,
                      'password': password}
        student_data = Student()  # Student class instance

        with requests.Session() as s:
            try:
                r = s.get(url, headers=headers)
            except:
                return None#self.main(username, password, retry + 1)
            #self.show_result.setText('    connected to the server')
            soup = BeautifulSoup(r.text, 'html5lib')
            login_data['_token'] = soup.find(
                'input', attrs={'name': '_token'})['value']
            r = s.post(form_action_url, data=login_data, headers=headers)

            # To extract student name from the dashboard page
            page = "".join(line.strip() for line in r.text.split("\n"))
            soup = BeautifulSoup(page, 'html5lib')
            try:
                student_data.name = soup.find(class_="user-panel").find('p').text
                #self.show_result.setText('   logged in')
            except AttributeError:
                print('wrong Credentials logout and check again')
                return None
            # # # # # # # # #

            dataset = []
            count = 0
            while True:
                r = s.get(attendance_url, headers=headers)
                page = "".join(line.strip() for line in r.text.split("\n"))
                soup = BeautifulSoup(page, 'html5lib')

                table = soup.find_all('tbody')[1]
                rows = table.find_all('tr')
                rows.pop()
                for row in rows:
                    row = row.find_all('td')
                    data_row = []
                    for cell in row:
                        data_row.append(cell.text)
                    dataset.append(data_row)
                    count += 1
                try:
                    attendance_url = soup.find('a', attrs={'rel': 'next'})['href']
                except TypeError:
                    break
            student_data.attendance_sheet(dataset)
        return student_data

def scapAttendance(s, headers, attendance_url):
    r = s.get(attendance_url, headers=headers)
    page = "".join(line.strip() for line in r.text.split("\n"))
    soup = BeautifulSoup(page, 'html5lib')
    dataset = []
    table = soup.find_all('tbody')[1]
    rows = table.find_all('tr')
    rows.pop()
    for row in rows:
        row = row.find_all('td')
        data_row = []
        for cell in row:
            data_row.append(cell.text)
        dataset.append(data_row)
    try:
        attendance_url = soup.find('a', attrs={'rel': 'next'})['href']
    except TypeError:
        pass
    return dataset

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
import json
class forAttendData(APIView):
    def get(self, request, username, password, format=None):
        name = username
        password = password
        student = main(name, password)
        if student is not None:
            attendance_info = student.attendance.get_full_information()
            subject_info,sub_name=student.subjects.all_subject_information()
            sub_name.sort()
            each_sub_info = {}
            for i in sub_name:
                each_sub_info[i]=subject_info[i]
            for i in attendance_info:
                each_sub_info[i]=attendance_info[i]
            json_obj = json.dumps(each_sub_info, indent=4)
        print(json_obj)
        return Response(json_obj)
