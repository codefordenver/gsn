from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from gsndb.models import District, School, Student, StudentSnap, Course, Behavior, Attendance, Grade
from gsndb.serializers import DistrictSerializer, SchoolSerializer, StudentSerializer, StudentSnapSerializer, CourseSerializer, BehaviorSerializer, AttendanceSerializer, GradeSerializer
from rest_framework import generics
from gsndb.forms import UploadFileForm
from gsndb.csvparser import CSVParser

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

class CSVParser(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            CSVParser(request.FILES['file'])
            response = HttpResponse()
            response.write("File successfully parsed!")
            response.status_code(200)
            return response
    else:
        form = UploadFileForm()
        response = HttpResponse()
        response.write("Uh Oh, check the file you uploaded. It may be corrupted.")
        response.status_code(400)


"""
//USE THE FOLLOWING JAVASCRIPT WITHIN REACT:

const fileInput = document.querySelector('#your-file-input') ;
const formData = new FormData();

formData.append('file', fileInput.files[0]);

const options = {
  method: 'POST',
  body: formData,
  }
};

fetch('your-upload-url', options);
"""