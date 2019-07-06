import hashlib, io
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from gsndb.models import Program, District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, FileSHA, StudentUserHasAccess, MyStudents, HistoricalStudentID
from gsndb.serializers import ProgramSerializer, ProgramDetailSerializer, CourseDetailSerializer, SchoolDetailSerializer, StudentDetailSerializer,DistrictSerializer, DistrictDetailSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer, ReferralDetailSerializer, CreateDistrictSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Q
from gsndb.filter_security import FilterSecurity
from .services.parser import CSVParser
from django.contrib.auth.models import User

def post_note(request, Model, pk, access_level):
    """
    This method allows notes to be posted to any object referenced in this
    function's dictionary: access_dict. It should only be called in the POST
    methods of views displaying these models.

    The body of the post request this method handles should be in JSON format:

    {"text": "note text here"}
    """
    user = FilterSecurity(request)
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
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                            })

#Table views
class StudentList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        if access_level == user.get_my_access():
            queryset = user.get_my_students()
        elif access_level == user.get_not_my_access():
            queryset = user.get_not_my_students()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_students()
        serializer = StudentSerializer(queryset , many = True)
        return Response(serializer.data)


class DistrictList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        if access_level == user.get_my_access():
            queryset = user.get_my_districts()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_districts()
        serializer = DistrictSerializer(queryset, many = True)
        return Response(serializer.data)

class SchoolList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        if access_level == user.get_my_access():
            queryset = user.get_my_schools()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_schools()
        serializer = SchoolSerializer(queryset, many = True)
        return Response(serializer.data)

class CourseList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        if access_level == user.get_my_access():
            queryset = user.get_my_courses()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_courses()
        serializer = CourseSerializer(queryset , many = True)
        return Response(serializer.data)


class ProgramList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        if access_level == user.get_my_access():
            queryset = user.get_my_programs()
        elif access_level == user.get_all_access():
            queryset = user.get_accessible_programs()
        serializer = ProgramSerializer(queryset , many = True)
        return Response(serializer.data)

class NoteList(generics.ListCreateAPIView):
    def get(self, request):
        user = FilterSecurity(request)
        queryset = Note.objects.filter(user_id = user.get_user().id)
        serializer = NoteSerializer(queryset, many = True)
        return Response(serializer.data)

class BookmarkList(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class ReferralList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        queryset = Referral.objects.filter(user = user.get_user())
        serializer = ReferralSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, access_level, format = None):
        """
        This method allows new referrals to be posted to the database. It
        redirects to the selfsame ReferralList view, allowing the user to
        see the new referral they created among their list of referrals.

        The body of the post request this method handles should be in JSON format:

        {"student": "student id here",
        "program": "program pk",
        "type": "list of types that can be found in referral model",
        "date_given": "YYYY-MM-DD",
        "reference_name": "the name of the person who referred whatever",
        "reference_phone": integer goes here,
        "reference_address": "an address goes here",
        "reason": "reason..."
        }
        """
        user = FilterSecurity(request)
        json = request.data
        student = Student.objects.get(pk = json["student"])
        if student not in user.get_accessible_students():
            return Response({"Sorry": "this user does not have access to add a referral for this student."})
        else:
            referral_data = {
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
            serializer = ReferralSerializer(data = referral_data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(f"/gsndb/{access_level}/student/{serializer.data['student']}/")
            else:

                return Response({
                                    "Sorry": "The serializer denied saving this referral.",
                                    "The serializer raised the following errors": serializer.errors
                                })

class SchoolPostList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        queryset = School.objects.all()
        serializer = SchoolSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, access_level, format = None):
        """
        This method allows new schools to be posted to the database.

        The body of the post request this method handles should be in JSON format:

        {"school_name": "new school name",
        "district_id": "district pk"
        }
        """

        json = request.data
        school_data = {
            "name": json["school_name"],
            "district": json["district_id"]
        }
        serializer = SchoolSerializer(data = school_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(f"/gsndb/{access_level}/create-school/")
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                            })

    def put(self, request, access_level, format = None):
        """
        This method allows a user to update an existing school via a PUT request.

        expected format of body:
        {
            "school_id": 1,
            "school_name": "legoland",
            "district_id": 4,
        }
        """
        json = request.data
        pk = json["school_id"]
        school_obj = School.objects.get(pk = pk)
        school_data = {
            "name": json["school_name"],
            "district": json["district_id"]
        }
        serializer = SchoolSerializer(school_obj, data = school_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(f"/gsndb/{access_level}/create-school/")
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                                })

    def delete(self, request, access_level, format = None):
        """
        This method allows individual schools to be deleted.

        interact via: DELETE <host>/gsndb/<access_level>/school/<pk> body = {"id": 1}
        """
        pk = request.data["id"]
        current_school = School.objects.get(pk = pk)
        is_connected = False
        all_historical_student_id = HistoricalStudentID.objects.all()
        for instance in all_historical_student_id:
            if instance.school.id == pk:
                is_connected = True
                break
        if is_connected == False:
            current_school.delete()
            return HttpResponseRedirect(f"/gsndb/{access_level}/create-school/")
        else:
            return Response(
                {
                    "Sorry": "You cannot delete a student with students already connected to it.",
                }
            )


