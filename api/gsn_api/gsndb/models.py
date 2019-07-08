from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey,  GenericRelation
from django.contrib.contenttypes.models import ContentType

"""updates to be made
- implement bookmark model
- implement note model
- track program in separate table
- define how to handle enumerations of behavior, attendance codes
"""

DEFAULT_CALENDAR_ID = 1
DEFAULT_SCHOOL_ID = 1
DEFAULT_STUDENT_ID = 1
DEFAULT_COURSE_ID = 1
DEFAULT_DISTRICT_ID =1

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.PROTECT,
    )
    created = models.DateTimeField(default = timezone.now)
    text = models.TextField()

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')


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
        blank = True,
        choices = STATE_CHOICES,
    )
    city = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=100, blank=True)
    notes = GenericRelation(Note)

class School(models.Model):
    name = models.TextField(max_length = 150, blank=True)
    district = models.ForeignKey(
        'District',
        null = True,
        on_delete=models.PROTECT,
    )
    notes = GenericRelation(Note)


class FileSHA(models.Model):
    filePath = models.CharField(max_length = 200)
    hasher = models.TextField()
    created = models.DateTimeField(default = timezone.now)

class Program(models.Model):
    notes = GenericRelation(Note)
    name = models.CharField(max_length=50)

class Student(models.Model):
    ''' IMPORTANT:
    This model must be filtered before outputting to user. It needs
    to be filtered by user through StudentUserHasAccess model
    '''
    current_school = models.ForeignKey(
        "School",
        null = True,
        on_delete = models.PROTECT,
    )
    current_program = models.ForeignKey(
        "Program",
        null = True,
        on_delete = models.PROTECT,
    )
    first_name = models.CharField(max_length = 35, blank=True)
    last_name = models.CharField(max_length = 35, blank=True)
    middle_name = models.CharField(max_length = 35, blank=True)
    """Establish choices for Gender"""
    GENDER_CHOICES = (
        ("M", 'Male'),
        ("F", 'Female'),
        ("NB", 'NonBinary'),
    )
    gender = models.CharField(
            max_length = 2,
            blank = True,
            choices = GENDER_CHOICES,
    )
    birth_date = models.DateField(null = True)
    state_id = models.BigIntegerField(null = True)
    """Establish choices for Grade Year"""
    GRADE_YEAR_CHOICES = (
        ("K", 'Kindergarten'),
        ("1", 'First Grade'),
        ("2", 'Second Grade'),
        ("3", 'Third Grade'),
        ("4", 'Fourth Grade'),
        ("5", 'Fifth Grade'),
        ("6", 'Sixth Grade'),
        ("7", 'Seventh Grade'),
        ("8", 'Eighth Grade'),
        ("9", 'Ninth Grade'),
        ("10", 'Tenth Grade'),
        ("11", 'Eleventh Grade'),
        ("12", 'Twelfth Grade'),
    )
    grade_year = models.CharField(
        choices = GRADE_YEAR_CHOICES,
        max_length = 3,
        null = True,
    )
    reason_in_program = models.TextField(blank=True)
    notes = GenericRelation(Note)

class Course(models.Model):
    school = models.ForeignKey(
        "School",
        null = True,
        on_delete = models.PROTECT,
    )
    name = models.CharField(max_length = 50, blank=True)
    code = models.CharField(max_length = 15, blank=True)
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
        ("JPN", 'Japanese'),
        ("LTN", 'Latin'),
        ("SNL", 'Subject Not Listed'),
    )
    subject = models.CharField(
        max_length = 3,
        blank = True,
        choices = SUBJECT_CHOICES,
    )
    notes = GenericRelation(Note)

class Calendar(models.Model):
    year = models.IntegerField(null=True)
    """establish choices for term"""
    TERM_CHOICES = (
        ("SPR", "Spring"),
        ("SMR", "Summer"),
        ("FLL", "Fall"),
        ("Q1", "1st Quarter"),
        ("Q2", "2nd Quarter"),
        ("Q3", "3rd Quarter"),
        ("Q4", "4th Quarter"),
    )
    term = models.CharField(
        max_length = 3,
        blank = True,
        choices = TERM_CHOICES,
    )
    notes = GenericRelation(Note)

    class Meta:
        unique_together = ('year', 'term')

