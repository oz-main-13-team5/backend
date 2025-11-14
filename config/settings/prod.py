from .base import *

ALLOWED_HOSTS = ["mydomain.com"]
DEBUG = False

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"