class DistrictPostList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        queryset = District.objects.all()
        serializer = CreateDistrictSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, access_level, format = None):
        """
        This method allows new districts to be posted to the database.

        The body of the post request this method handles should be in JSON format:

        {"district_name": "new district name",
        "city": "the city",
        "state": "two digit state",
        "code": "district code"
        }
        """

        json = request.data
        district_data = {
            "name": json["district_name"],
            "city": json["city"],
            "state": json["state"],
            "code": json["code"]
        }
        serializer = DistrictSerializer(data = district_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(f"/gsndb/{access_level}/create-district/")
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                            })
    def put(self, request, access_level, format = None):
        """
        This method allows a user to update an existing district via a PUT request.

        expected format of body:

        {
            "id": 1,
            "district_name": "namehere",
            "city": "Chicago",
            "state": "IL",
            "code": "h67"
        }
        """
        json = request.data
        pk = json["id"]
        district_obj = District.objects.get(pk = pk)
        district_data = {
            "name": json["district_name"],
            "city": json["city"],
            "state": json["state"],
            "code": json["code"]
        }
        serializer = DistrictSerializer(district_obj, data = district_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(f"/gsndb/{access_level}/create-district/")
        else:

            return Response({
                                "Sorry": "The serializer denied saving this note.",
                                "The serializer raised the following errors": serializer.errors
                                })

    def delete(self, request, access_level, format = None):
        """
        This method allows individual districts to be deleted.

        interact via: DELETE <host>/gsndb/<access_level>/district/<pk> body = {"id": 1}
        """
        pk = request.data["id"]
        current_district = District.objects.get(pk = pk)
        connected_schools = False
        all_schools = School.objects.all()
        for school in all_schools:
            if school.district.id == pk:
                connected_schools = True
                break
        if connected_schools == False:
            current_district.delete()
            return HttpResponseRedirect(f"/gsndb/{access_level}/create-district/")
        else:
            return Response(
                {
                    "Sorry": "You cannot delete a district with schools already connected to it. To delete this district, delete the following schools first.",
                    "schools": SchoolSerializer(current_district.school_set, many = True).data
                }
            )



class ModifyMyStudentList(generics.ListCreateAPIView):

    def get(self, request, access_level, format = None):
        user = FilterSecurity(request)
        if access_level == user.get_my_access():
            my_queryset = user.get_my_students()
            notmy_queryset = user.get_not_my_students()
        my_serializer = StudentSerializer(my_queryset , many = True)
        notmy_serializer = StudentSerializer(notmy_queryset, many = True)
        return Response(
            {
                "my_students": my_serializer.data,
                "notmy_students": notmy_serializer.data
            }
        )

    def post(self, request, access_level, format = None):
        """
        This method allows a user to select what students they want to be counted in the "my student"
        list. This post allows users to both add a student to the list and remove a student to the list
        depending on the value of remove. If remove is true then it will remove student from my student.
        If remove is false it will add the student to my student. This will take in more than one student
        at a time.

        The body of the post request this method handles should be in JSON format:

        [
            {"student_id": "student id",
                "remove": true/false
            },
            {"student_id": "student id",
                "remove": true/false
            },
            ...,
            {"student_id": "student id",
                "remove": true/false
            }
        ]
        """
        user = FilterSecurity(request)
        current_user = user.get_user().id
        user_instance = User.objects.get(pk=current_user)

        json = request.data
        try:
            for json_slice in range(0,len(json)):
                student_data = {
                    "student_id": json[json_slice]["student_id"],
                    "remove": json[json_slice]["remove"]
                }

                student_instance = Student.objects.get(pk=student_data["student_id"])
                accessible_student_instance = StudentUserHasAccess.objects.get(user=user_instance, student=student_instance)
                if(student_data["remove"]):
                    MyStudents.objects.get(student_user_has_access=accessible_student_instance).delete()
                else:
                    MyStudents.objects.create(student_user_has_access=accessible_student_instance)
            return HttpResponseRedirect(f"/gsndb/{access_level}/modify-my-students/")
        except Exception as e:
            return Response({
                                "Sorry": "The model denied modifying these students.",
                                "The model raised the following errors": str(e),
                            })


#Detail views
class ReferralDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
        queryset = Referral.objects.filter(pk = pk, )
        serializer = ReferralDetailSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
        response = post_note(request, Referral, pk, access_level)
        return response

    def put(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
        """
        This method allows a user to update an existing referral via a PUT request.
        """
        referral_obj = Referral.objects.get(pk = pk)
        json = request.data
        student = Student.objects.get(pk = json["student"])
        if student not in user.get_accessible_students():
            return Response({"Sorry": "this user does not have access to edit this referral for this student."})
        else:
            referral_data = {
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
            serializer = ReferralSerializer(referral_obj, data = referral_data)
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
        user = FilterSecurity(request)
        current_referral = Referral.objects.get(pk = pk)
        accessible_referrals = Referral.objects.filter(user_id = user.get_user().id)
        if current_referral not in accessible_referrals:
            return Response({"Sorry": "this user does not have access to do that."})
        else:
            current_referral.delete()
            return HttpResponseRedirect(f"/gsndb/{access_level}/referral/")

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
        response = post_note(request, Student, pk, access_level)
        return response



class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
        response = post_note(request, School, pk, access_level)
        return response


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
        response = post_note(request, Course, pk, access_level)
        return response


class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, pk, access_level, format = None):
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
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
        user = FilterSecurity(request)
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


class NoteByObject(APIView):

    def get(self, request, pk, objType):

        contType = ContentType.objects.get(app_label = "gsndb", model = objType).id
        notes = Note.objects.filter(content_type = contType, object_id = pk)
        data = NoteSerializer(notes, many = True).data

        return Response(data)


class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class UploadCSV(APIView):

    parser_classes = (
        MultiPartParser,
    )

    def __init__(self):
        self.file_name = ""
        self.hash = ""
        self.has_file_already_uploaded = False

    def hash_handler(self, byte_file_obj):
        """A hash function that identifies gives a csv file a hash that uniquely
        identifies it against other csv files.

        Note: the .read() method reads entire file to memory, so large
        files may cause your machine to crash. Use .chunks() for larger files.
        """
        blocksize = 65536
        hasher = hashlib.sha1()
        content = ""
        self.file_name = byte_file_obj.name
        buf = byte_file_obj.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            content += buf.decode('utf-8')
            buf = byte_file_obj.read(blocksize)
        self.hash = hasher.hexdigest()
        return content


    def has_file_already_been_uploaded(self):
        self.has_file_already_uploaded = FileSHA.objects.filter(hasher = self.hash).exists()
        if(not self.has_file_already_uploaded):
            FileSHA.objects.create(hasher = self.hash, filePath = self.file_name)

    def post(self, request, access_level):
        """Takes a file and turns it into an instance of Django's UploadedFile
        class. The response generated renders an html template offering some
        meta information.

        Interact with: POST <host>/gsndb/access_level/uploadcsv/ {"school_of_csv_origin": <school_name>, "term_final_value" = <boolean>, "csv": <csv_file>}
        """
        byte_file_obj = request.data["csv"]
        school_of_origin = request.data["school_of_csv_origin"]
        if request.data["term_final_value"] == "True":
            term_final_value = True
        else:
            term_final_value = False
        content = self.hash_handler(byte_file_obj)
        self.has_file_already_been_uploaded()
        string_io_obj = io.StringIO(content)
        parser = CSVParser(string_io_obj, school_of_origin, term_final_value)
        parser.organize()
        return Response(parser.parse_json())
        """
        if(self.has_file_already_uploaded):
            return Response(
                {
                    "Error": f"{self.file_name} has already been uploaded.",
                    "content": content,
                }
            )
        else:
            string_io_obj = io.StringIO(content)
            parser = CSVParser(string_io_obj, school_of_origin, False)
            dtypes = parser.get_csv_datatypes()
            csv_df = parser.get_dataframe(dtypes)
            identifying_column = "studentStateID"
            json_array = parser.get_json_array(csv_df, identifying_column)
            return Response(
                {
                    "file_name": self.file_name,
                    "content": json_array,
                }
            )
        """
