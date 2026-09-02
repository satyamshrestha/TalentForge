# TalentForge Architecture


TalentForge is designed as a production-style backend system with clear separation between API handling, business logic, data access, asynchronous processing, AI services, real-time communication, and infrastructure.


The architecture is designed to keep individual responsibilities isolated while allowing the system to evolve without tightly coupling the application to a specific database, task queue, AI provider, or communication protocol.


---


# 1. High-Level Architecture


```text
                         Client
                           │
                           ▼
                    ┌─────────────┐
                    │    Nginx    │
                    │ Reverse Proxy│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    │ Application │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌─────────────┐           ┌─────────────┐
       │   Routers   │           │  WebSocket  │
       │  REST API   │           │   Layer     │
       └──────┬──────┘           └──────┬──────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                    ┌─────────────┐
                    │  Services   │
                    │Business Logic│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │Repositories │
                    │ Data Access │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ PostgreSQL  │
                    │  Database   │
                    └─────────────┘

Supporting infrastructure operates alongside the main application:

                         TalentForge
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
      Redis                Celery              AI Layer
     Caching           Background Tasks       Provider System
        │                     │                     │
        │                     ▼                     ▼
        │               Resume Pipeline          Ollama
        │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                         PostgreSQL

Real-time communication operates alongside the traditional REST API:

Client
  │
  ├────────────── HTTP ──────────────► REST API
  │                                      │
  │                                      ▼
  │                                   Services
  │
  └──────────── WebSocket ──────────► WebSocket Layer
                                         │
                                         ▼
                                      Services
                                         │
                                         ▼
                                    Application
                                     Events

This separation allows synchronous API requests and real-time communication to coexist without coupling WebSocket handling to individual REST endpoints.

2. Architectural Layers

TalentForge follows a layered architecture.

Routers
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
Database

Real-time communication follows a parallel application entry point:

WebSocket
   │
   ▼
WebSocket Layer
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
Database

Each layer has a specific responsibility.

Routers

Routers are responsible for HTTP-level concerns.

They handle:

Request parsing
Response serialization
Dependency injection
Authentication dependencies
Authorization dependencies
HTTP status codes
Calling application services

Routers should not contain substantial business logic.

Example:

POST /interviews
       │
       ▼
Interview Router
       │
       ▼
Interview Service
WebSocket Layer

The WebSocket layer handles persistent real-time connections between clients and the application.

It is responsible for:

Accepting WebSocket connections
Authenticating connections
Managing connection lifecycle
Receiving client messages
Sending real-time events
Disconnect handling
Connection management
Delegating application behavior to services

The WebSocket layer should not contain substantial business logic.

Example:

Client
  │
  │ WebSocket Connection
  ▼
WebSocket Endpoint
  │
  ▼
Connection Manager
  │
  ▼
Application Service
  │
  ▼
Business Logic

This keeps real-time transport concerns separate from the application's business rules.

Services

Services contain the application's business logic.

Examples include:

UserService
ResumeService
InterviewService
AnswerService
DashboardService
AuditLogService

Services are responsible for operations such as:

Validating business rules
Coordinating repositories
Managing application workflows
Calling AI services
Triggering background tasks
Managing cache invalidation
Recording audit events
Coordinating real-time application events

This keeps business logic independent from the HTTP and WebSocket transport layers.

Repositories

Repositories provide the database access layer.

Examples include:

UserRepository
ResumeRepository
InterviewRepository
QuestionRepository
AnswerRepository
AuditLogRepository
DashboardRepository

Repositories are responsible for:

Creating records
Retrieving records
Updating records
Deleting records
Querying PostgreSQL

The service layer therefore does not need to contain raw database operations throughout its business logic.

3. Request Flow

A typical synchronous API request follows this path:

Client
  │
  ▼
Nginx
  │
  ▼
FastAPI
  │
  ▼
Router
  │
  ▼
Service
  │
  ▼
Repository
  │
  ▼
PostgreSQL
  │
  ▼
Repository
  │
  ▼
Service
  │
  ▼
Router
  │
  ▼
Client

For example, retrieving a user's resumes:

GET /resumes
     │
     ▼
Resume Router
     │
     ▼
Resume Service
     │
     ▼
Resume Repository
     │
     ▼
PostgreSQL

Redis may intercept this flow when cached data is available.

4. Redis Cache Architecture

TalentForge uses Redis as a caching layer.

The application follows a cache-aside strategy.

                  Request
                     │
                     ▼
                   Redis
                  /     \
             Hit /       \ Miss
                /         \
               ▼           ▼
        Return Cache   PostgreSQL
                           │
                           ▼
                      Store Cache
                           │
                           ▼
                      Return Data

Resume retrieval uses cache keys based on the user:

user:{user_id}:resumes

The current cache TTL is:

300 seconds

Cache invalidation occurs when relevant resume data changes.

Examples:

Resume Upload
     │
     ▼
Database Update
     │
     ▼
Invalidate Resume Cache
Resume Delete
     │
     ▼
Database Delete
     │
     ▼
Invalidate Resume Cache

Redis is therefore used as a performance optimization rather than the source of truth.

PostgreSQL remains the authoritative persistent data store.

5. Celery Background Processing

Long-running operations are separated from the API request-response cycle.

Resume processing is handled asynchronously using Celery.

Client
  │
  ▼
Resume Upload
  │
  ▼
FastAPI
  │
  ├── Store Resume
  │
  ├── Create Resume Record
  │       status = PENDING
  │
  └── Dispatch Celery Task
              │
              ▼
        Celery Worker
              │
              ▼
       Extract PDF Text
              │
              ▼
        Parse Resume
              │
              ▼
        AI Analysis
              │
              ▼
       Update PostgreSQL
              │
              ▼
       status = COMPLETED

The API does not wait for the entire resume-processing pipeline to finish.

This prevents expensive processing from blocking normal API requests.

6. AI Architecture

AI functionality is separated from the application's core business logic.

The architecture is:

Application Service
       │
       ▼
   AI Service
       │
       ▼
Provider Factory
       │
       ▼
AI Provider
       │
       ▼
     Ollama
       │
       ▼
     LLM Model

Current AI services include:

ResumeAnalyzer
QuestionGenerator
AnswerEvaluator

These services are responsible for AI-specific workflows while the provider layer handles communication with the configured model backend.

7. AI Provider Abstraction

TalentForge does not tightly couple its business logic to Ollama.

Instead, AI services depend on the provider abstraction.

                 AI Service
                     │
                     ▼
              Provider Factory
                     │
                     ▼
               Base Provider
                     │
                     ▼
              Ollama Provider
                     │
                     ▼
                   Ollama

The currently active provider is:

Ollama

Ollama is used as the primary model backend for the current system.

The current AI provider implementation is Ollama, while the provider abstraction keeps AI services independent of the underlying model backend.

This architecture allows additional providers to be introduced without rewriting the business logic inside:

ResumeAnalyzer
QuestionGenerator
AnswerEvaluator
8. Resume Processing Architecture

Resume processing combines synchronous API operations, asynchronous tasks, parsing, and AI analysis.

                  PDF Upload
                      │
                      ▼
               File Validation
                      │
          ┌───────────┼───────────┐
          │           │           │
       Extension   MIME Type   File Size
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
                 Store File
                      │
                      ▼
               Create Resume
                PENDING
                      │
                      ▼
               Celery Task
                      │
                      ▼
                PROCESSING
                      │
                      ▼
                PDF Parsing
                      │
                      ▼
              Resume Parser
                      │
                      ▼
              Resume Analyzer
                      │
                      ▼
                    Ollama
                      │
                      ▼
             Structured Analysis
                      │
                      ▼
               PostgreSQL
                      │
                      ▼
                 COMPLETED

If processing fails, the resume is marked:

FAILED

and the associated error information is stored with the resume.

9. Interview Architecture

Interview creation is based on processed resume information.

Completed Resume
       │
       ▼
Interview Service
       │
       ▼
Question Generator
       │
       ▼
AI Provider
       │
       ▼
Generated Questions
       │
       ▼
Question Repository
       │
       ▼
Interview

The domain relationship is:

User
 │
 ├── Resume
 │
 └── Interview
       │
       └── Question
              │
              └── Answer

This allows interviews, questions, and answers to remain independently persisted while maintaining their relationships.

10. Answer Evaluation Architecture

Answer evaluation is performed through the AI service layer.

Question + Answer
       │
       ▼
Answer Service
       │
       ▼
Answer Evaluator
       │
       ▼
AI Provider
       │
       ▼
Ollama
       │
       ▼
Structured Evaluation
       │
       ▼
Answer Repository
       │
       ▼
PostgreSQL

The evaluation contains information such as:

Feedback
Score
Suggested Improvement

Business rules such as preventing a question from being answered multiple times remain inside the application service layer.

11. Authentication and Authorization

Authentication and authorization are separated into dedicated components.

Client
  │
  ▼
Authentication
  │
  ├── Password Authentication
  │
  ├── JWT
  │
  └── Google OAuth
  │
  ▼
Authenticated User
  │
  ▼
Authorization
  │
  ├── Role
  │
  └── OAuth2 Scopes
  │
  ▼
Protected Resource

TalentForge uses:

JWT access tokens
JWT refresh tokens
Password hashing
OAuth2 password flow
Google OAuth
Role-based access control
Scope-based authorization
Ownership validation

Authorization decisions can therefore consider both the user's role and their granted scopes.

WebSocket connections use the same authentication and authorization principles where applicable.

12. Database Architecture

PostgreSQL is the primary persistent data store.

The core domain model is:

User
 │
 ├───────────────┐
 │               │
 ▼               ▼
Resume         Interview
                  │
                  ▼
               Question
                  │
                  ▼
                Answer

Audit logging is associated with users and application entities:

User
 │
 └── AuditLog

SQLAlchemy is used as the ORM and Alembic manages database schema migrations.

13. Middleware Architecture

Cross-cutting application concerns are handled through middleware and dedicated utilities.

Current middleware responsibilities include:

Request
  │
  ▼
Logging Middleware
  │
  ▼
Metrics Middleware
  │
  ▼
Security Headers
  │
  ▼
Trusted Host
  │
  ▼
FastAPI Application

Other cross-cutting concerns include:

CORS
Rate limiting
Request logging
Security headers
Metrics collection
Trusted host validation

These concerns remain outside individual business services.

# 14. WebSocket Architecture

TalentForge supports WebSocket-based real-time communication for interactive interview workflows.

The WebSocket architecture is separated from the REST API layer while still using the same application services and persistence layer.

```text
Client
   │
   │ WebSocket
   ▼
