from datetime import timedelta
from django.db import models
from django.utils.timezone import now


def timecount_3_minutes():
    return now() + timedelta(minutes=3)


class UserAuthEmail(models.Model):
    email = models.EmailField(unique=True)
    auth_code = models.CharField(max_length=8)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(default=timecount_3_minutes)


def __str__(self):
    return self.email
