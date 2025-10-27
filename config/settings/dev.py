from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# 개발용 DB (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev.sqlite3',
    }
}