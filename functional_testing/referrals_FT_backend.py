from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class Referrals(unittest.TestCase):

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
        self.assertIn("Referral", self.browser.title)

        #user can see drop down menu labelled "Student".

        labels = self.browser.find_elements_by_tag_name("label")

        self.assertTrue(
        any(label.text == "Student" for label in labels),
        "User does not see drop down menu labelled 'Student'.")

        #and pick said student from a drop down menu of all students.

        all_students_list = ["Student object (1)",
            "Student object (2)",
            "Student object (3)",
            "Student object (4)",
            "Student object (5)",
            "Student object (6)",
            "Student object (7)",
            "Student object (8)",
        ]

        drop_down_menus = self.browser.find_elements_by_class_name("form-control")

        for menu in drop_down_menus:
            if menu.get_attribute("name") == "student":
                student_drop_down = menu

        student_options = student_drop_down.find_elements_by_tag_name("option")

        self.assertTrue(
        all(student.text in all_students_list for student in student_options),
        "Some or all students are not present in 'Student' drop down menu.")

        #user can see drop down menu labelled "Referral Type".

        self.assertTrue(
        any(label.text == "Referral type" for label in labels),
        "User does not see drop down menu labelled 'Referral type'.")

        #and pick a referral type from a drop down menu all students.

        all_referral_types_list = ["Mental Health",
            "Drug & Alcohol/Addictions Counseling",
            "Social Services (Department of Human Services)",
            "Division of Youth Services/Corrections",
            "Childcare/Preschool Services,"
            "Family Resources",
            "Meals/Clothing",
            "Housing",
            "Transportation",
            "Specialized School Intervention Program",
            "Work Force Center",
            "Interagency Oversight Group (IOG)",
            "Other",
        ]

        for menu in drop_down_menus:
            if menu.get_attribute("name") == "referral_type":
                referral_type_drop_down = menu

        referral_type_options = referral_type_drop_down.find_elements_by_tag_name("option")

        self.assertTrue(
        all(referral_type.text in all_referral_types_list for referral_type in referral_type_options),
        "Some or all referral types are not present in 'Referral type' drop down menu.")
        
        #user can enter the date the referral was given, along with the
        #reference's name, phone number, and address.

        #once user enters a new referral entry, their entry appears in the
        #list of referrals given.

        self.fail("Finish the test!")

    #def test_user_tracking(self):

        #each referral is associated with the user who made itself.

        #a referral cannot be associated with a user different than the current
        # user without permission.

    #def test_not_nulls(self):

        #user cannot leave referral type, referral date, or reference name blank.



"""below logic statement checks to see if script is being run in terminalself.
unittest.main() runs any method that begins with "test." """
if __name__ == "__main__":
    unittest.main(warnings = "ignore")
