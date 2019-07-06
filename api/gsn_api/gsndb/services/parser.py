import json
from datetime import datetime
import pandas as pd
import numpy as np
from django.utils import timezone
from gsndb.models import Program, District, School, Course, Student, Calendar, HistoricalStudentID, Grade, Attendance, Behavior
from gsndb.serializers import ParserStudentSerializer, ParserCourseSerializer

class CSVParser():

    def __init__(self, string_file_obj, school_of_csv_origin, term_final_value = False):
        self.school_of_csv_origin = school_of_csv_origin
        self.School = School.objects.get(name = self.school_of_csv_origin)
        self.string_file_obj = string_file_obj
        self.term_final_value = term_final_value
        self.exceptions = []
        self.json_object = {"Not created yet.": "run CSVParser.organize() to create."}
        self.target_json_format = {
            "program.name": "Eargo",
            "district.name": "Jeffco",
            "district.state": "PA",
            "district.city": "Wakulla",
            "district.code": "H382",
            "school.name": "Carmody",
            "Student": [
                {
                    "student.first_name": "Fuller",
                    "student.last_name": "Hahn",
                    "student.middle_name": "Rodgers",
                    "student.gender": "M",
                    "student.birth_date": "2018-03-23",
                    "student.state_id": 542796,
                    "student.grade_year": 9,
                    "student.reason_in_program": "behavior",
                    "historicalstudentid.student_SISID": 298347928374,
                },
            ],
            "Course": [
                {
                    "course.name": "Algebra",
                    "course.code": "G7384",
                    "course.subject": "ENG",
                },
            ],
            "Grade": [
                {
                    "historicalstudentid.student_SISID": 19283192837,
                    "grade.course.name": "Algebra",
                    "grade.course.code": "HG3848",
                    "grade.calendar.year": 2004,
                    "grade.calendar.term": "SMR",
                    "grade.period": "6",
                    "grade.grade": 0.8091,
                    "grade.task": "Semester Grade",
                    "grade.term_final_value": True,
                    "grade.entry_datetime": "2016-03-24",
                },
            ],
            "Attendance": [
                {
                    "historicalstudentid.student_SISID": 19283192837,
                    "attendance.calendar.year": 2004,
                    "attendance.calendar.term": "SMR",
                    "attendance.entry_datetime": "2016-03-24",
                    "attendance.total_unexabs": 9.0,
                    "attendance.total_exabs": 6.0,
                    "attendance.total_abs": 54.0,
                    "attendance.total_tardies": 11,
                    "attendance.avg_daily_attendance": .98,
                    "attendance.term_final_value": True,
                },
            ],
            "Behavior": [
                {
                    "historicalstudentid.student_SISID": 19283192837,
                    "behavior.course.code": "HG838",
                    "behavior.period": "2",
                    "behavior.calendar.term": "SMR",
                    "behavior.calendar.year": 2004,
                    "behavior.incident_datetime": "2014-06-26",
                    "behavior.context": "H372",
                    "behavior.behavior_SISID": 293847923874,
                    "behavior.incident_type_program": "Small",
                    "behavior.incident_result_program": "Bad",
                    "behavior.incident_type_school": "Medium",
                    "behavior.incident_result_school": "Medium",
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
                #out of date.
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
                'grade.period': "grade.period",
                'grae.grade': "grade",
                'grade.term_final_value': "grade.term_final_value",
                'attendance.entry_datetime': "attendance.entry_datetime",
                'attendance.total_unexabs': "attendance.total_unexabs",
                'attendance.total_exabs': "attendance.total_exabs",
                'attendance.total_tardies': "attendance.total_tardies",
                'attendance.avg_daily_attendance': "attendance.avg_daily_attendance",
                'attendance.term_final_value': "attendance.term_final_value",
                'behavior.period': "behavior.period",
                'behavior.incident_datetime': "behavior.incident_datetime",
                'behavior.context': "behavior.context",
                'behavior.incident_type_school': "behavior.incident_type_school",
                'behavior.incident_result_school': "behavior.incident_result_school",
            },
            "Weld Central Middle School": {
                "direct": {
                    'student.first_name': "student.firstName",
                    'student.last_name': 'student.lastName',
                    "student.middle_name": 'student.middleName',
                    "student.gender": 'student.gender',
                    "student.state_id": 'student.stateID',
                    'historicalstudentid.student_SISID': 'student.studentNumber',
                    'student.grade_year': 'student.grade',
                    "course.name": 'grading.courseName',
                    "course.code": 'grading.courseNumber',
                    'grade.course.code': 'grading.courseNumber',
                    "grade.period": 'grading.periodName',
                    "grade.task":'grading.task',
                    "grade.grade": 'grading.percent',
                    "grade.course.name": "grading.courseName",
                    "attendance.total_unexabs": 'attExactDailyTermCount.unexcusedAbsentDays',
                    "attendance.total_abs": 'attExactDailyTermCount.absentDays',
                    'attendance.total_tardies': "attExactDailyTermCount.tardies",
                    'behavior.context': "behaviorDetail.contextDescription",
                    'behavior.behavior_SISID': "behaviorDetail.incidentID",
                    'behavior.incident_type_school': "behaviorDetail.eventName",
                    'behavior.incident_result_school': "behaviorDetail.resolutionName",
                },
                "parse": {
                    "student.birth_date": [
                        'student.birthdate',
                        lambda dataframe_row: str(datetime.strptime(dataframe_row['student.birthdate'], "%m/%d/%Y").strftime('%Y-%m-%d')),
                    ],
                    'behavior.incident_datetime': [
                        "behaviorDetail.incidentDate",
                        lambda dataframe_row: str(datetime.strptime(dataframe_row['behaviorDetail.incidentDate'], "%m/%d/%Y")),
                    ],
                    'grade.entry_datetime': [
                        'grading.date',
                        lambda dataframe_row: str(datetime.strptime(dataframe_row['grading.date'], "%m/%d/%Y")),
                    ],
                    "program.name": [
                        "django",
                        'Expelled and At-Risk Student Services Program',
                    ],
                    "district.name": [
                        "django",
                        self.School.district.name,
                    ],
                    "district.state": [
                        "django",
                        self.School.district.state,
                    ],
                    "district.city": [
                        "django",
                        self.School.district.city,
                    ],
                    "district.code": [
                        "django",
                        self.School.district.code,
                    ],
                    "school.name": [
                        "django",
                        self.School.name,
                    ],
                    "grade.calendar.year": [
                        "cal.endYear",
                        lambda dataframe_row: dataframe_row['cal.endYear'] - 1 if dataframe_row['grading.termName'] == "S1" else dataframe_row['cal.endYear'] if dataframe_row['grading.termName'] == "S2" else None,
                    ],
                    "grade.calendar.term": [
                        "grading.termName",
                        lambda dataframe_row: "FLL" if dataframe_row['grading.termName'] == "S1" else "SPR" if dataframe_row['grading.termName'] == "S2" else None,
                    ],
                    "attendance.calendar.year": [
                        "cal.endYear",
                        lambda dataframe_row: dataframe_row['cal.endYear'] - 1 if dataframe_row['attExactDailyTermCount.termName'] == "S1" else dataframe_row['cal.endYear'] if dataframe_row['attExactDailyTermCount.termName'] == "S2" else None,
                    ],
                    "attendance.calendar.term": [
                        "attExactDailyTermCount.termName",
                        lambda dataframe_row: "FLL" if dataframe_row['attExactDailyTermCount.termName'] == "S1" else "SPR" if dataframe_row['attExactDailyTermCount.termName'] == "S2" else None,
                    ],
                    "grade.term_final_value": [
                        "django",
                        self.term_final_value,
                    ],
                    "attendance.term_final_value": [
                        "django",
                        self.term_final_value,
                    ],
                    "attendance.entry_datetime": [
                        "django",
                        str(timezone.now()),
                    ],
                    "attendance.total_exabs": [
                        "attExactDailyTermCount.unexcusedAbsentDays",
                        lambda dataframe_row: round(dataframe_row['attExactDailyTermCount.absentDays'] - dataframe_row['attExactDailyTermCount.unexcusedAbsentDays'], 2)
                    ],
                },
                "blank": [
                    "behavior.incident_type_program",
                    "behavior.incident_result_program",
                    "behavior.course.code",
                    "student.reason_in_program",
                    "attendance.avg_daily_attendance",
                    "behavior.period",
                    "behavior.calendar.term",
                    "behavior.calendar.year",
                    "course.subject",
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

    def organize(self):
        """
        Organizes the csv file the parser was instantiated with and turns it into a single json_object.
        """
        datatypes = self.get_csv_datatypes()
        csv_df = self.get_dataframe(datatypes)
        self.json_object = self.build_json(csv_df)
        return self.json_object

    def parse_json(self):
        program = Program.objects.get(name = self.json_object["program.name"])
        district = District.objects.get(
            name = self.json_object["district.name"],
            city = self.json_object["district.city"],
            code = self.json_object["district.code"],
            state = self.json_object["district.state"],
        )
        school = School.objects.get(
            district = district,
            name = self.json_object["school.name"],
        )

        """#parse student data
        student_array = self.json_object["Student"]
        all_school_SISIDs = [object.student_SISID for object in HistoricalStudentID.objects.filter(school = school)]
        for student_element in student_array:
            SISID = student_element["historicalstudentid.student_SISID"]

            student_data = {}
            for key, value in student_element.items():
                if key.startswith("student.") and value != None:
                    field_name = key[len("student."):]
                    student_data[field_name] = value

            if SISID in all_school_SISIDs:
                student = HistoricalStudentID.objects.get(student_SISID = SISID).student
                student_data_currently_in_django = ParserStudentSerializer(student).data
                update = {}
                for field, value in student_data.items():
                    if value != student_data_currently_in_django[field]:
                        update[field] = value
                if len(update) > 0:
                    serializer = ParserStudentSerializer(student, data = update)
                    if serializer.is_valid():
                        student = serializer.save()
                    else:
                        output = {
                            "student": student_data_currently_in_django,
                            "error": {
                                "The following possible update couldn't be applied": update,
                                "Becuase the serializer found the following errors": serializer.errors,
                            },
                            "how_to_fix": "Consult the errors found and check CSV document is appropriately configured."

                        }
                        self.exceptions.append(output)

            elif SISID not in all_school_SISIDs:
                if len(student_data) >= 4:
                    duplicate_check_query = Student.objects.filter(**student_data)
                    if duplicate_check_query.exists():
                        if len(duplicate_check_query) == 1:
                            student = Student.objects.get(**student_data)
                            HistoricalStudentID.objects.create(
                                student = student,
                                school = school,
                                student_SISID = SISID
                            )
                        else:
                            serializer = ParserStudentSerializer(duplicate_check_query, many = True)
                            self.exceptions.append(
                                {
                                    "student": student_element,
                                    "error": {
                                        "Their information was too similar to more than one student:": serializer.data
                                    },
                                    "how_to_fix": "Include more biographical student data such as birthdate or stateID in your csv document."
                                }
                            )
                    elif duplicate_check_query.exists() == False:
                        student_data["current_program"] = program.id
                        student_data["current_school"] = school.id
                        serializer = ParserStudentSerializer(data = student_data)
                        if serializer.is_valid():
                            student = serializer.save()
                            HistoricalStudentID.objects.create(
                                student = student,
                                school = school,
                                student_SISID = SISID
                            )
                        else:
                            self.exceptions.append(
                                {
                                    "student": student_element,
                                    "error": {
                                        "This student was not found in the database, and a new student could not be created becuase the serializer found the following errors": serializer.errors,
                                    },
                                    "how_to_fix": "Consult the errors found and check CSV document is appropriately configured.",
                                }
                            )
                else:
                    self.exceptions.append(
                        {
                            "student": student_element,
                            "error": "There wasn't enough data provided for the following student to find them in the database",
                            "How_to_fix": "Include more biographical student data such as birthdate or stateID in your csv document"
                        }
                    )

        #parse course data
        course_array = self.json_object["Course"]
        for course_element in course_array:
            course_data = {"school": school.id}
            for key, value in course_element.items():
                if value != None:
                    field_name = key[len("course."):]
                    course_data[field_name] = value
            duplicate_check_query = Course.objects.filter(**course_data)
            if not duplicate_check_query.exists():
                serializer = ParserCourseSerializer(data = course_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    self.exceptions.append(
                        {
                            "course": course_element,
                            "error": {
                                "This course was not found in the database, and a new course could not be created because the serializer found the following errors": serializer.errors,
                            },
                            "how_to_fix": "Consult the errors found and check CSV document is appropriately configured.",
                        }
                    )
            else:
                continue"""

        #parse grade data
        grade_array = self.json_object["Grade"]
        for grade_element in grade_array:
            SISID = grade_element.pop("historicalstudentid.student_SISID")
            course_data = {
                "name": grade_element.pop("grade.course.name"),
                "code": grade_element.pop("grade.course.code"),
            }
            calendar_data = {
                "year": grade_element.pop("grade.calendar.year"),
                "term": grade_element.pop("grade.calendar.term"),
            }
            if SISID == None:
                self.exceptions.append(
                    {
                        "grade": grade_element,
                        "error": "too little information to link grade data to a student.",
                        "how_to_fix": "Check the CSV file you uploaded or the data extract that created it and see if the column labelled student.studentNumber is present."
                    }
                )
                continue
            if None in course_data.values():
                self.exceptions.append(
                    {
                        "grade": grade_element,
                        "error": "too little information to link grade data to a course.",
                        "how_to_fix": "Check the CSV file you uploaded or the data extract that created it and see if both columns labelled grading.courseNumber and grading.courseName are present."
                    }
                )
                continue
            if None in calendar_data.values():
                self.exceptions.append(
                    {
                        "grade": grade_element,
                        "error": "too little information to link grade to a year and/or term.",
                        "how_to_fix": "Check the CSV file you uploaded or the data extract that created it and see if both columns labelled cal.endYear and grading.termName are present."
                    }
                )
                continue
            else:
                calendar = Calendar.objects.get_or_create(**calendar_data)[0]
                student = HistoricalStudentID.objects.get(student_SISID = SISID).student
                course = Course.objects.get(**course_data)
                grade_data = {
                    "student": student.id,
                    "course": course.id,
                    "calendar": calendar.id,
                }
            break

        return {
            "grade_data": [grade_data, grade_element]
        }
        """
        - follow heirarchy of models.
        - check for duplicate data before inputting.
            - possible utilize get_or_creat() as Hannah did?
            - ignore None/null fields when checking for duplicates.
                - run get or create, if exception is multiplefound, do something
        - rename target json fields to assist in parsing json.
        -
        """
