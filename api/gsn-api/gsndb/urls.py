from django.urls import path
from gsndb import views

urlpatterns = [
  path('district/', views.DistrictList.as_view()),
  path('district/<int:pk>/', views.DistrictDetail.as_view()),
  path('school/', views.SchoolList.as_view()),
  path('school/<int:pk>/', views.SchoolDetail.as_view()),
  path('student/', views.StudentList.as_view()),
  path('student/<int:pk>/', views.StudentDetail.as_view()),
  path('mystudents/', views.MyStudentsList.as_view()),
  ]
