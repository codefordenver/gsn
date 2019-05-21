from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from gsndb.models import *
from gsndb.serializers import *
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


'''class StudentInfo(APIView):

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

'''

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
        if self.kwargs.get("grade"):
            school_obj = School.objects.filter(pk = pk)
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getGrades": True})
        elif self.kwargs.get("attendance"):
            school_obj = School.objects.filter(pk = pk)
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getAttendance": True})
        #elif self.kwargs.get("behavior"):
            #behavior_obj = Behavior.objects.filter(pk = pk)
            #serializer = NestedBehaviorSerializer(behavior_obj, many = True)
        #elif self.kwargs.get("referral"):
            #referral_obj = Referral.objects.filter(pk = pk)
            #serializer = NestedSchoolSerializer(referral_obj, many = True)
        
        return Response(serializer.data)


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

class CourseInfo(APIView):

    def get(self, request, pk, grade = False, course = False, behavior = False, referral = False, attendance = False, format = None):
        course_obj = Course.objects.filter(pk = pk)
        if self.kwargs.get("grade"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getGrades": True})
        elif self.kwargs.get("attendance"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getAttendance": True})
        elif self.kwargs.get("behavior"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getBehavior": True})
        elif self.kwargs.get("referral"):
            serializer = NestedSchoolSerializer(school_obj, many = True, context = {"getReferral": True})
        
        return Response(serializer.data)