from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    is_blacklisted = models.BooleanField(default=False)

    def blacklist(self):
        self.is_blacklisted = True
        self.save()
