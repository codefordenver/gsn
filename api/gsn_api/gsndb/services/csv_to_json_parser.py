import json
import pandas as pd
import numpy as np
from gsndb.models import Student, Program, District, School, Course, Grade, Attendance, Behavior, Calendar

class CSVToJsonParser():
    def __init__(self, school_of_csv_origin):
        #self.string_file_obj = string_file_obj
        self.school_of_csv_origin = school_of_csv_origin
        target_json_format = [
            {
            "studentFirstName": "Fuller",
            "studentLastName": "Hahn",
            "studentMiddleName": "Rodgers",
            "studentGender": "M",
            "studentBirthday": "2018-03-23",
            "studentStateID": 542796,
            "studentGradeYear": 9,
            "studentReasonInProgram": "behavior",
            "programName": "Eargo",
            "districtName": "Jeffco",
            "districtState": "PA",
            "districtCity": "Wakulla",
            "districtCode": "H382",
            "schoolName": "Carmody",
            "courses": [
                {
                "courseName": "Algebra",
                "courseCode": "G7384",
                "courseSubject": "ENG",
                "courseCalendarYear": 2004,
                "courseCalendarTerm": "SMR",
                "gradePeriod": 6,
                "grade": 0.8091,
                "gradeTermFinalValue": True,
                "attendanceEntryDate": "2016-03-24",
                "attendanceTotalUnexcusedAbsence": 28,
                "attendancetotalExcusedAbsence": 26,
                "attendanceTotalTardies": 11,
                "attendanceAverageDailyAttendance": 27,
                "attendanceTermFinalValue": True,
                "behaviorPeriod": 2,
                "behaviorIncidentDate": "2014-06-26",
                "behaviorContext": "H372",
                "behaviorIncidentTypeProgram": "Small",
                "behaviorIncidentResultProgram": "Bad",
                "behaviorIncidentTypeSchool": "Medium",
                "behaviorIncidentResultSchool": "Medium"
                },
                ],
            },
            ]
        self.target_json_format = json.dumps(target_json_format, separators = (",", ":"))

parser = CSVToJsonParser("Trivial")
print(parser.target_json_format)

"""
        parent_fields = list(self.json_target_format[0].keys())
        housing_fields = []
        #housing fields are parent fields that house child fields
        for field in parent_fields:
            if self.json_target_format[field].__class__ == list:
                housing_fields.append(field)
                parent_fields.remove(field)
        self.target_parent_fields = parent_fields
        self.target_housing_fields = housing_fields

        child_fields = {}
        for field in housing_fields:
            output = list(self.target_json_format[0][field][0].keys())
            child_fields[field] = output
        self.target_child_fields = child_fields

        self.datatypes_dict = {
            #datatypes are NumPy dtypes, and 'object' for strings.
            #Note: django appears to want datetimes as strings, not np.datetime64
            'int': np.int64,
            'str': object,
            'bool': np.bool_,
            'float': np.float64,
        }

        target_field_datatypes = {}
        for field in self.target_parent_fields:
            field_datatype = self.target_json_format[0][field].__class__.__name__
            if field_datatype not in list(target_field_datatypes.keys()):
                pandas_datatype = self.datatypes_dict[field_datatype]
                target_field_datatypes[field] = pandas_datatype
        for housing_field in list(self.target_child_fields.keys()):
            for child_field in self.target_child_fields[housing_field]:
                field_datatype = self.target_json_format[0][housing_field][0][child_field].__class__.__name__
                if field_datatype not in list(target_field_datatypes.keys()):
                    pandas_datatype = self.datatypes_dict[field_datatype]
                    target_field_datatypes[child_field] = pandas_datatype
        self.target_field_datatypes = target_field_datatypes

        self.csv_to_json_field_dict = {
            "Trivial": {
                'studentFirstName': 'studentFirstName',
                'studentLastName': 'studentLastName',
                'studentMiddleName': "studentMiddleName",
                'studentGender': "studentGender",
                'studentBirthday': "studentBirthday",
                'studentStateID': "studentStateID",
                'studentGradeYear': "studentGradeYear",
                'studentReasonInProgram': "studentReasonInProgram",
                'programName': "programName",
                'districtName': "districtName",
                'districtState': "districtState",
                'districtCity': "districtCity",
                'districtCode': "districtCode",
                'schoolName': "schoolName",
                'courseName': "courseName",
                'courseCode': "courseCode",
                'courseSubject': "courseSubject",
                'courseCalendarYear': "courseCalendarYear",
                'courseCalendarTerm': "courseCalendarTerm",
                'gradePeriod': "gradePeriod",
                'grade': "grade",
                'gradeTermFinalValue': "gradeTermFinalValue",
                'attendanceEntryDate': "attendanceEntryDate",
                'attendanceTotalUnexcusedAbsence': "attendanceTotalUnexcusedAbsence",
                'attendancetotalExcusedAbsence': "attendancetotalExcusedAbsence",
                'attendanceTotalTardies': "attendanceTotalTardies",
                'attendanceAverageDailyAttendance': "attendanceAverageDailyAttendance",
                'attendanceTermFinalValue': "attendanceTermFinalValue",
                'behaviorPeriod': "behaviorPeriod",
                'behaviorIncidentDate': "behaviorIncidentDate",
                'behaviorContext': "behaviorContext",
                'behaviorIncidentTypeProgram': "behaviorIncidentTypeProgram",
                'behaviorIncidentResultProgram': "behaviorIncidentResultProgram",
                'behaviorIncidentTypeSchool': "behaviorIncidentTypeSchool",
                'behaviorIncidentResultSchool': "behaviorIncidentResultSchool",
                },
        }

    def get_csv_datatypes(self, school_of_csv_origin):
        csv_to_json_field_dict = self.csv_to_json_field_dict[school_of_csv_origin]
        csv_datatypes = {}
        for csv_field, json_field in csv_to_json_field_dict.items():
            datatype = self.target_field_datatypes[json_field]
            csv_datatypes[csv_field] = datatype
        return csv_datatypes

    def get_dataframe(self, string_file_obj, csv_datatypes):
        csv_df = pd.read_csv(string_file_obj, dtype = csv_datatypes)
        return csv_df

    def get_json_array(self, csv_df, id_field):
        #id_field is the name of a parent field from self.target_parent_fields
        #that uniquely identifies to what student data belongs to.
        json_array = []
        parent_df = csv_df[self.target_parent_fields]
        parent_df = parent_df.drop_duplicates()
        for row in parent_df.itertuples():
            output = {}
            for field in self.target_parent_fields:
                output[field] = getattr(row, field)
            json_array.append(output)
        for housing_field in self.target_child_fields.keys():
            child_df_fields = self.targetchild_fields[housing_field][:]
            child_df_fields.append(id_field)
            child_df = csv_df[child_df_fields]
            child_df.drop_duplicates()
            for parent_element in json_array:
                child_array = []
                for row in child_df.itertuples():
                    if getattr(row, id_field) == parent_element[id_field]:
                        output = {}
                        for field in child_fields:
                            output[field] = getattr(row, field)
                        child_array.append(output)
                parent_element[housing_field] = child_array
        return json_array
"""
