#!/bin/bash
# Usage: ./scripts/docker-up.sh [dev|prod]
ENV_TARGET=${1:-dev}

if [ "$ENV_TARGET" = "prod" ]; then
  export ENV_FILE="envs/.env.prod"
  export ENV="prod"
else
  export ENV_FILE="envs/.env.dev"
  export ENV="dev"
fi

echo "🚀 Starting Docker with $ENV_FILE (ENV=$ENV)"
docker-compose up --build
