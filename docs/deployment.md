# TalentForge Deployment Guide

This guide explains how to deploy **TalentForge** using Docker Compose in a production-style environment.

---

# Production Architecture

TalentForge production deployment consists of the following services:

```text
                         Nginx
                           │
                           ▼
                    FastAPI Application
                      │            │
                      │            └──── WebSocket
                      │                   Connections
          ┌───────────┼───────────────┐
          ▼           ▼               ▼
     PostgreSQL     Redis        Celery Worker
          │           │               │
          ▼           ▼               ▼
       Database      Cache       Background Jobs
```

Nginx acts as the public reverse proxy and routes HTTP API traffic and WebSocket connections to the FastAPI application.

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

* Docker Engine
* Docker Compose
* Git

Required production files:

```text
.env.prod
docker-compose.prod.yml
```

Before deployment, ensure the production Docker configuration and required environment variables have been reviewed.

---

# Environment Configuration

Create the production environment file:

```bash
cp .env.example .env.prod
```

Configure the required environment variables:

```env
ENVIRONMENT=production

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

> **Never commit production secrets to version control.**

Production credentials should be strong, unique, and stored securely.

The `ENVIRONMENT=production` setting enables production-specific application behavior, including API documentation hardening.

---

# API Documentation Exposure

TalentForge uses environment-aware API documentation behavior.

When the application runs with:

```env
ENVIRONMENT=production
```

the following FastAPI documentation endpoints are disabled:

```text
/docs
/redoc
/openapi.json
```

This prevents the interactive Swagger UI, ReDoc interface, and generated OpenAPI schema from being exposed through the production application.

Development and testing environments retain API documentation to support local development and API testing.

For example, the development Swagger UI is available at:

```text
http://localhost:8000/docs
```

API documentation exposure should therefore be verified as part of production deployment validation.

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

Before starting the new version, verify that the expected image was pulled successfully.

---

# Start Production Services

Start the production containers:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  up -d
```

The deployment starts:

| Service       | Purpose                             |
| ------------- | ----------------------------------- |
| API           | FastAPI application                 |
| PostgreSQL    | Primary database                    |
| Redis         | Cache and Celery broker             |
| Celery Worker | Background processing               |
| Nginx         | Reverse proxy and WebSocket gateway |
| Prometheus    | Metrics collection                  |
| Grafana       | Monitoring dashboards               |

---

# Database Migration

Apply the latest database migrations:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  exec api alembic upgrade head
```

Database migrations should be applied only after the required application image is running and the database connection is available.

Always review migration changes before applying them to production.

---

# Verify Deployment

Check running containers:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  ps
```

Verify that the expected services are running and that containers are not repeatedly restarting.

For additional inspection:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  ps -a
```

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

A successful health response confirms that the application is reachable through the configured reverse proxy.

---

# WebSocket Verification

TalentForge uses WebSockets for real-time interview communication.

The production WebSocket endpoint follows this structure:

```text
wss://<domain>/ws/interview/{interview_id}?token=<jwt>
```

For local or non-TLS environments:

```text
ws://localhost/ws/interview/{interview_id}?token=<jwt>
```

Production deployments should use **WSS (`wss://`) behind HTTPS**.

WebSocket connections require:

1. A valid JWT.
2. Access to the requested interview.
3. A valid interview identifier.
4. A valid WebSocket message format when submitting answers.

The WebSocket connection should be verified after deployment to ensure that Nginx correctly forwards the WebSocket upgrade request to FastAPI.

The WebSocket path should remain consistent between Nginx, FastAPI, and the client application:

```text
/ws/interview/{interview_id}
```

---

# Monitoring

Available monitoring services:

| Service    | Address                 |
| ---------- | ----------------------- |
| API        | `http://localhost`      |
| Prometheus | `http://localhost:9090` |
| Grafana    | `http://localhost:3000` |

Prometheus should be checked after deployment to ensure that application metrics are being collected successfully.

Grafana should be checked to ensure that configured dashboards can retrieve the expected metrics.

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

Celery worker logs:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f celery_worker
```

For WebSocket-related issues, inspect both the Nginx and API logs:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs -f nginx api
```

Look for:

* failed WebSocket upgrades
* authentication failures
* unexpected disconnects
* application exceptions
* repeated container restarts
* database connection failures
* Redis connection failures

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

