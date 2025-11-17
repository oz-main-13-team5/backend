from.base import *

DEBUG = False

ALLOWED_HOSTS = [
    "ec2-13-209-193-43.ap-northeast-2.compute.amazonaws.com",
    "localhost",
    "127.0.0.1",
    "mydomain.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://ec2-13-209-193-43.ap-northeast-2.compute.amazonaws.com",
    "localhost",
    "127.0.0.1",
    "https://frontend-mu-ruby.vercel.app",
    "http://mydomain.com",
    "http://localhost:5173",
]

CORS_ALLOWED_ORIGINS=['http://localhost:5173']
CORS_ALLOW_METHODS = (
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
)

CORS_ALLOW_CREDENTIALS = True
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
