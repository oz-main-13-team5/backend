import uuid
from uuid import UUID
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


def uuid7() -> UUID:
    import os
    import time
    import struct

    ts_ms = int(time.time() * 1000)
    rand = os.urandom(10)
    b = struct.pack(">Q", ts_ms) + rand
    b_list = bytearray(b[:16])
    b_list[6] = (b_list[6] & 0x0F) | 0x70
    b_list[8] = (b_list[8] & 0x3F) | 0x80
    return UUID(bytes=bytes(b_list))


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 적어주세요.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

    def all_with_deleted(self):
        return super().get_queryset()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    provider_id = models.UUIDField(null=True, blank=True)
    auth_email_id = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=150)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.email
