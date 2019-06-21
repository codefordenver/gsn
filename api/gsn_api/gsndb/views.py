from rest_framework.response import Response
from gsndb.models import Program, District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, Program
from gsndb.serializers import ProgramSerializer, ProgramDetailSerializer, CourseDetailSerializer, SchoolDetailSerializer, StudentDetailSerializer,DistrictSerializer, DistrictDetailSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.http import HttpResponseRedirect
from gsndb.filter_security import FilterSecurity

user = FilterSecurity()

#Table views
class StudentList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_students()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_students()
        serializer = StudentSerializer(queryset , many = True)
        return Response(serializer.data)


class DistrictList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_districts()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_districts()
        serializer = DistrictSerializer(queryset , many = True)
        return Response(serializer.data)

class SchoolList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_schools()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_schools()
        serializer = SchoolSerializer(queryset , many = True)
        return Response(serializer.data)

class CourseList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_courses()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_courses()
        serializer = CourseSerializer(queryset , many = True)
        return Response(serializer.data)


class ProgramList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_programs()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_programs()
        serializer = ProgramSerializer(queryset , many = True)
        return Response(serializer.data)

class NoteList(generics.ListCreateAPIView):

    queryset = Note.objects.filter(user_id = user.get_user().id)
    serializer_class = NoteSerializer

class BookmarkList(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

#Detail views

def post_note_to_detail(request, Model, pk, access_level):
    """
    This method allows notes to be posted to our five detail views: Program,
    District, School, Course, and Student. It should only be called in the post
    methods of Detail views.

    Note: the CamelCaseJSONParser that our backend defaults to automatically
    turns camelCase requests generated on the front end into snake_case in
    the back end.
    """
    access_dict = {
        "Program": user.get_accessible_programs(),
        "District": user.get_accessible_districts(),
        "School": user.get_accessible_schools(),
        "Course": user.get_accessible_courses(),
        "Student": user.get_accessible_students(),
    }
    DetailInstance = Model.objects.get(pk = pk)
    detail_name = DetailInstance.__class__.__name__
    accessible_instances = access_dict[detail_name]
    if DetailInstance not in accessible_instances:
        return Response({"Sorry": "this user does not have access to do that."})
    else:
        note_text = request.data["text"]
        note_data = {
            "user": user.get_user().id,
            "created": timezone.now(),
            "text": note_text,
            "content_type": ContentType.objects.get(model = detail_name.lower()).id,
            "object_id": pk
        }
        serializer = NoteSerializer(data = note_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(f"/gsndb/{access_level}/{detail_name.lower()}/{pk}/")
            #return HttpResponseRedirect(redirect_to = f"/{accessLevel}/gsndb/district/{pk}")
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                            })

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_districts().filter(pk = pk)
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_districts().filter(pk = pk)
        serializer = DistrictDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        Interact via: POST <host>/gsndb/<access_level>/district/<pk> body = {"text": "My note text"}
        """
        response = post_note_to_detail(request, District, pk, access_level)
        return response

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_students().filter(pk = pk)
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_students().filter(pk = pk)
        serializer = StudentDetailSerializer(queryset , many = True)
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        Interact via: POST <host>/gsndb/<access_level>/student/<pk> body = {"text": "My note text"}
        """
        response = post_note_to_detail(request, Student, pk, access_level)
        return response

class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_schools().filter(pk = pk)
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_schools().filter(pk = pk)
        serializer = SchoolDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        Interact via: POST <host>/gsndb/<access_level>/School/<pk> body = {"text": "My note text"}
        """
        response = post_note_to_detail(request, School, pk, access_level)
        return response

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_courses().filter(pk = pk)
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_courses().filter(pk = pk)
        serializer = CourseDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        Interact via: POST <host>/gsndb/<access_level>/course/<pk> body = {"text": "My note text"}
        """
        response = post_note_to_detail(request, Course, pk, access_level)
        return response

class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        if access_level == user.get_my_access():
            queryset = user.get_my_programs().filter(pk = pk)
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_programs().filter(pk = pk)
        serializer = ProgramDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        Interact via: POST <host>/gsndb/<access_level>/program/<pk> body = {"text": "My note text"}
        """
        response = post_note_to_detail(request, Program, pk, access_level)
        return response

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        queryset = Note.objects.filter(user_id = user.get_user().id, pk = pk)
        serializer = NoteSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        """
        This method allows individual notes to be updated.

        interact via: http POST <host>/gsndb/<accessLevel>/note/<note_id> {"text": "My note text here."}

        Note: the CamelCaseJSONParser that our backend defaults to automatically
        turns camelCase requests generated on the front end into snake_case in
        the back end.
        """
        current_note = Note.objects.get(pk = pk)
        accessible_notes = Note.objects.filter(user_id = user.get_user().id)
        if current_note not in accessible_notes:
            return Response({"Sorry": "this user does not have access to do that."})
        else:
            note_text = request.data["text"]
            note_data = {
                "user": user.get_user().id,
                "created": timezone.now(),
                "text": note_text,
                "content_type": ContentType.objects.get(model = "note").id,
                "object_id": pk
            }
            serializer = NoteSerializer(current_note, data = note_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(f"/gsndb/{access_level}/note/{pk}/")
                #return HttpResponseRedirect(redirect_to = f"/{accessLevel}/gsndb/district/{pk}")
            else:

                return Response({
                                    "Sorry": "data parsed isn't valid for serializer",
                                    "serializer errors": serializer.errors
                                })
#Other
class NoteByObject(APIView):
    """
    - check if updating a new note
    - serializer.save will update a note if note called when serializer instantiated
        - NoteSerializer(existing_note)
    """
    def get(self, request, pk, obj_type):

        cont_type = ContentType.objects.get(app_label = "gsndb", model = obj_type).id
        notes = Note.objects.filter(content_type = cont_type, object_id = pk)
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
