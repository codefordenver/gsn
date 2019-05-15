from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from gsndb.models import District, School, Student, Calendar, Course, Grade, Behavior, Attendance, Referral, Bookmark, Note
from gsndb.serializers import DistrictSerializer, SchoolSerializer, MyStudentsSerializer, StudentSerializer, CalendarSerializer, GradeSerializer, GradeForStudentSerializer, CourseSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, StudentGradeSerializer, ParedGradeSerializer, BookmarkSerializer, NoteSerializer
from rest_framework import generics
from rest_framework.views import APIView

# Create your views here.


class DistrictList(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class SchoolList(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CalendarList(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class CalendarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


class MyStudentsList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = MyStudentsSerializer

class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeForStudent(APIView):
    """# http POST http://127.0.0.1:8000/gsndb/student/someviewendpoint requestParameter="requestValue"""
    def get(self, request, pk, format = None):
        student_obj = Student.objects.filter(pk = pk)
        serializer = GradeForStudentSerializer(student_obj, many = True)
        return Response(serializer.data)


class BehaviorList(generics.ListCreateAPIView):
    queryset = Behavior.objects.all()
    serializer_class = BehaviorSerializer

class BehaviorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Behavior.objects.all()
    serializer_class = BehaviorSerializer


class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class ReferralList(generics.ListCreateAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

class ReferralDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class StudentInfo(APIView):

    def post(self, request, grades=False, attendance=False, behavior=False, format=None):

        student_name = request.data["student_name"].split()

        if len(student_name) == 2:
            first_name = student_name[0]
            last_name = student_name[1]
        elif len(student_name) == 3:
            first_name = student_name[0]
            middle_name = student_name[1]
            last_name = student_name[2]
        elif len(student_name) >= 3:
            first_name = student_name[0]
            middle_name = " ".join(student_name[1:-1])
            last_name = student_name[-1]

        student = Student.objects.get(first_name=first_name, last_name=last_name, middle_name=middle_name)


        if self.kwargs.get("grades"):
            serializer = StudentGradeSerializer(student)
            return Response(serializer.data)

        # http POST http://127.0.0.1:80/gsndb/student/grades studentName="Nikolai Writer Dale"

class BookmarkList(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class CSVParser(APIView):

    renderer_classes = (
        TemplateHTMLRenderer,
        )

    parser_classes = (
        MultiPartParser,
    )

    def file_handler(self, file_obj):
        """Place holder method that currently returns the entire contents of a
        file.

        Note: the .read() method reads entire file to memory, so large
        files may cause your machine to crash. Use .chunks() for larger files.
        """
        content = file_obj.read()
        return content

    def get(self, request):
        """Displays html template with basic file upload functionality.

        Interact with: http GET <host>/gsndb/uploadcsv/

        or visit <host>/gsndb/uploadcsv in browser.
        """
        return Response(template_name = "backend_dev_simple_upload.html")

    def post(self, request):
        """Takes a file and turns it into an instance of Django's UploadedFile
        class. The response generated renders an html template offering some
        meta information.

        Note: it seems UploadedFile objects cannot be accessed by python's open()
        function.

        Interact with: http --form POST <host>/gsndb/uploadcsv/ mycsv@<abs path to file>
        """
        file_obj = request.data["mycsv"]
        content = self.file_handler(file_obj)
        return Response(
            {
                "file_name": file_obj.name,
                "content": content,
            },
            template_name = "backend_dev_successful_upload.html",
            )
