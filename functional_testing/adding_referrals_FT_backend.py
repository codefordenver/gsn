from selenium import webdriver
import unittest

class ReferralsTest(unittest.TestCase):

    def setUp(self):
        """automatically creates Chrome window at beginning of testing"""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """automatically removes Chrome window once testing is complete"""
        self.browser.quit()

    def test_can_add_and_save_new_referral(self):

        #user can visit root/gsndb/referral/ and see Referrals in title
        #of page.

        self.browser.get("http://192.168.99.100:8000/gsndb/referral/")
        self.assertIn("Referrals", self.browser.title)

        #user can pick which student they referred from list of students, and
        #and what type of referral they gave from a list of referral types.

        self.fail("Finish the test!")

        #user can enter the date the referral was given, along with the
        #reference's name, phone number, and locationself.

        #once user enters a new referral entry, their entry appears in the
        #list of referrals given.

        #user cannot leave referral type, referral date, or reference name blank.



"""below logic statement checks to see if script is being run in terminalself.
unittest.main() runs any method that begins with "test." """
if __name__ == "__main__":
    unittest.main(warnings = "ignore")
