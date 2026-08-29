# TalentForge 🚀

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy\&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis\&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Background%20Tasks-37814A?logo=celery\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker\&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions\&logoColor=white)

**Production-style AI-powered interview platform built with FastAPI.**

TalentForge is a backend engineering project focused on designing and building a modern AI-powered interview platform using production-oriented software engineering practices.

The platform allows users to upload resumes, process and analyze candidate information, generate personalized interviews, submit answers, and receive AI-powered evaluations.

The primary goal of TalentForge is not simply to build features, but to demonstrate how modern backend systems are **architected, tested, secured, deployed, monitored, and maintained**.

---

## 📌 Project Highlights

* Layered backend architecture
* Repository and service patterns
* Dependency injection
* JWT authentication
* OAuth2 password flow
* Google OAuth authentication
* Role-based access control
* Scope-based authorization
* Asynchronous processing with Celery
* Redis caching
* AI provider abstraction
* Ollama-based AI integration
* Resume parsing and analysis
* AI-generated interview questions
* AI-powered answer evaluation
* Interview retakes
* Audit logging
* Centralized exception handling
* Prometheus metrics
* Grafana dashboards
* Dockerized development and production environments
* Automated testing with Pytest
* GitHub Actions CI/CD

---

# 🏗️ Architecture

TalentForge follows a layered backend architecture that separates HTTP handling, business logic, persistence, and infrastructure concerns.

```text
                         Client
                           │
                           ▼
                    ┌─────────────┐
                    │   Routers   │
                    │   API Layer │
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
                    └─────────────┘
```

Supporting infrastructure operates alongside the core application:

```text
                         TalentForge
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
       Redis               Celery            AI Layer
      Caching          Background Tasks    Provider System
          │                   │                   │
          │                   ▼                   ▼
          │            Resume Pipeline       Ollama
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                         PostgreSQL
```

This separation allows individual components to evolve without tightly coupling the entire application.

---

# 🛠️ Tech Stack

| Category          | Technology                  |
| ----------------- | --------------------------- |
| Language          | Python 3.12                 |
| API Framework     | FastAPI                     |
| Database          | PostgreSQL 17               |
| ORM               | SQLAlchemy 2.x              |
| Migrations        | Alembic                     |
| Authentication    | JWT + OAuth2                |
| Authorization     | RBAC + OAuth2 Scopes        |
| Password Security | Passlib + bcrypt            |
| AI Runtime        | Ollama                      |
| AI Architecture   | Provider Abstraction        |
| Resume Processing | pypdf                       |
| Validation        | Pydantic                    |
| Cache             | Redis                       |
| Background Jobs   | Celery                      |
| Rate Limiting     | SlowAPI                     |
| Testing           | Pytest + FastAPI TestClient |
| Containerization  | Docker + Docker Compose     |
| CI/CD             | GitHub Actions              |
| Monitoring        | Prometheus + Grafana        |

---

# 🔐 Authentication & Authorization

TalentForge implements authentication and authorization as separate concerns.

## Authentication

Supported authentication features include:

* User registration
* Password hashing
* JWT access tokens
* JWT refresh tokens
* OAuth2 password flow
* Google OAuth authentication
* Protected API routes
* Current-user dependency
* Profile management
* Password management

## Role-Based Access Control

TalentForge supports multiple application roles:

```text
student
teacher
admin
```

## Scope-Based Authorization

Endpoint permissions can also be controlled through OAuth2 scopes.

Example JWT claims:

```json
{
  "sub": "user-id",
  "role": "student",
  "scopes": [
    "resume:read",
    "resume:write",
    "interview:create"
  ]
}
```

This allows the application to enforce fine-grained permissions at the endpoint level.

---

# 📄 Resume Processing Pipeline

Resume processing is handled asynchronously so that expensive operations do not block API requests.

```text
User Uploads Resume
        │
        ▼
File Validation
        │
        ▼
Store PDF
        │
        ▼
Create Resume Record
Status = PENDING
        │
        ▼
Dispatch Celery Task
        │
        ▼
PROCESSING
        │
        ▼
PDF Text Extraction
        │
        ▼
Resume Parser
        │
        ▼
AI Resume Analyzer
        │
        ▼
Save Parsed Data + Analysis
        │
        ▼
COMPLETED
```

Resume processing states:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

Failures are recorded against the resume so that processing errors can be inspected without losing the original resume record.

---

# 🤖 AI Architecture

TalentForge uses a provider abstraction layer to keep application logic independent from the underlying AI runtime.

The **current production implementation is Ollama**.

```text
AI Service
    │
    ▼
Provider Factory
    │
    ▼
AI Provider Interface
    │
    ▼
Ollama Provider
    │
    ▼
LLM Model
```

The AI services communicate with the provider abstraction rather than directly depending on Ollama-specific implementation details.

This makes the architecture extensible for future AI providers without requiring business logic to be rewritten.

---

# 🧠 AI Services

## Resume Analyzer

Analyzes extracted resume information and produces structured analysis.

