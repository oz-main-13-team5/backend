# -----------------------
#  Base image
# -----------------------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# -----------------------
#  Dependencies
# -----------------------
FROM base AS builder

# 환경 선택: dev 또는 prod (기본값: dev)
ARG ENV=dev

# requirements 복사
COPY requirements/$ENV requirements/$ENV

# pyproject.toml과 uv.lock 복사
COPY pyproject.toml uv.lock ./

# uv 설치
RUN pip install uv && uv pip install --system .

# requirements 설치
RUN pip install --no-cache-dir -r requirements/$ENV

# PostgreSQL 드라이버 설치
RUN pip install --no-cache-dir psycopg[binary]

# dotenv 설치
RUN pip install --no-cache-dir python-dotenv

# -----------------------
#  Runtime
# -----------------------
FROM base AS runtime

COPY --from=builder /usr/local /usr/local
COPY . /app

# 환경 변수 기본값
ARG ENV=dev
ENV DJANGO_SETTINGS_MODULE=config.settings.${ENV}

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
