# TalentForge Architecture

TalentForge is designed as a production-style backend system with clear separation between API handling, business logic, data access, asynchronous processing, AI services, and infrastructure.

The architecture is designed to keep individual responsibilities isolated while allowing the system to evolve without tightly coupling the application to a specific database, task queue, or AI provider.

---

## 1. High-Level Architecture

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
                           ▼
                    ┌─────────────┐
                    │   Routers   │
                    │  API Layer  │
                    └──────┬──────┘
                           │
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
```

Supporting infrastructure operates alongside the main request path:

```text
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
```

---

# 2. Architectural Layers

TalentForge follows a layered architecture.

```text
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
```

Each layer has a specific responsibility.

## Routers

Routers are responsible for HTTP-level concerns.

They handle:

* Request parsing
* Response serialization
* Dependency injection
* Authentication dependencies
* Authorization dependencies
* HTTP status codes
* Calling application services

Routers should not contain substantial business logic.

Example:

```text
POST /interviews
       │
       ▼
Interview Router
       │
       ▼
Interview Service
```

---

## Services

Services contain the application's business logic.

Examples include:

```text
UserService
ResumeService
InterviewService
AnswerService
DashboardService
AuditLogService
```

Services are responsible for operations such as:

* Validating business rules
* Coordinating repositories
* Managing application workflows
* Calling AI services
* Triggering background tasks
* Managing cache invalidation
* Recording audit events

This keeps business logic independent from the HTTP layer.

---

## Repositories

Repositories provide the database access layer.

Examples include:

```text
UserRepository
ResumeRepository
InterviewRepository
QuestionRepository
AnswerRepository
AuditLogRepository
DashboardRepository
```

Repositories are responsible for:

* Creating records
* Retrieving records
* Updating records
* Deleting records
* Querying PostgreSQL

The service layer therefore does not need to contain raw database operations throughout its business logic.

---

# 3. Request Flow

A typical synchronous API request follows this path:

```text
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
```

For example, retrieving a user's resumes:

```text
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
```

Redis may intercept this flow when cached data is available.

---

# 4. Redis Cache Architecture

TalentForge uses Redis as a caching layer.

The application follows a cache-aside strategy.

```text
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
```

Resume retrieval uses cache keys based on the user:

```text
user:{user_id}:resumes
```

The current cache TTL is:

```text
300 seconds
```

Cache invalidation occurs when relevant resume data changes.

Examples:

```text
Resume Upload
     │
     ▼
Database Update
     │
     ▼
Invalidate Resume Cache
```

```text
Resume Delete
     │
     ▼
Database Delete
     │
     ▼
Invalidate Resume Cache
```

Redis is therefore used as a performance optimization rather than the source of truth.

PostgreSQL remains the authoritative persistent data store.

---

# 5. Celery Background Processing

Long-running operations are separated from the API request-response cycle.

Resume processing is handled asynchronously using Celery.

```text
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
```

The API does not wait for the entire resume-processing pipeline to finish.

This prevents expensive processing from blocking normal API requests.

---

# 6. AI Architecture

AI functionality is separated from the application's core business logic.

The architecture is:

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
AI Provider
       │
       ▼
     Ollama
       │
       ▼
     LLM Model
```

Current AI services include:

```text
ResumeAnalyzer
QuestionGenerator
AnswerEvaluator
```

These services are responsible for AI-specific workflows while the provider layer handles communication with the configured model backend.

---

# 7. AI Provider Abstraction

TalentForge does not tightly couple its business logic to Ollama.

Instead, AI services depend on the provider abstraction.

```text
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
```

The currently active provider is:

```text
Ollama
```

Ollama is used as the primary model backend for the current system.

An OpenAI provider exists in the codebase as a placeholder for future integration and is **not the current production AI backend**.

This architecture allows additional providers to be introduced without rewriting the business logic inside:

```text
ResumeAnalyzer
QuestionGenerator
AnswerEvaluator
```

---

# 8. Resume Processing Architecture

Resume processing combines synchronous API operations, asynchronous tasks, parsing, and AI analysis.

```text
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
```

If processing fails, the resume is marked:

```text
FAILED
```

and the associated error information is stored with the resume.

---

# 9. Interview Architecture

Interview creation is based on processed resume information.

```text
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
```

The domain relationship is:

```text
User
 │
 ├── Resume
 │
 └── Interview
       │
       └── Question
              │
              └── Answer
```

This allows interviews, questions, and answers to remain independently persisted while maintaining their relationships.

---

# 10. Answer Evaluation Architecture