```text
Resume Text
     │
     ▼
Resume Analyzer
     │
     ▼
Ollama
     │
     ▼
Structured Analysis
```

## Question Generator

Generates interview questions based on the candidate's resume and experience.

```text
Resume Data
     │
     ▼
Question Generator
     │
     ▼
Ollama
     │
     ▼
Interview Questions
```

## Answer Evaluator

Evaluates candidate answers and generates structured feedback.

```text
Question + Answer
        │
        ▼
Answer Evaluator
        │
        ▼
Ollama
        │
        ▼
Feedback
Score
Improvement Suggestions
```

AI outputs are validated through Pydantic schemas before being used by the application.

---

# 🎤 Interview System

TalentForge generates AI-powered interviews from processed resumes.

The core domain relationship is:

```text
User
├── Resume
└── Interview
    └── Question
        └── Answer
```

Interview functionality includes:

* Resume-based interview generation
* AI-generated questions
* Interview sessions
* Answer submission
* AI evaluation
* Interview history
* Interview retakes

---

# ⚡ Real-Time Interview WebSocket

TalentForge provides real-time interview communication through WebSockets.

WebSockets are used for live interview events while the existing REST API remains responsible for normal request/response operations.

## Endpoint

```text
ws://localhost:8000/ws/interview/{interview_id}?token={jwt}
```

The JWT is supplied through the WebSocket query parameter.

## Connection Flow

```text
Client
  │
  ▼
WebSocket Connection
  │
  ▼
JWT Authentication
  │
  ▼
Interview Access Check
  │
  ▼
Connection Manager
  │
  ▼
Real-Time Interview Session
```

Connections that fail authentication or interview access validation are rejected with WebSocket policy-violation status `1008`.

## Answer Message

Clients submit answers using the following message structure:

```json
{
    "question_id": "question-uuid",
    "answer": "Candidate's answer"
}
```

Incoming messages are validated through the `WebSocketAnswerMessage` Pydantic schema before being processed.

Empty answers and malformed messages are rejected without terminating the WebSocket connection.

## Answer Processing

A valid answer follows the normal application service pipeline:

```text
WebSocket Message
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
       ├── Validate Question
       ├── Prevent Duplicate Answer
       ├── AI Evaluation
       ├── Persist Answer
       ├── Audit Log
       └── Update Interview Status
       │
       ▼
WebSocket Events
```

The WebSocket layer therefore does not duplicate answer-processing business logic.

## WebSocket Events

TalentForge currently defines the following WebSocket events:

| Event                 | Purpose                                                   |
| --------------------- | --------------------------------------------------------- |
| `interview.started`   | Indicates that an interview WebSocket session has started |
| `question.available`  | Indicates that a question is available to the client      |
| `answer.submitted`    | Indicates that an answer has been successfully submitted  |
| `answer.evaluated`    | Provides AI-generated answer evaluation                   |
| `interview.completed` | Indicates that the interview has been completed           |
| `error`               | Reports a client-visible WebSocket error                  |

### `answer.submitted`

```json
{
    "event": "answer.submitted",
    "data": {
        "interview_id": "interview-uuid",
        "user_id": "user-uuid",
        "answer_id": "answer-uuid"
    }
}
```

### `answer.evaluated`

```json
{
    "event": "answer.evaluated",
    "data": {
        "interview_id": "interview-uuid",
        "user_id": "user-uuid",
        "answer_id": "answer-uuid",
        "score": 8,
        "feedback": "Evaluation feedback",
        "suggested_improvement": "Suggested improvement"
    }
}
```

### `error`

```json
{
    "event": "error",
    "data": {
        "message": "Invalid answer message."
    }
}
```

## Connection Management

Active WebSocket connections are managed by the `ConnectionManager`.

Connections are grouped by `interview_id`, allowing events to be broadcast to clients participating in the same interview.

The manager also handles:

* connection registration
* connection removal
* personal error messages
* event broadcasting
* disconnect cleanup

## Error Handling

Client-side validation errors are returned through the WebSocket connection without terminating the session.

Unexpected server-side failures are logged and the connection is closed using WebSocket status `1011`.

This keeps the WebSocket layer resilient while preventing internal exceptions from being exposed to clients.


# 🔄 Interview Retakes

Completed interviews remain unchanged when a user starts a retake.

Instead, TalentForge creates a new interview instance.

```text
Original Interview
        │
        ▼
      Retake
        │
        ▼
New Interview
   ├── New Questions
   └── New Answers
```

This preserves historical interview data while allowing users to attempt the interview again.

---

# ⚡ Redis Caching

TalentForge uses Redis with a **cache-aside** strategy.

```text
Request
   │
   ▼
 Redis
   │
   ├── Cache Hit ───────► Return Cached Data
   │
   └── Cache Miss
            │
            ▼
       PostgreSQL
            │
            ▼
       Update Cache
            │
            ▼
       Return Data
```

Current caching behavior includes:

* Resume retrieval caching
* TTL-based expiration
* Cache invalidation when resume data changes

Default cache TTL:

```text
300 seconds
```

---

# ⚙️ Background Processing

