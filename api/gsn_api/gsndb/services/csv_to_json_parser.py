import json, os, csv
import pandas as pd
import numpy as np
from gsndb.models import Student, Program, District, School, Course, Grade, Attendance, Behavior, Calendar
"""NOTE: file must be run from gsn_api directory for testing"""

"""
Goal:get expected datatypes for fields in csv based on fieldnames in csv
Workflow:
    -map csv fields to model fields
    -map csv field datatypes to model field datatypes
            -get model field datatypes
            -get csv field datatypes
"""

#getting all possible model field datatypes
model_list = [
    Student,
    Program,
    District,
    School,
    Course,
    Grade,
    Attendance,
    Behavior,
    ]
field_descriptions = set()
for model in model_list:
    for field in model._meta.fields:
        field_descriptions.add(field.description)

#used field_descriptions set to create possible_datatypes dictionary
possible_datatypes = {
    #datatypes are NumPy dtypes, and 'object' for strings.
    #Note: django appears to want datetimes as strings, not np.datetime64
    'Foreign Key (type determined by related field)': np.int64,
    'Small integer': np.int64,
    'Integer': np.int64,
    'Date (without time)': object,
    'Boolean (Either True or False)': np.bool_,
    'String (up to %(max_length)s)': object,
    'Floating point number': np.float64,
    'Date (with time)': object,
    'Text': object,
    'Big (8 byte) integer': np.int64,
}

#map csv_fieldnames to model fields
csv_to_model_field_dict = {
    'studentFirstName': Student._meta.get_field("first_name"),
    'studentLastName': Student._meta.get_field("last_name"),
    'studentMiddleName': Student._meta.get_field("middle_name"),
    'studentGender': Student._meta.get_field("gender"),
    'studentBirthday': Student._meta.get_field("birth_date"),
    'studentStateID': Student._meta.get_field("state_id"),
    'studentGradeYear': Student._meta.get_field("grade_year"),
    'studentReasonInProgram': Student._meta.get_field("reason_in_program"),
    'programName': Program._meta.get_field("name"),
    'districtName': District._meta.get_field("name"),
    'districtState': District._meta.get_field("state"),
    'districtCity': District._meta.get_field("city"),
    'districtCode': District._meta.get_field("code"),
    'schoolName': School._meta.get_field("name"),
    'courseName': Course._meta.get_field("name"),
    'courseCode': Course._meta.get_field("code"),
    'courseSubject': Course._meta.get_field("subject"),
    'courseCalendarYear': Calendar._meta.get_field("year"),
    'courseCalendarTerm': Calendar._meta.get_field("term"),
    'gradePeriod': Grade._meta.get_field("period"),
    'grade': Grade._meta.get_field("grade"),
    'gradeTermFinalValue': Grade._meta.get_field("term_final_value"),
    'attendanceEntryDate': Attendance._meta.get_field("entry_datetime"),
    'attendanceTotalUnexcusedAbsence': Attendance._meta.get_field("total_unexabs"),
    'attendancetotalExcusedAbsence': Attendance._meta.get_field("total_exabs"),
    'attendanceTotalTardies': Attendance._meta.get_field("total_tardies"),
    'attendanceAverageDailyAttendance': Attendance._meta.get_field("avg_daily_attendance"),
    'attendanceTermFinalValue': Attendance._meta.get_field("term_final_value"),
    'behaviorPeriod': Behavior._meta.get_field("period"),
    'behaviorIncidentDate': Behavior._meta.get_field("incident_datetime"),
    'behaviorContext': Behavior._meta.get_field("context"),
    'behaviorIncidentTypeProgram': Behavior._meta.get_field("incident_type_program"),
    'behaviorIncidentResultProgram': Behavior._meta.get_field("incident_result_program"),
    'behaviorIncidentTypeSchool': Behavior._meta.get_field("incident_type_school"),
    'behaviorIncidentResultSchool': Behavior._meta.get_field("incident_result_school"),
    }

#get csv field datatypes for loading data into numpy array
csv_datatypes = {}
for fieldname, model_field_obj in csv_to_model_field_dict.items():
    datatype = possible_datatypes[model_field_obj.description]
    csv_datatypes[fieldname] = datatype

#load csv file as numpy array with datatypes dectated by csv_datatypes
__location__ = os.getcwd()
csv_file = open(os.path.join(__location__, "gsndb/services/test_parser.csv"))
csv_df = pd.read_csv(csv_file, dtype = csv_datatypes)
csv_file.close()

"""
Goal: take csv_df and create json array containing all data to add to database.
Workflow:
- define json fields
    - define what fields are parent fields and what parent field will house
      child fields. (to start: "courses" houses child fields)
- map all csv fields to json fields
- input csv_df into json array
    - create json elements containing only parent fields and add them to json
      array.
        - isolate all unique rows of csv_df pertaining to json parent fields.
    - add json child fields corresponding to json elements as sub element of "housing"
      parent field. (to start: "courses" houses child fields)
        - isolate all unique rows of the csv array pertaining to a parent json
          element.
"""

#Use csvParser.json as reference to define json fields, including parent and
#child fields, and housing field(s).
json_file = open(os.path.join(__location__, "gsndb/services/csvParser.json"))
data = json.load(json_file)
json_file.close()
parent_fields = list(data[0].keys())
housing_field = "courses"
parent_fields.remove(housing_field)
child_fields = list(data[0][housing_field][0].keys())

#map csv fields to json fields
csv_to_json_field_dict = {}
for name in child_fields:
    csv_to_json_field_dict[name] = name
for name in parent_fields:
    csv_to_json_field_dict[name] = name

#Isolate all unique rows of csv_df pertaining to json parent fields.
parent_df = csv_df[parent_fields]
parent_df = parent_df.drop_duplicates()

#add unique parent rows as json elements to json array.
json_array = []
for row in parent_df.itertuples():
    output = {}
    for field in parent_fields:
        output[field] = getattr(row, field)
    json_array.append(output)

#isolate all unique rows of the csv array pertaining to a parent json element.
#define csv_df field that uniquely associates rows with a student
id_field = "studentStateID"
child_df_fields = child_fields[:]
child_df_fields.append(id_field)
child_df = csv_df[child_df_fields]
child_df.drop_duplicates()

#insert unique child rows into existing parent elements of json array.
for parent_element in json_array:
    child_array = []
    for row in child_df.itertuples():
        if getattr(row, id_field) == parent_element[id_field]:
            output = {}
            for field in child_fields:
                output[field] = getattr(row, field)
            child_array.append(output)
    parent_element[housing_field] = child_array
