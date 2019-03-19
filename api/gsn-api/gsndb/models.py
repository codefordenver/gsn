from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

"""updates to be made
- implement bookmark model
- implement note model
- track program in separate table
- define how to handle enumerations of behavior, attendance codes
"""

# Create your models here.

class District(models.Model):
    """establish state choices"""
    STATE_CHOICES = (
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
    )
    state = models.CharField(
        max_length=2,
        choices = STATE_CHOICES,
    )
    city = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class School(models.Model):
    name = models.TextField(max_length = 150)
    district = models.ForeignKey(
        'District',
        on_delete=models.PROTECT,
    )

class Student(models.Model):
    current_school = models.ForeignKey(
        "School",
        on_delete = models.PROTECT,
    )
    first_name = models.CharField(max_length = 35)
    last_name = models.CharField(max_length = 35)
    middle_name = models.CharField(max_length = 35, null = True)
    """Establish choices for Gender"""
    GENDER_CHOICES = (
        ("M", 'Male'),
        ("F", 'Female'),
        ("NB", 'NonBinary'),
    )
    gender = models.CharField(
            max_length = 2,
            choices = GENDER_CHOICES,
    )
    birth_date = models.DateField()
    state_id = models.IntegerField(null = True)
    """Establish choices for Grade Year"""
    GRADE_YEAR_CHOICES = (
        (0, 'Kindergarten'),
        (1, 'First Grade'),
        (2, 'Second Grade'),
        (3, 'Third Grade'),
        (4, 'Fourth Grade'),
        (5, 'Fifth Grade'),
        (6, 'Sixth Grade'),
        (7, 'Seventh Grade'),
        (8, 'Eighth Grade'),
        (9, 'Ninth Grade'),
        (10, 'Tenth Grade'),
        (11, 'Eleventh Grade'),
        (12, 'Twelfth Grade'),
    )
    grade_year = models.SmallIntegerField(
        choices = GRADE_YEAR_CHOICES,
    )
    """establish choices for program"""
    PROGRAM_CHOICES = (
        ("EA", "Expelled and At-Risk Student Servies"),
    )
    program = models.CharField(
        max_length = 2,
        choices = PROGRAM_CHOICES,
    )
    reason_in_program = models.TextField()

class Course(models.Model):
    school = models.ForeignKey(
        "School",
        on_delete = models.PROTECT,
    )
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 15)
    """establish choices for Subject"""
    SUBJECT_CHOICES = (
        ("MTH", 'Math'),
        ("SCI", 'Science'),
        ('HIS', 'History'),
        ('SST', 'Social Studies'),
        ('CED', 'Computer Education'),
        ("PHS", "Physical Education"),
        ("RDG", "Reading"),
        ("WRT", "Writing"),
        ("STH", 'Study Hall'),
        ("SPE", 'Special Education'),
        ("ENG", 'English'),
        ("ESL", 'English As a Second Language'),
        ("ESP", 'Spanish'),
        ("CHI", 'Chinese'),
        ("FRN", 'French'),
        ("GER", 'German'),
        ("JAP", 'Japanese'),
        ("LTN", 'Latin'),
        ("SNL", 'Subject Not Listed'),
    )
    subject = models.CharField(
        max_length = 3,
        choices = SUBJECT_CHOICES,
    )

class Calendar(models.Model):
    year = models. IntegerField()
    """establish choices for term"""
    TERM_CHOICES = (
        ("SPR", "Spring"),
        ("SMR", "Summer"),
        ("FLL", "Fall"),
    )
    term = models.CharField(
        max_length = 3,
        choices = TERM_CHOICES,
    )

class Behavior(models.Model):
    #will probably want to add choices to incident_type and _result
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT
    )
    school = models.ForeignKey(
        "School",
        on_delete = models.PROTECT
    )
    calendar = models.ForeignKey(
        "Calendar",
        on_delete = models.PROTECT
    )
    incident_datetime = models.DateTimeField(default = timezone.now)
    context = models.TextField(null = True)
    incident_type_program = models.CharField(
        max_length = 50,
        null = True,
    )
    incident_result_program = models.CharField(
        max_length = 50,
        null = True,
    )
    incident_type_school = models.CharField(
        max_length = 50,
        null = True,
    )
    incident_result_school = models.CharField(
        max_length = 50,
        null = True,
    )

class Grade(models.Model):
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT,
    )
    course = models.ForeignKey(
        "Course",
        on_delete = models.PROTECT,
    )
    calendar = models.ForeignKey(
        "Calendar",
        on_delete = models.PROTECT,
    )
    entry_datetime = models.DateTimeField(default = timezone.now)
    grade = models.FloatField()
    term_final_value = models.BooleanField(default = False)

class Attendance(models.Model):
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT,
    )
    school = models.ForeignKey(
        "School",
        on_delete = models.PROTECT,
    )
    calendar = models.ForeignKey(
        "Calendar",
        on_delete = models.PROTECT,
    )
    entry_datetime = models.DateTimeField(default = timezone.now)
    total_unexabs = models.IntegerField(null = True)
    total_exabs = models.IntegerField(null = True)
    total_tardies = models.IntegerField(null = True)
    avg_daily_attendance = models.FloatField()
    term_final_value = models.BooleanField(default = False)

class Referral(models.Model):
    #need to alter phone number field probably, for formatting purposes
    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.PROTECT,
    )
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT,
    )
    """ establish choices for Referral Type"""
    REFERRAL_TYPE = (
        ("MTL", "Mental Health"),
        ("DAC", "Drug & Alcohol/Addictions Counseling"),
        ("DHS", "Social Services (Department of Human Services)"),
        ("YSC", "Division of Youth Services/Corrections"),
        ("CPS", "Childcare/Preschool Services"),
        ("FMR", "Family Resources"),
        ("M/C", "Meals/Clothing"),
        ("HOU", "Housing"),
        ("SIP", "Specialized School Intervention Program"),
        ("TRN", "Transportation"),
        ("WFC", "Work Force Center"),
        ("IOG", "Interagency Oversight Group (IOG)"),
        ("OTH", "Other")
    )
    type = models.CharField(
        max_length = 3,
        choices = REFERRAL_TYPE,
    )
    date_given = models.DateField(default = timezone.now)
    reference_name = models.CharField(max_length = 100, null = True)
    reference_phone = models.BigIntegerField(null = True)
    reference_address = models.CharField(max_length = 150, null = True)

""" tables yet to be implemented

class Note(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete = models.PROTECT,
    )
    related_contet = dymanimc_foreign_Key
    created = models.DateTimeField(default = timezone.now)
    content = models.TextField()

class Bookmark(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete = models.PROTECT,
    )
    created = models.DateTimeField(default = timezone.now)
    url = unknown
    react_component = unknown
    json_request_data = unknown

    """
