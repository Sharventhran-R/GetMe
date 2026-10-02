# PROJECT: Community Missing Item & Asset Tracker

## 1. Product Objective
Build a community-based platform for reporting, discovering, matching, and recovering missing people, pets, items, and other assets based on geographic location.
The platform should allow people in a community to publish missing or found reports and allow other users in the same or nearby geographic area to discover those reports.

The system should support:
- Missing item reports
- Found item reports
- Missing pet reports
- Found pet reports
- Missing-person reports where appropriate and legally permitted
- General missing/found asset reports
- Geographic/radius-based discovery
- Interactive maps
- Images/photos
- Descriptions
- Categories
- Date/time information
- Rewards offered by report owners
- Potential match detection
- Claim requests
- Claim verification
- Notifications
- Report resolution
- User accounts
- Abuse/spam prevention

The primary differentiating capability is location-aware community discovery.
A user should be able to say: "I lost my wallet near this location."
The system should allow other users within a configurable geographic radius to discover that report.
Likewise, someone who finds an item can publish a found report, and the system can identify nearby potential matches.

## 2. Supported Platforms
The application must support BOTH:
- **Mobile**
  Use Flutter for Android and iOS.
  Mobile capabilities should include: GPS/location access, Interactive map, Nearby reports, Radius selection, Report creation, Report images, Report details, Claims, Notifications, User account, My reports.
- **Web / PC**
  The same Flutter codebase should also support Flutter Web.
  Users should be able to access the application through desktop browsers such as Chrome, Edge, Firefox.
  The web application should provide: Responsive desktop interface, Interactive map, Nearby reports, Report creation, Report management, Authentication, Claims, User dashboard, Search/filtering.

The backend must be client-independent.
Architecture:
```
Flutter Mobile ───────┐
                      │
Flutter Web ──────────┼──→ FastAPI REST API
                      │         ▼
                      │    PostgreSQL + PostGIS
                      │         ▼
                      │    Kafka
```
Do NOT create separate backend implementations for mobile and web. Both clients must use the same backend APIs and business logic.

## 3. Planned Technology Stack
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2, PostgreSQL, PostGIS, JWT authentication, pytest, Ruff, mypy
- **Messaging / Event Processing**: Apache Kafka, aiokafka.
  Kafka will eventually be used for asynchronous workflows (report-created events, potential-match events, etc.). Kafka must NOT be used unnecessarily for normal synchronous CRUD/database operations.
- **Frontend**: Flutter, Dart (Flutter Web, Android, iOS) communicating via REST APIs.
- **Infrastructure**: Docker, Docker Compose
  Potential future technologies (Redis, object storage, etc.) must only be introduced when justified by an actual requirement.

## 4. Python Development Environment
The backend must use a project-local Python virtual environment: `.venv/`
Requirements:
- Python 3.12+
- Never install project dependencies globally
- Use `.venv` for development (must be ignored by Git)
- Use `python -m pip`, `python -m pytest`, `python -m ruff`, `python -m mypy`
- Project should contain `requirements.txt` and `pyproject.toml` (with Ruff, mypy, pytest configs).
- Strict typing with zero tolerance for unnecessary `Any`, untyped functions, `# type: ignore`, dead code, or unused imports.

## 5. High-Level Architecture
```
┌───────────────────┐     │     Flutter Mobile    │     │     Android / iOS     │
└─────────┬─────────┘     │
┌─────────▼─────────┐     │
Flutter Web         │     │
Desktop Browser     │
└─────────┬─────────┘     │
REST / JSON               │
▼
┌───────────────────┐     │
FastAPI             │     │
│                   │     │
Authentication      │     │
Reports             │     │
Claims              │     │
Search              │     │
Business Logic      │
└───────┬─────┬─────┘     │
│             │
┌───────┘             └───────────┐
▼                           ▼
┌───────────────┐     ┌──────────────┐
│ PostgreSQL    │     │ Kafka        │
│ + PostGIS     │     │              │
│               │     │ Events       │
│ Users         │     │ Topics       │
│ Reports       │     └──────┬───────┘
│ Claims        │            │
│ Locations     │            │
┌────────┼─────────┐     └───────────────┘
▼        ▼         ▼
Matching Notification Analytics
Consumer Consumer Consumer
```

## 6. PostgreSQL + PostGIS
PostgreSQL is the primary relational database. PostGIS provides geographic capabilities.
The eventual system should use geographic types such as `GEOGRAPHY(POINT, 4326)` for report locations.
PostGIS will support radius searches, distance calculations, nearby report discovery, geographic filtering, spatial indexing (GiST), and location-based matching.
PostGIS should be responsible for actual geographic calculations.

