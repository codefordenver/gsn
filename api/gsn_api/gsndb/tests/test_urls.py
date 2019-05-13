from django.urls import resolve
from django.test import TestCase

print("test_urls")

class DistrictURLTest(TestCase):

    #test that the view for the URL matches the expected view
    def test_url_resolves_to_view(self):
        resolver = resolve('/gsndb/district/')
        self.assertEqual(resolver.view_name,'gsndb.views.DistrictList')


class DistrictArgumentURLTest(TestCase):

    #test that the view for the URL matches the expected view
    def test_url_resolves_to_view(self):
        resolver = resolve('/gsndb/district/7/')
        self.assertEqual(resolver.view_name,'gsndb.views.DistrictDetail')


''' Do this for the following URLs
Ask if you need help specifically if you are doin it on a multi level one

**********************************************************************
    path('school/', views.SchoolList.as_view()),
    path('school/<int:pk>/', views.SchoolDetail.as_view()),
    path('student/', views.StudentList.as_view()),
    path('student/<int:pk>/', views.StudentDetail.as_view()),
    path('course/', views.CourseList.as_view()),
    path('course/<int:pk>/', views.CourseDetail.as_view()),
    path('calendar/', views.CalendarList.as_view()),
    path('calendar/<int:pk>/', views.CalendarDetail.as_view()),
    path('grade/', views.GradeList.as_view()),
    path('grade/<int:pk>/', views.GradeDetail.as_view()),
    path('attendance/', views.AttendanceList.as_view()),
    path('attendance/<int:pk>/', views.AttendanceDetail.as_view()),
    path('behavior/', views.BehaviorList.as_view()),
    path('behavior/<int:pk>/', views.BehaviorDetail.as_view()),
    path('referral/', views.ReferralList.as_view()),
    path('referral/<int:pk>/', views.ReferralDetail.as_view()),
    path('mystudents/', views.MyStudentsList.as_view()),
    path('bookmark/', views.BookmarkList.as_view()),
    path('bookmark/<int:pk>/', views.BookmarkDetail.as_view()),
    path('school/grade/<int:pk>/', views.SchoolInfo.as_view(), {'grade' : True}),
    path('school/attendance/<int:pk>/', views.SchoolInfo.as_view(), {'attendance' : True}),
    path('school/referral/<int:pk>/', views.SchoolInfo.as_view(), {'referral' : True}),
    path('school/behavior/<int:pk>/', views.SchoolInfo.as_view(), {'behavior' : True}),
    path('school/course/<int:pk>/', views.SchoolInfo.as_view(), {'course' : True}),
    path('student/grade/<int:pk>/', views.StudentInfo.as_view(), {'grade' : True}),
    path('student/attendance/<int:pk>/', views.StudentInfo.as_view(), {'attendance' : True}),
    path('student/referral/<int:pk>/', views.StudentInfo.as_view(), {'referral' : True}),
    path('student/behavior/<int:pk>/', views.StudentInfo.as_view(), {'behavior' : True}),
    path('program/grade/<int:pk>/', views.ProgramInfo.as_view(), {'grade' : True}),
    path('program/attendance/<int:pk>/', views.ProgramInfo.as_view(), {'attendance' : True}),
    path('program/referral/<int:pk>/', views.ProgramInfo.as_view(), {'referral' : True}),
    path('program/behavior/<int:pk>/', views.ProgramInfo.as_view(), {'behavior' : True}),
    path('program/course/<int:pk>/', views.ProgramInfo.as_view(), {'course' : True}), #still need to work on this one
    path('note/', views.NoteList.as_view()),
    path('note/<str:objType>/<int:pk>/', views.NoteByObject.as_view()),

  **********************************************************************
'''