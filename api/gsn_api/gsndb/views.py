from rest_framework.response import Response
from gsndb.models import Program, District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, Program
from gsndb.serializers import ProgramSerializer, ProgramDetailSerializer, CourseDetailSerializer, SchoolDetailSerializer, StudentDetailSerializer,DistrictSerializer, DistrictDetailSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer, ReferralDetailSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Q
from gsndb.filter_security import FilterSecurity, FilterSecurityFake

user = FilterSecurity()

def post_note(request, Model, pk, access_level):
    """
    This method allows notes to be posted to any object referenced in this
    function's dictionary: access_dict. It should only be called in the POST
    methods of views displaying these models.

    The body of the post request this method handles should be in JSON format:

    {"text": "note text here"}
    """
    access_dict = {
        "Program": user.get_accessible_programs(),
        "District": user.get_accessible_districts(),
        "School": user.get_accessible_schools(),
        "Course": user.get_accessible_courses(),
        "Student": user.get_accessible_students(),
        "Referral": Referral.objects.filter(user_id = user.get_user()),
        "Calendar": Calendar.objects.filter(
            Q(pk__in = Grade.objects.filter(
                student_id__in = user.get_accessible_students().values("id")
                ).values("calendar")
            ) |
            Q(pk__in = Attendance.objects.filter(
                student_id__in = user.get_accessible_students().values("id")
                ).values("calendar")
            ) |
            Q(pk__in = Behavior.objects.filter(
                student_id__in = user.get_accessible_students().values("id")
                ).values("calendar")
            )
        ),
        "Behavior": Behavior.objects.filter(
            student_id__in = user.get_accessible_students().values("id")
        ),
        "Grade": Grade.objects.filter(
            student_id__in = user.get_accessible_students().values("id")
        ),
        "Attendance": Attendance.objects.filter(
            student_id__in = user.get_accessible_students().values("id")
        ),
        "Bookmark": Bookmark.objects.filter(user_id = user.get_user()),
    }
    ModelInstance = Model.objects.get(pk = pk)
    model_name = ModelInstance.__class__.__name__
    accessible_instances = access_dict[model_name]
    if ModelInstance not in accessible_instances:
        return Response({"Sorry": "this user does not have access to do that."})
    else:
        note_text = request.data["text"]
        note_data = {
            "user": user.get_user().id,
            "created": timezone.now(),
            "text": note_text,
            "content_type": ContentType.objects.get(model = model_name.lower()).id,
            "object_id": pk
        }
        serializer = NoteSerializer(data = note_data)
        if serializer.is_valid():
            serializer.save()
            if Model in [Program, District, School, Course, Student]:
                return HttpResponseRedirect(f"/gsndb/{access_level}/{model_name.lower()}/{pk}/")
            else:
                return HttpResponseRedirect(f"/gsndb/{access_level}/note/{model_name.lower()}/{pk}/")
            #return HttpResponseRedirect(redirect_to = f"/{accessLevel}/gsndb/district/{pk}")
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                            })

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
        user = FilterSecurityFake(request)
        if access_level == user.get_my_access():
            # print(request.user)
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

