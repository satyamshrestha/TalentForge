# TalentForge Observability

TalentForge includes an observability foundation designed to make the backend easier to monitor, diagnose, and operate.

The current system focuses on four areas:

```text
                    Observability
                         │
             ┌───────────┼───────────┬──────────────┐
             ▼           ▼           ▼              ▼
           Logs        Metrics      Health       WebSockets
             │           │           │              │
             ▼           ▼           ▼              ▼
        Application   Prometheus   Health       Connection
           Logs           │         Checks        Events
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

WebSocket failures
```

Observability focuses on understanding why a system behaves the way it does.

TalentForge currently establishes observability through:

* Application logging
* Request logging middleware
* Application metrics
* Prometheus
* Grafana
* Health endpoints
* Middleware-based instrumentation
* Background task state tracking
* WebSocket lifecycle and error logging

More advanced capabilities such as distributed tracing and centralized log aggregation can be introduced as the system evolves.

---

# 2. Observability Architecture

The current architecture is:

```text
                         TalentForge
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           Logging         Metrics        Health
              │              │              │
              ▼              ▼              ▼
        Application       Prometheus   Health Routes
           Logs              │
                             ▼
                          Grafana
```

Real-time WebSocket activity forms an additional observability boundary:

```text
Client
  │
  ▼
WebSocket Endpoint
  │
  ├── Authentication
  │
  ├── Authorization
  │
  ├── Connection Lifecycle
  │
  ├── Message Validation
  │
  ├── Answer Submission
  │
  └── Error Handling
          │
          ▼
     Application Logs
```

The application itself remains responsible for producing logs and metrics.

Prometheus collects metrics, while Grafana provides visualization.

WebSocket-specific operational events are handled through the application's logging and event infrastructure.

---

# 3. Application Logging

TalentForge uses a dedicated logging system rather than relying entirely on ad-hoc print statements.

The logging components include:

```text
utils/logger.py

middleware/logging_middleware.py
```

Request logging is handled through middleware so that HTTP activity can be observed consistently across the application.

WebSocket components also use application logging for operational failures.

A typical HTTP request lifecycle can therefore produce information such as:

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

A typical WebSocket lifecycle can produce information such as:

```text
Connection attempt

      ↓

Authentication

      ↓

Authorization

      ↓

Connection established

      ↓

Message received

      ↓

Answer processing

      ↓

Evaluation

      ↓

Event broadcast

      ↓

Connection closed
```

Application logs are particularly useful for diagnosing failures that cannot be understood from metrics alone.

For example:

```text
INFO  Resume processing started

INFO  Resume processing completed

ERROR AI provider request failed

ERROR Database operation failed

ERROR WebSocket answer submission failed

ERROR Unexpected WebSocket error
```

---

# 4. Logging Principles

Production logging should provide enough information to diagnose failures without exposing sensitive application data.

TalentForge should therefore follow these principles:

### Do Not Log Secrets

Sensitive values must never be written to application logs.

Examples include:

```text
JWT tokens

OAuth client secrets

Database passwords

Redis credentials

API keys

Production environment variables
```

### Avoid Logging Sensitive User Content

Resume contents, authentication credentials, and complete interview answers should not be logged unnecessarily.

For example, application logs should prefer:

```text
answer_id
question_id
interview_id
user_id
```

over logging the complete answer text.

### Use Appropriate Log Levels

Use log levels according to operational importance:

```text
DEBUG
    Detailed development information

INFO
    Normal application lifecycle events

WARNING
    Unexpected but recoverable conditions

ERROR
    Operation failed

EXCEPTION
    Unexpected failure requiring investigation
```

### Preserve Context

Operational logs should contain enough identifiers to connect related events.

Useful identifiers include:

```text
user_id

interview_id

question_id

answer_id

task_id
```

This is especially important when debugging asynchronous processing and WebSocket interactions.

---

# 5. Metrics

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

# 6. Metric Cardinality

Production metrics should avoid creating an excessive number of unique time-series labels.

Identifiers such as:

```text
user_id

interview_id

question_id

answer_id
```

should generally not be used as high-cardinality Prometheus labels.

Instead, metrics should prefer bounded dimensions such as:

```text
HTTP method

Route

Status code

Operation type

Service component
```

For example:

```text
Good:

request_count{method="POST",route="/interviews",status="201"}

Risky:

request_count{user_id="...",interview_id="...",question_id="..."}
```

High-cardinality metrics can increase memory usage and reduce monitoring-system performance.

Detailed identifiers belong in logs rather than metric labels.

---

