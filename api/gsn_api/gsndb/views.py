from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from gsndb.models import District, School, Student, Calendar, Course, Grade, Behavior, Attendance, Referral, Bookmark
from gsndb.serializers import DistrictSerializer, SchoolSerializer, MyStudentsSerializer, StudentSerializer, CalendarSerializer, GradeSerializer, GradeForStudentSerializer, CourseSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, StudentGradeSerializer, ParedGradeSerializer, BookmarkSerializer
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
    """this view is currently linked to the url path
     /gsndb/gradeforstudent/<int:pk>/. It displays grade data for a student
     selected by the primary key entered into the last part of the endpoint.
     Ex: /gsndb/gradeforstudent/1 returnts grade data for the student with
     primary key 1 in the student table."""
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