Celery handles long-running workloads outside the main request-response cycle.

Current resume processing flow:

```text
PDF Processing
      │
      ▼
Resume Extraction
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

Benefits include:

* Faster API responses
* Non-blocking request handling
* Better workload isolation
* Retry handling for failures
* Improved scalability

---

# 🧾 Audit Logging

Important user actions are recorded through the audit logging system.

Examples include:

```text
CREATE_INTERVIEW
RETAKE_INTERVIEW
DELETE_INTERVIEW
SUBMIT_ANSWER
```

Audit records contain:

```text
id
user_id
action
entity_type
entity_id
```

This provides a persistent record of important application-level actions.

---

# 🧱 Exception Architecture

TalentForge uses centralized application-specific exceptions rather than scattering raw HTTP exceptions throughout the service layer.

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

Centralized exception handling provides:

* Consistent API error responses
* Cleaner service-layer code
* Easier debugging
* Better separation between business logic and HTTP concerns

---

# 📊 Observability

TalentForge includes foundations for production monitoring and observability.

Current components include:

* Prometheus metrics
* Grafana dashboards
* Request logging middleware
* Metrics middleware
* Security middleware
* Health endpoints

The monitoring architecture is designed to provide visibility into application behavior and operational health.

---

# 🧪 Testing

TalentForge uses Pytest and FastAPI's testing utilities.

Testing infrastructure includes:

* Pytest
* FastAPI TestClient
* Dependency overrides
* Dedicated test database

Current test coverage includes areas such as:

* Application startup
* Authentication
* JWT flows
* Protected routes
* Resume workflows
* Interview workflows
* Answer submission
* Dashboard services
* AI services

The project also runs automated tests through GitHub Actions.

---

# 🐳 Docker Architecture

TalentForge uses Docker Compose to provide a consistent development environment.

```text
                         FastAPI
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        PostgreSQL        Redis      Celery Worker
             │              │              │
             └──────────────┴──────────────┘
```

Development services include:

```text
api
db
redis
celery_worker
pgadmin
```

Production deployment additionally includes infrastructure such as:

```text
nginx
prometheus
grafana
```

---

# 🔄 CI/CD Pipeline

GitHub Actions automatically validates changes pushed to the repository.

The general pipeline is:

```text
Push / Pull Request
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
Publish Image
```

This provides automated validation before changes are considered stable.

---

# 📁 Project Structure

```text
TalentForge/
│
├── .github/
│   └── workflows/
│
├── ai/
│   ├── providers/
│   ├── services/
│   ├── schemas.py
│   ├── prompts.py
│   └── provider_factory.py
│
├── alembic/
│   └── versions/
│
├── api/
│   └── v1/
│
├── auth/
├── db/
├── docs/
├── exceptions/
├── infra/
├── metrics/
├── middleware/
├── models/
├── nginx/
├── prometheus/
├── repositories/
├── routers/
├── schemas/
├── scripts/
├── services/
├── tasks/
├── tests/
├── utils/
├── websocket/
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── alembic.ini
├── app.py
└── requirements.txt
```

The project follows clear boundaries between API routing, business logic, persistence, infrastructure, AI functionality, and background processing.

---

# 🚀 Running Locally

## 1. Clone the Repository

```bash
git clone https://github.com/satyamshrestha/TalentForge.git
cd TalentForge
```

## 2. Configure Environment Variables

Create a local `.env` file based on `.env.example`.

```bash
cp .env.example .env
```

Configure the required database, Redis, authentication, OAuth, and AI settings.

For local AI processing, TalentForge currently uses Ollama.

## 3. Start the Development Environment

```bash
docker compose up -d
```

## 4. Apply Database Migrations

```bash
docker compose exec api alembic upgrade head
```

## 5. Access the API

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# 🎯 Engineering Principles

TalentForge is built around several engineering principles.

### Separation of Concerns

Each application layer owns a specific responsibility.

### Dependency Injection

Components are constructed and injected independently, improving testability and reducing coupling.

### Repository Pattern

Database access is separated from business logic.

### Service Layer

Business rules remain outside API route handlers.

### Asynchronous Architecture

Long-running workloads are delegated to background workers.

### Provider Abstraction

AI services depend on an abstraction layer rather than directly coupling business logic to a specific AI provider.

### Centralized Exception Handling

Application-specific exceptions provide consistent error handling across the system.

### Production Thinking

The project emphasizes:

* Reliability
* Maintainability
* Security
* Observability
* Scalability
* Testability
* Deployment practices

---

# 🧭 Project Direction

TalentForge is being developed as a long-term backend engineering project.

The focus is on progressively improving the system through:

* Advanced observability
* Production deployment
* Distributed-system patterns
* Performance optimization
* System design
* Scalability improvements
* Additional AI provider support
* Infrastructure improvements

The project prioritizes **engineering depth over continuously adding features**.

---

# 👨‍💻 Author

**Satyam Shrestha**

AI Computer Engineering Student
Far East University

Building TalentForge as a long-term backend engineering project focused on learning and demonstrating how production-style backend systems are designed, built, tested, and deployed.