Nginx
   │
   ▼
FastAPI
   │
   ▼
WebSocket Router
   │
   ├── Authentication
   │
   ├── Interview Authorization
   │
   ├── Message Validation
   │
   ▼
Connection Manager
   │
   ▼
Answer Service
   │
   ├── Answer Repository
   ├── AI Answer Evaluator
   ├── Interview Status
   └── Audit Log
   │
   ▼
PostgreSQL
```

The WebSocket layer is responsible for communication and connection lifecycle management. Business rules remain inside the application service layer.

## WebSocket Connection Lifecycle

```text
Client
   │
   ▼
WebSocket Connection
   │
   ▼
Authenticate JWT
   │
   ▼
Authorize Interview Access
   │
   ▼
Accept Connection
   │
   ▼
Register Connection
   │
   ▼
Receive Messages
   │
   ▼
Validate Message
   │
   ▼
Process Answer
   │
   ▼
Broadcast Event
   │
   ▼
Disconnect
   │
   ▼
Remove Connection
```

Authentication is performed before the connection is accepted. Invalid or missing authentication results in the connection being closed with a WebSocket policy-violation status.

Interview ownership is validated before a client is allowed to participate in an interview WebSocket session.

## Connection Manager

The `ConnectionManager` maintains active WebSocket connections grouped by interview.

```text
Connection Manager
        │
        ├── Interview A
        │      ├── WebSocket
        │      └── WebSocket
        │
        └── Interview B
               └── WebSocket
