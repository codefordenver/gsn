""" 
    I am but an empty file desparetely in search of a purpose in life...
    Please turn me into a script for parsing csv files!
"""
data from json 

# this takes data from json (using csvParser.json to test) 
# and inputs it into the various models
# csvParser.json is an example of the type of json it can accept as input
import json
import os
from gsndb.models import District, School, Program, Student, Course, Attendance, Grade, Behavior, Calendar

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = open(os.path.join(__location__, 'csvParser.json'))
jsonData = json.load(file)
file.close()


for i in range(0,len(jsonData)-1):
    newDistrict= District.objects.get_or_create(
        state = jsonData[i]['districtState'],
        city = jsonData[i]['districtCity'],
        code = jsonData[i]['districtCode'],
        name = jsonData[i]['districtName']
    )[0]

    newSchool = School.objects.get_or_create(
        name = jsonData[i]['schoolName'],
        district = newDistrict
    )[0]

    newProgram = Program.objects.get_or_create(
        name = jsonData[i]['programName']
    )[0]

    newStudent = Student.objects.get_or_create(
        current_school = newSchool,
        current_program = newProgram,
        first_name = jsonData[i]['studentFirstName'],
        last_name = jsonData[i]['studentLastName'],
        middle_name = jsonData[i]['studentMiddleName'],
        gender = jsonData[i]['studentGender'],
        birth_date = jsonData[i]['studentBirthday'],
        state_id = jsonData[i]['studentStateID'],
        grade_year = jsonData[i]['studentGradeYear'],
        reason_in_program = jsonData[i]['studentReasonInProgram']
    )[0]

    for j in range(0,len(jsonData[i]['courses'])-1):

        newCalendar = Calendar.objects.get_or_create(
            year = jsonData[i]['courses'][j]['courseCalendarYear'],
            term = jsonData[i]['courses'][j]['courseCalendarTerm']
        )[0]

        newCourse = Course.objects.get_or_create(
            school = newSchool,
            name = jsonData[i]['courses'][j]['courseName'],
            code = jsonData[i]['courses'][j]['courseCode'],
            subject = jsonData[i]['courses'][j]['courseSubject']
        )[0]

        newGrade = Grade.objects.get_or_create(
            student = newStudent,
            course = newCourse,
            calendar = newCalendar,
            program = newProgram,
            period = jsonData[i]['courses'][j]['gradePeriod'],
            grade = jsonData[i]['courses'][j]['grade'],
            term_final_value = jsonData[i]['courses'][j]['gradeTermFinalValue']
        )[0]

        newAttendance = Attendance.objects.get_or_create(
            student = newStudent,
            school  = newSchool,
            calendar = newCalendar,
            program = newProgram,
            total_unexabs = jsonData[i]['courses'][j]['attendanceTotalUnexcusedAbsence'],
            total_exabs = jsonData[i]['courses'][j]['attendancetotalExcusedAbsence'],
            total_tardies = jsonData[i]['courses'][j]['attendanceTotalTardies'],
            avg_daily_attendance = jsonData[i]['courses'][j]['attendanceAverageDailyAttendance'],
            term_final_value = jsonData[i]['courses'][j]['attendanceTermFinalValue']
        )[0]

        newBehavior = Behavior.objects.get_or_create(
            student = newStudent,
            school = newSchool,
            calendar = newCalendar,
            program = newProgram,
            course = newCourse,
            period = jsonData[i]['courses'][j]['behaviorPeriod'],
            incident_datetime = jsonData[i]['courses'][j]['behaviorIncidentDate'],
            context = jsonData[i]['courses'][j]['behaviorContext'],
            incident_type_program = jsonData[i]['courses'][j]['behaviorIncidentTypeProgram'],
            incident_result_program = jsonData[i]['courses'][j]['behaviorIncidentResultProgram'],
            incident_type_school = jsonData[i]['courses'][j]['behaviorIncidentTypeSchool'],
            incident_result_school = jsonData[i]['courses'][j]['behaviorIncidentResultSchool']
        )[0]
