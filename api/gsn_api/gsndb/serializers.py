from rest_framework import serializers
from gsndb.models import District, School, Student, Course, Calendar, Grade, Attendance, Behavior, Referral, Bookmark
from django.db.models.fields.related import ForeignKey

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

class StudentSerializer(serializers.BaseSerializer):

        def to_representation(self, student_obj):
            return {
                "current_school": student_obj.current_school.id,
                "current_program": student_obj.current_program.id,
                "first_name": student_obj.first_name,
                "last_name": student_obj.last_name,
                "middle_name": student_obj.middle_name,
                "gender": student_obj.gender,
                "birth_date": student_obj.birth_date,
                "state_id": student_obj.state_id,
                "grade_year": student_obj.grade_year,
                "reason_in_program": student_obj.reason_in_program,
            }

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


class AttendanceSerializer(serializers.BaseSerializer):

    def to_representation(self, attendance_obj):
        return {
            "student": attendance_obj.student.id,
            "school": attendance_obj.school.id,
            "calendar": attendance_obj.calendar.id,
            "program": attendance_obj.program.id,
            "entry_date": attendance_obj.entry_datetime,
            "total_unexabs": attendance_obj.total_unexabs,
            "total_exabs": attendance_obj.total_exabs,
            "total_tardies": attendance_obj.total_tardies,
            "avg_daily_attendance": attendance_obj.avg_daily_attendance,
            "term_final_value": attendance_obj.term_final_value,
        }

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

class ParedGrade2Serializer(serializers.ModelSerializer):
    #can we get rid of this?
    grade = serializers.CharField()
    class Meta:
        model = Grade
        fields = ('grade','term_final_value')



class StudentGradeSerializer(serializers.ModelSerializer):
    grade_set = ParedGrade2Serializer(read_only=True, many=True),
    birthday = serializers.DateField(source= 'birth_date')

    class Meta:
        model = Student
        fields = ('grade_set', 'birthday')


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id','user','url','created','json_request_data')

class Child_setSerializer(serializers.BaseSerializer):
    """This class serializes an instance of a model and specified sets of data
    from child models. For example, it can serialize an instance of the student
    model and the set of grade data associated with it. This class functions
    similarly to the serializers already created, such as DistrictSerializer.

    There are two main differences:'data' no longer a positional argument, it is
    now a keyword argument; and the format of the inputs it takes is now
    Child_setSerializer(instsance, *child_model). *child_model is an arbitrary
    number of models related to the instance by a many-to-one relationship.
    Currently the serializer cannot serialize sets of data more than one degree
    removed from the instance."""
    def __init__(self, instance = None, *child_model, **kwargs):
        super().__init__(instance = instance, **kwargs)
        self.child_model = child_model
        self.serializer_dic = {
            "Student": StudentSerializer,
            "Grade": GradeSerializer,
            "Attendance": AttendanceSerializer,
            "District": DistrictSerializer,
            "School": SchoolSerializer,
            "Course": CourseSerializer,
            "Calendar": CalendarSerializer,
            "Behavior": BehaviorSerializer,
            "Referral": ReferralSerializer,
        }

    def find_foreign_key_field_connection(self, instance, child_model):
        instance_model_name = instance.__class__.__name__
        child_fields = child_model._meta.fields
        for field in child_fields:
            field_type = field.__class__
            if field_type == ForeignKey:
                field_name = field.__dict__["name"]
                if field_name == instance_model_name.lower():
                    connecting_field = field
                    break
        return field_name

    def construct_data(self):
        instance_model_name = self.instance.__class__.__name__
        InstanceSerializer = self.serializer_dic[instance_model_name]
        serialized_instance = InstanceSerializer(self.instance)
        json = serialized_instance.data
        if len(self.child_model) >= 1:
            for Child in self.child_model:
                child_model_name = Child.__name__
                ChildSerializer = self.serializer_dic[child_model_name]
                foreign_key = self.find_foreign_key_field_connection(self.instance, Child)
                query = {foreign_key: self.instance.id}
                queryset = Child.objects.filter(**query)
                child_set_serializer = ChildSerializer(queryset, many = True)
                json[child_model_name] = child_set_serializer.data
            return json
        else:
            return json

    def to_representation(self, instance):
        json_data = self.construct_data()
        return json_data


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

# Below we have the serializers for the endpoints



 
class NestedGradeSerializer(serializers.ModelSerializer):
    def to_representation(self, grade_obj):
        return {
            "grade_id": grade_obj.id,
            "course": grade_obj.course.id,
            "grade": grade_obj.grade
        }

class NestedAttendanceSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Attendance
		fields = ("id","total_unexabs","total_exabs","total_tardies","avg_daily_attendance")

class NestedStudentGradeSerializer(serializers.ModelSerializer):
	
    def to_representation(self,student_obj):
        #if statement that determines if it is grade, attendance, course, behavior, or referral
        grade = NestedGradeSerializer(student_obj.grade_set, many = True, read_only = True)
        grade_json = grade.data
        return {
            "student_id": student_obj.id,
            "first_name": student_obj.first_name,
            "last_name": student_obj.last_name,
            "grade_set": grade_json
        }


class NestedSchoolSerializer(serializers.ModelSerializer):
    
    def to_representation(self, school_obj):
        #if statement that determines if it is grade, attendance, course, behavior, or referral; need to pass down to student
        student = NestedStudentGradeSerializer(school_obj.student_set, many = True, read_only = True)
        student_json = student.data
        return {
            "school_id": school_obj.id,
            "school_name": school_obj.name,
            "student_set": student_json,
        }

'''
    class Meta:
        model = School
        fields = ("id","name","student_set")
'''





#student in school/program/district etc
#Student School/program/district/etc
#Pared student serializer