```

The manager is responsible for:

* registering connections
* removing disconnected connections
* sending personal messages
* broadcasting events
* cleaning up failed connections
* tracking active connections per interview

The manager does not contain interview or answer business logic.

## Answer Submission Flow

Answers received through WebSockets follow the existing application service architecture.

```text
WebSocket Client
      │
      ▼
WebSocket Router
      │
      ▼
Pydantic Validation
      │
      ▼
Question Authorization
      │
      ▼
AnswerService
      │
      ├── Prevent duplicate answers
      ├── Evaluate answer through AI
      ├── Persist answer
      ├── Create audit log
      └── Update interview status
      │
      ▼
WebSocket Events
```

This ensures that WebSocket requests do not bypass the application's existing business rules.

## WebSocket Events

The WebSocket event system is centralized in `websocket/events.py`.

Current events include:

```text
INTERVIEW_STARTED
QUESTION_AVAILABLE
ANSWER_SUBMITTED
ANSWER_EVALUATED
INTERVIEW_COMPLETED
ERROR
```

Events are transmitted using a consistent structure:

```json
{
    "event": "answer.evaluated",
    "data": {
        "interview_id": "...",
        "answer_id": "...",
        "score": 8,
        "feedback": "...",
        "suggested_improvement": "..."
    }
}
```

The event name identifies what happened, while the `data` object contains the associated information.

## Real-Time Interview Flow

A typical interview interaction follows this sequence:

```text
Client connects
      │
      ▼
