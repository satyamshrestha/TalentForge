# TalentForge Deployment Guide

## Requirements

- Docker
- Docker Compose
- Git

## Environment Variables

Create a `.env.prod` file based on `.env.example`.

## Pull Latest Image

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  pull
```

## Start Services

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  up -d
```

## Verify Containers

```bash
docker ps
```

## Check API

```bash
curl http://localhost/
```

## View Logs

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f
```

## Stop Services

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  down
```

## Update Deployment

```bash
./scripts/deploy.sh
```