FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock /app/

ENV PATH="/root/.local/bin:${PATH}"

RUN pip install --no-cache-dir pipx \
    && pipx install uv \
    && uv pip install --system -r pyproject.toml

COPY . /app

ENV ENV_FILE=.env.prod

RUN python manage.py collectstatic --noinput || true

CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
