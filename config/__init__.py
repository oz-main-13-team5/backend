# 환경 변수를 읽어 적절한 설정을 import
import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "dev")

if ENVIRONMENT == "prod":
    from .settings.prod import *
else:
    from .settings.dev import *
