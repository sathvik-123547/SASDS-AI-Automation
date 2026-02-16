# ⚙️ Backend Documentation

> SASDS Backend — FastAPI-Powered AI Service Layer

---

## Overview

The SASDS backend is a high-performance, asynchronous API built with **FastAPI**. It serves as the orchestration layer between the React frontend and Google's Gemini AI, managing code generation, project analysis, file operations, terminal sessions, and conversational AI.

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **FastAPI** | 0.109+ | Async web framework |
| **Uvicorn** | 0.27+ | ASGI server |
| **Google Generative AI** | 0.3.2+ | Gemini API SDK |
| **SQLAlchemy** | 2.0+ | Database ORM |
| **Pydantic** | 2.6+ | Data validation & serialization |
| **Pydantic Settings** | 2.1+ | Environment configuration |
| **Redis** | 5.0+ | Task queue backend |
| **Celery** | 5.3+ | Distributed task processing |
| **Pytest** | 8.0+ | Testing framework |
| **HTTPX** | 0.26+ | Async HTTP client (testing) |

---

## Directory Structure

```
backend/
├── app/
│   ├── core/
│   │   └── config.py           # Settings class (env vars)
│   ├── db/                     # Database models and connections
│   ├── routers/                # 13 API route handlers
│   │   ├── autopilot.py        # POST /autopilot/analyze
│   │   ├── chat.py             # POST /chat/send
│   │   ├── code_writer.py      # File writing endpoint
│   │   ├── codegen.py          # POST /code/generate, /code/generate/stream
│   │   ├── files.py            # CRUD: /files/create, /delete, /rename
│   │   ├── github_sync.py      # GitHub repository sync
│   │   ├── projects.py         # GET /projects/, /projects/{id}/download
│   │   ├── refine.py           # POST /refine/
│   │   ├── requirements.py     # POST /requirements/analyze
│   │   ├── review.py           # Code review endpoint
│   │   ├── runs.py             # Execution run history
│   │   ├── self_corrector.py   # Self-correction trigger
│   │   ├── terminal.py         # WS /terminal/ws
│   │   └── test_generator.py   # Test generation
│   ├── schemas/                # Pydantic models
│   │   ├── codegen.py          # CodeGenerationRequest/Response
│   │   ├── requirements.py     # RequirementAnalysisRequest/Response
│   │   ├── review.py           # CodeReviewRequest/Response
│   │   └── tests.py            # TestGenerationRequest/Response
│   ├── services/               # Business logic
│   │   ├── auto_pilot.py       # Project-wide AI analysis
│   │   ├── chat_agent.py       # Context-aware chat
│   │   ├── code_generator.py   # Code gen (batch + stream + refine)
│   │   ├── code_reviewer.py    # Structured code review
│   │   ├── fix_generator.py    # Bug fix generation
│   │   ├── gemini_client.py    # Requirements analysis
│   │   ├── github_sync.py      # GitHub API integration
│   │   ├── metadata_store.py   # SQLite event logging
│   │   ├── self_corrector.py   # Iterative test-fix loop
│   │   └── test_generator.py   # Test file generation
│   └── utils/                  # Shared utilities
│       ├── file_writer.py      # File I/O operations
│       └── test_runner.py      # Pytest execution wrapper
├── tests/                      # Test suite
├── generated_projects/         # Output directory for AI-generated code
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
└── pyproject.toml              # Project metadata
```

---

## Key Services

### 1. Requirements Analyzer (`gemini_client.py`)

Transforms natural language into a structured analysis containing modules, entities, APIs, non-functional requirements, and tech stack suggestions.

- **Function:** `analyze_requirements_with_gemini(requirements_text)`
- **AI Model:** Gemini 2.5 Flash
- **Output:** Strict JSON validated against Pydantic schema

### 2. Code Generator (`code_generator.py`)

The core service with three modes of operation:

| Mode | Function | Use Case |
|---|---|---|
| **Batch** | `generate_code_with_gemini()` | Returns complete JSON with all files |
| **Streaming** | `generate_code_with_gemini_stream()` | Yields text chunks for real-time UI |
| **Refinement** | `refine_code_with_gemini()` | Modifies a single file based on instructions |

### 3. Self-Corrector (`self_corrector.py`)

Implements a closed-loop test-fix cycle:
1. Runs `pytest` on the generated project
2. Parses output to identify failing files
3. Sends failing code + error to Gemini for fix
4. Writes fix and repeats (max 3 attempts)

### 4. Auto-Pilot (`auto_pilot.py`)

Performs holistic project analysis:
- Reads all source files (`.py`, `.js`, `.ts`, `.html`, etc.)
- Skips `node_modules`, `.venv`, `__pycache__`
- Returns severity-rated issues and categorized improvements

### 5. Chat Agent (`chat_agent.py`)

Context-aware conversational assistant that:
- Maintains conversation history via the Gemini Chat API
- Injects current file content and project structure as context
- Truncates files over 20KB to manage token limits

### 6. Code Reviewer (`code_reviewer.py`)

Returns structured reviews with:
- Summary assessment
- Issue list with severity (info → critical), file, line, and recommendation

### 7. Terminal Service (`terminal.py`)

Full WebSocket-based PTY terminal:
- Spawns a pseudo-terminal via Python's `pty` module
- Bidirectional communication (input/output) over WebSocket
- Supports terminal resize events
- Handles process cleanup on disconnect

---

## Configuration Reference

Managed via `app/core/config.py` and `backend/.env`:

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ | — | Google Gemini API key |
| `GEMINI_MODEL_NAME` | ❌ | `models/gemini-2.5-flash` | AI model identifier |
| `DB_URL` | ❌ | `sqlite:///./metadata.sqlite` | Database connection string |
| `GITHUB_TOKEN` | ❌ | — | GitHub PAT for sync |
| `GITHUB_REPO` | ❌ | — | Target repo (`owner/repo`) |
| `GITHUB_BRANCH` | ❌ | `main` | Target Git branch |

---

## Running the Backend

### Development
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key_here" > .env
uvicorn app.main:app --reload --port 8000
```

### Docker
```bash
docker compose up backend
```

### Running Tests
```bash
cd backend
pytest
```

---

## Middleware & Infrastructure

| Middleware | Purpose |
|---|---|
| **CORS** | Allows cross-origin requests (configurable) |
| **Request Logger** | Logs method, path, status code, and response time for every request |
| **Error Handler** | Catches unhandled exceptions and returns structured JSON errors |
