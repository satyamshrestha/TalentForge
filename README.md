# TalentForge 🚀

TalentForge is a production-style backend project built to simulate a real-world AI-powered interview preparation platform while serving as my flagship project for learning advanced backend engineering concepts.

The project focuses on backend architecture, authentication, caching, asynchronous processing, DevOps, and system design concepts that are commonly used in modern software engineering.

---

# Features

## Authentication & Authorization

* User Signup
* User Login
* JWT Access Tokens
* Refresh Tokens
* OAuth2 Password Flow
* Protected Routes
* Current User Dependency
* Role-Based Access Control (RBAC)

---

## Resume Management

* Resume Upload
* Resume Parsing
* AI-powered Resume Analysis
* Resume Ownership Validation

---

## Interview System

* Generate Interviews From Resume Skills
* AI-generated Backend Questions
* Retake Previous Interviews
* Interview Statistics
* Interview Summary & Feedback
* Interview Details Endpoint
* Interview Deletion

---

## Dashboard

* User Dashboard Statistics
* Recent Interviews
* Completion Tracking

---

## Performance & Infrastructure

* Redis Caching
* Targeted Cache Invalidation
* Pagination
* Filtering
* Sorting
* Search Functionality

---

## Background Processing

* Celery Workers
* Redis Broker
* Asynchronous Tasks

---

## Logging & Monitoring

* Request Logging Middleware
* Request IDs
* Request Duration Tracking
* Client IP Logging
* Audit Logging

---

## Database

* PostgreSQL
* SQLAlchemy ORM
* Alembic Migrations
* ORM Relationships
* Foreign Keys
* Back Populates

---

## DevOps

* Docker
* Multi-Container Architecture
* Development & Production Compose Files
* Multi-Stage Docker Builds
* GitHub Actions Continuous Integration
* Docker Hub Image Publishing
* Continuous Delivery Pipeline (In Progress)

---

# Tech Stack

## Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic

## Database

* PostgreSQL

## Caching

* Redis

## Background Tasks

* Celery

## Authentication

* JWT
* OAuth2
* Passlib (bcrypt)

## DevOps

* Docker
* Docker Compose
* GitHub Actions
* Docker Hub

## Testing

* Pytest
* FastAPI TestClient

---

# Project Structure

```text
TalentForge
│
├── alembic/
├── api/
├── auth/
├── db/
├── middleware/
├── models/
├── repositories/
├── routers/
├── schemas/
├── services/
├── tasks/
├── tests/
├── uploads/
├── utils/
│
├── app.py
├── celery_app.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
└── README.md
```

---

# Architecture

```text
Client
   ↓
Routers
   ↓
Services
   ↓
Repositories
   ↓
Database
```

The project follows a layered architecture to maintain separation of concerns and improve maintainability.

---

# Database Relationships

```text
User
 ├── Resumes (1:M)
 └── Interviews (1:M)

Interview
 └── Questions (1:M)

Question
 └── Answer (1:1)
```

---

# Running Locally

## Clone Repository

```bash
git clone <repository-url>
cd TalentForge
```

---

## Create Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:database123@db:5432/talentforge
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

---

## Start Application

```bash
docker compose up --build
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Running Tests

```bash
pytest
```

---

# Continuous Integration

Every push to GitHub automatically:

1. Installs dependencies
2. Runs tests
3. Validates the application

---

# Docker Hub

TalentForge images are published to:

```text
docker.io/satyamshrestha/talentforge
```

---

# Learning Goals

TalentForge is primarily built to learn and implement:

* Production Backend Architecture
* OAuth2 & JWT Authentication
* Redis Caching Strategies
* Asynchronous Task Processing
* CI/CD Pipelines
* Docker & Containerization
* Kubernetes
* System Design
* Observability
* Scalable Backend Engineering Practices

---

# Current Status

```text
Authentication                 ✅
Role-Based Access Control      ✅
Resume System                  ✅
Interview System               ✅
Redis Caching                  ✅
Celery Background Tasks        ✅
Audit Logging                  ✅
Docker                         ✅
GitHub Actions (CI)            ✅
Docker Hub Publishing          ✅
Continuous Delivery            ⏳
Kubernetes                     ⏳
Observability                  ⏳
System Design                  ⏳
```

---

# Author

**Satyam Shrestha**

AI Computer Engineering Student
Backend & AI Engineering Enthusiast
Building TalentForge to master production backend engineering.