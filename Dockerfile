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

ARG ENV=prod
ENV ENV=$ENV

# requirements 복사
COPY requirements/$ENV/ requirements/$ENV/

# pyproject.toml과 uv.lock 복사
COPY pyproject.toml uv.lock ./

# uv 설치 및 의존성 설치
RUN pip install uv && uv pip install --system .
RUN pip install --no-cache-dir -r requirements/$ENV/requirements.txt
RUN pip install --no-cache-dir psycopg[binary]
RUN pip install --no-cache-dir python-dotenv

# -----------------------
#  Runtime
# -----------------------
FROM base AS runtime

COPY --from=builder /usr/local /usr/local
COPY . .

ARG ENV=dev
ENV DJANGO_SETTINGS_MODULE=config.settings.${ENV}

EXPOSE 8000

# dev/prod 자동 실행 분기
CMD ["sh", "-c", "if [ \"$ENV\" = 'prod' ]; then gunicorn config.wsgi:application --bind 0.0.0.0:8000; else python manage.py runserver 0.0.0.0:8000; fi"]
