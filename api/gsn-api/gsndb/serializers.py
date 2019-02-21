from rest_framework import serializers
from gsndb.models import District, School, Student, Course, Grade, Attendance, Behavior, Referral

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
            "program",
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

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            "id",
            "student",
            "course",
            "entry_datetime",
            "calendar_year",
            "term",
            "grade",
            "final_boolean",
        )

class GradeForStudentSerializer(serializers.ModelSerializer):

    #if URL is ______: set serializer field to _______
    grade_set = GradeSerializer(many = True, read_only = True)

    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "grade_set",
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
