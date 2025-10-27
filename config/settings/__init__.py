import os
from pathlib import Path
from dotenv import load_dotenv

# 환경 선택: dev(default) / prod
env = os.getenv("DJANGO_SETTINGS_MODULE_ENV", "dev")

# .env 파일 로드
BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / f".env.{env}"
load_dotenv(dotenv_path)

# 환경별 settings import
if env == "prod":
    from .prod import *
else:
    from .dev import *
