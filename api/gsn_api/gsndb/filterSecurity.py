from django.contrib.auth.models import User
from gsndb.models import StudentUserHasAccess

user = User.objects.first()
accessibleStudents = StudentUserHasAccess.objects.filter(user=user).values('student')
