from django.urls import path
from gsndb import views

urlpatterns = [
    path('program/', views.ProgramList.as_view()),
    path('program/<int:pk>/', views.ProgramDetail.as_view()),
    path('district/', views.DistrictList.as_view()),
    path('district/<int:pk>/', views.DistrictDetail.as_view()),
    path('school/', views.SchoolList.as_view()),
    path('school/<int:pk>/', views.SchoolDetail.as_view()),
    path('student/', views.StudentList.as_view()),
    path('student/<int:pk>/', views.StudentDetail.as_view()),
    path('course/', views.CourseList.as_view()),
    path('course/<int:pk>/', views.CourseDetail.as_view()),
    path('bookmark/', views.BookmarkList.as_view()),
    path('bookmark/<int:pk>/', views.BookmarkDetail.as_view()),
    path('note/', views.NoteList.as_view()),
    path('note/<int:pk>/', views.NoteDetail.as_view()),
    path('note/<str:obj_type>/<int:pk>/', views.NoteByObject.as_view()),
    path('referral/', views.ReferralList.as_view()),
    path('referral/<int:pk>/', views.ReferralDetail.as_view()),
    #path('uploadcsv/', views.UploadCSV.as_view()),
    path('create-school/', views.SchoolPostList.as_view()),
    path('create-district/', views.DistrictPostList.as_view()),
    path('modify-my-students/', views.ModifyMyStudentList.as_view())
  ]