INTERVIEW_STARTED
      │
      ▼
Client submits answer
      │
      ▼
ANSWER_SUBMITTED
      │
      ▼
AI evaluation
      │
      ▼
ANSWER_EVALUATED
      │
      ▼
All questions answered?
      │
     Yes
      │
      ▼
INTERVIEW_COMPLETED
```

The WebSocket layer therefore provides real-time communication while the existing service layer remains responsible for business logic and persistence.

## REST vs WebSocket

TalentForge uses both communication models for different responsibilities.

| Communication | Purpose                                        |
| ------------- | ---------------------------------------------- |
| REST          | CRUD operations and request/response workflows |
| WebSocket     | Real-time interview events and live updates    |
| Celery        | Long-running asynchronous processing           |
| Redis         | Caching and infrastructure support             |

WebSockets are therefore used where persistent real-time communication provides value, while ordinary application operations continue to use the REST API.

15. Exception Architecture

TalentForge uses application-specific exceptions.

The general hierarchy is:

AppException
     │
     ├── User Exceptions
     ├── Resume Exceptions
     ├── Interview Exceptions
     ├── Question Exceptions
     ├── Answer Exceptions
     └── AI Exceptions

Examples include:

UserAlreadyExistsException
InvalidCredentialsException
ResumeNotFoundException
ResumeAccessDeniedException
InterviewNotFoundException
QuestionAlreadyAnsweredException
AIProviderException

Exceptions are handled centrally rather than scattering HTTP error handling throughout the service layer.

This keeps business logic focused on application behavior.

16. Observability Architecture

TalentForge includes an observability stack for application monitoring.

TalentForge
     │
     ▼
Metrics Middleware
     │
     ▼
Prometheus
     │
     ▼
Grafana

The application exposes metrics through the metrics subsystem.

Prometheus collects those metrics and Grafana provides visualization dashboards.

This separates:

Application
    ↓
Metrics Collection
    ↓
Metrics Storage
    ↓
Visualization

from the application's core business logic.

WebSocket connections and real-time activity can also be monitored through application metrics and structured logging.

17. Production Infrastructure

The production deployment uses Docker Compose.

The major services are:

┌──────────────────────────────────────────┐
│                Nginx                     │
│          Reverse Proxy / Entry           │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│               FastAPI                    │
│        REST API + WebSocket Layer        │
└───────────────┬───────────┬──────────────┘
                │           │
                ▼           ▼
          PostgreSQL      Redis
                │           │
                │           ▼
                │      Celery Worker
                │
                └───────────────────────┐
                                        │
                                        ▼
                                  Persistent Data

Monitoring operates alongside the application:

FastAPI
   │
   ▼
Prometheus
   │
   ▼
Grafana

Nginx is responsible for the external entry point and reverse proxying of both HTTP and WebSocket traffic.

Docker provides consistent environments across development and deployment.

18. Health Check Architecture

TalentForge exposes dedicated health endpoints for application monitoring
and container orchestration.

The health-check system separates liveness from readiness.

Liveness Probe

GET /health/live

The liveness endpoint verifies that the FastAPI application process is
running.

It does not perform dependency checks.

Example response:

{
    "status": "alive"
}

Readiness Probe

GET /health/ready

The readiness endpoint verifies that the application can handle requests
by checking connectivity to its critical infrastructure dependencies:

PostgreSQL
Redis

The readiness flow is:

Client / Monitoring System
          │
          ▼
   /health/ready
          │
     ┌────┴────┐
     ▼         ▼
PostgreSQL    Redis
     │         │
     └────┬────┘
          ▼
       Ready

If both dependencies are available, the endpoint returns a successful
response indicating that the service is ready.

If a dependency check fails, the endpoint returns HTTP 503 Service
Unavailable.

This distinction allows infrastructure and monitoring systems to determine
whether the application process is alive and whether it is currently
capable of serving requests.

19. CI/CD Architecture

GitHub Actions is used to validate changes automatically.

The general pipeline is:

Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Install Dependencies
        │
        ▼
Run Tests
        │
        ▼
Build Docker Image
        │
        ▼
Push Image

The pipeline provides an automated quality gate before a new application image is published.

20. Dependency Flow

A major architectural principle is controlling dependency direction.

The REST application flow is:

Router
  ↓
Service
  ↓
Repository
  ↓
Database

The WebSocket application flow is:

WebSocket Layer
  ↓
Service
  ↓
Repository
  ↓
Database

AI-related dependencies follow a separate abstraction:

Service
  ↓
AI Service
  ↓
Provider Abstraction
  ↓
Concrete Provider
  ↓
Ollama

Infrastructure components such as Redis and Celery are accessed through their respective application integrations rather than being embedded directly into route handlers or WebSocket handlers.

This keeps transport concerns separate from business logic.

21. Design Principles

TalentForge is built around the following principles.

Separation of Concerns

Each layer has a clearly defined responsibility.

Dependency Injection

Dependencies are provided through FastAPI's dependency injection system rather than being tightly instantiated throughout route handlers.

Repository Pattern

Persistence logic is separated from business logic.

Service Layer

Business rules remain outside the HTTP and WebSocket transport layers.

Asynchronous Processing

Long-running operations are delegated to Celery workers.

Real-Time Communication

WebSockets are used for workflows that benefit from persistent, bidirectional communication and live updates.

Cache-Aside

Redis improves read performance without becoming the source of truth.

Provider Abstraction

AI services are isolated from specific LLM implementations.

Centralized Exception Handling

Application errors are represented through dedicated exception types.

Containerized Infrastructure

Application and infrastructure services are reproducible through Docker.

Automated Validation

Tests and Docker builds are integrated into CI/CD.

22. Architectural Goal

TalentForge is intentionally structured as more than a conventional CRUD backend.

The architecture is designed to demonstrate practical backend engineering concepts including:

API Design
    ↓
Layered Architecture
    ↓
Authentication & Authorization
    ↓
Database Abstraction
    ↓
Caching
    ↓
Asynchronous Processing
    ↓
Real-Time Communication
    ↓
AI Integration
    ↓
Observability
    ↓
Containerization
    ↓
CI/CD

TalentForge is structured as a maintainable, testable, observable, and deployable backend system while keeping the architecture understandable and its responsibilities clearly separated.