# 7. Prometheus

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

Metrics should remain focused on operational measurements rather than application-specific user data.

---

# 8. Grafana

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

Useful dashboard categories include:

```text
Request volume

Request latency

HTTP error rates

Application availability

Background processing activity

WebSocket activity
```

---

# 9. Health Checks

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

A liveness check should remain lightweight and should not perform expensive database or AI operations unless a separate readiness check is explicitly introduced.

---

# 10. Request Observability

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

# 11. WebSocket Observability

TalentForge includes a WebSocket-based interview communication layer.

The WebSocket endpoint provides real-time interview interaction:

```text
Client

   │

   ▼

WebSocket

   │

   ▼

Authentication

   │

   ▼

Interview Authorization

   │

   ▼

Message Validation

   │

   ▼

Answer Service

   │

   ▼

AI Evaluation

   │

   ▼

WebSocket Events
```

The WebSocket implementation uses application logging to record operational failures.

Important events include:

```text
Connection accepted

Authentication failure

Authorization failure

Invalid message

Invalid question

Answer submission failure

Unexpected WebSocket error

Client disconnect
```

The WebSocket event system also defines application-level events such as:

```text
interview.started

question.available

answer.submitted

answer.evaluated

interview.completed

error
```

These events are part of the application's real-time communication layer and should remain distinguishable from infrastructure-level logs.

---

# 12. WebSocket Failure Observability

WebSocket failures should be observable without logging sensitive message contents.

For example, an answer submission failure can be associated with:

```text
interview_id

question_id

user_id
```

rather than logging the complete submitted answer.

The current WebSocket logging pattern records failures such as:

```text
WebSocket answer submission failed

Unexpected WebSocket error
```

along with relevant identifiers.

This provides enough context to investigate failures while reducing unnecessary exposure of user-generated content.

---

# 13. WebSocket Connection Lifecycle

A production WebSocket system should make connection lifecycle behavior observable.

The important lifecycle states are:

```text
CONNECTING

     ↓

AUTHENTICATING

     ↓

AUTHORIZED

     ↓

CONNECTED

     ↓

MESSAGE PROCESSING

     ↓

DISCONNECTED
```

Operationally useful measurements include:

```text
Active WebSocket connections

Connection attempts

Authentication failures

Authorization failures

Message validation failures

Answer submission failures

Unexpected disconnects

Connection duration
```

These measurements can be introduced as dedicated metrics as the real-time system grows.

The current implementation primarily provides lifecycle and failure visibility through application behavior and logging.

---

# 14. Background Task Observability

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

Future improvements can expose dedicated Celery metrics such as:

```text
Tasks submitted

Tasks completed

Tasks failed

Task duration

Retry count

Queue depth
```

---

# 15. AI Provider Observability

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

AI observability should focus on operational metadata such as:

```text
Provider

Operation type

Latency

Success/failure

Retry count
```

rather than logging complete prompts, resumes, or candidate answers.

---

# 16. Database and Redis Observability

PostgreSQL and Redis are critical infrastructure dependencies.

Application-level observability should therefore distinguish between:

```text
Application failure

Database failure

Cache failure

AI provider failure

Background worker failure
```

For example:

```text
API request
    │
    ▼
Service
    │
    ├── PostgreSQL
    │
    ├── Redis
    │
    └── AI Provider
```

A production investigation should determine which dependency is responsible for the observed failure rather than treating every failure as an API problem.

Future infrastructure metrics can provide deeper visibility into:

```text
Database connection usage

Database latency

Slow queries

Redis availability

Redis latency

Cache hit rate

Celery queue depth
```

These capabilities can be added as the deployment becomes more distributed.

---

# 17. Diagnosing a Production Problem

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

For a WebSocket problem, the investigation could instead follow:

```text
                 Problem

                    │

                    ▼

          Interview connection fails

                    │

                    ▼

             WebSocket logs

                    │

          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Auth      Access     Validation
      Failure   Failure     Failure

                    │

                    ▼

             Identify root cause
```

The combination of metrics and logs provides more useful information than either system alone.

---

# 18. Monitoring Production Health

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

WebSocket connection failures
```

---

# 19. Observability During Deployments

Observability should also be used during deployments.

A deployment verification workflow can be:

```text
Deploy New Version

       │

       ▼

Check Container Status

       │

       ▼

Check Health Endpoint

       │

       ▼

Check Application Logs

       │

       ▼

Check Error Rate

       │

       ▼

Check Background Workers

       │

       ▼

Check WebSocket Behavior

       │

       ▼