class Behavior(models.Model):
    student = models.ForeignKey(
        "Student",
        null = True,
        on_delete = models.PROTECT
    )
    school = models.ForeignKey(
        "School",
        null = True,
        on_delete = models.PROTECT
    )
    calendar = models.ForeignKey(
        "Calendar",
        null = True,
        on_delete = models.PROTECT
    )
    program = models.ForeignKey(
        "Program",
        null = True,
        on_delete = models.PROTECT,
    )
    course = models.ForeignKey(
        "Course",
        null = True,
        on_delete = models.PROTECT
    )
    period = models.CharField(
        max_length = 10,
        null = True,
    )
    incident_datetime = models.DateTimeField(default = timezone.now)
    context = models.TextField(blank = True)
    incident_type_program = models.CharField(
        max_length = 50,
        blank = True,
    )
    incident_result_program = models.CharField(
        max_length = 50,
        blank = True,
    )
    incident_type_school = models.CharField(
        max_length = 50,
        blank = True,
    )
    incident_result_school = models.CharField(
        max_length = 50,
        blank = True,
    )
    behavior_SISID = models.BigIntegerField()
    notes = GenericRelation(Note)

class Grade(models.Model):
    student = models.ForeignKey(
        "Student",
        null = True,
        on_delete = models.PROTECT,
    )
    course = models.ForeignKey(
        "Course",
        null = True,
        on_delete = models.PROTECT,
    )
    calendar = models.ForeignKey(
        "Calendar",
        null = True,
        on_delete = models.PROTECT,
    )
    program = models.ForeignKey(
        "Program",
        on_delete = models.PROTECT,
    )
    period = models.CharField(
        max_length = 10,
        null = True,
    )
    entry_datetime = models.DateTimeField(default = timezone.now)
    grade = models.FloatField(null = True)
    task = models.CharField(
        max_length = 100,
        null = True
    )
    term_final_value = models.BooleanField(default = False)
    notes = GenericRelation(Note)


class Attendance(models.Model):
    student = models.ForeignKey(
        "Student",
        null = True,
        on_delete = models.PROTECT,
    )
    school = models.ForeignKey(
        "School",
        null = True,
        on_delete = models.PROTECT,
    )
    calendar = models.ForeignKey(
        "Calendar",
        null = True,
        on_delete = models.PROTECT,
    )
    program = models.ForeignKey(
        "Program",
        on_delete = models.PROTECT,
    )
    entry_datetime = models.DateTimeField(default = timezone.now)
    total_abs = models.FloatField(null = True)
    total_unexabs = models.FloatField(null = True)
    total_exabs = models.FloatField(null = True)
    total_tardies = models.IntegerField(null = True)
    avg_daily_attendance = models.FloatField(null = True)
    term_final_value = models.BooleanField(default = False)
    notes = GenericRelation(Note)

class Referral(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.PROTECT,
    )
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT,
    )
    program = models.ForeignKey(
        "Program",
        on_delete = models.PROTECT,
    )
    """ establish choices for Referral Type"""
    '''
    If this is ever changed, it needs to be changed on the frontend as well
    '''
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
    reason = models.TextField(null = True)
    notes = GenericRelation(Note)

class Bookmark(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.PROTECT,
    )
    created = models.DateTimeField(default = timezone.now)
    url = models.CharField(max_length=500)
    json_request_data = models.TextField()
    notes = GenericRelation(Note)

class StudentUserHasAccess(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.PROTECT,
    )
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT,
    )

    class Meta:
        unique_together = ('user', 'student',)


class MyStudents(models.Model):
    student_user_has_access = models.OneToOneField(
        "StudentUserHasAccess",
        on_delete = models.PROTECT,
    )

class HistoricalStudentID(models.Model):
    student = models.ForeignKey(
        "Student",
        on_delete = models.PROTECT,
    )
    school = models.ForeignKey(
        "School",
        on_delete = models.PROTECT,
    )
    student_SISID = models.BigIntegerField()

    class Meta:
        unique_together = ('student', 'school', 'student_SISID')
