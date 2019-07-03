from rest_framework import serializers
from gsndb.models import Note, District, School, Calendar, Referral, Bookmark, Program, Student, Course, Behavior, Grade, Attendance
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from gsndb.filter_security import FilterSecurity
from rest_framework.fields import CurrentUserDefault

'''
For the following serializers we are frequently overwriting the to_representation.
We then assign various fields from the model to a specific name of the representation.
'''

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "id",
            "user",
            "created",
            "text",
            "content_type",
            "object_id",
            )

    def to_representation(self, note_obj):
        representation = super().to_representation(note_obj)

        representation["noteId"] = representation.pop("id")
        representation["user"] = note_obj.user.id
        representation["createdUpdated"] = representation.pop("created")
        representation["text"] = note_obj.text
        representation["contentType"] = note_obj.content_type.id
        representation["objectId"] = note_obj.object_id

        return representation


# all table serializer
'''These serializers throw errors when it doesn't have Meta in it.
So it adds meta & the id field. Then it pops id field out and renames it
appropriately for the serializer. It also adds other fields to representation
including some nested serializers.'''

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = (
            "id",
            "state",
            "city",
            "code",
            "name",
        )

    def to_representation(self, district_obj):
        representation = super().to_representation(district_obj)

        representation["districtId"] = representation.pop("id")
        representation["districtName"] = representation.pop("name")
        representation["state"] = representation.pop("state")
        representation["city"] = representation.pop("city")
        representation["code"] = representation.pop("code")

        return representation


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            "id",
            "name",
            "district",
        )

    def to_representation(self, school_obj):
        representation = super().to_representation(school_obj)

        representation["schoolId"] = representation.pop("id")
        representation["schoolName"] = representation.pop("name")
        representation["districtId"] = representation.pop("district")
        representation["districtName"] = school_obj.district.name

        return representation


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id",)

    def to_representation(self, student_obj):
        representation = super().to_representation(student_obj)
        representation["studentId"] = representation.pop("id")
        representation["studentName"] = student_obj.first_name + " " + student_obj.middle_name + " " + student_obj.last_name
        representation["schoolName"] = student_obj.current_school.name
        representation["schoolId"] = student_obj.current_school.id
        representation["birthdate"] = student_obj.birth_date

        return representation


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ("id",)

    def to_representation(self, program_obj):
        representation = super().to_representation(program_obj)

        representation["programId"] = representation.pop("id")
        representation["programName"] = program_obj.name

        return representation


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id",)

    def to_representation(self, course_obj):
        representation = super().to_representation(course_obj)

        representation["courseId"] = representation.pop("id")
        representation["courseName"] = course_obj.name
        representation["schoolName"] = course_obj.school.name
        representation["schoolId"] = course_obj.school.id
        representation["courseCode"] = course_obj.code
        representation["courseSubject"] = course_obj.subject

        return representation

class BehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Behavior
        fields = ("id",)

    def to_representation(self, behavior_obj):
        representation = super().to_representation(behavior_obj)

        representation["behaviorId"] = representation.pop("id")
        representation["date"] = behavior_obj.incident_datetime
        representation["context"] = behavior_obj.context
        representation["result"] = behavior_obj.incident_result_school

        return representation


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("id",)

    def to_representation(self, attendance_obj):
        representation = super().to_representation(attendance_obj)

        representation["attendanceId"] = representation.pop("id")
        representation["studentId"] = attendance_obj.student.id
        representation["studentName"] = attendance_obj.student.first_name + " " + attendance_obj.student.last_name
        representation["attendanceEntryDate"] = attendance_obj.entry_datetime
        representation["attendanceTermFinalValue"] = attendance_obj.term_final_value
        representation["totalUnexabs"] = attendance_obj.total_unexabs
        representation["totalExabs"] = attendance_obj.total_exabs
        representation["totalTardies"] = attendance_obj.total_tardies
        representation["avgDailyAttendance"] = attendance_obj.avg_daily_attendance


        return representation



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ("id",)

    def to_representation(self, grade_obj):
        representation = super().to_representation(grade_obj)

        representation["gradeId"] = representation.pop("id")
        representation["studentId"] = grade_obj.student.id
        representation["studentName"] = grade_obj.student.first_name + " " + grade_obj.student.last_name
        representation["courseId"] = grade_obj.course.id
        representation["courseName"] = grade_obj.course.name
        representation["courseTermId"] = grade_obj.calendar.id
        representation["courseTerm"] = grade_obj.calendar.term + " " + str(grade_obj.calendar.year)
        representation["grade"] = grade_obj.grade
        representation["finalGradeForTerm"] = grade_obj.term_final_value


        return representation

