from django.urls import path
from gsndb import views

urlpatterns = [
  path('districts/', views.district_list),
  path('districts/<int:pk>/', views.district_detail),
  path('schools/', views.SchoolList.as_view()),
  path('schools/<int:pk>/', views.SchoolDetail.as_view()),
  path('students/', views.StudentList.as_view()),
  path('students/<int:pk>/', views.StudentDetail.as_view()),
  path('studentsnaps/', views.StudentSnapList.as_view()),
  path('studentsnaps/<int:pk>/', views.StudentDetail.as_view()),
  path('courses/', views.CourseList.as_view()),
  path('courses/<int:pk>/', views.CourseDetail.as_view()),
  path('behaviors/', views.BehaviorList.as_view()),
  path('behaviors/<int:pk>/', views.BehaviorDetail.as_view()),
  path('attendances/', views.AttendanceList.as_view()),
  path('attendances/<int:pk>/', views.AttendanceDetail.as_view()),
  path('grades/', views.GradeList.as_view()),
  path('grades/<int:pk>/', views.GradeDetail.as_view())
]
