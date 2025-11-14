from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "ec2-13-209-193-43.ap-northeast-2.compute.amazonaws.com",
    "mydomain.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://ec2-13-209-193-43.ap-northeast-2.compute.amazonaws.com",
    "http://mydomain.com",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"