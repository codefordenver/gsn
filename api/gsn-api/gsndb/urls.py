from django.urls import path
from gsndb import views

urlpatterns = [
  path('district/', views.DistrictList.as_view()),
  path('district/<int:pk>/', views.DistrictDetail.as_view()),
  path('school/', views.SchoolList.as_view()),
  path('school/<int:pk>/', views.SchoolDetail.as_view()),
  path('student/', views.StudentList.as_view()),
  path('student/<int:pk>/', views.StudentDetail.as_view()),
  path('student/grades', views.StudentInfo.as_view(), {'grades' : True}),
  path('student/attendance', views.StudentInfo.as_view(), {'attendance' : True}),
  path('student/behavior', views.StudentInfo.as_view(), {'behavior' : True}),
  path('studentsnap/', views.StudentSnapList.as_view()),
  path('studentsnap/<int:pk>/', views.StudentDetail.as_view()),
  path('course/', views.CourseList.as_view()),
  path('course/<int:pk>/', views.CourseDetail.as_view()),
  path('behavior/', views.BehaviorList.as_view()),
  path('behavior/<int:pk>/', views.BehaviorDetail.as_view()),
  path('attendance/', views.AttendanceList.as_view()),
  path('attendance/<int:pk>/', views.AttendanceDetail.as_view()),
  path('grade/', views.GradeList.as_view()),
  path('grade/<int:pk>/', views.GradeDetail.as_view())
]
