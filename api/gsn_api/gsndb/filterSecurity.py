from django.contrib.auth.models import User
from gsndb.models import StudentUserHasAccess, MyStudents, Student, School, Grade



class FilterSecurity():
    all_access = "all"
    my_access = "my"

    def __init__(self):
        self.user = User.objects.first()

    def get_all_access(self):
        return self.all_access

    def get_my_access(self):
        return self.my_access

    def get_accessible_students(self):
        accessible_students = StudentUserHasAccess.objects.filter(user=self.user).values('student')
        return accessible_students

    def get_my_students(self):
        my_students_pk = MyStudents.objects.values('student_user_has_access')
        my_students = StudentUserHasAccess.objects.filter(user=self.user, pk__in=my_students_pk).values('student')
        return my_students

    def get_accessible_districts(self):
        school_list = self.get_accessible_schools()
        district_list = School.objects.filter(pk__in=school_list).values('district')
        return district_list

    def get_my_districts(self):
        school_list = self.get_my_schools()
        district_list = School.objects.filter(pk__in=school_list).values('district')
        return district_list

    def get_accessible_schools(self):
        student_list = self.get_accessible_students()
        school_list = Student.objects.filter(pk__in=student_list).values('current_school')
        return school_list

    def get_my_schools(self):
        student_list = self.get_my_students()
        school_list = Student.objects.filter(pk__in=student_list).values('current_school')
        return school_list

    def get_accessible_courses(self):
        student_list = self.get_accessible_students()
        course_list = Grade.objects.filter(student__in=student_list).values('course')
        return course_list

    def get_my_courses(self):
        student_list = self.get_my_students()
        course_list = Grade.objects.filter(student__in=student_list).values('course')
        return course_list

    def get_accessible_programs(self):
        student_list = self.get_accessible_students()
        program_list = Student.objects.filter(pk__in=student_list).values('current_program')
        return program_list

    def get_my_programs(self):
        student_list = self.get_my_students()
        program_list = Student.objects.filter(pk__in=student_list).values('current_program')
        return program_list
