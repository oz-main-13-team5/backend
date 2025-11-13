from .base import *

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ROOT_URLCONF = "config.urls"

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "내 프로젝트 API",
    "DESCRIPTION": "내 서비스 API 문서",
    "VERSION": "1.0.0",
}