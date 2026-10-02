@[Project Memory](AGENT_MEMORY.md)

## Tech Stack
- Backend: Python 3.12+, FastAPI, SQLAlchemy 2.x, PostgreSQL/PostGIS, aiokafka, Pydantic v2.
- Testing: pytest
- Linting/Formatting: Ruff
- Type Checking: mypy

## Canonical Commands (Windows)
- Create environment: `python -m venv .venv`
- Activate environment: `.venv\Scripts\Activate.ps1`
- Install dependencies: `.venv\Scripts\python.exe -m pip install -r requirements.txt`
- Run backend: `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
- Lint: `.venv\Scripts\python.exe -m ruff check .`
- Format check: `.venv\Scripts\python.exe -m ruff format --check .`
- Typecheck: `.venv\Scripts\python.exe -m mypy .`
- All tests: `.venv\Scripts\python.exe -m pytest`
- Single test: `.venv\Scripts\python.exe -m pytest path/to/test_file.py::test_name -q`

## Execution Guardrails
1. **Minimal Diffs**: Make precise, in-place edits. Do not rewrite files unnecessarily.
2. **Strict Typing**: Zero tolerance for untyped or loose variables. All Python code must pass `mypy --strict`.
3. **Mandatory Tests**: Run the appropriate single-test or typecheck command before marking a task as complete.
4. **Session Logging**: Update `AGENT_MEMORY.md` under `# Session Log` after completing substantive milestones.
5. **No Global Dependencies**: Use `.venv\Scripts\python.exe` for all tool executions.
