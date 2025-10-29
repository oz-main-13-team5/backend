#!/bin/bash
# Usage: ./scripts/docker-up.sh [local|prod]
ENV=${1:-local}

if [ "$ENV" = "prod" ]; then
  export ENV_FILE=".env.prod"
else
  export ENV_FILE=".env.local"
fi

echo "🚀 Starting Docker with $ENV_FILE"
docker-compose up --build
