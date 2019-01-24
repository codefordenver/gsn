from django.test import TestCase
from django.urls import resolve

class ReferralsTest(TestCase):

    def test_can_resolve_referrals_url(self):
        resolve("/gsndb/referral/")

    def test_can_see_referral_types_drop_down(self):
        response = self.client.get("/gsndb/referral/")

# Create your tests here.
