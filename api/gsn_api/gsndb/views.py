from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from gsndb.models import Program, District, School, Student, Course, Calendar, Grade, Behavior, Attendance, Referral, Note, Bookmark, Program
from gsndb.serializers import ProgramSerializer, ProgramDetailSerializer, CourseDetailSerializer, SchoolDetailSerializer, StudentDetailSerializer,DistrictSerializer, DistrictDetailSerializer, SchoolSerializer, StudentSerializer, CourseSerializer, CalendarSerializer, GradeSerializer, BehaviorSerializer, AttendanceSerializer, ReferralSerializer, NoteSerializer, BookmarkSerializer, NestedSchoolSerializer, NestedStudentSerializer, NestedProgramSerializer, MyStudentsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from gsndb.filterSecurity import FilterSecurity

#Table views
class StudentList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):  

        if access_level == self.user.get_my_access():
            queryset = Student.objects.filter(pk__in = self.user.get_my_students())
        elif access_level == self.user.get_all_access():
            queryset = Student.objects.filter(pk__in = self.user.get_accessible_students())
        serializer = StudentSerializer(queryset , many = True)
        return Response(serializer.data)

class DistrictList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = District.objects.filter(pk__in = self.user.get_my_districts())
        elif access_level == self.user.get_all_access():
            queryset = District.objects.filter(pk__in = self.user.get_accessible_districts())
        serializer = DistrictSerializer(queryset , many = True)
        return Response(serializer.data)

class SchoolList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = School.objects.filter(pk__in = self.user.get_my_schools())
        elif access_level == self.user.get_all_access():
            queryset = School.objects.filter(pk__in = self.user.get_accessible_schools())
        serializer = SchoolSerializer(queryset , many = True)
        return Response(serializer.data)

class CourseList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = Course.objects.filter(pk__in = self.user.get_my_courses())
        elif access_level == self.user.get_all_access():
            queryset = Course.objects.filter(pk__in = self.user.get_accessible_courses())
        serializer = CourseSerializer(queryset , many = True)
        return Response(serializer.data)

class ProgramList(generics.ListCreateAPIView):
    user = FilterSecurity()

    def get(self, request, accessLevel, format = None):
        if access_level == self.user.get_my_access():
            queryset = Program.objects.filter(pk__in = self.user.get_my_programs())
        if access_level == self.user.get_all_access():
            queryset = Program.objects.all()
        serializer = ProgramSerializer(queryset , many = True)
        return Response(serializer.data)


#Detail views
class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = District.objects.filter(pk=pk,pk__in=self.user.get_my_districts())
        elif access_level == self.user.get_all_access():
            queryset = District.objects.filter(pk=pk,pk__in=self.user.get_accessible_districts())
        serializer = DistrictDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = Student.objects.filter(pk__in = self.user.get_my_students(), pk=pk)
        elif access_level == self.user.get_all_access():
            queryset = Student.objects.filter(pk__in = self.user.get_accessible_students(), pk=pk)
        serializer = StudentSerializer(queryset , many = True)
        return Response(serializer.data)

class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = School.objects.filter(pk=pk,pk__in=self.user.get_my_schools())
        elif access_level == self.user.get_all_access():
            queryset =  School.objects.filter(pk=pk,pk__in=self.user.get_accessible_schools())
        serializer = SchoolDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, access_level, format = None):
        if access_level == self.user.get_my_access():
            queryset = Course.objects.filter(pk=pk, pk__in=self.user.get_my_courses())
        elif access_level == self.user.get_all_access():
            queryset = Course.objects.filter(pk=pk, pk__in=self.user.get_accessible_courses())
        serializer = CourseDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)

class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    user = FilterSecurity()

    def get(self, request, pk, accessLevel, format = None):
        if accessLevel == self.user.get_my_access():
            queryset = Program.objects.filter(pk=pk)
        elif accessLevel == self.user.get_all_access():
            queryset = Program.objects.filter(pk__in=self.user.get_my_programs(),pk=pk)
        serializer = ProgramDetailSerializer(queryset , many = True, context = {"access": access_level})
        return Response(serializer.data)


#Other
class NoteByObject(APIView):

    def get(self, request, pk, objType):
        
        contType = ContentType.objects.get(app_label = "gsndb", model = objType).id
        notes = Note.objects.filter(content_type = contType, object_id = pk)
        data = NoteSerializer(notes, many = True).data
        
        return Response(data)





class DistrictDetail(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer



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





