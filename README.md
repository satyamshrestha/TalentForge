# TalentForge 🚀

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy\&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis\&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Background%20Tasks-37814A?logo=celery\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker\&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions\&logoColor=white)

**Production-style AI-powered interview platform built with FastAPI**

TalentForge is a backend engineering project designed around real-world software engineering practices: layered architecture, authentication and authorization, asynchronous processing, caching, AI provider abstraction, testing, containerization, and CI/CD.

</div>

---

## 📖 Overview

TalentForge is an AI-powered interview preparation platform that allows users to upload resumes, process and analyze them using AI, generate interview questions based on their experience, submit answers, and receive AI-generated evaluations.

The project is intentionally built as a **production-style backend system rather than a simple CRUD application**.

The main goal is to use TalentForge as an engineering playground for learning and demonstrating how modern backend systems are designed, structured, tested, containerized, and prepared for production.

---

# 🏗️ Architecture

TalentForge follows a layered backend architecture:

```text
                    Client
                      │
                      ▼
              ┌───────────────┐
              │    Routers    │
              │   API Layer   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   Services    │
              │ Business Logic│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Repositories  │
              │ Data Access   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  PostgreSQL   │
              └───────────────┘
```

Supporting infrastructure:

```text
                         TalentForge
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
       Redis               Celery               AI
      Caching           Background Tasks      Providers
          │                   │                   │
          │                   ▼                   ▼
          │             Resume Pipeline      Provider Factory
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                         PostgreSQL
```

The application separates responsibilities across:

```text
routers
   ↓
services
   ↓
repositories
   ↓
database
```

AI functionality is separately abstracted behind provider and service layers.

---

# 🛠️ Tech Stack

| Category              | Technology                                         |
| --------------------- | -------------------------------------------------- |
| Language              | Python 3.12                                        |
| API Framework         | FastAPI                                            |
| Database              | PostgreSQL 17                                      |
| ORM                   | SQLAlchemy                                         |
| Migrations            | Alembic                                            |
| Authentication        | JWT                                                |
| Password Hashing      | Passlib + bcrypt                                   |
| Authorization         | RBAC + OAuth2 Scopes                               |
| OAuth                 | Google OAuth                                       |
| Caching               | Redis                                              |
| Background Processing | Celery                                             |
| AI                    | Provider abstraction with configurable LLM backend |
| Resume Processing     | pypdf                                              |
| Validation            | Pydantic                                           |
| Rate Limiting         | SlowAPI                                            |
| Containerization      | Docker + Docker Compose                            |
| Testing               | Pytest + FastAPI TestClient                        |
| CI/CD                 | GitHub Actions                                     |
| Image Registry        | Docker Hub                                         |

---

# ✨ Current Features

## 🔐 Authentication

TalentForge currently supports:

* User registration
* Password hashing with bcrypt
* Password-based login
* JWT access tokens
* JWT refresh tokens
* Protected API routes
* Current-user dependency
* OAuth2 password flow
* Google OAuth authentication
* Google account connection
* Password change
* Profile retrieval
* Profile updates

Authentication is handled through dedicated authentication utilities and the `UserService`.

---

# 🛡️ Authorization

TalentForge implements both **role-based authorization** and **scope-based authorization**.

Supported roles:

```text
student
teacher
admin
```

JWT tokens contain authorization information such as:

```json
{
  "sub": "user-id",
  "role": "admin",
  "scopes": [
    "resume:read",
    "resume:write",
    "interview:create",
    "interview:delete",
    "admin"
  ]
}
```

This allows protected endpoints to make authorization decisions based on both the user's role and permissions.

---

# 📄 Resume Processing

Users can upload PDF resumes through the API.

The upload pipeline is asynchronous:

```text
User
 │
 ▼
Upload PDF
 │
 ▼
Validate file
 │
 ├── Extension check
 ├── Content-Type check
 ├── PDF signature check
 └── File-size check
 │
 ▼
Store PDF
 │
 ▼
Create Resume
status = PENDING
 │
 ▼
Dispatch Celery Task
 │
 ▼
PROCESSING
 │
 ▼
Extract PDF text
 │
 ▼
ResumeParser
 │
 ├── Name
 ├── Email
 ├── Phone
 ├── Skills
 ├── Education
 └── Experience
 │
 ▼
ResumeAnalyzer
 │
 ▼
Store parsed data + AI analysis
 │
 ▼
COMPLETED
```

Resume states:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

Failures are stored on the resume using `error_message`.

