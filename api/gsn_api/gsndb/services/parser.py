import json
from datetime import datetime
import pandas as pd
import numpy as np
from django.utils import timezone
from gsndb.models import School, Student

class CSVParser():

    def __init__(self, string_file_obj, school_of_csv_origin, term_final_value = False):
        self.school_of_csv_origin = school_of_csv_origin
        self.School = School.objects.get(name = self.school_of_csv_origin)
        self.string_file_obj = string_file_obj
        self.term_final_value = term_final_value
        self.target_json_format = {
            "programName": "Eargo",
            "districtName": "Jeffco",
            "districtState": "PA",
            "districtCity": "Wakulla",
            "districtCode": "H382",
            "schoolName": "Carmody",
            "Student": [
                {
                    "studentFirstName": "Fuller",
                    "studentLastName": "Hahn",
                    "studentMiddleName": "Rodgers",
                    "studentGender": "M",
                    "studentBirthday": "2018-03-23",
                    "studentStateID": 542796,
                    "studentGradeYear": 9,
                    "studentReasonInProgram": "behavior",
                    "studentSISID": 298347928374,
                },
            ],
            "Course": [
                {
                    "courseName": "Algebra",
                    "courseCode": "G7384",
                    "courseSubject": "ENG",
                },
            ],
            "Grade": [
                {
                    "gradeStudentSISID": 19283192837,
                    "gradeCourseCode": "HG3848",
                    "gradeCalendarYear": 2004,
                    "gradeCalendarTerm": "SMR",
                    "gradePeriod": "6",
                    "grade": 0.8091,
                    "gradeTask": "Semester Grade",
                    "gradeTermFinalValue": True,
                    "gradeEntryDate": "2016-03-24",
                },
            ],
            "Attendance": [
                {
                    "attendanceStudentSISID": 19283192837,
                    "attendanceCalendarYear": 2004,
                    "attendanceCalendarTerm": "SMR",
                    "attendanceEntryDate": "2016-03-24",
                    "attendanceTotalUnexcusedAbsence": 9.0,
                    "attendanceTotalExcusedAbsence": 6.0,
                    "attendanceTotalAbsence": 54.0,
                    "attendanceTotalTardies": 11,
                    "attendanceAverageDailyAttendance": .98,
                    "attendanceTermFinalValue": True,
                },
            ],
            "Behavior": [
                {
                    "behaviorStudentSISID": 19283192837,
                    "behaviorCourseCode": "HG838",
                    "behaviorPeriod": "2",
                    "behaviorCalendarTerm": "SMR",
                    "behaviorCalendarYear": 2004,
                    "behaviorIncidentDate": "2014-06-26",
                    "behaviorContext": "H372",
                    "behaviorSISID": 293847923874,
                    "behaviorIncidentTypeProgram": "Small",
                    "behaviorIncidentResultProgram": "Bad",
                    "behaviorIncidentTypeSchool": "Medium",
                    "behaviorIncidentResultSchool": "Medium",
                },
            ],
        }
        #find target parent and housing fields, returns lists
        #housing fields are parent fields that house child fields
        target_fields = list(self.target_json_format.keys())
        parent_fields = []
        housing_fields = []
        for field in target_fields:
            if self.target_json_format[field].__class__ == list:
                housing_fields.append(field)
            else:
                parent_fields.append(field)
        self.target_parent_fields = parent_fields
        self.target_housing_fields = housing_fields

        #find target child fields, child fields are housed in housing fields
        #returns dictionary of housing field as keys and lists of child fields as values.
        child_fields = {}
        for field in self.target_housing_fields:
            output = list(self.target_json_format[field][0].keys())
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
        #find target field datatypes
        target_field_datatypes = {}
        for field in self.target_parent_fields:
            field_datatype = self.target_json_format[field].__class__.__name__
            pandas_datatype = self.datatypes_dict[field_datatype]
            target_field_datatypes[field] = pandas_datatype
        for housing_field in list(self.target_child_fields.keys()):
            for child_field in self.target_child_fields[housing_field]:
                field_datatype = self.target_json_format[housing_field][0][child_field].__class__.__name__
                pandas_datatype = self.datatypes_dict[field_datatype]
                target_field_datatypes[child_field] = pandas_datatype
        self.target_field_datatypes = target_field_datatypes

        #a dictionary of dictionaries linking target json fields to associated
        #csv fields based on school of origin.
        self.master_field_dict = {
            #Keys: json fields. Values: csv fields.
            "Trivial": {
                'studentFirstName': 'studentFirstName',
                'studentLastName': 'studentLastName',
                'studentMiddleName': "studentMiddleName",
                'studentGender': "studentGender",
                'studentBirthday': "studentBirthday",
                'studentStateID': "studentStateID",
                'studentGradeYear': "studentGradeYear",
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
                'behaviorIncidentTypeSchool': "behaviorIncidentTypeSchool",
                'behaviorIncidentResultSchool': "behaviorIncidentResultSchool",
            },
            "Weld Central Middle School": {
                "direct": {
                    'studentFirstName': "student.firstName",
                    'studentLastName': 'student.lastName',
                    "studentMiddleName": 'student.middleName',
                    "studentGender": 'student.gender',
                    "studentStateID": 'student.stateID',
                    'studentSISID': 'student.studentNumber',
                    'studentGradeYear': 'student.grade',
                    "courseName": 'grading.courseName',
                    "courseCode": 'grading.courseNumber',
                    'gradeCourseCode': 'grading.courseNumber',
                    "gradePeriod": 'grading.periodName',
                    "gradeTask":'grading.task',
                    "grade": 'grading.percent',
                    "gradeStudentSISID": 'student.studentNumber',
                    "attendanceStudentSISID": 'student.studentNumber',
                    "attendanceTotalUnexcusedAbsence": 'attExactDailyTermCount.unexcusedAbsentDays',
                    "attendanceTotalAbsence": 'attExactDailyTermCount.absentDays',
                    'attendanceTotalTardies': "attExactDailyTermCount.tardies",
                    "attendanceStudentSISID": 'student.studentNumber',
                    'behaviorContext': "behaviorDetail.contextDescription",
                    'behaviorSISID': "behaviorDetail.incidentID",
                    'behaviorIncidentTypeSchool': "behaviorDetail.eventName",
                    'behaviorIncidentResultSchool': "behaviorDetail.resolutionName",
                    "behaviorStudentSISID": 'student.studentNumber',
                },
                "parse": {
                    "studentBirthday": [
                        'student.birthdate',
                        lambda dataframe_row: str(datetime.strptime(dataframe_row['student.birthdate'], "%m/%d/%Y")),
                    ],
                    'behaviorIncidentDate': [
                        "behaviorDetail.incidentDate",
                        lambda dataframe_row: str(datetime.strptime(dataframe_row['behaviorDetail.incidentDate'], "%m/%d/%Y")),
                    ],
                    'gradeEntryDate': [
                        'grading.date',
                        lambda dataframe_row: str(datetime.strptime(dataframe_row['grading.date'], "%m/%d/%Y")),
                    ],
                    "programName": [
                        "django",
                        'Expelled and At-Risk Student Services Program',
                    ],
                    "districtName": [
                        "django",
                        self.School.district.name,
                    ],
                    "districtState": [
                        "django",
                        self.School.district.state,
                    ],
                    "districtCity": [
                        "django",
                        self.School.district.city,
                    ],
                    "districtCode": [
                        "django",
                        self.School.district.code,
                    ],
                    "schoolName": [
                        "django",
                        self.School.name,
                    ],
                    "gradeCalendarYear": [
                        "cal.endYear",
                        lambda dataframe_row: dataframe_row['cal.endYear'] - 1 if dataframe_row['grading.termName'] == "S1" else dataframe_row['cal.endYear'] if dataframe_row['grading.termName'] == "S2" else None,
                    ],
                    "gradeCalendarTerm": [
                        "grading.termName",
                        lambda dataframe_row: "FLL" if dataframe_row['grading.termName'] == "S1" else "SPR" if dataframe_row['grading.termName'] == "S2" else None,
                    ],
                    "attendanceCalendarYear": [
                        "cal.endYear",
                        lambda dataframe_row: dataframe_row['cal.endYear'] - 1 if dataframe_row['attExactDailyTermCount.termName'] == "S1" else dataframe_row['cal.endYear'] if dataframe_row['attExactDailyTermCount.termName'] == "S2" else None,
                    ],
                    "attendanceCalendarTerm": [
                        "attExactDailyTermCount.termName",
                        lambda dataframe_row: "FLL" if dataframe_row['attExactDailyTermCount.termName'] == "S1" else "SPR" if dataframe_row['attExactDailyTermCount.termName'] == "S2" else None,
                    ],
                    "gradeTermFinalValue": [
                        "django",
                        self.term_final_value,
                    ],
                    "attendanceTermFinalValue": [
                        "django",
                        self.term_final_value,
                    ],
                    "attendanceEntryDate": [
                        "django",
                        str(timezone.now()),
                    ],
                    "attendanceTotalExcusedAbsence": [
                        "attExactDailyTermCount.unexcusedAbsentDays",
                        lambda dataframe_row: round(dataframe_row['attExactDailyTermCount.absentDays'] - dataframe_row['attExactDailyTermCount.unexcusedAbsentDays'], 2)
                    ],
                },
                "blank": [
                    "behaviorIncidentTypeProgram",
                    "behaviorIncidentResultProgram",
                    "behaviorCourseCode",
                    "studentReasonInProgram",
                    "attendanceAverageDailyAttendance",
                    "behaviorPeriod",
                    "behaviorCalendarTerm",
                    "behaviorCalendarYear",
                    "courseSubject",
                ]
            }
        }

    def get_csv_datatypes(self):
        """
        returns dictionary mapping the datatypes that should be applied to the
        dataframe created from the csv file.
        """
        json_to_csv_field_dict = self.master_field_dict[self.school_of_csv_origin]
        csv_datatypes = {}
        for json_field, csv_field in json_to_csv_field_dict["direct"].items():
            datatype = self.target_field_datatypes[json_field]
            csv_datatypes[csv_field] = datatype
        for json_field, parsing_pair in json_to_csv_field_dict["parse"].items():
            csv_field = parsing_pair[0]
            if csv_field != "django":
                datatype = self.target_field_datatypes[json_field]
                csv_datatypes[csv_field] = datatype
        return csv_datatypes

    def get_dataframe(self, csv_datatypes):
        """
        creates dataframe from csv file, using datatypes found with get_csv_datatypes()
        for the datatype of each column.
        """
        csv_df = pd.read_csv(self.string_file_obj, dtype = csv_datatypes, sep = ',')
        return csv_df

    def build_json(self, csv_df):
        json_to_csv_field_dict = self.master_field_dict[self.school_of_csv_origin]

        direct_dict = json_to_csv_field_dict["direct"]
        direct_fields = list(direct_dict.keys())

        parse_dict = json_to_csv_field_dict["parse"]
        parse_fields = list(parse_dict.keys())

        blank_fields = json_to_csv_field_dict["blank"]

        output = {}

        for field in self.target_parent_fields:
            csv_field = parse_dict[field][0]
            value = parse_dict[field][1]
            output[field] = value

        for housing_field, child_fields in self.target_child_fields.items():

            #get subset dataframe of csv dataframe that corresponds to the housing field.
            subset_fields = []
            for child_field in child_fields:
                if child_field in direct_fields:
                    csv_field = direct_dict[child_field]
                    subset_fields.append(csv_field)
                elif child_field in parse_fields:
                    csv_field = parse_dict[child_field][0]
                    if csv_field == "django":
                        continue
                    else:
                        subset_fields.append(csv_field)
                elif child_field in blank_fields:
                    continue
            subset_fields = set(subset_fields)
            child_df = csv_df[subset_fields]
            child_df.drop_duplicates(inplace = True)
            replacement_for_nan = "@ fOr RePlacIng np.NaN!!!"
            child_df.replace(np.nan, replacement_for_nan, inplace = True)

            #turn rows of subset dataframe into json elements
            housing_output = []

            for index, row in child_df.iterrows():
                child_output = {}
                for child_field in child_fields:
                    if child_field in direct_fields:
                        csv_field = direct_dict[child_field]
                        value = row[csv_field]
                    elif child_field in parse_fields:
                        csv_field = parse_dict[child_field][0]
                        if csv_field == "django":
                            value = parse_dict[child_field][1]
                        else:
                            lambda_parser = parse_dict[child_field][1]
                            value = lambda_parser(row)
                    elif child_field in blank_fields:
                        value = None
                    if value == replacement_for_nan:
                        value = None
                    child_output[child_field] = value
                housing_output.append(child_output)
            output[housing_field] = housing_output
        return output

    def parse_json(self, json_obj):
        return json_obj
        """
        - use district = District(field = value) to instantiate and check, then save.
        - follow heirarchy through student, bring in course and calendar for grade/attendance.
        - use get or create like hannah, but allow for blanks
        - filter students first via HistoricalStudentID
        - only parse grade elements with task == "Semester Grade"
        """
