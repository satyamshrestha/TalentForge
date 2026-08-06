# TalentForge Deployment Guide

## Prerequisites

- Docker Engine
- Docker Compose
- Git
- A configured `.env.prod` file

---

## Environment Configuration

Create a production environment file from the provided template.

```bash
cp .env.prod.example .env.prod
```

Fill in all required environment variables before deployment.

---

## Pull Latest Image

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  pull
```

---

## Start Production Services

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  up -d
```

---

## Verify Running Containers

```bash
docker ps
```

---

## Verify API

```bash
curl http://localhost/
```

Health endpoint:

```bash
curl http://localhost/api/v1/health/live
```

---

## Access Monitoring

| Service | URL |
|---------|-----|
| API | http://localhost |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

## View Logs

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f
```

---

## Stop Services

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  down
```

---

## Deploy Latest Version

```bash
./scripts/deploy.sh
```