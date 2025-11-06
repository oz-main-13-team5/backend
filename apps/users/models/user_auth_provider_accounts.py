from django.db import models
from django.conf import settings


class UserAuthProviderAccounts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=30)
    provider_user_id = models.CharField(max_length=200, unique=True)
    email = models.EmailField(null=True, blank=True)
    profile_image_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_auth_provider_accounts"
