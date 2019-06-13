from django.test import TestCase
from django.contrib.auth.models import User
from gsndb.models import StudentUserHasAccess, MyStudents, Student



# Create your tests here.
user = User.objects.first()

student1 = Student.objects.get(pk=1)
student2 = Student.objects.get(pk=2)
student3 = Student.objects.get(pk=3)

#StudentUserHasAccess.objects.create(user=user,student=student1)
suha = StudentUserHasAccess.objects.get(user=user,student=student1)
StudentUserHasAccess.objects.create(user=user,student=student2)
StudentUserHasAccess.objects.create(user=user,student=student3)

#accessibleStudents = StudentUserHasAccess.objects.filter(user=user,student=student).values('pk')

MyStudents.objects.create(studentUserHasAccess=suha)