from rest_framework import serializers
from gsndb.models import District, School, Student, Course, Calendar, Grade, Attendance, Behavior, Referral, Bookmark, Note
from django.db.models.fields.related import ForeignKey


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("user",
            "created",
            "text",
            "content_type",
            "object_id",
            "content_object")

class DistrictSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
    class Meta:
        model = District
        fields = (
            "id",
            "code",
            "city",
            "state",
            "name",
            "notes",)

class SchoolSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
    class Meta:
        model = School
        fields = (
            "id",
            "district",
            "name",
            "notes",
        )

class StudentSerializer(serializers.BaseSerializer):

        def to_representation(self, student_obj):
            notes = NoteSerializer(many = True)
            notes_json = notes.data
            
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
                "notes": notes_json,
            }

class MyStudentsSerializer(serializers.ModelSerializer):
    current_school = SchoolSerializer(read_only = True)
    notes = NoteSerializer(many=True)
    class Meta:
        model = Student
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "current_school",
            "birth_date",
            "notes",
        )

class CalendarSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
    class Meta:
        model = Calendar
        fields = (
            "id",
            "year",
            "term",
            "notes",
        )

class CourseSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
    class Meta:
        model = Course
        fields = (
            "id",
            "school",
            "name",
            "code",
            "subject",
            "notes",
        )

class BehaviorSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
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
            "notes",
        )

class GradeSerializer(serializers.BaseSerializer):

    def to_representation(self, grade_obj):
        notes = NoteSerializer(many = True)
        notes_json = notes.data
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
            "notes": notes_json,
        }


'''
#can we delete this
# class GradeForStudentSerializer(serializers.BaseSerializer):

    def to_representation(self, student_obj):
        grade = GradeSerializer(student_obj.grade_set, many = True)
        grade_json = grade.data
        note = NoteSerializer(student_obj.notes, many = True)
        note_json = note.data
        return {
            "First Name": student_obj.first_name,
            "Last Name": student_obj.last_name,
            "Grades": grade_json,
            "Note": note_json,

        }

'''


class AttendanceSerializer(serializers.BaseSerializer):

    def to_representation(self, attendance_obj):
        notes = NoteSerializer(many = True)
        notes_json = notes.data
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
            "notes": notes_json,
        }

class ReferralSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
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
            "notes",
        )

'''
class ParedGrade2Serializer(serializers.ModelSerializer):
    #can we get rid of this?
    grade = serializers.CharField()
    class Meta:
        model = Grade
        fields = ('grade','term_final_value')



class StudentGradeSerializer(serializers.ModelSerializer):
    grade_set = ParedGrade2Serializer(read_only=True, many=True),
    birthday = serializers.DateField(source= 'birth_date')
    notes = NoteSerializer(many=True)
    class Meta:
        model = Student
        fields = ('grade_set', 'birthday','notes')
'''

class BookmarkSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
    class Meta:
        model = Bookmark
        fields = ('id','user','url','created','json_request_data','notes')

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


'''name = serializers.SerializerMethodField(),
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

'''

# Below we have the serializers for the nested endpoints



 
class NestedGradeSerializer(serializers.ModelSerializer):
    def to_representation(self, grade_obj):
        return {
            "grade_id": grade_obj.id,
            "course": grade_obj.course.id,
            "grade": grade_obj.grade
        }

class NestedBehaviorSerializer(serializers.ModelSerializer):
    def to_representation(self, behavior_obj):
        return {
            "behavior_id": behavior_obj.id,
            "incident_datetime": behavior_obj.incident_datetime,
            "context": behavior_obj.context, 
            "incident_type_program": behavior_obj.incident_type_program,
            "incident_result_program": behavior_obj.incident_result_program,
            "incident_type_school": behavior_obj.incident_type_school,
            "incident_result_school": behavior_obj.incident_result_school
        }

class NestedAttendanceSerializer(serializers.ModelSerializer):
    def to_representation(self, attendance_obj):
        return {
            "attendance_id": attendance_obj.id,
            "total_unexabs": attendance_obj.total_unexabs,
            "total_exabs": attendance_obj.total_exabs,
            "total_tardies": attendance_obj.total_tardies,
            "avg_daily_attendance": attendance_obj.avg_daily_attendance
        }

class NestedReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ("id",)

class NestedCourseSerializer(serializers.ModelSerializer):
    def to_representation(self, course_obj):
        return {
            "course_id": course_obj.id,
            "course_name": course_obj.name,
            "course_code": course_obj.code,
            "course_subject": course_obj.subject,
        }


class NestedStudentSerializer(serializers.ModelSerializer):
    def to_representation(self,student_obj):
        #if statement that determines if it is grade, attendance, course, behavior, or referral
        getGrades = self.context.get('getGrades', False)
        getAttendance = self.context.get('getAttendance', False)
        getBehavior = self.context.get('getBehavior', False)
        getReferral = self.context.get('getReferral', False)
        getCourse = self.context.get('getCourse', False)

        representation = {
            "student_id": student_obj.id,
            "first_name": student_obj.first_name,
            "last_name": student_obj.last_name,
        }

        if getGrades:
            representation["grade_set"] = NestedGradeSerializer(student_obj.grade_set, many = True, read_only = True).data
        elif getAttendance:
            representation["attendance_set"] = NestedAttendanceSerializer(student_obj.attendance_set, many = True, read_only = True).data
        elif getBehavior:
            representation["behavior_set"] = NestedBehaviorSerializer(student_obj.behavior_set, many = True, read_only = True).data
        elif getReferral:
            representation["referral_set"] = NestedReferralSerializer(student_obj.referral_set, many = True, read_only = True).data
        

        return representation


class NestedSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ("id",)

    def to_representation(self, school_obj):
        #if statement that determines if it is grade, attendance, course, behavior, or referral; need to pass down to student
        #student = NestedStudentGradeSerializer(school_obj.student_set, many = True, read_only = True)
        #student_json = student.data

        representation = super().to_representation(school_obj)
        representation["school_id"] = representation.pop("id")
        representation["school_name"] = school_obj.name

        getGrades = self.context.get('getGrades', False)
        getAttendance = self.context.get('getAttendance', False)
        getBehavior = self.context.get('getBehavior', False)
        getReferral = self.context.get('getReferral', False)
        getCourse = self.context.get('getCourse', False)


        if getGrades:
            representation["student_set"] = NestedStudentSerializer(school_obj.student_set, many = True, read_only = True, context = {"getGrades": True}).data
        elif getAttendance:
            representation["student_set"] = NestedStudentSerializer(school_obj.student_set, many = True, read_only = True, context = {"getAttendance": True}).data
        elif getBehavior:
            representation["student_set"] = NestedStudentSerializer(school_obj.student_set, many = True, read_only = True, context = {"getBehavior": True}).data
        elif getReferral:
            representation["student_set"] = NestedStudentSerializer(school_obj.student_set, many = True, read_only = True, context = {"getReferral": True}).data
        elif getCourse:
            representation["course_set"] = NestedCourseSerializer(school_obj.course_set, many = True, read_only = True).data

        return representation

class NestedCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id",)

    def to_representation(self, course_obj):
        #if statement that determines if it is grade, attendance, course, behavior, or referral; need to pass down to student
        #student = NestedStudentGradeSerializer(school_obj.student_set, many = True, read_only = True)
        #student_json = student.data

        representation = super().to_representation(course_obj)
        representation["course_id"] = representation.pop("id")
        representation["course_name"] = school_obj.name

        getName = self.context.get('getName', False)
        getCode = self.context.get('getCode', False)
        getBehavior = self.context.get('getBehavior', False)
        getReferral = self.context.get('getReferral', False)
        


        if getGrades:
            representation["student_set"] = NestedStudentSerializer(course_obj.student_set, many = True, read_only = True, context = {"getGrades": True}).data
        elif getAttendance:
            representation["student_set"] = NestedStudentSerializer(course_obj.student_set, many = True, read_only = True, context = {"getAttendance": True}).data
        elif getBehavior:
            representation["student_set"] = NestedStudentSerializer(course_obj.student_set, many = True, read_only = True, context = {"getBehavior": True}).data
        elif getReferral:
            representation["student_set"] = NestedStudentSerializer(course_obj.student_set, many = True, read_only = True, context = {"getReferral": True}).data

        return representation

