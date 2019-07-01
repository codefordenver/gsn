import json
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
        self.target_json_format = [
            {
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
                        "attendanceTotalUnexcusedAbsence": 29.0,
                        "attendanceTotalExcusedAbsence": 26.0,
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
            },
            ]
        #find target parent and housing fields
        #housing fields are parent fields that house child fields
        target_fields = list(self.target_json_format[0].keys())
        parent_fields = []
        housing_fields = []
        for field in target_fields:
            if self.target_json_format[0][field].__class__ == list:
                housing_fields.append(field)
            else:
                parent_fields.append(field)
        self.target_parent_fields = parent_fields
        self.target_housing_fields = housing_fields

        #find target child fields, child fields are housed in housing fields
        child_fields = {}
        for field in self.target_housing_fields:
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
        #find target field datatypes
        target_field_datatypes = {}
        for field in self.target_parent_fields:
            field_datatype = self.target_json_format[0][field].__class__.__name__
            pandas_datatype = self.datatypes_dict[field_datatype]
            target_field_datatypes[field] = pandas_datatype
        for housing_field in list(self.target_child_fields.keys()):
            for child_field in self.target_child_fields[housing_field]:
                field_datatype = self.target_json_format[0][housing_field][0][child_field].__class__.__name__
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
                    'studentFirstName': 'student.firstName',
                    'studentLastName': 'student.lastName',
                    "studentMiddleName": 'student.middleName',
                    "studentGender": 'student.gender',
                    "studentStateID": 'student.stateID',
                    'studentSISID': 'student.studentNumber',
                    'studentGradeYear': 'student.grade',
                    "courseName": 'grading.courseName',
                    "courseCode": 'grading.courseNumber',
                    "gradePeriod": 'grading.periodName',
                    "gradeTask":'grading.task',
                    "grade": 'grading.percent',
                    "attendanceTotalUnexcusedAbsence": 'attExactDailyTermCount.unexcusedAbsentDays',
                    "attendanceTotalAbsence": 'attExactDailyTermCount.absentDays',
                    'attendanceTotalTardies': "attExactDailyTermCount.tardies",
                    'behaviorContext': "behaviorDetail.contextDescription",
                    'behaviorSISID': "behaviorDetail.incidentID",
                    'behaviorIncidentTypeSchool': "behaviorDetail.eventName",
                    'behaviorIncidentResultSchool': "behaviorDetail.resolutionName",
                },
                "parse": {
                    "studentBirthday": [
                        'student.birthdate',
                        lambda dataframe: str(datetime.strptime(dataframe['student.birthdate'], "%m/%d/%Y")),
                    ],
                    'behaviorIncidentDate': [
                        "behaviorDetail.incidentDate",
                        lambda dataframe: str(datetime.strptime(dataframe['student.birthdate'], "%m/%d/%Y")),
                    ],
                    'gradeEntryDate': [
                        'grading.date',
                        lambda dataframe: str(datetime.strptime(dataframe['student.birthdate'], "%m/%d/%Y")),
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
                        lambda dataframe: dataframe["cal.endYear"] - 1 if dataframe["grading.termName"] == "S1" else dataframe["cal.endYear"] if dataframe["grading.termName"] == "S2" else False,
                    ],
                    "gradeCalendarTerm": [
                        "grading.termName",
                        lambda dataframe: "FLL" if dataframe["grading.termName"] == "S1" else "SPR" if dataframe["grading.termName"] == "S2" else False,
                    ],
                    "attendanceCalendarYear": [
                        "cal.endYear",
                        lambda dataframe: dataframe["cal.endYear"] - 1 if dataframe["attExactDailyTermCount.termName"] == "S1" else dataframe["cal.endYear"] if dataframe["attExactDailyTermCount.termName"] == "S2" else False,
                    ],
                    "attendanceCalendarTerm": [
                        "attExactDailyTermCount.termName",
                        lambda dataframe: "FLL" if dataframe["attExactDailyTermCount.termName"] == "S1" else "SPR" if dataframe["attExactDailyTermCount.termName"] == "S2" else False,
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
                        timezone.now(),
                    ],
                    "attendanceTotalExcusedAbsence": [
                        "attExactDailyTermCount.unexcusedAbsentDays",
                        lambda dataframe: dataframe['attExactDailyTermCount.absentDays'] - dataframe["attExactDailyTermCount.unexcusedAbsentDays"],
                    ],
                },
                "blank": [
                    "behaviorIncidentTypeProgram",
                    "behaviorIncidentResultProgram",
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

    def get_json_array(self, csv_df, id_field):
        #id_field is the name of a parent field from self.target_parent_fields
        #that uniquely identifies to what student data belongs to.
        #only parse grade elements with task == "Semester Grade"
        json_array = []
        parent_df = csv_df[self.target_parent_fields]
        parent_df = parent_df.drop_duplicates()
        for row in parent_df.itertuples():
            output = {}
            for field in self.target_parent_fields:
                output[field] = getattr(row, field)
            json_array.append(output)
        for housing_field in self.target_child_fields.keys():
            child_df_fields = self.target_child_fields[housing_field][:]
            child_df_fields.append(id_field)
            child_df = csv_df[child_df_fields]
            child_df.drop_duplicates()
            for parent_element in json_array:
                child_array = []
                for row in child_df.itertuples():
                    if getattr(row, id_field) == parent_element[id_field]:
                        output = {}
                        for field in self.target_child_fields[housing_field]:
                            output[field] = getattr(row, field)
                        child_array.append(output)
                parent_element[housing_field] = child_array
        return json_array

    def parse_json():
        """
        - use district = District(field = value) to instantiate and check, then save.
        - follow heirarchy through student, bring in course and calendar for grade/attendance.
        - use get or create like hannah, but allow for blanks
        - filter students first via HistoricalStudentID
        - only parse grade elements with task == "Semester Grade"
        """
        pass
