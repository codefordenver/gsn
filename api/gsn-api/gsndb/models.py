from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#

# Create your models here.

class District(models.Model):
   state = models.CharField(max_length=2)
   city = models.CharField(max_length=50)
   code = models.CharField(max_length=10)
   name = models.CharField(max_length=100)

class School(models.Model):
    name = models.TextField(max_length = 150)
    district = models.ForeignKey(
        'District',
        on_delete=models.CASCADE,
    )

class Student(models.Model):
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
        (12, 'Twelfth Grade')
    )
    grade_year = models.SmallIntegerField(
        choices = GRADE_YEAR_CHOICES,
    )
    current_school = models.ForeignKey(
        "School",
        on_delete = models.CASCADE,
    )
    program = models.CharField(max_length = 100)
    reason_in_program = models.TextField()

class Course(models.Model):
    school = models.ForeignKey(
        "School",
        on_delete = models.CASCADE,
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

class Behavior(models.Model):
    #will probably want to add choices to incident_type and _result
    student = models.ForeignKey(
        "Student",
        on_delete = models.CASCADE
    )
    school = models.ForeignKey(
        "School",
        on_delete = models.CASCADE
    )
    incident_datetime = models.DateTimeField()
    calendar_year = models.IntegerField()
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
        on_delete = models.CASCADE,
    )
    course = models.ForeignKey(
        "Course",
        on_delete = models.CASCADE,
    )
    entry_datetime = models.DateTimeField(default = timezone.now)
    calendar_year = models.IntegerField()
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
    grade = models.FloatField()
    final_boolean = models.BooleanField(default = False)

class Attendance(models.Model):
    #may want to track term attendance percentage (percent of days present)
    student = models.ForeignKey(
        "Student",
        on_delete = models.CASCADE
    )
    school = models.ForeignKey(
        "School",
        on_delete = models.CASCADE
    )
    entry_datetime = models.DateTimeField(default = timezone.now)
    calendar_year = models.IntegerField()
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
    total_unexcused_absences = models.IntegerField(null = True)
    total_excused_absences = models.IntegerField(null = True)
    total_tardies = models.IntegerField(null = True)
    term_total_boolean = models.BooleanField(default = False)

class Referral(models.Model):
    #need to add user field, which requires fleshing out user_app
    #need to alter phone number field probably, for formatting purposes
    student = models.ForeignKey(
        "Student",
        on_delete = models.CASCADE,
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
    referral_type = models.CharField(
        max_length = 3,
        choices = REFERRAL_TYPE,
    )
    referral_date = models.DateField(default = timezone.now)
    reference_name = models.CharField(max_length = 100, null = True)
    reference_phone = models.BigIntegerField(null = True)
    reference_address = models.CharField(max_length = 150, null = True)
