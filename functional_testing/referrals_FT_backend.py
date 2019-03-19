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

    def cross_check_list_with_drop_down_options(self, list, element_name):
        """ takes a list a cross checks that all items in the list are present
        in a drop down menu html element, and all options in the drop down menu
        element are present in the list. The menu html element is identified
        from a list of elements of the class = "form-control" by its element name.
        Function takes two arguments: an element name as a string and a list to cross check. """
        drop_down_menus = self.browser.find_elements_by_class_name("form-control")

        for menu in drop_down_menus:
            if menu.get_attribute("name") == element_name:
                menu_element = menu

        menu_option_elements = menu_element.find_elements_by_tag_name("option")
        menu_option_text_list = [option.text for option in menu_option_elements]

        self.assertTrue(
        all(option.text in list for option in menu_option_elements),
        f"Some or all drop down menu items are not in the list you are checking.")

        self.assertTrue(
        all(item in menu_option_text_list for item in list),
        f"Some or all items in the list you are checking are not present in " + element_name + " drop down menu.")

    def test_can_add_and_save_new_referral(self):

        #user can visit root/gsndb/referral/ and see Referrals in title
        #of page.

        self.browser.get("http://192.168.99.100:8000/gsndb/referral/")
        self.assertIn("Referral", self.browser.title)

        #user can see label "Student".

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

        self.cross_check_list_with_drop_down_options(all_students_list, "student")

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

        self.cross_check_list_with_drop_down_options(all_referral_types_list, "referal_type")

        #user can enter the date the referral was given, along with the
        #reference's name, phone number, and address.

        #When user enters a new referral entry, their entry appears in the
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