---

# 🤖 AI Integration

AI functionality is intentionally separated from the rest of the application.

The current AI services include:

### Resume Analyzer

Analyzes extracted resume text and returns structured resume analysis.

```text
Resume text
     ↓
ResumeAnalyzer
     ↓
AI Provider
     ↓
Structured ResumeAnalysisResponse
```

### Question Generator

Generates interview questions based on the candidate's resume.

```text
Resume
  ↓
QuestionGenerator
  ↓
AI Provider
  ↓
Structured questions
```

### Answer Evaluator

Evaluates submitted interview answers.

```text
Question + Answer
       ↓
AnswerEvaluator
       ↓
AI Provider
       ↓
Structured evaluation
       ↓
Feedback + Score + Suggested Improvement
```

AI responses are parsed into Pydantic schemas rather than being passed directly through the application.

This keeps the application logic independent from the exact format returned by an LLM.

---

# 🔌 AI Provider Abstraction

AI services do not directly depend on one specific LLM implementation.

Instead:

```text
AI Service
    │
    ▼
Provider Factory
    │
    ▼
AI Provider
    │
    ▼
LLM
```

The provider is selected through configuration.

Example:

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

The configuration also provides support for future providers through environment variables such as:

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_AI_API_KEY=
```

This abstraction makes it possible to change AI providers without rewriting the business logic inside services such as `ResumeAnalyzer`, `QuestionGenerator`, and `AnswerEvaluator`.

---

# 🎤 Interview System

TalentForge can create interviews from processed resumes.

The flow is:

```text
Completed Resume
       │
       ▼
Extract raw resume text
       │
       ▼
QuestionGenerator
       │
       ▼
AI-generated questions
       │
       ▼
Create Interview
       │
       ▼
Create Questions
```

Each interview contains:

* Target role
* Interview status
* Questions
* User ownership
* Answer relationships

Interview statuses include:

```text
CREATED
IN_PROGRESS
COMPLETED
```

---

# 📝 Answer Evaluation

Users can submit an answer for each interview question.

The system:

1. Validates that the question exists.
2. Checks whether the question has already been answered.
3. Sends the question and answer to the AI evaluator.
4. Stores the evaluation.
5. Records an audit event.
6. Updates the interview status.

An evaluation contains:

```text
answer_text
feedback
score
suggested_improvement
```

An answer can only be submitted once for a question.

---

# 🔄 Interview Retakes

Completed interviews can be retaken.

The original interview remains unchanged.

TalentForge creates:

```text
Original Interview
       │
       ▼
Retake
       │
       ▼
New Interview
       │
       ├── New Question 1
       ├── New Question 2
       └── ...
```

The new interview receives its own ID and questions while preserving the original interview history.

---

# 📊 Dashboard

The dashboard service aggregates user interview information.

Current dashboard metrics include:

* Total resumes
* Total interviews
* Completed interviews
* Average interview score
* Recent interviews

Average interview score is calculated from answered questions belonging to the user's interviews.

---

# ⚡ Redis Caching

TalentForge uses Redis with a **cache-aside pattern**.

Resume retrieval follows:

```text
Request
   │
   ▼
Redis
   │
   ├── Cache Hit ───────► Return cached data
   │
   └── Cache Miss
            │
            ▼
        PostgreSQL
            │
            ▼
        Store in Redis
            │
            ▼
        Return data
```

Resume cache keys follow the pattern:

```text
user:{user_id}:resumes
```

Cached resume data currently uses a TTL of:

```text
300 seconds
```

Cache invalidation occurs when resume data changes, including:

* Resume upload
* Resume processing
* Resume deletion

---

# ⚙️ Celery Background Processing

Resume processing is intentionally moved out of the request-response cycle.

The API creates the resume and dispatches:

```python
process_resume.delay(resume.id)
```

The Celery worker then handles:

```text
PDF extraction
      ↓
Resume parsing
      ↓
AI analysis
      ↓
Database update
```

The worker also implements retry behavior for AI provider failures.

Current configuration:

```text
Maximum retries: 3
Retry delay: 10 seconds
```

This prevents potentially slow AI processing from blocking the API request.

---

# 🧾 Audit Logging

Important user actions are recorded through a dedicated audit logging service.

Current actions include events such as:

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

The service follows the same repository-based architecture as the rest of the application.

---

# 🧱 Custom Exception Architecture

TalentForge uses application-specific exceptions rather than scattering raw HTTP exceptions throughout business logic.

Examples include:

```text
UserAlreadyExistsException
UserNotFoundException
InvalidCredentialsException
InvalidRefreshTokenException

