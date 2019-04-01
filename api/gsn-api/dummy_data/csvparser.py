import csv
import json
from datetime import datetime

"""Notes:
        When referencing a foreign key, the field name should just be the name of the referenced model, as opposed to appending the word 'id' to the end: i.e. - "district" is good "district_id" is bad. The reasoning goes that any foreign key relationship is actually referencing an instance of another table, not just that table's id. We only use an id as reference in the specific case of loading fixtures for initial data. Following this naming convention should prevent any confusion.
"""

json_array = []
writer = open('database_fixture.json', 'w')

with open('user_app.CustomUser.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "user_app.customuser",
            "pk" : int(row['id']),
            "fields" : {
                "username" : row['username'],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "groups" : row["groups"],
                "user_permissions" : row["user_permissions"],
                "is_staff" : row["is_staff"],
                "is_active" : row["is_active"],
                "is_superuser" : row["is_superuser"],
                "last_login" : row["last_login"],
                "date_joined" : row["date_joined"],
            }
        }
        json_array.append(output)

with open('gsndb.District.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.district",
            "pk" : int(row['id']),
            "fields" : {
                "name" : row['name'],
                "state" : row['state'],
                "city" : row['city'],
                "code" : row['code']
            }
        }
        json_array.append(output)


with open('gsndb.School.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.school",
            "pk" : int(row['id']),
            "fields" : {
                "name" : row['name'],
                "district" : int(row['district']),
            }
        }
        json_array.append(output)

with open('gsndb.Program.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.program",
            "pk" : int(row['id']),
            "fields" : {
                "name" : row['name'],
            }
        }
        json_array.append(output)

with open('gsndb.Calendar.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.calendar",
            "pk" : int(row['id']),
            "fields" : {
                "year" : int(row['year']),
                "term" : row["term"],
            }
        }
        json_array.append(output)

with open('gsndb.Course.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.course",
            "pk" : int(row['id']),
            "fields" : {
                "code" : row['code'],
                "name" : row["name"],
                "subject" : row["subject"],
                "school" : int(row["school"])
            }
        }
        json_array.append(output)


with open('gsndb.Student.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.student",
            "pk" : int(row['id']),
            "fields" : {
                "current_school" : int(row["current_school"]),
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "middle_name" : row["middle_name"],
                "gender" : row["gender"],
                "birthdate" : row["birthdate"],
                "state_id" : int(row["state_id"]),
                "grade_year" : int(row["grade_year"]),
                "current_program" : int(row["program"]),
                "reason_in_program" : row["reason_in_program"]
            }
        }
        json_array.append(output)


with open('gsndb.Grade.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.grade",
            "pk" : int(row["id"]),
            "fields" : {
                "student" : int(row["student"]),
                "course" : int(row["course"]),
                "calendar" : int(row["calendar"]),
                "program" : int(row["program"]),
                "period" : int(row["period"]),
                "entry_datetime" : row["entry_datetime"],
                "grade" : float(row["grade"]),
                "term_final_value" : row["term_final_value"]
            }
        }
        json_array.append(output)

with open('gsndb.Attendance.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.attendance",
            "pk" : int(row["id"]),
            "fields" : {
                "student" : int(row["student"]),
                "school" : int(row["school"]),
                "program" : int(row["program"]),
                "entry_datetime" : row["entry_datetime"],
                "calendar" : int(row["calendar"]),
                "total_unexabs" : int(row["total_unexabs"]),
                "total_exabs" : int(row["total_exabs"]),
                "total_tardies" : int(row["total_tardies"]),
                "avg_daily_attendance" : float(row["avg_daily_attendance"]),
                "term_final_value" : row["term_final_value"],
            }
        }
        json_array.append(output)

with open('gsndb.Behavior.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.behavior",
            "pk" : int(row["id"]),
            "fields" : {
                "student" : int(row["student"]),
                "school" : int(row["school"]),
                "calendar" : int(row["calendar"]),
                "program" : int(row["program"]),
                "course" : int(row["course"]),
                "period" : int(row["period"]),
                "incident_datetime" : row["incident_datetime"],
                "context" : row["context"],
                "incident_type_program" : row["incident_type_program"],
                "incident_result_program" : row["incident_result_program"],
                "incident_type_school" : row["incident_type_school"],
                "incident_result_school" : row["incident_result_school"],
            }
        }
        json_array.append(output)

with open('gsndb.Referral.csv', newline='') as f:
    reader = csv.DictReader(f)
    csv_array = []
    for row in reader:
        output = {
            "model" : "gsndb.referral",
            "pk" : int(row['id']),
            "fields" : {
                "user" : int(row['user']),
                "student" : int(row["student"]),
                "program" : int(row["program"]),
                "type" : row["type"],
                "date_given" : row["date_given"],
                "reference_name" : row["reference_name"],
                "reference_phone" : row["reference_phone"],
                "reference_address" : row["reference_address"],
                "reason" : row["reason"],
            }
        }
        json_array.append(output)

    json_data = json.dumps(json_array, indent=4)
    writer.write(json_data)
