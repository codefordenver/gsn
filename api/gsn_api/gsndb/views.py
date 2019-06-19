from rest_framework.response import Response
from gsndb.models import Program, District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, Program
from gsndb.serializers import ProgramSerializer, ProgramDetailSerializer, CourseDetailSerializer, SchoolDetailSerializer, StudentDetailSerializer,DistrictSerializer, DistrictDetailSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.http import HttpResponseRedirect
from gsndb.filter_security import FilterSecurity

#Table views
class StudentList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_students()
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_students()
        serializer = StudentSerializer(queryset , many = True)
        return Response(serializer.data)


class DistrictList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_districts()
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_districts()
        serializer = DistrictSerializer(queryset , many = True)
        return Response(serializer.data)

class SchoolList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_schools()
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_schools()
        serializer = SchoolSerializer(queryset , many = True)
        return Response(serializer.data)

class CourseList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_courses()
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_courses()
        serializer = CourseSerializer(queryset , many = True)
        return Response(serializer.data)


class ProgramList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_programs()
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_programs()
        serializer = ProgramSerializer(queryset , many = True)
        return Response(serializer.data)

class NoteList(generics.ListCreateAPIView):
    #returns all notes for anything
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class BookmarkList(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class NoteList(generics.ListCreateAPIView):
    #returns all notes for anything
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class BookmarkList(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

#Detail views

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_districts().filter(pk = pk)
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_districts().filter(pk = pk)
        serializer = DistrictDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        Goal: allowing for posting of notes to district object, and allow for
        generalization to course, school, student, program.

        Workflow:
        - generate POST request containing all data needed to generate note.
            - {
                "text": "a very important note",
            }
        - extract data from POST request in view's post method.
        - parse data to generate serializable JSON containing all fields/values for new note.
            {
                "user": 1,
                "created": timezone.now(),
                "text": "a very important note",
                "content_type": ContentType.objects.get(model = "model_of_note").pk
                "object_id": pk,
            }
        - verify that user has the right to insert new note into database
            look into verification of user rights
                - utilizer FilterSecurity().get_my_districts()/get_all_districts()
        - Save new note into database
            serializer.save
        - refresh page to show addition of note to detail page
        - Change NoteByObject view to handle note updates via POST request
        """
        """
        Note: the CamelCaseJSONParser that our backend defaults to automatically
        turns camelCase requests generated on the front end into snake_case in
        the back end.
        """
        current_district = District.objects.get(pk = pk)
        accessible_districts = District.objects.filter(pk__in = self.user.get_accessible_districts())
        if current_district not in accessible_districts:
            return Response({"sorry": "this user does not have access to do that."})
        else:
            note_text = request.data["text"]
            note_data = {
                "user": self.user.get_user(),
                "created": timezone.now(),
                "text": note_text,
                "content_type": ContentType.objects.get(model = "district").id,
                "object_id": pk
            }
            serializer = NoteSerializer(data = note_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(f"/{accessLevel}/gsndb/district/{pk}")
            else:
                Response({"error": "data parsed isn't valid for serializer"})

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_students().filter(pk = pk)
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_students().filter(pk = pk)
        serializer = StudentDetailSerializer(queryset , many = True)
        return Response(serializer.data)


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_schools().filter(pk = pk)
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_schools().filter(pk = pk)
        serializer = SchoolDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_courses().filter(pk = pk)
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_courses().filter(pk = pk)
        serializer = CourseDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = self.user.get_my_programs().filter(pk = pk)
        elif access_level == self.user.get_all_access():
            queryset = self.user.get_accessible_programs().filter(pk = pk)
        serializer = ProgramDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

#Other
class NoteByObject(APIView):
    """
    - check if updating a new note
    - serializer.save will update a note if note called when serializer instantiated
        - NoteSerializer(existing_note)
    """
    def get(self, request, pk, objType):

        contType = ContentType.objects.get(app_label = "gsndb", model = objType).id
        notes = Note.objects.filter(content_type = contType, object_id = pk)
        data = NoteSerializer(notes, many = True).data

        return Response(data)

class SchoolInfo(APIView):

    def get(self, request, pk, grade = False, course = False, behavior = False, referral = False, attendance = False, format = None):
        school_obj = School.objects.filter(pk = pk)
        if self.kwargs.get("grade"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getGrades": True})
        elif self.kwargs.get("attendance"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getAttendance": True})
        elif self.kwargs.get("behavior"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getBehavior": True})
        elif self.kwargs.get("referral"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getReferral": True})
        elif self.kwargs.get("course"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getCourse": True})

        return Response(serializer.data)

class StudentInfo(APIView):

    def get(self, request, pk, grade = False, course = False, behavior = False, referral = False, attendance = False, format = None):
        student_obj = Student.objects.filter(pk = pk)
        if self.kwargs.get("grade"):
            serializer = NestedStudentSerializer(student_obj, many = True, context = {"getGrades": True})
        elif self.kwargs.get("attendance"):
            serializer = NestedStudentSerializer(student_obj, many = True, context = {"getAttendance": True})
        elif self.kwargs.get("behavior"):
            serializer = NestedStudentSerializer(student_obj, many = True, context = {"getBehavior": True})
        elif self.kwargs.get("referral"):
            serializer = NestedStudentSerializer(student_obj, many = True, context = {"getReferral": True})
        return Response(serializer.data)


class ProgramInfo(APIView):

    def get(self, request, pk, grade = False, course = False, behavior = False, referral = False, attendance = False, format = None):
        program_obj = Program.objects.filter(pk = pk)
        if self.kwargs.get("grade"):
            serializer = NestedProgramSerializer(program_obj, many = True, context = {"getGrades": True})
        elif self.kwargs.get("attendance"):
            serializer = NestedProgramSerializer(program_obj, many = True, context = {"getAttendance": True})
        elif self.kwargs.get("behavior"):
            serializer = NestedProgramSerializer(program_obj, many = True, context = {"getBehavior": True})
        elif self.kwargs.get("referral"):
            serializer = NestedProgramSerializer(program_obj, many = True, context = {"getReferral": True})
        elif self.kwargs.get("course"):
            serializer = NestedProgramSerializer(program_obj, many = True, context = {"getCourse": True})

        return Response(serializer.data)
