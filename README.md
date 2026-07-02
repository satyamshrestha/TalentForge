# TalentForge 🚀

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=sqlalchemy\&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis\&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Background%20Tasks-37814A?logo=celery\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions\&logoColor=white)

**Production-style backend engineering project built with FastAPI**

*Designed to explore scalable backend architecture, authentication, authorization, caching, asynchronous processing, containerization, CI/CD, and modern backend engineering practices.*

</div>

---

## 📖 Overview

TalentForge is a production-style backend platform developed to simulate how modern backend systems are built in industry.

Rather than focusing solely on CRUD operations, the project emphasizes clean architecture, secure authentication, scalable APIs, background processing, caching strategies, containerization, and continuous integration.

The long-term vision is to evolve TalentForge into an AI-powered interview preparation platform while using it as a practical playground for mastering backend engineering concepts and production-ready software development.


---

# Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL 17
* **ORM:** SQLAlchemy
* **Database Migrations:** Alembic
* **Caching:** Redis
* **Background Tasks:** Celery
* **Authentication:** JWT + OAuth2 Password Flow
* **Authorization:** Role-Based Access Control (RBAC)
* **OAuth2 Scopes:** JWT claims-based permissions
* **Containerization:** Docker & Docker Compose
* **Image Registry:** Docker Hub
* **CI/CD:** GitHub Actions
* **Testing:** Pytest + SQLite

---

# Project Architecture

```text
Client
   ↓
Routers (API Layer)
   ↓
Services (Business Logic)
   ↓
Repositories (Data Access)
   ↓
Database
```

Project follows a layered architecture:

```text
routers → services → repositories → database
```

---

# Current Features

## Authentication

* User Signup
* User Login
* Password Hashing (bcrypt)
* JWT Access Tokens
* JWT Refresh Tokens
* OAuth2 Password Flow
* Protected Routes
* Current User Dependency

---

## Authorization

### Role-Based Access Control (RBAC)

Roles:

* student
* teacher
* admin

Example:

* Admin-only endpoints
* Role verification dependencies
* Protected administrative actions

---

## OAuth2 Scopes

JWT tokens contain:

* sub
* role
* scopes
* exp
* type

Example admin token:

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

---

## Resume Module

* Resume Upload
* Resume Retrieval
* Resume Deletion
* Ownership Validation
* File Storage
* Status Tracking

Resume statuses:

* PENDING
* PROCESSING
* COMPLETED
* FAILED

---

## Caching

Redis cache-aside pattern:

* Read-through caching
* Cache invalidation
* Reduced database load
* TTL-based caching

---

## Background Processing

Celery Worker:

* Asynchronous task execution
* Background resume processing pipeline
* Redis-backed message broker

---

## Testing

* Authentication tests
* Protected route tests
* RBAC tests
* SQLite test database
* GitHub Actions CI pipeline

---

# Database Models

## User

* id
* email
* password
* role

## Resume

* id
* file_path
* parsed_text
* status
* error_message
* user_id

## Interview

* id
* user_id

## Question

* id
* interview_id

## Answer

* id
* question_id

---

# Docker Setup

Development:

```bash
docker compose up -d
```

Production:

```bash
docker compose -f docker-compose.prod.yml up -d
```

---

# Docker Hub

Image:

```text
satyamshrestha/talentforge:latest
```

Pull:

```bash
docker pull satyamshrestha/talentforge:latest
```

---

# Running Locally

## Clone

```bash
git clone https://github.com/<your-username>/TalentForge.git
cd TalentForge
```

## Create Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run with Docker

```bash
docker compose up -d
```

---

## Apply Migrations

```bash
docker compose exec api alembic upgrade head
```

---

## Run Tests

```bash
pytest
```

---

# CI/CD

GitHub Actions automatically:

* Runs tests on every push
* Validates application integrity
* Builds Docker images
* Prepares project for deployment

---

# Current Learning Goals

* Advanced OAuth2
* Permission-based authorization
* System Design
* Observability and Logging
* Kubernetes
* Distributed Systems
* Production Deployment

---

# Project Purpose

TalentForge is not merely a CRUD application.

It is an engineering playground built to learn:

* Backend Architecture
* Authentication & Authorization
* Caching Strategies
* Asynchronous Processing
* Containerization
* CI/CD
* Production Engineering Practices
* System Design Concepts

---

# Author

**Satyam Shrestha**

AI Computer Engineering Student
Far East University

Building one feature at a time with consistency and discipline.