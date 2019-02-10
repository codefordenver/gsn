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

class AllStudentSerializer(serializers.ModelSerializer):
    current_school = SchoolSerializer(read_only = True)

    class Meta:
        model = student
        fields = (
        "first_name",
        "last_name",
        "middle_name",
        "current_school",
        "birth_date",
        )

class StudentDetailSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only = True)

    class Meta:
        model = student
        fields = (
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
