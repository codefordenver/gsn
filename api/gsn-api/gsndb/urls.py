from django.urls import path
from gsndb import views

urlpatterns = [
  path('district/', views.DistrictList.as_view()),
  path('district/<int:pk>/', views.DistrictDetail.as_view()),
  ]
