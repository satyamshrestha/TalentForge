#!/bin/bash

set -e

echo "Pulling latest Docker images..."
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  pull

echo "Starting updated containers..."
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  up -d

echo "Removing unused Docker images..."
docker image prune -f

echo "Deployment completed successfully."