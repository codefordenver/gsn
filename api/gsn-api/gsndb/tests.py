from django.test import TestCase
from django.urls import resolve
from gsndb.models import District, School, Student

class ReferralsTest(TestCase):

    def test_can_create_district_instance(self):
        self.client.get("/gsndb/district/")






# Create your tests here.
