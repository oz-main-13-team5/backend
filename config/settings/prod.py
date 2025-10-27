from .base import *
import os
import dj_database_url

DEBUG = os.getenv("DEBUG") == "True"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# 프로덕션 DB (환경변수 DATABASE_URL)
DATABASES = {
    "default": dj_database_url.parse(os.getenv("DATABASE_URL"))
}

# INSTALLED_APPS는 base.py에서 상속 (덮어쓰지 않음)
