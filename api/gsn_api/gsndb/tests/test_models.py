print("test_models")

# test bad inputs to models
# test create model
# test delete model
# test filter model
# test minimum number of fields that need to be entered
from django.test import TestCase
from gsndb.models import Note, District
from django.contrib.auth.models import User


class DistrictModelTest(TestCase):
    def test_create_instance_minimum_fields(self):
        newDistrict = District.objects.create()

    def test_bad_field_inputs(self):
        print("Need to addresss")
        #newDistrict = District.objects.create(state = 'Colorado')

'''
do this for the remaining models
we want to make sure that the minimum fields we want work for all models
we also want to test any strange inputs to ensure it works out okay

Remaining Models:
School
Program
Student
Course
Calendar
Behavior
Grade
Attendance
'''

class NoteModelTest(TestCase):
    def setUp(self):
        self.newUser = User.objects.create_user(
            username='Hannah',
            email='hannahkamundson@beatles.com',
            password='glass onion')
        
    def test_district_note(self):
        newDistrict = District.objects.create(name = 'Denver Public Schools')
        newNote = Note.objects.create(user = self.newUser, text = 'This is a district', content_object = newDistrict)

'''
under this NoteModelTest do the same as test_district_note for the following  models:

Remaining Models:
School
Program
Student
Course
Calendar
Behavior
Grade
Attendance
Referral
Bookmark
'''
