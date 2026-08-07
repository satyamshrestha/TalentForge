# TalentForge Deployment Guide

This guide explains how to deploy **TalentForge** using Docker Compose in a production-style environment.

---

# Production Architecture

TalentForge production deployment consists of the following services:

```text
                         Nginx
                           │
                           ▼
                      FastAPI API
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     PostgreSQL          Redis        Celery Worker
          │                │                │
          ▼                ▼                ▼
      Database          Cache        Background Jobs
```

Monitoring stack:

```text
                    FastAPI Application
                            │
                            ▼
                      Prometheus
                            │
                            ▼
                         Grafana
```

---

# Prerequisites

Install the following:

- Docker Engine
- Docker Compose
- Git

Required production files:

```text
.env.prod
docker-compose.prod.yml
```

---

# Environment Configuration

Create the production environment file:

```bash
cp .env.example .env.prod
```

Configure required environment variables:

```env
SECRET_KEY=

DATABASE_URL=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

REDIS_URL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

LLM_PROVIDER=ollama
LLM_MODEL=
OLLAMA_BASE_URL=
```

> Never commit production secrets to version control.

---

# Pull Latest Image

TalentForge uses Docker images for deployment.

Pull the latest image:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  pull
```

---

# Start Production Services

Start all production containers:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  up -d
```

The deployment starts:

| Service | Purpose |
|---|---|
| API | FastAPI application |
| PostgreSQL | Primary database |
| Redis | Cache and Celery broker |
| Celery Worker | Background processing |
| Nginx | Reverse proxy |
| Prometheus | Metrics collection |
| Grafana | Monitoring dashboards |

---

# Database Migration

Apply the latest database migrations:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  exec api alembic upgrade head
```

---

# Verify Deployment

Check running containers:

```bash
docker ps
```

Expected services should be running successfully.

---

# Health Check

Verify that the API is responding:

```bash
curl http://localhost/api/v1/health/live
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# Monitoring

Available monitoring services:

| Service | Address |
|---|---|
| API | http://localhost |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

# Viewing Logs

View logs from all services:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f
```

View logs from a specific service:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f api
```

Example:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f celery_worker
```

---

# Updating Deployment

Pull the newest image:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  pull
```

Restart services:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  up -d
```

Apply new migrations:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  exec api alembic upgrade head
```

---

# Deployment Script

TalentForge includes an automated deployment script:

```bash
./scripts/deploy.sh
```

The script automates the deployment workflow.

---

# Stopping Services

Stop production containers:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  down
```

---

# Production Checklist

Before exposing TalentForge publicly:

- [ ] Use strong production secrets
- [ ] Configure HTTPS
- [ ] Restrict database access
- [ ] Configure database backups
- [ ] Monitor application metrics
- [ ] Rotate credentials regularly
- [ ] Review container security
- [ ] Configure proper logging

---

# Future Improvements

Potential production improvements:

- Kubernetes deployment
- Horizontal scaling
- Automated database backups
- Cloud object storage for resume files
- Managed PostgreSQL deployment
- Advanced observability stack