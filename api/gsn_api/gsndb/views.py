from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from gsndb.models import District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, Program, FileSHA
from gsndb.serializers import DistrictSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
import hashlib
from .services import csv_to_json_parser


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
    #returns all notes for anything
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class BookmarkList(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

class BookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

'''
class SchoolFakeInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSchoolSerializer
'''



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

class CSVParser(APIView):
    def __init__(self):
        self.fileName = ""
        self.hash = ""
        self.hasFileAlreadyUploaded = False

    renderer_classes = (
        TemplateHTMLRenderer,
        )

    parser_classes = (
        MultiPartParser,
    )

    def hash_handler(self, byte_file_on):
        """A hash function that identifies gives a csv file a hash that uniquely
        identifies it against other csv files.

        Note: the .read() method reads entire file to memory, so large
        files may cause your machine to crash. Use .chunks() for larger files.
        """
        blocksize = 65536
        hasher = hashlib.sha1()
        content = ""
        self.fileName = byte_file_obj.name
        buf = byte_file_obj.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            content += buf.decode('utf-8')
            buf = byte_file_obj.read(blocksize)
        self.hash = hasher.hexdigest()
        return content


    def has_file_already_been_uploaded(self):
        self.hasFileAlreadyUploaded = FileSHA.objects.filter(hasher = self.hash).exists()
        if(not self.hasFileAlreadyUploaded):
            FileSHA.objects.create(hasher = self.hash, filePath = self.fileName)

    def parse_csv_from_byte_file_obj(self, byte_file_obj):
        byte_string = byte_file_obj.read()
        string = byte_string.decode("utf-8")
        string_file_obj = io.StringIO(string)

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
        byte_file_on = request.data["mycsv"]
        content = self.hash_handler(byte_file_on)
        self.has_file_already_been_uploaded()


        if(self.hasFileAlreadyUploaded):
            return Response(
                {
                    "file_name": self.fileName,
                    "content": content,
                },
                    template_name = "backend_dev_unsuccessful_hash_upload.html",
                )
        else:
            return Response(
                {
                    "file_name": self.fileName,
                    "content": content,
                },
                    template_name = "backend_dev_successful_upload.html",
                )
