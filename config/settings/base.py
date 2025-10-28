import os
import datetime
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_FILE = os.getenv("ENV_FILE", ".env.dev")
load_dotenv(BASE_DIR / ENV_FILE)

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

AUTH_USER_MODEL = 'users.User'
# 개발용 임시
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@example.com'
"""
#실 운영용
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = '앱 비밀번호 또는 SMTP 비번'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
"""

INSTALLED_APPS = [
    'django.contrib.admin',          # admin
    'django.contrib.auth',           # 사용자 인증
    'django.contrib.contenttypes',   # 모델 타입 관련
    'django.contrib.sessions',       # 세션
    'django.contrib.messages',       # 메시지 프레임워크
    'django.contrib.staticfiles',    # static 파일 처리

    # 프로젝트 앱
    'apps.users',
    #'apps.pills',
    #'apps.me',
]

#third party app

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

#JWT토큰발급,갱신,폐기
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_LIFETIME = datetime.timedelta(minutes=15)# 액세스 토큰 유효기간
JWT_REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=7)# 리프레시 토큰 유효기간
JWT_AUTH_HEADER = "Authorization"
JWT_PREFIX = "Bearer"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"

# 공통 DB 설정 (각 환경에서 덮어쓰기 가능)
DATABASES = {}

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"