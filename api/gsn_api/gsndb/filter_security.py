from django.contrib.auth.models import User
from gsndb.models import StudentUserHasAccess, MyStudents, Student, School, District, Program, Course



class FilterSecurity():
    all_access = "all"
    my_access = "my"

    def __init__(self):
        self.user = User.objects.first()

    def get_all_access(self):
        return self.all_access

    def get_my_access(self):
        return self.my_access

    def get_user(self):
        return self.user

    def get_accessible_students(self):
        all_accessible = StudentUserHasAccess.objects.filter(user=self.user)
        queryset = Student.objects.filter(
            pk__in = all_accessible.values('student'),
            )
        return queryset

    def get_my_students(self):
        my_accessible = StudentUserHasAccess.objects.filter(
            user = self.user,
            pk__in = MyStudents.objects.values('student_user_has_access'),
            )
        queryset = Student.objects.filter(
            pk__in = my_accessible.values('student'),
            )
        return queryset

    def get_accessible_schools(self):
        queryset = School.objects.filter(
            pk__in = self.get_accessible_students().values('current_school'),
            )
        return queryset

    def get_my_schools(self):
        queryset = School.objects.filter(
            pk__in = self.get_my_students().values('current_school'),
            )
        return queryset

    def get_accessible_districts(self):
        queryset = District.objects.filter(
            pk__in = self.get_accessible_schools().values('district'),
        )
        return queryset

    def get_my_districts(self):
        queryset = District.objects.filter(
            pk__in = self.get_my_schools().values('district'),
        )
        return queryset

    def get_accessible_courses(self):
        queryset = Course.objects.filter(
            school_id__in = self.get_accessible_schools().values('id'),
        )
        return queryset

    def get_my_courses(self):
        queryset = Course.objects.filter(
            school_id__in = self.get_my_schools().values('id'),
        )
        return queryset

    def get_accessible_programs(self):
        queryset = Program.objects.filter(
            pk__in = self.get_accessible_students().values('current_program'),
        )
        return queryset

    def get_my_programs(self):
        queryset = Program.objects.filter(
            pk__in = self.get_my_students().values('current_program')
        )
        return queryset