ResumeNotFoundException
ResumeAccessDeniedException
ResumeNotReadyException
ResumeTooLargeException

InterviewNotFoundException
InterviewAccessDeniedException
ResumeTextNotFoundException

QuestionNotFoundException
QuestionAlreadyAnsweredException

AIProviderException
```

These exceptions are handled centrally by the application's exception handler.

Example response:

```json
{
  "detail": "Resume does not exist!"
}
```

This keeps service-layer logic cleaner and makes error handling consistent across the API.

---

# 🛡️ API Security

The application currently includes several security mechanisms:

* JWT authentication
* Password hashing
* RBAC
* OAuth2 scopes
* Protected routes
* Google OAuth
* Trusted host middleware
* Security headers middleware
* CORS configuration
* Rate limiting with SlowAPI
* Custom exception handling
* Ownership validation
* Resume file validation
* Maximum resume size validation

---

# 🧩 Middleware

TalentForge currently uses middleware for:

### Request Logging

Requests are logged through a custom logging middleware.

### Security Headers

Security-related response headers are applied through a dedicated security middleware.

### Trusted Hosts

Incoming requests are restricted through Starlette's `TrustedHostMiddleware`.

### CORS

The API is configured to support frontend development environments such as:

```text
http://localhost:3000
http://localhost:5173
```

### Rate Limiting

SlowAPI is integrated into the application for API rate limiting.

---

# 🗃️ Database Models

The current core domain consists of:

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

## User

Stores authentication and account information.

Main fields include:

```text
id
full_name
email
password
provider
google_id
role
```

## Resume

Stores uploaded resume information.

```text
id
file_path
parsed_text
status
error_message
user_id
```

## Interview

Stores interview sessions.

```text
id
role_target
status
user_id
```

## Question

Stores generated interview questions.

```text
id
question_text
interview_id
```

## Answer

Stores candidate responses and AI evaluations.

```text
id
answer_text
feedback
score
suggested_improvement
question_id
```

## AuditLog

Stores important user actions.

```text
id
user_id
action
entity_type
entity_id
```

---

# 📁 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── backend.yml
│
├── ai/
│   ├── services/
│   │   ├── answer_evaluator.py
│   │   ├── question_generator.py
│   │   └── resume_analyzer.py
│   ├── provider_factory.py
│   ├── prompts.py
│   ├── schemas.py
│   └── utils/
│       └── parser.py
│
├── alembic/
│   └── ...
│
├── api/
│   └── v1/
│       └── ...
│
├── auth/
│   ├── hashing.py
│   ├── jwt_handler.py
│   └── scopes.py
│
├── db/
│   ├── database.py
│   ├── deps.py
│   └── redis.py
│
├── exceptions/
│   ├── ai_exception.py
│   ├── answer_exception.py
│   ├── app_exception.py
│   ├── interview_exception.py
│   ├── question_exception.py
│   ├── resume_exception.py
│   └── user_exception.py
│
├── middleware/
│   ├── logging_middleware.py
│   ├── rate_limit.py
│   └── security_headers.py
│
├── models/
│   ├── answer.py
│   ├── audit_log.py
│   ├── interview.py
│   ├── question.py
│   ├── resume.py
│   └── user.py
│
├── repositories/
│   ├── answer_repository.py
│   ├── audit_log_repository.py
│   ├── dashboard_repository.py
│   ├── interview_repository.py
│   ├── question_repository.py
│   ├── resume_repository.py
│   └── user_repository.py
│
├── routers/
│   └── ...
│
├── schemas/
│   └── ...
│
├── services/
│   ├── answer_service.py
│   ├── audit_log_service.py
│   ├── dashboard_service.py
│   ├── interview_service.py
│   ├── resume_parser.py
│   ├── resume_service.py
│   └── user_service.py
│
├── tasks/
│   ├── __init__.py
│   ├── celery_app.py
│   └── resume_tasks.py
│
├── tests/
│   ├── conftest.py
│   ├── test_answer.py
│   ├── test_app.py
│   ├── test_auth.py
│   ├── test_dashboard.py
│   ├── test_interview.py
│   └── test_resume.py
│
├── utils/
│   ├── config.py
│   ├── file_validation.py
│   └── logger.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── app.py
├── docker-compose.yml
├── docker-compose.prod.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

---

# 🐳 Docker Architecture

Development uses Docker Compose with the following services:

```text
┌─────────────┐
│     API     │
│   FastAPI   │
└──────┬──────┘
       │
 ┌─────┼──────────────┐
 │     │              │
 ▼     ▼              ▼
