import hashlib, io
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from gsndb.models import Program, District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, FileSHA
from gsndb.serializers import ProgramSerializer, ProgramDetailSerializer, CourseDetailSerializer, SchoolDetailSerializer, StudentDetailSerializer,DistrictSerializer, DistrictDetailSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from gsndb.filter_security import FilterSecurity
from .services.csv_to_json_parser import CSVToJsonParser
from .services.json_parser import parse_json_into_db

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

    def hash_handler(self, byte_file_obj):
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
        byte_file_obj = request.data["mycsv"]
        content = self.hash_handler(byte_file_obj)
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
            string_io_obj = io.StringIO(content)
            school_of_csv_origin = "Trivial"
            parser = CSVToJsonParser(string_io_obj, school_of_csv_origin)
            dtypes = parser.get_csv_datatypes()
            csv_df = parser.get_dataframe(dtypes)
            identifying_column = "studentStateID"
            json_array = parser.get_json_array(csv_df, identifying_column)
            parse_json_into_db(json_array)
            return Response(
                {
                    "file_name": self.fileName,
                    "content": json_array,
                },
                    template_name = "backend_dev_successful_upload.html",
                )