Verify the containers:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  ps
```

Apply new migrations when required:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  exec api alembic upgrade head
```

After an update, verify:

* API health
* API documentation exposure
* database connectivity
* Redis connectivity
* Celery worker status
* WebSocket connectivity
* Prometheus metrics
* application logs

---

# Deployment Script

TalentForge includes an automated deployment script:

```bash
./scripts/deploy.sh
```

The script automates the deployment workflow.

When using the script, review its behavior before executing it against a production environment.

---

# Stopping Services

Stop production containers:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  down
```

Stopping the stack terminates the running application containers.

Before stopping a production environment, confirm that active workloads and background jobs can safely be interrupted.

---

# Rollback

If a deployment introduces an application failure, revert to a previously known-good image version.

The rollback process should follow this general workflow:

```text
Identify Failure
      │
      ▼
Inspect Logs
      │
      ▼
Identify Known-Good Image
      │
      ▼
Deploy Previous Version
      │
      ▼
Verify Health
      │
      ▼
Verify WebSocket
      │
      ▼
Verify Background Workers
```

Avoid automatically rolling back database migrations without first reviewing whether the migration is backward-compatible.

Database rollback procedures should be treated separately from application image rollback.

---

# Production Checklist

Before exposing TalentForge publicly:

### Security

* [ ] Use strong production secrets
* [ ] Never commit `.env.prod`
* [ ] Configure HTTPS
* [ ] Use WSS for production WebSocket connections
* [ ] Restrict PostgreSQL access
* [ ] Restrict Redis access
* [ ] Review container permissions
* [ ] Review exposed ports
* [ ] Verify `/docs` is not publicly available
* [ ] Verify `/redoc` is not publicly available
* [ ] Verify `/openapi.json` is not publicly available
* [ ] Verify production API documentation exposure is disabled

### Application

* [ ] Set `ENVIRONMENT=production`
* [ ] Apply database migrations
* [ ] Verify API health endpoint
* [ ] Verify authentication
* [ ] Verify WebSocket authentication
* [ ] Verify WebSocket interview access control
* [ ] Verify answer submission
* [ ] Verify Celery workers

### Operations

* [ ] Configure database backups
* [ ] Monitor application metrics
* [ ] Configure proper logging
* [ ] Verify Prometheus collection
* [ ] Verify Grafana dashboards
* [ ] Test deployment rollback procedure
* [ ] Rotate credentials regularly

---

# Troubleshooting

## API Is Not Responding

Check the container status:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  ps
```

Then inspect API logs:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs --tail=200 api
```

---

## Database Connection Failure

Check PostgreSQL status:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  ps postgres
```

Then inspect PostgreSQL logs:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs --tail=200 postgres
```

Verify that `DATABASE_URL` and the PostgreSQL credentials are correctly configured.

---

## Redis or Celery Failure

Inspect Redis:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs --tail=200 redis
```

Inspect Celery:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs --tail=200 celery_worker
```

Verify that the configured `REDIS_URL` is reachable from the application and Celery worker.

---

## WebSocket Connection Failure

Check both Nginx and FastAPI logs:

```bash
docker compose \
  --env-file .env.prod \
  -f docker-compose.prod.yml \
  logs --tail=200 nginx api
```

Verify:

* the client is using the correct WebSocket URL
* production uses `wss://` when HTTPS is enabled
* the `/ws/` path is forwarded by Nginx
* the JWT is supplied correctly
* the JWT is valid
* the user has access to the interview
* the FastAPI application is running
* Nginx supports WebSocket upgrade forwarding

A WebSocket failure should be investigated across the complete path:

```text
Client
  │
  ▼
HTTPS / WSS
  │
  ▼
Nginx
  │
  ▼
FastAPI WebSocket Router
  │
  ▼
Authentication
  │
  ▼
Interview Access
```

---

## API Documentation Is Unexpectedly Available

If API documentation is accessible in production, first verify that the application is actually running with:

```env
ENVIRONMENT=production
```

Then verify the production container environment and deployment configuration.

The following endpoints should not be available when production mode is active:

```text
/docs
/redoc
/openapi.json
```

If the endpoints remain accessible, inspect the running application configuration before considering the deployment successful.