Answer evaluation is performed through the AI service layer.

```text
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
```

The evaluation contains information such as:

```text
Feedback
Score
Suggested Improvement
```

Business rules such as preventing a question from being answered multiple times remain inside the application service layer.

---

# 11. Authentication and Authorization

Authentication and authorization are separated into dedicated components.

```text
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
```

TalentForge uses:

* JWT access tokens
* JWT refresh tokens
* Password hashing
* OAuth2 password flow
* Google OAuth
* Role-based access control
* Scope-based authorization
* Ownership validation

Authorization decisions can therefore consider both the user's role and their granted scopes.

---

# 12. Database Architecture

PostgreSQL is the primary persistent data store.

The core domain model is:

```text
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
```

Audit logging is associated with users and application entities:

```text
User
 │
 └── AuditLog
```

SQLAlchemy is used as the ORM and Alembic manages database schema migrations.

---

# 13. Middleware Architecture

Cross-cutting application concerns are handled through middleware and dedicated utilities.

Current middleware responsibilities include:

```text
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
```

Other cross-cutting concerns include:

* CORS
* Rate limiting
* Request logging
* Security headers
* Metrics collection
* Trusted host validation

These concerns remain outside individual business services.

---

# 14. Exception Architecture

TalentForge uses application-specific exceptions.

The general hierarchy is:

```text
AppException
     │
     ├── User Exceptions
     ├── Resume Exceptions
     ├── Interview Exceptions
     ├── Question Exceptions
     ├── Answer Exceptions
     └── AI Exceptions
```

Examples include:

```text
UserAlreadyExistsException
InvalidCredentialsException
ResumeNotFoundException
ResumeAccessDeniedException
InterviewNotFoundException
QuestionAlreadyAnsweredException
AIProviderException
```

Exceptions are handled centrally rather than scattering HTTP error handling throughout the service layer.

This keeps business logic focused on application behavior.

---

# 15. Observability Architecture

TalentForge includes an observability stack for application monitoring.

```text
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
```

The application exposes metrics through the metrics subsystem.

Prometheus collects those metrics and Grafana provides visualization dashboards.

This separates:

```text
Application
    ↓
Metrics Collection
    ↓
Metrics Storage
    ↓
Visualization
```

from the application's core business logic.

---

# 16. Production Infrastructure

The production deployment uses Docker Compose.

The major services are:

```text
┌──────────────────────────────────────────┐
│                Nginx                     │
│          Reverse Proxy / Entry           │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│               FastAPI                    │
│                 API                      │
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
```

Monitoring operates alongside the application:

```text
FastAPI
   │
   ▼
Prometheus
   │
   ▼
Grafana
```

Docker provides consistent environments across development and deployment.

---

# 17. CI/CD Architecture

GitHub Actions is used to validate changes automatically.

The general pipeline is:

```text
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
```

The pipeline provides an automated quality gate before a new application image is published.

---

# 18. Dependency Flow

A major architectural principle is controlling dependency direction.

The intended flow is:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

AI-related dependencies follow a separate abstraction:

```text
Service
  ↓
AI Service
  ↓
Provider Abstraction
  ↓
Concrete Provider
  ↓
Ollama
```

Infrastructure components such as Redis and Celery are accessed through their respective application integrations rather than being embedded directly into route handlers.

This keeps the application modular and easier to test.

---

# 19. Design Principles

TalentForge is built around the following principles.

### Separation of Concerns

Each layer has a clearly defined responsibility.

### Dependency Injection

Dependencies are provided through FastAPI's dependency injection system rather than being tightly instantiated throughout route handlers.

### Repository Pattern

Persistence logic is separated from business logic.

### Service Layer

Business rules remain outside the HTTP layer.

### Asynchronous Processing

Long-running operations are delegated to Celery workers.

### Cache-Aside

Redis improves read performance without becoming the source of truth.

### Provider Abstraction

AI services are isolated from specific LLM implementations.

### Centralized Exception Handling

Application errors are represented through dedicated exception types.

### Containerized Infrastructure

Application and infrastructure services are reproducible through Docker.

### Automated Validation

Tests and Docker builds are integrated into CI/CD.

---

# 20. Architectural Goal

TalentForge is intentionally structured as more than a conventional CRUD backend.

The architecture is designed to demonstrate practical backend engineering concepts including:

```text
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
AI Integration
    ↓
Observability
    ↓
Containerization
    ↓
CI/CD
```

The goal is to evolve TalentForge as a maintainable, testable, observable, and deployable backend system while keeping the architecture understandable as the project grows.