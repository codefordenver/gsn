import json
from datetime import datetime
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from gsndb.models import District, School, Student, StudentSnap, Course, Behavior, Attendance, Grade
from gsndb.serializers import DistrictSerializer, SchoolSerializer, StudentSerializer, StudentSnapSerializer, CourseSerializer, BehaviorSerializer, AttendanceSerializer, GradeSerializer
from rest_framework import generics



# Create your views here.

"""The district views will be functional and verbose with the intent of clarifying their purpose. Every view hereafter will be generic in nature"""

class DistrictList(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

"""As stated, all of the following views will utilize generic view classes provided by the Django Rest framework."""

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


class StudentSnapList(generics.ListCreateAPIView):
    queryset = StudentSnap.objects.all()
    serializer_class = StudentSnapSerializer

class StudentSnapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentSnap.objects.all()
    serializer_class = StudentSnapSerializer


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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


class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class StudentInfo(APIView):

    def post(self, request, grades=False, attendance=False, behavior=False, format=None):
        student_name = request.data["student_name"].split()
        first_name = student_name[0]
        last_name = student_name[1]
        
        student = Student.objects.get(student_first_name=first_name, student_last_name=last_name)
        student_id = student.student_state_id
        birthday = student.student_birth_date
        current_snap = StudentSnap.objects.filter(student__student_first_name=first_name).order_by('pk').reverse()[0]
        school_name = current_snap.school.school_name

        total_snaps = StudentSnap.objects.filter(student__student_first_name=first_name, student__student_last_name=last_name)

        kwarg_key = ""
        kwarg_data = []

        for snap in total_snaps:
            if self.kwargs.get("grades"):
                kwarg_key = "grades"
                grades = Grade.objects.filter(student_snap=snap)
                cereal = GradeSerializer(grades, many=True)
            if self.kwargs.get("attendance"):
                kwarg_key = "attendance"
                attendance = Attendance.objects.filter(student_snap=snap)
                cereal = AttendanceSerializer(attendance, many=True)
            if self.kwargs.get("behavior"):
                kwarg_key = "behavior"
                behavior = Behavior.objects.filter(student_snap=snap)
                cereal = BehaviorSerializer(behavior, many=True)
            data = JSONRenderer().render(cereal.data)
            python_data = json.loads(data)
            kwarg_data += python_data
        
        output = {
            "studentId" : student_id,
            "name" : request.data["student_name"],
            "school" : school_name,
            "birthdate" : datetime.strftime(birthday, '%-m/%-d/%Y'),
            kwarg_key : kwarg_data
        }

        return Response(output)