class ReferralSerializer(serializers.ModelSerializer):

    notes = NoteSerializer(many=True, read_only = True)
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

    def to_representation(self, referral_obj):
        representation = super().to_representation(referral_obj)
        user = FilterSecurity(self.context.get('request'))

        representation["referralId"] = representation.pop("id")
        representation["user"] = referral_obj.user.id
        representation["student"] = referral_obj.student.id
        representation["program"] = referral_obj.program.id
        representation["type"] = referral_obj.type
        representation["dateGiven"] = referral_obj.date_given

        return representation

class CreateDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = (
            "id",
            "name",
        )

    def to_representation(self, district_obj):
        representation = super().to_representation(district_obj)

        representation["districtId"] = representation.pop("id")
        representation["districtName"] = representation.pop("name")
        representation["schoolSet"] = SchoolSerializer(district_obj.school_set, many = True, read_only = True).data

        return representation

#detail serializer
class DistrictDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ("id",)

    def to_representation(self, district_obj):
        user = FilterSecurity(self.context.get('request'))
        current_user = user.get_user()
        accessible_schools = user.get_accessible_schools()
        my_schools = user.get_my_schools()
        accessible_students = user.get_accessible_students()
        my_students = user.get_my_students()

        
        access_level = self.context.get("access", False)
        representation = super().to_representation(district_obj)

        representation["districtId"] = representation.pop("id")
        representation["districtName"] = district_obj.name
        representation["state"] = district_obj.state
        representation["city"] = district_obj.city
        representation["code"] = district_obj.code

        representation["noteSet"] = NoteSerializer(district_obj.notes.filter(user=current_user), many = True).data

        if access_level == user.get_all_access():
            representation["schoolSet"] = SchoolSerializer(accessible_schools.filter(district = district_obj.id), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(accessible_students.filter(current_school__district_id = district_obj.id), many = True, read_only = True).data
            representation["gradeSet"] = GradeSerializer(Grade.objects.filter(student_id__in = accessible_students.values('id'), course__school__district_id = district_obj.id), many = True, read_only = True).data
            representation["attendanceSet"] = AttendanceSerializer(Attendance.objects.filter(student_id__in = accessible_students.values('id'), school__district_id = district_obj.id), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(Behavior.objects.filter(student_id__in = accessible_students, school__district_id = district_obj.id), many = True, read_only = True).data
        elif access_level == user.get_my_access():
            representation["schoolSet"] = SchoolSerializer(my_schools.filter(district = district_obj.id), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(my_students.filter(current_school__district_id = district_obj.id), many = True, read_only = True).data
            representation["gradeSet"] = GradeSerializer(Grade.objects.filter(student_id__in = my_students.values('id'), course__school__district_id = district_obj.id), many = True, read_only = True).data
            representation["attendanceSet"] = AttendanceSerializer(Attendance.objects.filter(student_id__in = my_students.values('id'), school__district_id = district_obj.id), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(Behavior.objects.filter(student_id__in = my_students, school__district_id = district_obj.id), many = True, read_only = True).data
        return representation


class StudentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ("id",)

    def to_representation(self, student_obj):
        user = FilterSecurity(self.context.get('request'))
        current_user = user.get_user()

        representation = super().to_representation(student_obj)

        representation["studentId"] = representation.pop("id")
        representation["studentName"] = student_obj.first_name + " " + student_obj.middle_name + " " + student_obj.last_name
        representation["gender"] = student_obj.gender
        representation["schoolId"] = student_obj.current_school.id

        program = Program.objects.get(student=representation["studentId"]).id

        representation["programId"] = program
        representation["schoolName"] = student_obj.current_school.name
        representation["birthdate"] = student_obj.birth_date
        representation["stateId"] = student_obj.state_id
        representation["studentYear"] = student_obj.grade_year
        representation["reasonInProgram"] = student_obj.reason_in_program

        representation["noteSet"] = NoteSerializer(student_obj.notes.filter(user=current_user), many = True).data
        representation["gradeSet"] = GradeSerializer(student_obj.grade_set, many = True, read_only = True).data
        representation["attendanceSet"] = AttendanceSerializer(student_obj.attendance_set, many = True, read_only = True).data
        representation["behaviorSet"] = BehaviorSerializer(student_obj.behavior_set, many = True, read_only = True).data
        representation["referralSet"] = ReferralDetailSerializer(student_obj.referral_set, many = True, read_only = True).data

        return representation


class SchoolDetailSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = School
        fields = ("id",)

    def to_representation(self, school_obj):
        user = FilterSecurity(self.context.get('request'))
        current_user = user.get_user()
        accessible_students = user.get_accessible_students()
        my_students = user.get_my_students()
        accessible_courses = user.get_accessible_courses()
        my_courses = user.get_my_courses()

        access_level = self.context.get("access", False)

        representation = super().to_representation(school_obj)

        representation["schoolId"] = representation.pop("id")
        representation["schoolName"] = school_obj.name
        representation["districtId"] = school_obj.district.id
        representation["districtName"] = school_obj.district.name

        representation["noteSet"] = NoteSerializer(school_obj.notes.filter(user=current_user), many = True).data

        if access_level == user.get_all_access():
            representation["gradeSet"] = GradeSerializer(Grade.objects.filter(student_id__in = accessible_students.values("id"), course__school_id = school_obj.id), many = True, read_only = True).data
            representation["attendanceSet"] = AttendanceSerializer(school_obj.attendance_set.filter(student_id__in = accessible_students.values("id")), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(school_obj.behavior_set.filter(student_id__in = accessible_students.values("id")), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(accessible_students.filter(current_school_id = school_obj.id), many = True, read_only = True).data
            representation["courseSet"] = CourseSerializer(accessible_courses.filter(school_id = school_obj.id), many = True, read_only = True).data
        elif access_level == user.get_my_access():
            representation["gradeSet"] = GradeSerializer(Grade.objects.filter(student_id__in = my_students.values("id"), course__school_id = school_obj.id), many = True, read_only = True).data
            representation["attendanceSet"] = AttendanceSerializer(school_obj.attendance_set.filter(student_id__in = my_students.values("id")), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(school_obj.behavior_set.filter(student_id__in = my_students.values("id")), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(my_students.filter(current_school_id = school_obj.id), many = True, read_only = True).data
            representation["courseSet"] = CourseSerializer(my_courses.filter(school_id = school_obj.id), many = True, read_only = True).data


        return representation


class CourseDetailSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Course
        fields = ("id",)

    def to_representation(self, course_obj):
        user = FilterSecurity(self.context.get('request'))
        current_user = user.get_user()
        accessible_students = user.get_accessible_students()
        my_students = user.get_my_students()
        access_level = self.context.get("access", False)

        representation = super().to_representation(course_obj)

        representation["courseId"] = representation.pop("id")
        representation["courseName"] = course_obj.name
        representation["schoolId"] = course_obj.school.id
        representation["schoolName"] = course_obj.school.name
        representation["courseSubject"] = course_obj.subject
        representation["courseCode"] = course_obj.code

        representation["noteSet"] = NoteSerializer(course_obj.notes.filter(user=current_user), many = True).data

        if access_level == user.get_all_access():
            representation["gradeSet"] = GradeSerializer(Grade.objects.filter(student_id__in = accessible_students.values("id"), course_id = course_obj.id), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(Behavior.objects.filter(student_id__in = accessible_students.values("id"), course_id = course_obj.id), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(accessible_students.filter(pk__in = Grade.objects.filter(course_id = course_obj.id).values("student")), many = True, read_only = True).data
        elif access_level == user.get_my_access():
            representation["gradeSet"] = GradeSerializer(Grade.objects.filter(student_id__in = my_students.values("id"), course_id = course_obj.id), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(Behavior.objects.filter(student_id__in = my_students.values("id"), course_id = course_obj.id), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(my_students.filter(pk__in = Grade.objects.filter(course_id = course_obj.id).values("student")), many = True, read_only = True).data
        return representation

class ProgramDetailSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Program
        fields = ("id",)

    def to_representation(self, program_obj):
        user = FilterSecurity(self.context.get('request'))
        current_user = user.get_user()
        accessible_students = user.get_accessible_students()
        my_students = user.get_my_students()

        access_level = self.context.get("access", False)

        representation = super().to_representation(program_obj)

        representation["programId"] = representation.pop("id")
        representation["programName"] = program_obj.name

        representation["noteSet"] = NoteSerializer(program_obj.notes.filter(user=current_user), many = True).data

        if access_level == user.get_all_access():
            representation["gradeSet"] = GradeSerializer(program_obj.grade_set.filter(student__in=accessible_students), many = True, read_only = True).data
            representation["attendanceSet"] = AttendanceSerializer(program_obj.attendance_set.filter(student__in=accessible_students), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(program_obj.behavior_set.filter(student__in=accessible_students), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(program_obj.student_set.filter(pk__in=accessible_students), many = True, read_only = True).data
        if access_level == user.get_my_access():
            representation["gradeSet"] = GradeSerializer(program_obj.grade_set.filter(student__in=my_students), many = True, read_only = True).data
            representation["attendanceSet"] = AttendanceSerializer(program_obj.attendance_set.filter(student__in=my_students), many = True, read_only = True).data
            representation["behaviorSet"] = BehaviorSerializer(program_obj.behavior_set.filter(student__in=my_students), many = True, read_only = True).data
            representation["studentSet"] = StudentSerializer(program_obj.student_set.filter(pk__in=my_students), many = True, read_only = True).data

        return representation

class ReferralDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referral
        fields = ("id",)

    def to_representation(self, referral_obj):
        user = FilterSecurity(self.context.get('request'))
        representation = super().to_representation(referral_obj)

        representation["referralId"] = representation.pop("id")
        representation["user"] = referral_obj.user.id
        representation["student"] = referral_obj.student.id
        representation["program"] = referral_obj.program.id
        representation["type"] = referral_obj.type
        representation["dateGiven"] = referral_obj.date_given
        representation["referenceName"] = referral_obj.reference_name
        representation["referencePhone"] = referral_obj.reference_phone
        representation["referenceAddress"] = referral_obj.reference_address
        representation["reason"] = referral_obj.reason
        # representation["notes"] = NoteSerializer(referral_obj.notes.filter(user = self.user.get_user()), many = True).data

        return representation








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



class BookmarkSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)
    class Meta:
        model = Bookmark
        fields = ('id','user','url','created','json_request_data','notes')

class RelatedSetSerializer(serializers.BaseSerializer):
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
        #look up and down to find relationship without iterating through all relationships
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
class NestedInternalCourseSerializer(serializers.ModelSerializer):
    def to_representation(self, course_obj):
        return {
            "course_id": course_obj.id,
            "course_name": course_obj.name,
            "course_code": course_obj.code,
            "course_subject": course_obj.subject,
        }

class NestedGradeSerializer(serializers.ModelSerializer):
    def to_representation(self, grade_obj):
        representation = {
            "grade_id": grade_obj.id,
            "course": grade_obj.course.id,
            "grade": grade_obj.grade
        }

        getCourse = self.context.get('getCourse', False)

        #if getCourse:
            #representation["course_set"] = NestedInternalCourseSerializer(grade_obj.course_set, many = True, read_only = True).data


        return representation

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
    def to_representation(self, referral_obj):
        return {
            "referral_id": referral_obj.id,
            "referral_type": referral_obj.type,
            "referance_name": referral_obj.reference_name,
            "referral_reason": referral_obj.reason
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
        elif getCourse:
            representation["grade_set"] = NestedGradeSerializer(student_obj.grade_set, many = True, read_only = True, context = {"getCourse": True}).data


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
            representation["course_set"] = NestedInternalCourseSerializer(school_obj.course_set, many = True, read_only = True).data

        return representation

class NestedProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ("id",)

    def to_representation(self, program_obj):
        #if statement that determines if it is grade, attendance, course, behavior, or referral; need to pass down to student
        #student = NestedStudentGradeSerializer(school_obj.student_set, many = True, read_only = True)
        #student_json = student.data

        representation = super().to_representation(program_obj)
        representation["program_id"] = representation.pop("id")
        representation["program_name"] = program_obj.name

        getGrades = self.context.get('getGrades', False)
        getAttendance = self.context.get('getAttendance', False)
        getBehavior = self.context.get('getBehavior', False)
        getReferral = self.context.get('getReferral', False)
        getCourse = self.context.get('getCourse', False)


        if getGrades:
            representation["student_set"] = NestedStudentSerializer(program_obj.student_set, many = True, read_only = True, context = {"getGrades": True}).data
        elif getAttendance:
            representation["student_set"] = NestedStudentSerializer(program_obj.student_set, many = True, read_only = True, context = {"getAttendance": True}).data
        elif getBehavior:
            representation["student_set"] = NestedStudentSerializer(program_obj.student_set, many = True, read_only = True, context = {"getBehavior": True}).data
        elif getReferral:
            representation["student_set"] = NestedStudentSerializer(program_obj.student_set, many = True, read_only = True, context = {"getReferral": True}).data
        elif getCourse:
            representation["student_set"] = NestedStudentSerializer(program_obj.student_set, many = True, read_only = True, context = {"getCourse": True}).data

        return representation
