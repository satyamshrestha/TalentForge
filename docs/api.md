# TalentForge API Documentation

TalentForge exposes a RESTful API built with **FastAPI**.

The API follows a layered architecture:

```text
Client
  |
  ▼
Router
  |
  ▼
Service Layer
  |
  ▼
Repository Layer
  |
  ▼
Database
```

---

# Base URL

Development:

```text
http://localhost:8000
```

Production:

```text
http://localhost
```

API version:

```text
/api/v1
```

---

# Authentication

TalentForge uses **JWT-based authentication**.

Authentication flow:

```text
User
 |
 ▼
Login
 |
 ▼
JWT Access Token
 |
 ▼
Protected API Routes
```

Tokens are sent using:

```http
Authorization: Bearer <access_token>
```

---

# Auth Endpoints

## Register User

Creates a new TalentForge account.

### Request

```http
POST /api/v1/auth/signup
```

Body:

```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

---

## Login

Authenticates a user and returns JWT tokens.

### Request

```http
POST /api/v1/auth/login
```

Body:

```json
{
  "username": "john@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```

---

## Refresh Token

Creates a new access token using a refresh token.

### Request

```http
POST /api/v1/auth/refresh
```

Body:

```json
{
  "refresh_token": "jwt_refresh_token"
}
```

---

## Current User

Returns the authenticated user's information.

### Request

```http
GET /api/v1/auth/me
```

Requires authentication.

---

# Resume API

Resume processing is asynchronous.

Flow:

```text
Upload PDF
    |
    ▼
Validate File
    |
    ▼
Store Resume
    |
    ▼
Celery Task
    |
    ▼
Extract Text
    |
    ▼
AI Analysis
    |
    ▼
Completed Resume
```

---

## Upload Resume

Uploads a PDF resume.

### Request

```http
POST /api/v1/resumes/upload
```

Authentication required.

Content-Type:

```text
multipart/form-data
```

Example:

```text
file: resume.pdf
```

Initial response:

```json
{
  "id": "resume_id",
  "status": "PENDING"
}
```

---

## Get Resumes

Returns user's resumes.

### Request

```http
GET /api/v1/resumes
```

---

## Get Resume

Returns a specific resume.

### Request

```http
GET /api/v1/resumes/{resume_id}
```

---

## Delete Resume

Deletes a resume.

### Request

```http
DELETE /api/v1/resumes/{resume_id}
```

---

# Interview API

TalentForge generates interviews based on processed resumes.

Interview flow:

```text
Completed Resume
       |
       ▼
Question Generator
       |
       ▼
AI Generated Questions
       |
       ▼
Interview Session
```

---

## Create Interview

Creates an interview from a resume.

### Request

```http
POST /api/v1/interviews
```

Example body:

```json
{
  "resume_id": "resume_id",
  "target_role": "Backend Engineer"
}
```

---

## Get Interviews

Returns user interviews.

### Request

```http
GET /api/v1/interviews
```

---

## Get Interview

Returns a specific interview.

### Request

```http
GET /api/v1/interviews/{interview_id}
```

---

## Retake Interview

Creates a new interview attempt while preserving history.

### Request

```http
POST /api/v1/interviews/{interview_id}/retake
```

---

## Delete Interview

Deletes an interview.

### Request

```http
DELETE /api/v1/interviews/{interview_id}
```

---

# Question API

Questions belong to interview sessions.

---

## Get Question

Returns a specific interview question.

### Request

```http
GET /api/v1/questions/{question_id}
```

---

# Answer API

Answers are evaluated using AI.

Flow:

```text
Question + Answer
        |
        ▼
Answer Evaluator
        |
        ▼
AI Provider
        |
        ▼
Feedback + Score
```

---

## Submit Answer

Submits an answer for evaluation.

### Request

```http
POST /api/v1/answers
```

Body:

```json
{
  "question_id": "question_id",
  "answer_text": "Candidate response"
}
```

Response:

```json
{
  "answer_text": "Candidate response",
  "feedback": "AI feedback",
  "score": 8,
  "suggested_improvement": "Improve explanation depth"
}
```

A question can only be answered once.

---

# Dashboard API

Provides aggregated interview statistics.

---

## Get Dashboard

Returns user analytics.

### Request

```http
GET /api/v1/dashboard
```

Example response:

```json
{
  "total_resumes": 3,
  "total_interviews": 5,
  "completed_interviews": 4,
  "average_score": 8.2
}
```

---

# Profile API

Manages user profile information.

---

## Get Profile

```http
GET /api/v1/profile
```

---

## Update Profile

```http
PUT /api/v1/profile
```

---

# Admin API

Admin endpoints require administrator privileges.

Authorization uses:

- JWT authentication
- Role-based access control
- OAuth2 scopes

---

# Health API

Health endpoints are used for monitoring and deployment checks.

---

## Liveness Check

```http
GET /api/v1/health/live
```

Example response:

```json
{
  "status": "ok"
}
```

---

## Metrics

Application metrics endpoint.

```http
GET /api/v1/metrics
```

---

# Error Handling

TalentForge uses centralized application exceptions.

Example error response:

```json
{
  "detail": "Resume does not exist!"
}
```

Common errors:

| Status Code | Meaning |
|---|---|
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Resource conflict |
| 500 | Internal server error |

---

# Authorization

TalentForge supports:

- JWT authentication
- Role-based authorization
- OAuth2 scopes
- Ownership validation

Example roles:

```text
student
teacher
admin
```

Example scopes:

```text
resume:read
resume:write
interview:create
interview:delete
admin
```

---

# AI Integration

AI functionality is abstracted behind providers.

Architecture:

```text
AI Service
     |
     ▼
Provider Factory
     |
     ▼
Ollama Provider
     |
     ▼
LLM
```

Current production provider:

```text
Ollama
```

Future providers can be added without modifying business logic.

---

# API Documentation UI

FastAPI automatically provides interactive documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Summary

TalentForge API is designed around:

- REST principles
- Layered architecture
- JWT authentication
- Role and scope authorization
- Asynchronous processing
- AI provider abstraction
- Centralized error handling
- Production-style backend practices