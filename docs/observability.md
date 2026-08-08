# TalentForge Observability

TalentForge includes an observability foundation designed to make the backend easier to monitor, diagnose, and operate.

The current system focuses on three areas:

```text
                    Observability
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           Logs        Metrics     Health
             │           │           │
             ▼           ▼           ▼
         Application  Prometheus   Health
           Logs           │         Checks
                          ▼
                       Grafana
```

The goal is to provide visibility into application behavior without coupling observability concerns to business logic.

---

# 1. Monitoring vs Observability

Monitoring focuses on detecting known problems through measurable signals.

Examples include:

```text
Request count
Request latency
HTTP error rate
Application health
Background task activity
```

Observability focuses on understanding why a system behaves the way it does.

TalentForge currently establishes observability through:

* Structured application logging
* Application metrics
* Prometheus
* Grafana
* Health endpoints
* Middleware-based instrumentation

More advanced capabilities such as distributed tracing can be introduced as the system evolves.

---

# 2. Observability Architecture

The current architecture is:

```text
                         TalentForge
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           Logging        Metrics        Health
              │              │              │
              ▼              ▼              ▼
         Application      Prometheus    Health Routes
            Logs              │
                              ▼
                           Grafana
```

The application itself remains responsible for producing logs and metrics.

Prometheus collects metrics, while Grafana provides visualization.

---

# 3. Application Logging

TalentForge uses a dedicated logging system rather than relying entirely on ad-hoc print statements.

The logging components include:

```text
utils/logger.py
middleware/logging_middleware.py
```

Request logging is handled through middleware so that HTTP activity can be observed consistently across the application.

A typical request lifecycle can therefore produce information such as:

```text
Request received
      ↓
Route processing
      ↓
Service execution
      ↓
Database / external operation
      ↓
Response generated
```

Application logs are particularly useful for diagnosing failures that cannot be understood from metrics alone.

For example:

```text
INFO  Resume processing started
INFO  Resume processing completed
ERROR AI provider request failed
ERROR Database operation failed
```

---

# 4. Metrics

TalentForge exposes application metrics through its metrics subsystem.

The relevant components include:

```text
metrics/
├── __init__.py
└── metrics.py

middleware/
└── metrics_middleware.py
```

Metrics provide numerical information about application behavior over time.

Examples of useful application metrics include:

```text
Request count
Request latency
HTTP status codes
Error rates
Endpoint activity
```

Metrics are particularly useful for identifying trends.

For example:

```text
Normal traffic
      │
      ▼
Request volume increases
      │
      ▼
Latency increases
      │
      ▼
5xx errors increase
      │
      ▼
Potential production incident
```

---

# 5. Prometheus

Prometheus is used as the metrics collection and monitoring system.

The project contains a Prometheus configuration at:

```text
prometheus/prometheus.yml
```

The general flow is:

```text
TalentForge
     │
     │ metrics
     ▼
Prometheus
     │
     │ stored time-series data
     ▼
Grafana
```

Prometheus provides the time-series data required for monitoring application behavior.

---

# 6. Grafana

Grafana is used to visualize application metrics.

TalentForge contains a dashboard configuration under:

```text
infra/grafana/dashboards/
```

The dashboard can be used to visualize metrics collected by Prometheus.

A typical monitoring workflow is:

```text
Application
     │
     ▼
Metrics
     │
     ▼
Prometheus
     │
     ▼
Grafana Dashboard
```

This makes changes in application behavior easier to identify than inspecting raw metric values manually.

---

# 7. Health Checks

TalentForge exposes health endpoints for determining whether the API is operational.

The health routes are separated from normal business endpoints.

The live health endpoint is:

```text
GET /api/v1/health/live
```

Example:

```bash
curl http://localhost/api/v1/health/live
```

Expected response:

```json
{
  "status": "ok"
}
```

Health checks are useful for:

* Container health verification
* Deployment verification
* Reverse proxy checks
* Infrastructure monitoring
* Basic service availability checks

A health endpoint answers a different question from application metrics:

```text
Health Check
    ↓
"Is the service alive?"

Metrics
    ↓
"How is the service behaving?"
```

---

# 8. Request Observability

Request-level middleware provides visibility into API activity.

The general flow is:

```text
Incoming Request
       │
       ▼
Logging Middleware
       │
       ▼
Metrics Middleware
       │
       ▼
FastAPI Router
       │
       ▼
Service
       │
       ▼
Response
```

This allows cross-cutting observability concerns to remain outside individual route handlers.

The advantage is that new endpoints automatically participate in the application's monitoring infrastructure without requiring every route to implement its own logging and instrumentation.

---

# 9. Background Task Observability

TalentForge uses Celery for asynchronous processing.

