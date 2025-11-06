import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


class ActiveUserQuerySet(models.QuerySet):
    # 활성 사용자만 조회
    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):

    # user모델을 커스텀 하기 위해 usermanager사용

    def get_queryset(self):
        return super().get_queryset()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 적어주세요.")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)

    def all_with_deleted(self):
        # 비활성된 계정을 포함해 조회
        return super().get_queryset()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    provider_id = models.UUIDField(null=True)  # 소셜로그인 인증 제공자 ID
    auth_email_id = models.IntegerField(null=True)  # 이메일 인증 테이블

    username = models.CharField(max_length=150)
    nickname = models.CharField(max_length=20, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_superuser = models.BooleanField(default=False)  # 관리자 계정
    is_active = models.BooleanField(default=True)  # 소프트 삭제를 위한 활성화 필드

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True)

    objects = UserManager()

    def soft_delete(self):
        self.is_active = False  # 계정 비활성화
        self.save()

    def __str__(self):
        return self.email
