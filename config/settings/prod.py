from .base import *
# base 오버라이딩하여 진행

DEBUG = False
ALLOWED_HOSTS = ["myapp.com", "localhost"]

# 보안 관련 설정
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True