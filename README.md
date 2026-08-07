# TalentForge 🚀

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-593D88)
![Redis](https://img.shields.io/badge/Redis-Caching-DC382D?logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Background%20Tasks-37814A?logo=celery&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-111111)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Observability-F46800?logo=grafana&logoColor=white)

# TalentForge

**Production-style AI-powered interview platform built with FastAPI**

TalentForge is a backend engineering project focused on designing and building a modern AI-powered platform using real-world software engineering practices.

The system allows users to upload resumes, analyze candidate information using AI, generate personalized interviews, submit answers, and receive AI-powered evaluations.

The primary goal of TalentForge is not simply building features, but demonstrating how scalable backend systems are architected, tested, deployed, and maintained.

---

# 📌 Project Highlights

- Layered backend architecture
- Repository and service patterns
- JWT authentication
- OAuth2 and Google OAuth integration
- Role-based and scope-based authorization
- Async processing with Celery
- Redis caching
- AI provider abstraction
- Local LLM integration with Ollama
- Automated testing
- Dockerized development environment
- CI/CD pipeline
- Observability foundations

---

# 🏗️ Architecture

TalentForge follows a layered backend architecture:

                Client
                  |
                  v

          +---------------+
          |    Routers    |
          |   API Layer   |
          +-------+-------+
                  |
                  v

          +---------------+
          |   Services    |
          | Business Logic|
          +-------+-------+
                  |
                  v

          +---------------+
          | Repositories  |
          | Data Access   |
          +-------+-------+
                  |
                  v

          +---------------+
          | PostgreSQL 17 |
          +---------------+

Supporting infrastructure:

                     TalentForge

                          |
    ------------------------------------------------
    |                     |                       |
    v                     v                       v

  Redis                Celery                  AI Layer
 Caching          Background Tasks        Provider System

    |                     |                       |
    |                     |                       |
    v                     v                       v

PostgreSQL Resume Pipeline Ollama LLM


---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| API Framework | FastAPI |
| Database | PostgreSQL 17 |
| ORM | SQLAlchemy 2.x |
| Migration | Alembic |
| Authentication | JWT + OAuth2 |
| Authorization | RBAC + OAuth2 Scopes |
| Password Security | Passlib + bcrypt |
| AI Runtime | Ollama |
| AI Architecture | Provider Abstraction |
| Resume Processing | pypdf |
| Validation | Pydantic |
| Cache | Redis |
| Background Jobs | Celery |
| Rate Limiting | SlowAPI |
| Testing | Pytest |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |

---

# 🔐 Authentication & Authorization

TalentForge implements a complete authentication system.

Features:

- User registration
- Secure password hashing
- JWT access tokens
- JWT refresh tokens
- OAuth2 password flow
- Google OAuth authentication
- Protected routes
- Profile management


Authorization uses both:

## Role-Based Access Control

Supported roles:


student
teacher
admin



## Scope-Based Authorization

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

This allows fine-grained endpoint permissions.

📄 Resume Processing Pipeline

Resume processing is handled asynchronously.

Flow:

User Uploads Resume

        |
        v

File Validation

        |
        v

Store PDF

        |
        v

Create Resume Record
Status = PENDING

        |
        v

Celery Background Task

        |
        v

PDF Text Extraction

        |
        v

Resume Parser

        |
        v

AI Resume Analyzer

        |
        v

Save Analysis

        |
        v

COMPLETED

Resume states:

PENDING
PROCESSING
COMPLETED
FAILED

Long-running operations are moved outside the request-response cycle.

🤖 AI Architecture

TalentForge uses an AI provider abstraction layer.

Current provider:

Ollama

Architecture:

AI Service

      |
      v

Provider Factory

      |
      v

AI Provider Interface

      |
      v

Ollama Provider

      |
      v

LLM Model

This keeps business logic independent from the underlying AI implementation.

🧠 AI Services
Resume Analyzer

Analyzes extracted resume information.

Resume Text

     |
     v

Resume Analyzer

     |
     v

Ollama

     |
     v

Structured Analysis
Question Generator

Creates interview questions based on candidate experience.

Resume Data

     |
     v

Question Generator

     |
     v

Ollama

     |
     v

Interview Questions
Answer Evaluator

Evaluates candidate answers.

Question + Answer

        |
        v

Answer Evaluator

        |
        v

Ollama

        |
        v

Feedback
Score
Improvement Suggestions

AI outputs are validated using Pydantic schemas.

🎤 Interview System

TalentForge generates AI-powered interviews from processed resumes.

Entity relationship:

User

 |
 +---- Resume


 |
 +---- Interview
          |
          +---- Question
                    |
                    +---- Answer

Features:

Resume-based interviews
AI-generated questions
Answer submission
AI evaluation
Interview history
Interview retakes
🔄 Interview Retakes

Completed interviews remain unchanged.

A retake creates a new interview instance.

Original Interview

        |
        v

New Interview

        |
        +--- New Questions
        |
        +--- New Answers

This preserves historical data.

⚡ Redis Caching

TalentForge uses Redis with the cache-aside pattern.

Example:

Request

   |
   v

Redis

   |
   +---- Cache Hit
   |
   +---- Cache Miss
             |
             v
        PostgreSQL
             |
             v
        Update Cache

Current caching:

Resume retrieval caching
TTL expiration
Cache invalidation on updates

Default TTL:

300 seconds
⚙️ Background Processing

Celery handles heavy operations.

Current tasks:

PDF Processing

      |
      v

Resume Extraction

      |
      v

AI Analysis

      |
      v

Database Update

Benefits:

Faster API responses
Better scalability
Retry handling for failures
🧾 Audit Logging

Important user actions are tracked.

Examples:

CREATE_INTERVIEW
RETAKE_INTERVIEW
DELETE_INTERVIEW
SUBMIT_ANSWER

Audit records:

id
user_id
action
entity_type
entity_id
🧱 Exception Architecture

TalentForge uses centralized application exceptions.

Examples:

UserAlreadyExistsException

InvalidCredentialsException

ResumeNotFoundException

ResumeAccessDeniedException

InterviewNotFoundException

QuestionAlreadyAnsweredException

AIProviderException

Benefits:

Consistent API responses
Cleaner services
Easier debugging
📊 Observability

The project includes foundations for production monitoring.

Current components:

Prometheus metrics
Grafana dashboards
Request logging middleware
Security middleware
🧪 Testing

Testing stack:

Pytest
FastAPI TestClient
Dependency overrides
Test database

Covered areas:

Application startup
Authentication
JWT flows
Protected routes
Resume workflows
Interview workflows
Answer evaluation
Dashboard services
AI services
🐳 Docker Architecture

Development environment:

              FastAPI

                 |
     -------------------------

     |          |            |

 PostgreSQL   Redis      Celery Worker

Docker services:

api
db
redis
celery_worker
pgadmin
🔄 CI/CD Pipeline

GitHub Actions validates every change.

Pipeline:

Push / Pull Request

          |
          v

Install Dependencies

          |
          v

Run Tests

          |
          v

Build Docker Image

          |
          v

Publish Image
📁 Project Structure
TalentForge

├── ai/
│   ├── providers/
│   ├── services/
│   ├── schemas.py
│   └── provider_factory.py
│
├── auth/
├── db/
├── exceptions/
├── middleware/
├── metrics/
├── models/
├── repositories/
├── routers/
├── schemas/
├── services/
├── tasks/
├── tests/
├── utils/
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── app.py
🚀 Running Locally
Clone
git clone https://github.com/<username>/TalentForge.git

cd TalentForge
Environment

Create:

.env

from:

.env.example
Start Services
docker compose up -d
Database Migration
docker compose exec api alembic upgrade head
API
http://localhost:8000

Swagger:

http://localhost:8000/docs
🎯 Engineering Principles

TalentForge is built around:

Separation of Concerns

Each layer owns a specific responsibility.

Dependency Injection

Components remain loosely coupled and testable.

Repository Pattern

Database logic is separated from business logic.

Service Layer

Business rules remain outside API routes.

Async Architecture

Heavy workloads are processed asynchronously.

Provider Abstraction

AI systems can evolve without rewriting application logic.

Production Thinking

Focus is placed on reliability, maintainability, security, and scalability.

🧭 Future Direction

TalentForge continues evolving toward a production-grade backend system.

Planned improvements:

Advanced observability
Kubernetes deployment
Distributed system patterns
More AI providers
Advanced system design improvements
Performance optimization
👨‍💻 Author

Satyam Shrestha

AI Computer Engineering Student

Building TalentForge as a long-term backend engineering project focused on learning and demonstrating how production systems are designed.