from rest_framework import serializers
from gsndb.models import District, School, Student, Course, StudentSnap, Attendance, Grade, Behavior

"""The following serializer is verbose for the purpose of illustrating the process of data serialization and it`s interaction with django models. Every serializer hereafter will be generic in nature"""

class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    district_state = serializers.CharField(max_length = 2)
    district_city = serializers.CharField(max_length=50)
    district_code = serializers.CharField(max_length=10)

    def create(self, validated_data):
      """
      Create and return a new `District` instance, given the validated data.
      """
      return District.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `District` instance, given the validated data.
        """
        instance.district_state = validated_data.get('district_state', instance.district_state)
        instance.district_city = validated_data.get('district_city', instance.district_city)
        instance.district_code = validated_data.get('district_code', instance.district_code)
        instance.save()
        return instance

"""As stated, every serializer declared beneath this comment shall be generic in nature"""

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'school_name', 'district')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','student_first_name', 'student_last_name', 'student_gender', 'student_birth_date', 'student_state_id')

class StudentSnapSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSnap
        fields = ('id', 'school', 'student', 'student_grade_placement', 'student_attendance_term')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'school', 'course_name', 'course_subject')

class BehaviorSerializer(serializers.ModelSerializer):
    context = serializers.CharField(source= "behavior_context")
    date = serializers.DateTimeField(format= "%-m/%-d/%-Y", source= 'behavior_incident_date_time')
    result = serializers.CharField(source= "behavior_result")
    class Meta:
        model = Behavior
        exclude = ('id', 'student_snap', 'behavior_incident_date_time', 'behavior_context', 'behavior_result')

class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format= "%-m/%-d/%-Y", source= 'attendance_data_entry_time')
    unexcused = serializers.CharField(source= 'attendance_total_unexcused_absences')
    excused = serializers.CharField(source= 'attendance_total_excused_absences')
    tardies = serializers.CharField(source= 'attendance_total_tardies')
    class Meta:
        model = Attendance
        exclude = ('student_snap', 'attendance_data_entry_time', 'attendance_total_unexcused_absences', 'attendance_total_excused_absences',
        'attendance_total_tardies', 'id')

class GradeSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source= 'course.course_name', read_only=True)
    scale = serializers.CharField(source= 'grade_scale')
    date = serializers.DateTimeField(format = "%-m/%-d/%-Y", source= 'grade_data_entry_time')
    metric = serializers.CharField(source= 'grade_metric')
    final = serializers.BooleanField(source= 'grade_is_final')
    class Meta:
        model = Grade
        exclude = ('id', 'student_snap', 'grade_metric', 'grade_scale', 'grade_is_final', 'grade_data_entry_time')