## 7. Kafka Architecture
Kafka is an important part of the eventual distributed architecture but should be introduced only in its designated phase.
The intended architecture is:
```
FastAPI
│
├── PostgreSQL/PostGIS
│
└── Kafka Producer
    │
    ├── report-events
    ├── match-events
    ├── claim-events
    └── notification-events
    │
    ├── Matching Consumer
    ├── Notification Consumer
    └── Analytics Consumer
```
The API should remain responsive while asynchronous workflows are processed independently. Kafka should provide meaningful decoupling.

## 8. Core Domain Concepts
- **User**: Authenticated application user.
- **Report**: Missing or found report (MISSING, FOUND).
- **Claim**: User's attempt to claim or verify ownership of a found item.
- **Potential Match**: Possible relationship between a missing report and a found report.
- **Notification**: Event communicated to a user.
- **Report Status**: ACTIVE, POTENTIAL_MATCH, CLAIMED, VERIFIED, RESOLVED, EXPIRED.
Do not implement all concepts immediately.

## 9. Missing/Found Workflow
- **Missing Workflow**: User -> Creates missing report -> FastAPI -> DB/Kafka -> Matching -> Notifications -> Claim/Verification -> Recovery -> Resolved.
- **Found Workflow**: User -> Creates found report -> PostGIS nearby search -> Matching -> Notifications -> Verification -> Item returned -> Resolved.

## 10. Matching System
Start with deterministic signals (Geographic distance, Category, Description similarity, Time proximity, Report type).
A future version may introduce embeddings or ML-based matching if there is a demonstrated requirement. Do not introduce ML prematurely.

## 11. Maps
Interactive map supporting: User location, Missing/Found markers, Potential-match indicators, Report details, Search radius, Map movement.
Mobile uses GPS, Web uses browser geolocation (handle lack of permissions gracefully).

## 12. Rewards
Reward information is metadata associated with a report. Do NOT implement payment processing unless explicitly added as a future requirement.

## 13. Authentication & Security
Eventual application must use JWT authentication. Security requirements: Registration, Login, Password hashing, Protected endpoints, Authorization, User ownership checks, Rate limiting, Spam/duplicate prevention, Secure environment variables. No secrets in Git.

## 14. Development Roadmap
- **Phase 0 — Agentic Workspace**: (Current) Setup environment, guardrails, docs.
- **Phase 1 — Backend Infrastructure**: FastAPI, PostgreSQL, PostGIS, Docker Compose, configuration, initial tests. (No auth, no reports, no Kafka, no Flutter).
- **Phase 2 — Database Domain Model**: User, Report, Location, statuses, Alembic migrations.
- **Phase 3 — Authentication & Authorization**: JWT, roles, ownership validation.
- **Phase 4 — Missing/Found Reports**: CRUD, status, images abstraction, rewards.
- **Phase 5 — PostGIS Geospatial Search**: Spatial indexes, radius searches.
- **Phase 6 — Flutter Mobile + Web**: Shared codebase for Android, iOS, Chrome, Edge, Firefox.
- **Phase 7 — Kafka Event Architecture**: Producers, consumers, topics.
- **Phase 8 — Matching Engine**: Deterministic matching.
- **Phase 9 — Notifications**: Notification system.
- **Phase 10 — Security & Abuse Prevention**: Rate limiting, spam prevention.
- **Phase 11 — Testing & Observability**: Logs, tracing, comprehensive tests.
- **Phase 12 — Production Hardening**: Deploy, scaling.

## 15. Phase Control Rules
Only the currently authorized phase may be implemented. The agent MUST NOT autonomously jump ahead. If a later-phase dependency appears necessary, stop, explain, and ask for authorization.

## 16. Engineering Principles
Prioritize: Correctness, Maintainability, Strong typing, Testability, Separation of concerns, Minimal dependencies, Small diffs, Good error handling.
Avoid: Premature optimization, unnecessary abstraction, microservices, ML, payment processing, untyped code.

## 17. Agentic Development Workflow
PLAN -> IMPLEMENT -> TEST -> VERIFY -> REVIEW DIFF -> UPDATE AGENT_MEMORY.md -> COMMIT -> NEXT AUTHORIZED TASK
Every milestone must have explicit acceptance criteria. Must run relevant tests before completing tasks.

## 18. Current Project State
The project is currently in: **Phase 0 — Agentic Workspace Initialization**.
The next authorized phase is: **Phase 1 — Backend Infrastructure** (Do NOT start yet).

## 19. Current Workspace Files
```
project/
├── .venv/
├── app/
├── tests/
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── AGENTS.md
├── AGENT_MEMORY.md
├── PROJECT_SPEC.md
└── README.md
```

## 20. Separation of Responsibilities
- **AGENTS.md**: HOW the agent works (rules, commands, guardrails). References AGENT_MEMORY.md using `@[Project Memory](AGENT_MEMORY.md)`.
- **PROJECT_SPEC.md**: WHAT the project is (objectives, roadmap, architecture).
- **AGENT_MEMORY.md**: WHAT HAS ALREADY HAPPENED (current state, log, architecture decisions).
