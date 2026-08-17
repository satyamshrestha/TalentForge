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

An OpenAI provider exists in the codebase as a placeholder for future integration and is not the current production AI backend.

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

14. WebSocket Architecture

TalentForge supports WebSocket-based real-time communication for interactive application workflows.

The WebSocket architecture is intentionally separated from the REST API layer.

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
WebSocket Endpoint
  │
  ▼
Connection Manager
  │
  ▼
Application Service
  │
  ├───────────────┐
  ▼               ▼
PostgreSQL       Redis

The WebSocket layer is responsible for connection lifecycle management rather than business logic.

Connection
     │
     ▼
Authentication
     │
     ▼
Accept Connection
     │
     ▼
Register Connection
     │
     ▼
Receive / Send Events
     │
     ▼
Disconnect
     │
     ▼
Remove Connection

A connection manager maintains active connections.

Conceptually:

Connection Manager
       │
       ├── User A ─── WebSocket
       ├── User B ─── WebSocket
       └── User C ─── WebSocket

This provides a centralized location for:

Connection registration
Connection removal
Sending messages to individual clients
Broadcasting events
Handling disconnects
Real-Time Interview Updates

WebSockets are particularly useful for real-time interview workflows.

For example:

Interview Processing
       │
       ▼
Application Event
       │
       ▼
WebSocket Layer
       │
       ▼
Connected Client

A client can receive events such as:

INTERVIEW_STARTED
QUESTION_AVAILABLE
ANSWER_SUBMITTED
ANSWER_EVALUATED
INTERVIEW_COMPLETED

The exact event types can evolve independently from the WebSocket transport.

REST vs WebSocket

TalentForge uses both communication models for different responsibilities.

Communication	Purpose
REST	CRUD operations and request/response workflows
WebSocket	Real-time events and live application updates
Celery	Long-running asynchronous processing
Redis	Caching and infrastructure support

This prevents WebSockets from being used where ordinary REST requests are more appropriate.

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

18. CI/CD Architecture

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

19. Dependency Flow

A major architectural principle is controlling dependency direction.

The intended REST flow is:

Router
  ↓
Service
  ↓
Repository
  ↓
Database

The intended WebSocket flow is:

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

20. Design Principles

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

21. Architectural Goal

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

The goal is to evolve TalentForge as a maintainable, testable, observable, and deployable backend system while keeping the architecture understandable as the project grows.