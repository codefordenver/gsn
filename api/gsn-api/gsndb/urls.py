from django.urls import path
from gsndb import views

urlpatterns = [
  path('district/', views.DistrictList.as_view()),
  path('district/<int:pk>/', views.DistrictDetail.as_view()),
  path('school/', views.SchoolList.as_view()),
  path('school/<int:pk>/', views.SchoolDetail.as_view()),
  path('student/', views.StudentList.as_view()),
  path('student/<int:pk>/', views.StudentDetail.as_view()),
  path('course/', views.CourseList.as_view()),
  path('course/<int:pk>/', views.CourseDetail.as_view()),
  path('mystudents/', views.MyStudentsList.as_view()),
  path('gradeforstudent/<int:pk>', views.GradeForStudent.as_view()),
  path('grade/', views.GradeList.as_view()),
  path('exp/<group>/<int:pk>/', views.ExpGFS.as_view()),
  ]
