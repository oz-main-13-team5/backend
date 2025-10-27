from .base import *
import os

DEBUG = True
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
ALLOWED_HOSTS = ["*"]  # 개발용

# 개발용 DB: 기본 SQLite 사용
# DATABASES = same as base.py (필요시 override 가능)
