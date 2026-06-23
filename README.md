# TalentForge

TalentForge is a production-style backend project built to learn advanced backend engineering concepts including authentication, caching, asynchronous processing, testing, containerization, CI/CD, and eventually system design, observability, and Kubernetes.

The project simulates an AI-powered interview preparation platform where users can upload resumes, generate backend interview questions, take interviews, and receive feedback.

---

# Tech Stack

## Backend

* FastAPI
* Python 3.12
* SQLAlchemy ORM
* Alembic

## Database

* PostgreSQL

## Caching

* Redis

## Asynchronous Tasks

* Celery

## Authentication

* JWT Access Tokens
* Refresh Tokens
* OAuth2 Password Flow

## Containerization

* Docker
* Docker Compose

## DevOps

* GitHub Actions (CI/CD)
* Docker Hub

## Testing

* Pytest
* FastAPI TestClient
* SQLite test database

---

# Features

## Authentication

* User Signup
* User Login
* Password Hashing using bcrypt
* JWT Access Tokens
* Refresh Tokens
* Protected Routes
* Current User Endpoint

## Resume Module

* Resume Upload
* PDF Storage
* Resume Retrieval
* Resume Deletion
* Ownership Validation
* Redis Caching
* Celery Processing Hook

## Interview Module

* Interview Generation from Resume Skills
* Interview Retake
* Interview Statistics
* Interview Summary
* Pagination
* Filtering by Status
* Interview Deletion

## Audit Logging

* User Action Tracking
* Interview Activity Logging

---

# Architecture

The project follows a layered architecture:

```text
Routers
↓
Services
↓
Repositories
↓
Database
```

Folder Structure:

```text
api/
auth/
db/
middleware/
models/
repositories/
routers/
schemas/
services/
tasks/
tests/
utils/
```

---

# Database Models

* User
* Resume
* Interview
* Question
* Answer

Relationships:

```text
User
 ├── Resumes
 └── Interviews

Interview
 └── Questions

Question
 └── Answer
```

---

# Docker Setup

## Development Environment

```bash
docker compose up -d
```

Services:

* FastAPI API
* PostgreSQL
* Redis
* Celery Worker
* pgAdmin

---

## Production Environment

```bash
docker compose -f docker-compose.prod.yml up -d
```

---

# Running Locally

Create a virtual environment:

```bash
python -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn app:app --reload
```

---

# Running Tests

```bash
pytest
```

---

# CI/CD Pipeline

The project uses GitHub Actions.

Workflow:

```text
git push
    ↓
Run Tests
    ↓
Build Docker Image
    ↓
Push Image to Docker Hub
```

Docker image:

```text
docker.io/satyamshrestha/talentforge
```

---

# Current Learning Goals

* OAuth2 Authentication
* System Design
* Observability
* Kubernetes
* Production Deployment

---

# Future Features

* AI Resume Parsing
* AI Interview Feedback
* Email Notifications
* Monitoring and Logging
* Kubernetes Deployment
* Cloud Deployment
* API Rate Limiting
* Distributed Caching
* Microservices Exploration

---

# Purpose

TalentForge is primarily a learning project designed to gain hands-on experience with production backend engineering concepts and industry practices.