Background work is particularly important to monitor because it does not execute inside the normal HTTP request lifecycle.

The resume-processing flow is:

```text
API
 │
 ▼
Celery Task
 │
 ▼
PDF Extraction
 │
 ▼
Resume Parsing
 │
 ▼
AI Analysis
 │
 ▼
Database Update
```

Failures in this pipeline can therefore occur independently from the API request that originally created the task.

Logging and application state are used to help identify processing failures.

Resume records also maintain processing states:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

This provides application-level visibility into the progress of asynchronous resume processing.

---

# 10. AI Provider Observability

AI operations can be significantly slower than ordinary database operations.

TalentForge therefore treats AI processing as an important operational boundary.

A typical AI request follows:

```text
Application Service
       │
       ▼
AI Service
       │
       ▼
Provider Factory
       │
       ▼
Ollama Provider
       │
       ▼
Ollama
```

The current active AI backend is Ollama.

Observability around this boundary is useful for identifying issues such as:

```text
Slow model responses
Provider failures
Timeouts
Retry activity
Resume processing failures
```

Celery retry behavior also helps prevent temporary AI provider failures from immediately terminating background processing.

---

# 11. Diagnosing a Production Problem

Observability becomes most valuable when something goes wrong.

For example, suppose resume processing starts taking significantly longer.

A possible investigation flow is:

```text
                Problem
                   │
                   ▼
          Resume processing slow
                   │
                   ▼
               Metrics
                   │
                   ▼
          Request/task activity
                   │
                   ▼
                Logs
                   │
                   ▼
        AI provider is slow
                   │
                   ▼
                Ollama
                   │
                   ▼
        Model response latency
```

The combination of metrics and logs provides more useful information than either system alone.

---

# 12. Monitoring Production Health

A basic production monitoring workflow can be:

```text
1. Check service health
        │
        ▼
2. Check application metrics
        │
        ▼
3. Check Grafana dashboards
        │
        ▼
4. Inspect application logs
        │
        ▼
5. Identify failing component
        │
        ▼
6. Investigate root cause
```

Useful signals include:

```text
API availability
HTTP error rate
Request latency
Request volume
Background task failures
Resume processing failures
AI provider failures
```

---

# 13. Current Observability Stack

The current TalentForge observability stack consists of:

| Component           | Responsibility                     |
| ------------------- | ---------------------------------- |
| Application Logging | Application and request events     |
| Logging Middleware  | HTTP request visibility            |
| Metrics Middleware  | Request-level instrumentation      |
| Prometheus          | Metrics collection and storage     |
| Grafana             | Metrics visualization              |
| Health Endpoints    | Service availability checks        |
| Celery Status       | Background processing state        |
| Resume Status       | Application-level processing state |

---

# 14. What Is Not Currently Implemented

TalentForge currently focuses on a practical observability foundation rather than implementing every observability technology.

The project does **not currently require**:

* Distributed tracing
* OpenTelemetry
* Centralized log aggregation
* Loki
* Elasticsearch
* Automated incident management
* Advanced alert routing

These can be introduced later if the system requires them.

The architecture intentionally leaves room for these capabilities without requiring them for the current deployment.

---

# 15. Future Improvements

Potential future observability improvements include:

### Distributed Tracing

Introduce OpenTelemetry to trace requests across:

```text
Nginx
  ↓
FastAPI
  ↓
PostgreSQL
  ↓
Redis
  ↓
Celery
  ↓
Ollama
```

### Centralized Logging

Move application logs into a centralized logging system so that logs can be searched across multiple containers.

### Alerting

Introduce alerts for conditions such as:

```text
High 5xx rate
High request latency
Celery task failures
Database availability problems
Redis failures
AI provider failures
```

### Advanced Dashboards

Expand Grafana dashboards with operational views covering:

```text
API performance
Database activity
Redis activity
Celery processing
AI latency
Error rates
```

These improvements would become increasingly valuable as TalentForge moves toward a larger multi-instance deployment.

---

# 16. Observability Principle

The main principle behind TalentForge's observability architecture is:

> **The application should be observable without making business logic responsible for observability.**

Logging, metrics, and health checks are therefore implemented through dedicated infrastructure, middleware, and supporting modules.

The architecture keeps operational visibility separate from the application's core business workflows while still providing the information required to understand system behavior.

---

# 17. Summary

TalentForge currently provides a practical observability foundation:

```text
                TalentForge
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
      Logs       Metrics      Health
        │           │           │
        │           ▼           │
        │       Prometheus       │
        │           │           │
        │           ▼           │
        │        Grafana         │
        │                       │
        └───────────┬───────────┘
                    ▼
             System Visibility
```

This provides the foundation required to monitor application behavior today while leaving room for more advanced tracing, logging aggregation, and alerting as the platform evolves.