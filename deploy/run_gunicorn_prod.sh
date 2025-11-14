#!/usr/bin/env bash
set -e

PROJECT_DIR="/home/ubuntu/backend"
cd "$PROJECT_DIR"

# 가상환경 활성화
source .venv/bin/activate

# prod 환경 변수 파일 지정
export ENV_FILE="envs/.env.prod"

# 워커 수 3 - 임의 지정상태
exec gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3
