from django.db import models
#

# Create your models here.

class District(models.Model):
   district_state = models.CharField(max_length=2)
   district_city = models.CharField(max_length=50)
   district_code = models.CharField(max_length=10)

class School(models.Model):
    school_name = models.TextField(max_length=150)
    district = models.ForeignKey(
        'District',
        on_delete=models.CASCADE,
    )

class Student(models.Model):
    school = models.ManyToManyField(
        'School',
    )
    student_first_name = models.CharField(max_length=35)
    student_last_name = models.CharField(max_length=35)
    """Establish choices for Gender"""
    MALE = 'M'
    FEMALE = 'F'
    NONBINARY = 'NB'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NONBINARY, 'NonBinary'),
    )
    student_gender = models.CharField(
            max_length=2,
            choices=GENDER,
            default=NONBINARY,
    )
    student_birth_date = models.DateField()
    student_state_id = models.IntegerField()

class StudentSnap(models.Model):
    school = models.ForeignKey(
        'School',
        on_delete = models.CASCADE,
    )
    student = models.ForeignKey(
        'Student',
        on_delete = models.CASCADE,
    )
    """ESTABLISH CHOICES FOR GRADE PLACEMENT"""
    K = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
    ELEVENTH = 11
    TWELFTH = 12
    GRADE_PLACEMENT = (
        (K, 'Kindergarten'),
        (FIRST, 'First Grade'),
        (SECOND, 'Second Grade'),
        (THIRD, 'Third Grade'),
        (FOURTH, 'Fourth Grade'),
        (FIFTH, 'Fifth Grade'),
        (SIXTH, 'Sixth Grade'),
        (SEVENTH, 'Seventh Grade'),
        (EIGHTH, 'Eighth Grade'),
        (NINTH, 'Ninth Grade'),
        (TENTH, 'Tenth Grade'),
        (ELEVENTH, 'Eleventh Grade'),
        (TWELFTH, 'Twelfth Grade')
    )
    student_grade_placement = models.SmallIntegerField(
            choices=GRADE_PLACEMENT,
            default=K,
    )
    """ESTABLISH CHOICES FOR ATTENDANCE TERM"""
    SPRING = 'SPR'
    SUMMER = "SMR"
    FALL = 'FLL'
    WINTER = 'WNT'
    SPECIAL = 'SPC'
    NOT_SPECIFIED = 'NSP'
    TERMS = (
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
        (FALL, 'Fall'),
        (WINTER, 'Winter'),
        (SPECIAL, 'Special Term'),
        (NOT_SPECIFIED, 'No Term Specified')
    )
    student_attendance_term = models.CharField(
            max_length=3,
            choices=TERMS,
            default=NOT_SPECIFIED,
    )

class Course(models.Model):
    school = models.ForeignKey(
        'School',
        on_delete= models.CASCADE,
    )
    course_name = models.CharField(max_length=100)
    """Establish choices for course subject"""
    MATH = 'MTH'
    SCIENCE = 'SNC'
    HISTORY = 'HST'
    SOCIAL_STUDIES = 'SCS'
    COMPUTER_EDUCATION = 'CMP'
    STUDY_HALL = 'STD'
    SPECIAL_EDUCATION = 'SPL'
    ENGLISH = 'ENG'
    ENGLISH_AS_SECOND_LANGUAGE = 'ESL'
    SPANISH = 'SPA'
    CHINESE = 'CHN'
    FRENCH = 'FRH'
    GERMAN = 'GRM'
    JAPANESE = 'JPN'
    LATIN = 'LTN'
    SUBJECT_NOT_LISTED = 'SNL'
    SUBJECT = (
        (MATH, 'Math'),
        (SCIENCE, 'Science'),
        (HISTORY, 'History'),
        (SOCIAL_STUDIES, 'Social Studies'),
        (COMPUTER_EDUCATION, 'Computer Education'),
        (STUDY_HALL, 'Study Hall'),
        (SPECIAL_EDUCATION, 'Special Education'),
        (ENGLISH, 'English'),
        (ENGLISH_AS_SECOND_LANGUAGE, 'English As a Second Language'),
        (SPANISH, 'Spanish'),
        (CHINESE, 'Chinese'),
        (FRENCH, 'French'),
        (GERMAN, 'German'),
        (JAPANESE, 'Japanese'),
        (LATIN, 'Latin'),
        (SUBJECT_NOT_LISTED, 'Subject Not Listed')
    )
    course_subject = models.CharField(
            max_length=3,
            choices=SUBJECT,
            default=SUBJECT_NOT_LISTED,
    )

class Behavior(models.Model):
    student_snap = models.ForeignKey(
        'StudentSnap',
        on_delete=models.CASCADE,
    )
    behavior_incident_date_time = models.DateTimeField()
    behavior_context = models.TextField(max_length=500)
    behavior_result = models.TextField(max_length=500)

class Attendance(models.Model):
    student_snap = models.ForeignKey(
        'StudentSnap',
        on_delete=models.CASCADE,
    )
    attendance_data_entry_time = models.DateTimeField(auto_now_add=True)
    attendance_total_unexcused_absences = models.IntegerField()
    attendance_total_excused_absences = models.IntegerField()
    attendance_total_tardies = models.IntegerField()

class Grade(models.Model):
    student_snap = models.ForeignKey(
        'StudentSnap',
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
    )
    grade_data_entry_time = models.DateTimeField(auto_now_add=True)
    grade_metric = models.DecimalField(
            max_digits=3,
            decimal_places=2
    )
    """Establish choices for GPA scale"""
    FOUR_POINT_SCALE = 4
    SEVEN_POINT_SCALE = 7
    SCALE = (
        (FOUR_POINT_SCALE, 'Four Point Scale'),
        (SEVEN_POINT_SCALE, 'Seven Point Scale')
    )
    grade_scale = models.SmallIntegerField(
            choices=SCALE,
            default=FOUR_POINT_SCALE,
    )
    grade_is_final = models.BooleanField(default=True)

class Referral(models.Model):
    reference_name = models.CharField(
    max_length = 150
    )
