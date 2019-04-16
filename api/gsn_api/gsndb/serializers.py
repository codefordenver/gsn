from rest_framework import serializers
from gsndb.models import District, School, Student, Course, Calendar, Grade, Attendance, Behavior, Referral, Bookmark


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = (
            "id",
            "code",
            "city",
            "state",
            "name")

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            "id",
            "district",
            "name",
        )

class StudentSerializer(serializers.ModelSerializer):
    current_school = SchoolSerializer()

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "current_school",
            "birth_date",
            "gender",
            "grade_year",
            "current_program",
            "reason_in_program",
            "state_id",
        )

class MyStudentsSerializer(serializers.ModelSerializer):
    current_school = SchoolSerializer(read_only = True)

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "current_school",
            "birth_date",
        )

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = (
            "id",
            "year",
            "term",
        )

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "id",
            "school",
            "name",
            "code",
            "subject",
        )

class BehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Behavior
        fields = (
            "id",
            "student",
            "school",
            "calendar",
            "program",
            "period",
            "incident_datetime",
            "context",
            "incident_type_program",
            "incident_result_program",
            "incident_type_school",
            "incident_result_school",
        )

class GradeSerializer(serializers.BaseSerializer):

    def to_representation(self, grade_obj):
        return {
            "Grade PK": grade_obj.id,
            "Student": grade_obj.student.id,
            "Course": grade_obj.course.id,
            "Calendar": grade_obj.calendar.id,
            "entry_date": grade_obj.entry_datetime,
            "period": grade_obj.period,
            "program": grade_obj.program.id,
            "Grade Value": grade_obj.grade,
            "Final Grade for Term": grade_obj.term_final_value,
        }


class GradeForStudentSerializer(serializers.BaseSerializer):

    def to_representation(self, student_obj):
        grade = GradeSerializer(student_obj.grade_set, many = True)
        grade_json = grade.data
        return {
            "First Name": student_obj.first_name,
            "Last Name": student_obj.last_name,
            "Grades": grade_json,
        }


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            "id",
            "student",
            "school",
            "program",
            "calendar",
            "entry_datetime",
            "total_unexabs",
            "total_exabs",
            "total_tardies",
            "avg_daily_attendance",
            "term_final_value",
        )

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = (
            "id",
            "user",
            "student",
            "program",
            "type",
            "date_given",
            "reference_name",
            "reference_phone",
            "reference_address",
            "reason",
        )

class ParedGradeSerializer(serializers.ModelSerializer):
    grade = serializers.CharField()
    class Meta:
        model = Grade
        fields = ('grade','term_final_value')


class StudentGradeSerializer(serializers.ModelSerializer):
    grade_set = ParedGradeSerializer(read_only=True, many=True),
    birthday = serializers.DateField(source= 'birth_date')

    class Meta:
        model = Student
        fields = ('grade_set', 'birthday')

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id','user','url','created','json_request_data')



"""
name = serializers.SerializerMethodField(),
    school = serializers.CharField(source= 'current_school.name', read_only=True)
    birthdate = serializers.DateTimeField(format = "%-m/%-d/%-Y", source= 'birth_date'),
    stateId = serializers.IntegerField(source='state_id'),
    year = serializers.IntegerField(source='grade_year')

    def get_name(self, obj):
        return '{} {} {}'.format(obj.last_name, obj.first_name, obj.middle_name)

        fields = ('grades', 'current_school', 'first_name', 'last_name', 'middle_name', 'gender', 'birth_date', 'state_id', 'grade_year', 'program', 'reason_in_program')


            course = serializers.CharField(source= 'course.name', read_only=True),
    term = serializers.CharField(source= 'calendar.term', read_only=True),
    year = serializers.IntegerField(source= 'calendar.year', read_only=True),
    grade = serializers.CharField(source= 'grade'),
    final = serializers.BooleanField(source= 'term_final_value')
"""
