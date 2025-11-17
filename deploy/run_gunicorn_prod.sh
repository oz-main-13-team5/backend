#!/usr/bin/env bash
set -e

PROJECT_DIR="/home/ubuntu/backend"
cd "$PROJECT_DIR"

# 가상환경 활성화
source .venv/bin/activate

# prod 환경 변수 파일 지정
export ENV_FILE="envs/.env.prod"

# 백그라운드(데몬) 실행, 로그 파일 저장 안 함
gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3 \
  --log-level info \
  --daemon
