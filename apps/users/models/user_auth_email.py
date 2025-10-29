from django.db import models
from django.utils.timezone import now
from datetime import timedelta

def timecount_3_minutes():
    return now() + timedelta(minutes=3)

class UserAuthEmail(models.Model):
    email = models.EmailField(unique=True) #이메일 형식 자동 검증 및 중복방지
    auth_code = models.CharField(max_length=6) #6자리 코드 저장
    is_verified = models.BooleanField(default=False) #인증 전 기본상태 False
    created_at = models.DateTimeField(default=now) #인증 요청 생성 시각
    verified_at = models.DateTimeField(null=True, blank=True) #인증 완료 시각
    expires_at = models.DateTimeField(default=timecount_3_minutes) #인증 코드 생성 3분후 만료.

    def __str__(self):
        return self.email
