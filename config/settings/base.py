import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from rest_framework.settings import api_settings


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env_file = os.getenv("ENV_FILE", ".env.dev")
load_dotenv(BASE_DIR / env_file)

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

#s3서비스
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_UPLOAD_BUCKET="oz-main-pill-imgs"
AWS_S3_UPLOAD_REGION="ap-northeast-2"
AWS_S3_UPLOAD_BASE_URL="https://oz-main-pill-imgs.s3.ap-northeast-2.amazon.com"

# Email서비스
AUTH_USER_MODEL = "users.User"
# sendgrid
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('WELCOME_EMAIL_SENDER')

# 소셜로그인 서비스
# Google OAuth Credentials
GOOGLE_AUTH_URL = os.getenv("GOOGLE_AUTH_URL")
GOOGLE_AUTH_RESPONSE_TYPE = "code"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_TOKEN_URL = os.getenv("GOOGLE_TOKEN_URL")
GOOGLE_USERINFO_URL = os.getenv("GOOGLE_USERINFO_URL")
# Kakao OAuth
KAKAO_AUTH_URL = os.getenv("KAKAO_AUTH_URL")
KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")
KAKAO_TOKEN_URL = os.getenv("KAKAO_TOKEN_URL")
KAKAO_USERINFO_URL = os.getenv("KAKAO_USERINFO_URL")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "apps.users.validators.CustomPasswordValidator"},
]

# 공공데이터 URL
MFDS_BASE_URL = (
    "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
)
MFDS_API_KEY = os.getenv("MFDS_API_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",  # admin
    "django.contrib.auth",  # 사용자 인증
    "django.contrib.contenttypes",  # 모델 타입 관련
    "django.contrib.sessions",  # 세션
    "django.contrib.messages",  # 메시지 프레임워크
    "django.contrib.staticfiles",  # static 파일 처리
    "corsheaders",
    # DRF
    "rest_framework_simplejwt.token_blacklist",
    # 프로젝트 앱
    "apps.users",
    "apps.pills",
    "apps.bookmarks",
    "apps.pills.search_histories",
    "apps.pills.search_uploads",
    #'apps.me'
]

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Team5 Backend API",
    "DESCRIPTION": "북마크, 마이페이지, 이미지 업로드 등 주요 엔드포인트 문서",
    "VERSION": "1.0.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATIC_URL = "/static/"
