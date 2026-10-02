# Project Memory

## Current State
- Initialized Python backend setup with FastAPI, SQLAlchemy, PostgreSQL, PostGIS, aiokafka, and JWT authentication.
- Configured Ruff for linting and formatting.
- Configured mypy for strict type checking.
- Configured pytest for testing.

## Architectural Decisions
- Backend: Python 3.12+, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, PostGIS, Pydantic v2.
- Messaging: Apache Kafka (aiokafka).
- Frontend: Flutter, Dart (to be implemented).
- Environment: Project-local `.venv`.
- Guardrails: Strict type checking, no untyped variables, minimal diffs, mandatory tests before task completion.

## Session Log
- 2026-10-02: Initialized agentic workflow guardrails.
