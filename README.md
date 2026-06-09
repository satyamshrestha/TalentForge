# TalentForge

TalentForge is an AI-powered interview preparation platform built with FastAPI and modern backend engineering practices.

The goal of the project is to help users upload resumes, generate interview questions, practice interviews, receive feedback, and prepare for technical and behavioral interviews.

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic

### Authentication

* JWT Access Tokens
* Refresh Tokens
* OAuth2 Password Flow

### Infrastructure

* Docker Compose
* Redis
* Celery

### Future AI Layer

* Resume Analysis
* Interview Question Generation
* Answer Evaluation
* Feedback Engine

---

## Current Features

### Authentication

* User Registration
* User Login
* Password Hashing
* JWT Authentication
* Refresh Tokens
* Protected Endpoints

### Resume Management

* Upload Resume PDFs
* Resume Ownership Validation
* Retrieve Uploaded Resumes
* Delete Resumes
* Redis Caching

### Resume Processing Pipeline

1. User uploads a PDF resume.
2. Resume metadata is stored in PostgreSQL.
3. Resume is queued for background processing using Celery.
4. Worker extracts text from the PDF.
5. Resume parser extracts structured information.
6. Parsed data is stored in the database.

### Extracted Resume Data

* Name
* Email
* Phone Number
* Skills
* Education
* Experience
* Raw Resume Text
* Page Count

### Resume Status Lifecycle

* PENDING
* PROCESSING
* COMPLETED
* FAILED

---

## Project Structure

```text
TalentForge/
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
├── tasks.py
├── tests/
├── utils/
│
├── celery_app.py
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Current Architecture

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

Background Processing:

```text
Upload PDF
    ↓
FastAPI Endpoint
    ↓
Database Record
    ↓
Celery Queue
    ↓
Worker
    ↓
PDF Parsing
    ↓
Structured Resume Data
    ↓
Database
```

---

## Roadmap

### Completed

* Authentication System
* JWT Authorization
* Redis Integration
* Celery Integration
* Resume Uploads
* PDF Parsing
* Structured Resume Extraction

### In Progress

* Resume Intelligence Improvements

### Planned

* Interview Generation
* Question Bank
* Answer Submission
* AI Feedback Engine
* File Storage Improvements
* CI/CD Pipeline
* Kubernetes Deployment
* Monitoring & Observability
* Production Architecture

---

## Author

Satyam Shrestha

AI Computer Engineering Student

Building TalentForge as a production-grade backend engineering project while mastering modern software engineering practices.