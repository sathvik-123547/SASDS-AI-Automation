# SASDS — Pseudocode Explanation

> Detailed explanation of the broad project pseudocode

---

## Overview

This document explains the high-level pseudocode used to describe the SASDS (Single Agent Software Development System) project flow. The pseudocode is intentionally broad and abstracts implementation details to convey the conceptual flow.

---

## 1. PROGRAM SASDS_MAIN

### Pseudocode

```
PROGRAM SASDS_MAIN:
    INIT backend_server
    INIT frontend_app
    MOUNT routers (requirements, codegen, files, chat, terminal, ...)
    START API on port 8000
    START frontend on port 5173
    LISTEN for requests
END PROGRAM
```

### Explanation

**Purpose:** This is the entry point that bootstraps the entire SASDS application.

| Step | Description |
|------|-------------|
| **INIT backend_server** | Creates the FastAPI application instance. Loads configuration (e.g., `GEMINI_API_KEY`, `DB_URL`), sets up CORS, and registers middleware for request logging and error handling. |
| **INIT frontend_app** | Builds the React application (Vite + TypeScript). The frontend is a single-page app with components for requirements input, file explorer, code viewer, terminal, and chat. |
| **MOUNT routers** | Registers API route handlers. Each router maps HTTP endpoints to service functions: `requirements` → analyze, `codegen` → generate (batch/stream), `code_writer` → write files, `files` → CRUD, `chat` → agent chat, `terminal` → WebSocket PTY, `autopilot` → project analysis, `self_fix` → test-fix loop, etc. |
| **START API on port 8000** | Launches Uvicorn ASGI server. The backend listens for REST and WebSocket requests. |
| **START frontend on port 5173** | Launches Vite dev server (or serves built assets in production). The UI is available at `http://localhost:5173`. |
| **LISTEN for requests** | Both servers run until shutdown. The frontend sends HTTP/WebSocket requests to the backend, which orchestrates AI and persistence. |

**In actual code:** `backend/app/main.py` initializes the FastAPI app and mounts routers; `frontend/` is a Vite React app served separately.

---

## 2. PROGRAM REQUIREMENTS_TO_PROJECT

### Pseudocode

```
PROGRAM REQUIREMENTS_TO_PROJECT (user_requirements):
    // Phase 1: Analyze
    analysis = AI_AGENT.analyze(user_requirements)
    STORE log in DATABASE
    RETURN analysis to USER

    // Phase 2: Generate
    LOOP stream chunk FROM AI_AGENT.generate_code(user_requirements, analysis):
        PARSE chunk for ### FILE: path
        DISPLAY chunk to USER
    END LOOP

    // Phase 3: Persist
    project_id = GENERATE uuid
    FOR each file IN parsed_files:
        WRITE file TO generated_projects/project_id/path
    END FOR
    RETURN project_id to USER

    // Optional: Self-fix
    IF user requests self-fix:
        RUN self_correction_loop(project_id)
    END IF

    // Optional: Chat / Refine / Auto-Pilot
    IF user sends chat message:
        context = READ project from DATABASE
        response = AI_AGENT.chat(message, context)
        RETURN response to USER
    END IF
END PROGRAM
```

### Explanation

**Purpose:** Describes the end-to-end pipeline from natural language requirements to a working project on disk, plus optional self-correction and chat.

#### Phase 1: Analyze

| Step | Description |
|------|-------------|
| **AI_AGENT.analyze(user_requirements)** | Sends the raw text to Google Gemini. The AI returns structured JSON with `modules`, `entities`, `apis`, `tech_stack_suggestions`, `missing_information`, etc. This breakdown guides the code generator. |
| **STORE log in DATABASE** | A `RunLog` row is inserted (kind: "analysis", payload: JSON). Used for audit and run history. |
| **RETURN analysis to USER** | The frontend displays the structured analysis so the user can review before generating code. |

**API:** `POST /requirements/analyze`

#### Phase 2: Generate

| Step | Description |
|------|-------------|
| **LOOP stream chunk** | Gemini streams text chunks. The backend uses `generate_content_stream()` and yields chunks via `StreamingResponse`. |
| **PARSE chunk for ### FILE: path** | The stream uses a delimiter protocol: `### FILE: path` marks the start of a file; `### END FILE ###` marks the end. The frontend's `parseStreamBuffer()` uses regex to extract path and content. |
| **DISPLAY chunk to USER** | As chunks arrive, the UI updates the file tree and code viewer in real time. |

**API:** `POST /code/generate/stream`

#### Phase 3: Persist

| Step | Description |
|------|-------------|
| **project_id = GENERATE uuid** | A unique ID (e.g., `project_abc123`) identifies the project. |
| **WRITE file TO generated_projects/project_id/path** | Each parsed file is written to `backend/generated_projects/{project_id}/{path}`. Directories are created as needed. |
| **RETURN project_id to USER** | The frontend can then list files, run Auto-Pilot, or trigger self-fix using this ID. |