class ReferralList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        queryset = Referral.objects.filter(user = user.get_user())
        serializer = ReferralSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, access_level, format = None):
        """
        This method allows new referrals to be posted to the database. It
        redirects to the selfsame ReferralList view, allowing the user to
        see the new referral they created among their list of referrals.
        """
        json = request.data
        student = Student.objects.get(pk = json["student"])
        if student not in user.get_accessible_students():
            return Response({"Sorry": "this user does not have access to add a referral for this student."})
        else:
            note_data = {
                "user": user.get_user().id,
                "student": json["student"],
                "program": json["program"],
                "type": json["type"],
                "date_given": json["date_given"],
                "reference_name": json["reference_name"],
                "reference_phone": json["reference_phone"],
                "reference_address": json["reference_address"],
                "reason": json["reason"],
                "notes": [],
            }
            serializer = ReferralSerializer(data = note_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(f"/gsndb/{access_level}/referral/{serializer.data['referralId']}/")
            else:

                return Response({
                                    "Sorry": "The serializer denied saving this note.",
                                    "The serializer raised the following errors": serializer.errors
                                })


#Detail views


class ReferralDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        queryset = Referral.objects.filter(pk = pk, )
        serializer = ReferralDetailSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        response = post_note(request, Referral, pk, access_level)
        return response

    def put(self, request, pk, access_level, format = None):
        """
        This method allows a user to update an existing referral via a PUT request.
        """
        referral_obj = Referral.objects.get(pk = pk)
        json = request.data
        student = Student.objects.get(pk = json["student"])
        if student not in user.get_accessible_students():
            return Response({"Sorry": "this user does not have access to edit this referral for this student."})
        else:
            note_data = {
                "user": user.get_user().id,
                "student": json["student"],
                "program": json["program"],
                "type": json["type"],
                "date_given": json["date_given"],
                "reference_name": json["reference_name"],
                "reference_phone": json["reference_phone"],
                "reference_address": json["reference_address"],
                "reason": json["reason"],
            }
            serializer = ReferralSerializer(referral_obj, data = note_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(f"/gsndb/{access_level}/referral/{serializer.data['referralId']}/")
            else:

                return Response({
                                    "Sorry": "The serializer denied saving this note.",
                                    "The serializer raised the following errors": serializer.errors
                                })

    def delete(self, request, pk, access_level, format = None):
        """
        This method allows individual referrals to be deleted.

        interact via: DELETE <host>/gsndb/<accessLevel>/referral/<note_id>
        """
        current_referral = Referral.objects.get(pk = pk)
        accessible_referrals = Referral.objects.filter(user_id = user.get_user().id)
        if current_referral not in accessible_referrals:
            return Response({"Sorry": "this user does not have access to do that."})
        else:
            current_referral.delete()
            return HttpResponseRedirect(f"/gsndb/{access_level}/referral/")


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
        response = post_note(request, District, pk, access_level)
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
        response = post_note(request, Student, pk, access_level)
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
        response = post_note(request, School, pk, access_level)
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
        response = post_note(request, Course, pk, access_level)
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
        response = post_note(request, Program, pk, access_level)
        return response

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        queryset = Note.objects.filter(user_id = user.get_user().id, pk = pk)
        serializer = NoteSerializer(queryset, many = True)
        return Response(serializer.data)

    def put(self, request, pk, access_level, format = None):
        """
        This method allows individual notes to be updated.

        interact via: http PUT <host>/gsndb/<accessLevel>/note/<note_id> {"text": "My note text here."}

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

    def delete(self, request, pk, access_level, format = None):
        """
        This method allows individual notes to be deleted.

        interact via: DELETE <host>/gsndb/<accessLevel>/note/<note_id>
        """
        current_note = Note.objects.get(pk = pk)
        accessible_notes = Note.objects.filter(user_id = user.get_user().id)
        if current_note not in accessible_notes:
            return Response({"Sorry": "this user does not have access to do that."})
        else:
            current_note.delete()
            return HttpResponseRedirect(f"/gsndb/{access_level}/note/")

#Other
class NoteByObject(APIView):

    def get(self, request, pk, access_level, obj_type):
        cont_type = ContentType.objects.get(app_label = "gsndb", model = obj_type).id
        notes = Note.objects.filter(
            user_id = user.get_user(),
            content_type = cont_type,
            object_id = pk,
        )
        data = NoteSerializer(notes, many = True).data
        return Response(data)

    def post(self, request, pk, access_level, obj_type):
        """
        Allows users to post a new note to the list of notes for a model
        instance being displayed. Note that obj_type will be a lowercase string.

        Interact via: POST <host>/gsndb/<access_level>/note/<str:obj_type>/<int:pk>/ body = {"text": "My note text"}

        Note: We override the response given by the post_note() method here
        and instead explicitly redirect.
        """
        model_dict = {
            "program": Program,
            "district": District,
            "school": School,
            "course": Course,
            "student": Student,
            "referral": Referral,
            "calendar": Calendar,
            "behavior": Behavior,
            "grade": Grade,
            "attendance": Attendance,
            "bookmark": Bookmark,
        }
        Model = model_dict[obj_type]
        response = post_note(request, Model, pk, access_level)
        return response

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
