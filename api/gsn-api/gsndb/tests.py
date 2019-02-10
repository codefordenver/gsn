from django.test import TestCase
from django.urls import resolve
from gsndb.models import District

class ReferralsTest(TestCase):

    def test_can_create_district_instance(self):
        self.client.get("/gsndb/district/")
        instance = District.objects.create()





# Create your tests here.