Deployment Verified
```

This helps detect problems that may not be visible from container startup status alone.

A container being `running` does not necessarily mean the application is functioning correctly.

---

# 20. Observability Security

Observability systems themselves must be treated as production infrastructure.

Logs and monitoring interfaces can contain operational information that should not be publicly exposed.

Production deployments should therefore protect:

```text
Grafana

Prometheus

Application logs

Celery monitoring

Database metrics

Infrastructure dashboards
```

Monitoring interfaces should not be exposed publicly without appropriate authentication and network controls.

Production logs should also be retained according to operational requirements while avoiding unnecessary retention of sensitive user information.

---

# 21. Current Observability Stack

The current TalentForge observability stack consists of:

| Component           | Responsibility                                  |
| ------------------- | ----------------------------------------------- |
| Application Logging | Application and request events                  |
| Logging Middleware  | HTTP request visibility                         |
| Metrics Middleware  | Request-level instrumentation                   |
| Prometheus          | Metrics collection and storage                  |
| Grafana             | Metrics visualization                           |
| Health Endpoints    | Service availability checks                     |
| Celery Status       | Background processing state                     |
| Resume Status       | Application-level processing state              |
| WebSocket Logging   | Real-time connection and failure visibility     |
| WebSocket Events    | Application-level real-time event communication |

---

# 22. Current vs Future Observability

TalentForge intentionally distinguishes between capabilities that are implemented and capabilities that are planned.

### Currently Implemented

```text
Application logging

HTTP request logging

Application metrics

Prometheus

Grafana

Health endpoints

Celery processing state

Resume processing state

WebSocket error logging

WebSocket event infrastructure
```

### Future Enhancements

```text
Distributed tracing

OpenTelemetry

Centralized log aggregation

Loki

Elasticsearch

Dedicated WebSocket metrics

Celery queue metrics

Database performance metrics

Redis performance metrics

Advanced alerting

Automated incident management
```

This distinction prevents the project documentation from claiming operational capabilities that have not yet been implemented.

---

# 23. What Is Not Currently Implemented

TalentForge currently focuses on a practical observability foundation rather than implementing every observability technology.

The project does not currently require:

* Distributed tracing
* OpenTelemetry
* Centralized log aggregation
* Loki
* Elasticsearch
* Automated incident management
* Advanced alert routing
* Dedicated WebSocket Prometheus metrics
* Full distributed request tracing

These can be introduced later if the system requires them.

The architecture intentionally leaves room for these capabilities without requiring them for the current deployment.

---

# 24. Future Improvements

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

For WebSocket workloads, tracing can additionally cover:

```text
WebSocket Connection

       ↓

Authentication

       ↓

Message Processing

       ↓

Answer Service

       ↓

AI Evaluation
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

WebSocket failure spikes
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

WebSocket activity
```

### Correlation IDs

Introduce consistent correlation or request IDs across HTTP, background tasks, and real-time workflows.

A future distributed flow could therefore be traceable as:

```text
Request ID

   ↓

FastAPI Request

   ↓

Celery Task

   ↓

AI Operation

   ↓

Database Update
```

This becomes increasingly valuable when multiple services and workers are running simultaneously.

---

# 25. Observability Principle

The main principle behind TalentForge's observability architecture is:

> **The application should be observable without making business logic responsible for observability.**

Logging, metrics, and health checks are therefore implemented through dedicated infrastructure, middleware, and supporting modules.

The architecture keeps operational visibility separate from the application's core business workflows while still providing the information required to understand system behavior.

A second important principle is:

> **Operational identifiers belong in logs, while bounded dimensions belong in metrics.**

This prevents monitoring systems from becoming overloaded with high-cardinality application data while preserving detailed information for debugging.

---

# 26. Summary

TalentForge currently provides a practical observability foundation:

```text
                         TalentForge

                             │

        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
      Logs                Metrics              Health
        │                    │                    │
        │                    ▼                    │
        │                Prometheus              │
        │                    │                    │
        │                    ▼                    │
        │                 Grafana                │
        │                                         │
        └────────────────────┬────────────────────┘
                             │
                             ▼
                       System Visibility
                             │
                             ▼
                       WebSocket Layer
                             │
                             ▼
                  Real-Time Operational Signals
```

The current foundation provides visibility into:

```text
HTTP requests

Application errors

Application metrics

Service health

Background processing

AI operations

WebSocket failures

Real-time application events
```

This provides the foundation required to monitor application behavior today while leaving room for more advanced tracing, logging aggregation, alerting, infrastructure metrics, and distributed observability as TalentForge evolves.