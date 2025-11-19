#!/usr/bin/env bash
set -e

PROJECT_DIR="/home/ubuntu/backend"
PIDFILE="$PROJECT_DIR/run/gunicorn.pid"

mkdir -p "$PROJECT_DIR/run"

cd "$PROJECT_DIR"

# 가상환경 활성화
source .venv/bin/activate

export ENV_FILE="envs/.env.prod"

# 1) 기존 백엔드 gunicorn만 종료
if [ -f "$PIDFILE" ]; then
  OLD_PID=$(cat "$PIDFILE" || echo "")

  if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "Killing old gunicorn (pid=$OLD_PID)"
    kill "$OLD_PID"
    # 필요하면 조금 대기
    sleep 2
  fi
fi

# 2) 새 백엔드 gunicorn 실행 (PID 파일 지정)
gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3 \
  --log-level info \
  --pid "$PIDFILE" \
  --daemon