DB   Redis       Celery Worker
 │     │              │
 ▼     ▼              ▼
Postgres Cache    Background Jobs
```

Services:

```text
api
db
redis
celery_worker
pgadmin
```

---

# 🚀 Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/TalentForge.git
cd TalentForge
```

## 2. Create environment configuration

Copy:

```text
.env.example
```

to:

```text
.env
```

Then configure the required variables.

---

## 3. Start the development environment

```bash
docker compose up -d
```

This starts:

* FastAPI
* PostgreSQL
* Redis
* Celery worker
* pgAdmin

---

## 4. Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

---

## 5. Access the API

The API runs on:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# 🧪 Testing

TalentForge uses Pytest for automated testing.

The test suite covers areas including:

* Application startup
* Authentication
* Signup
* Duplicate registration
* Login
* Invalid credentials
* Protected endpoints
* Refresh tokens
* Google-account restrictions
* Resume uploads
* Invalid resume uploads
* Resume retrieval
* Redis caching behavior
* Interview creation behavior
* Interview retakes
* Answer submission
* Dashboard access

The tests use a dedicated SQLite test database and FastAPI dependency overrides.

```text
Application
     │
     ▼
FastAPI TestClient
     │
     ▼
SQLite test database
```

The test environment is primarily intended to run through CI rather than as part of the normal development workflow.

---

# 🔄 CI/CD

GitHub Actions is used to automatically validate the backend.

The CI workflow performs automated testing and Docker image building.

General pipeline:

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Install dependencies
        │
        ▼
Run Pytest
        │
        ▼
Build Docker Image
        │
        ▼
Push Image
```

The project is designed so that changes must pass the automated CI pipeline before being considered stable.

---

# 🐋 Docker Image

The project is also packaged as a Docker image.

Current image:

```text
satyamshrestha/talentforge:latest
```

Pull with:

```bash
docker pull satyamshrestha/talentforge:latest
```

---

# 🏭 Production Compose

A separate production Compose configuration is provided:

```bash
docker compose -f docker-compose.prod.yml up -d
```

The production configuration separates the main application from its supporting infrastructure:

```text
API
│
├── PostgreSQL
├── Redis
└── Celery Worker
```

The API and Celery worker use the same application image while executing different commands.

---

# 🔐 Environment Variables

Example configuration:

```env
SECRET_KEY=
ALGORITHM=HS256

DATABASE_URL=
REDIS_URL=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

PGADMIN_DEFAULT_EMAIL=
PGADMIN_DEFAULT_PASSWORD=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

LLM_PROVIDER=ollama
LLM_MODEL=
OLLAMA_BASE_URL=
OLLAMA_TIMEOUT=300
OLLAMA_RETRIES=2
```

AI provider credentials can also be configured through:

```env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_AI_API_KEY=
```

Secrets should never be committed to Git.

---

# 🎯 Engineering Principles

TalentForge is built around several backend engineering principles:

### Separation of Concerns

Routers handle HTTP concerns.

Services handle business logic.

Repositories handle persistence.

AI services handle AI-specific operations.

### Dependency Injection

Services and repositories are constructed independently and injected into API dependencies.

### Repository Pattern

Database access is separated from business logic.

### Service Layer

Business rules are kept outside route handlers.

### Asynchronous Processing

Long-running resume processing is delegated to Celery.

### Cache-Aside Strategy

Redis is used to reduce repeated database reads.

### Provider Abstraction

AI services depend on an abstract provider layer rather than a specific LLM implementation.

### Centralized Exceptions

Application-specific exceptions provide consistent error handling.

### Automated Validation

CI runs the test suite and validates changes automatically.

---

# 🧭 Project Direction

TalentForge is being developed as a **backend engineering portfolio project**, not simply as a feature collection.

The focus is on progressively improving:

* Code quality
* Architecture
* Reliability
* Testing
* AI integration
* Security
* Observability
* Scalability
* Deployment practices
* Distributed-system understanding
* System design

The project intentionally prioritizes engineering depth over continuously adding new endpoints and features.

---

# 👨‍💻 Author

**Satyam Shrestha**

AI Computer Engineering Student
Far East University

Building TalentForge as a long-term backend engineering project focused on learning how production-style systems are actually designed and built.