**API:** `POST /code/write`

#### Optional: Self-fix

If the user clicks "Self-Fix," the system runs `self_correction_loop(project_path)` to automatically fix failing tests. See Section 3.

#### Optional: Chat / Refine / Auto-Pilot

| Feature | Description |
|---------|-------------|
| **Chat** | User sends a message; the AI agent receives `message`, `history`, and `context` (selected file, project structure). Gemini returns a conversational response. |
| **Refine** | User selects a file and gives NL instructions (e.g., "Add input validation"). The AI returns modified content. |
| **Auto-Pilot** | Scans all project files, sends them to Gemini, and returns `issues` (bugs, security) and `improvements` (refactor, feature suggestions). |

**APIs:** `POST /chat/send`, `POST /refine/`, `POST /autopilot/analyze`

---

## 3. PROGRAM SELF_CORRECTION_LOOP

### Pseudocode

```
PROGRAM SELF_CORRECTION_LOOP (project_path):
    FOR attempt = 1 TO max_attempts:
        (passed, output) = RUN pytest IN project_path
        IF passed: RETURN success
        failing_file = DETECT from output
        IF NOT failing_file: RETURN failure
        content = READ failing_file
        fixed = AI_AGENT.generate_fix(failing_file, content, output)
        WRITE fixed TO failing_file
    END FOR
    RETURN max_attempts_reached
END PROGRAM
```

### Explanation

**Purpose:** Automatically fix failing tests by running pytest, detecting the failing file, asking the AI for a fix, and rewriting the file. Repeats up to `max_attempts` (default 3).

| Step | Description |
|------|-------------|
| **RUN pytest IN project_path** | Spawns a subprocess that runs `pytest` in the generated project directory. Captures stdout/stderr. |
| **IF passed** | All tests pass → return success immediately. |
| **failing_file = DETECT from output** | Parses pytest output (e.g., `tests/test_sample.py:12: AssertionError`) to find the first failing `.py` file that exists on disk. Uses regex to extract path. |
| **IF NOT failing_file** | If the failing file cannot be detected (e.g., setup error), return failure. |
| **content = READ failing_file** | Loads the full file content. |
| **fixed = AI_AGENT.generate_fix(...)** | Sends the file path, original content, and pytest error output to Gemini. The AI returns corrected code. |
| **WRITE fixed TO failing_file** | Overwrites the file with the fix. The next loop iteration will run pytest again. |
| **max_attempts_reached** | If tests still fail after all attempts, return this status. |

**In actual code:** `backend/app/services/self_corrector.py` and `fix_generator.py`; called via `POST /self/fix`.

---

## 4. PROGRAM API_REQUEST_HANDLER

### Pseudocode

```
PROGRAM API_REQUEST_HANDLER (method, path, body):
    VALIDATE body with Pydantic
    ROUTE to appropriate service
    CALL service function
    LOG event to DATABASE
    RETURN response OR stream
END PROGRAM
```

### Explanation

**Purpose:** Describes how each incoming API request is processed by the backend.

| Step | Description |
|------|-------------|
| **VALIDATE body with Pydantic** | Request bodies are parsed and validated against Pydantic models (e.g., `RequirementAnalysisRequest`, `CodeGenerationRequest`). Invalid JSON or missing fields return 400. |
| **ROUTE to appropriate service** | FastAPI's router matches `(method, path)` to a handler. For example, `POST /requirements/analyze` → `requirements_router`, `POST /code/generate/stream` → `codegen_router`. |
| **CALL service function** | The handler imports and calls the corresponding service (e.g., `analyze_requirements_with_gemini`, `generate_code_with_gemini_stream`). |
| **LOG event to DATABASE** | Many routes call `log_event(kind, payload)` to insert a `RunLog` row. Kinds include "analysis", "codegen", "write", "review", etc. |
| **RETURN response OR stream** | Most endpoints return JSON. The code generation endpoint returns a `StreamingResponse` with `text/plain` chunks. |

**Additional behavior:** CORS middleware allows cross-origin requests. A global exception handler catches unhandled errors and returns 500 with a sanitized message. Request timing is logged.

---

## Summary Table

| Program | Role in SASDS |
|---------|---------------|
| **SASDS_MAIN** | Bootstraps backend (FastAPI) and frontend (React), mounts routes, starts servers. |
| **REQUIREMENTS_TO_PROJECT** | Core pipeline: analyze requirements → stream code → persist to disk; optionally self-fix, chat, refine, or run Auto-Pilot. |
| **SELF_CORRECTION_LOOP** | Iterative test-fix loop: run pytest, detect failing file, get AI fix, rewrite, retry (max 3 attempts). |
| **API_REQUEST_HANDLER** | Per-request flow: validate, route, call service, log, respond (or stream). |

---

*This document explains the pseudocode in `docs/SASDS_COMPREHENSIVE_ARCHITECTURE.md` Section 6.4.*
