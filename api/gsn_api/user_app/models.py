from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

class SpecialKeyLog(models.Model):
    special_key = models.TextField()
    created  = models.DateTimeField(default = timezone.now)
    user_that_create_request = models.ForeignKey(
        get_user_model(),
        on_delete = models.PROTECT,
    )