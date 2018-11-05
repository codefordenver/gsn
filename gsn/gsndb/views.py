from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from gsndb.models import District, School, Student, StudentSnap, Course, Behavior, Attendance, Grade
from gsndb.serializers import DistrictSerializer, SchoolSerializer, StudentSerializer, StudentSnapSerializer, CourseSerializer, BehaviorSerializer, AttendanceSerializer, GradeSerializer
from rest_framework import generics

# Create your views here.

"""The district views will be functional and verbose with the intent of clarifying their purpose. Every view hereafter will be generic in nature"""

@csrf_exempt
def district_list(request):
    """
    List all districts, or create a new district.
    """

    if request.method == 'GET':
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DistrictSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)

@csrf_exempt
def district_detail(request, pk):
    """
    Retrieve, update or delete a district.
    """
    try:
        district = District.objects.get(pk=pk)
    except District.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DistrictSerializer(district)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DistrictSerializer(district, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        district.delete()
        return HttpResponse(status=204)

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
